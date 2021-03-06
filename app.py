# ***************************************************************************
# * CS361 Project - Analytics Application 
# * Spencer Wagner
# * Server-Side functionality for Analytics App
# ***************************************************************************

# Basic Flask functionality, importing modules for parsing results and accessing MySQL. 

from flask import Flask, render_template, request, json, flash, redirect, url_for, session
import requests
import static.py.graphing as grph
import static.py.stats as stat
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
import io
import base64

# Using environment variables on Flip to store our DB credentials. 
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "NOT_A_SECRET" 


# -------------------------------------------------------------------------------------------------
# Main Index page 
# -------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')   

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        # Handle uploaded file
        if request.files['user-file'].filename != '':

            # Convert uploaded csv to pandas dataframe, then store in Flask session
            df = pd.read_csv(request.files.get('user-file'))
            session['filename'] = request.files.get('user-file').filename
            session['data'] = df.to_dict('list')

            return render_template('index.html')
        
        # Return to home page if no file uploaded
        return index()


# -------------------------------------------------------------------------------------------------
# Text Parsing page - Microservice connectivity 
# -------------------------------------------------------------------------------------------------
@app.route('/parse')
def parse():
    return render_template('parse.html')

# Send request to external api and return a graph of word stats
@app.route('/parse', methods=['POST'])
def get_text_data():
    # Ready information to send to target microservice
    text = request.form['user-text'] 
    url = "https://cs361-parsely-rjg4g6kr7q-uw.a.run.app/pos"
    payload = { "text": text }

    response = requests.post(url, data=json.dumps(payload))
    
    if response.status_code == 200:
        try:
            # Get parsed information about text
            parsed_text = json.loads(response.text)

            # Reorganize parsed text to make a graph
            del parsed_text['count']

            grammar = {}
            grammar['c1'], grammar['c2'] = [], []
            for key in parsed_text.keys():
                grammar['c1'].append(key)
                grammar['c2'].append(len(parsed_text[key]))

            # Format data to return a graph
            df = pd.DataFrame(grammar)
            specs = ['pie', 'Blues', df.keys()[0], df.keys()[1], 'Word', 
                    'Type', 'Parsed Text Chart']
            
            # Plot and return figure   
            plot_url = grph.get_plot(df, specs) 
            plot = '<img class="img-responsive" src="data:image/png;base64,{}">'.format(plot_url)

            return render_template('parse.html', graph_requested=True, plot=plot)
    
        except:        
            return "Text could not be analyzed. Sorry."

 

# -------------------------------------------------------------------------------------------------
# Graphing page - create graphs with uploaded data
# ------------------------------------------------------------------------------------------------- 
@app.route('/graph')
def graph():
    # Display a table containing the user data
    if 'data' in session:
        df = pd.DataFrame(session['data'])
        df_html = df.to_html()
        return render_template('graph.html', df_html=df_html, cmaps=plt.colormaps())

    return render_template('graph.html', df_html=False)

# Allows the user to select graph configuration and generate a graph
@app.route('/graph', methods=['POST'])
def do_plot():
    """
    If the user clicks certain buttons, will generate a few different
    types of plots depending on what they choose
    """
    # Get current session data as pandas dataframe
    df = pd.DataFrame(session['data'])
    df_html = df.to_html()

    # Get user selection
    specs = grph.get_graph_specs(request.form.to_dict())

    # Attempt to pass the user selection to graphing functions
    try:
        # Plot figure
        plot_url = grph.get_plot(df, specs)
        plot = '<img class="img-responsive" src="data:image/png;base64,{}">'.format(plot_url)
    
        return render_template('graph.html', df_html=df_html, plot=plot,
                                cmaps=plt.colormaps(), graph_requested=True)

    # Graph doesn't work
    except:
        print('Invalid Graph!')
        return graph() 

# -------------------------------------------------------------------------------------------------
# Stats page - get statistics out of the data
# -------------------------------------------------------------------------------------------------
@app.route('/stats')
def stats():
    # Display a table containing the user data
    if 'data' in session:
        df = pd.DataFrame(session['data'])
        df_html = df.to_html()
        return render_template('stats.html', df_html=df_html)

    return render_template('stats.html', df_html=False)

@app.route('/stats', methods=['POST'])
def get_stats():
    # Get session data in pandas dataframe
    df = pd.DataFrame(session['data'])
    df_html = df.to_html()

    # Mean, median, and mode standard deviation form 
    if 'stat-col' in request.form:
        col = request.form.get('stat-col')
        mean, median, mode, stddev = None, None, None, None

        if request.form.get('mean'):
           mean = stat.get_mean(df, col)
        
        if request.form.get('median'):
            median = stat.get_median(df, col)

        if request.form.get('mode'):
            mode = stat.get_mode(df, col)

        if request.form.get('stddev'):
            stddev = stat.get_stddev(df, col)

        return render_template('stats.html', stats_requested=True, df_html=df_html,
                                mean=mean, median=median, mode=mode, stddev=stddev)

# -------------------------------------------------------------------------------------------------
# Microservice portion - return a graph to external application sending POST request
# -------------------------------------------------------------------------------------------------
@app.route('/graphs_ms', methods=['POST', 'GET'])
def http_graphs():
    if request.method == 'POST':

        try:
            # Get specifications from user
            data = request.get_json()
            specs = grph.get_graph_specs(data)
    
            # Convert JSON data to dataframe
            table = pd.io.json.json_normalize(data['table'])
            df = pd.DataFrame(table)

            # Create plot given specifications
            plot = grph.get_plot(df, specs)

            # Make response
            response = app.response_class(
                response=json.dumps(plot),
                status=200,
                mimetype='application/json'
            )

            # Send response to requestor
            return response

        except:
            # Return bad response
            response = app.response_class(
                response='Invalid request',
                status=400,
            )
            return response

    # Send user back to homepage if they access via GET
    else:
        return redirect('/')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
