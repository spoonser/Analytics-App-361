# ***************************************************************************
# * CS361 Project - Analytics Application 
# * Spencer Wagner
# * Server-Side functionality for Analytics App
# ***************************************************************************

# Basic Flask functionality, importing modules for parsing results and accessing MySQL. 

from flask import Flask, render_template, request, json, flash, redirect, url_for, session
import requests
import static.py.graphing as grph
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

            word_freq = {}
            word_freq['c1'] = []
            word_freq['c2'] = []
            for key in parsed_text.keys():
                word_freq['c1'].append(key)
                word_freq['c2'].append(len(parsed_text[key]))

            df = pd.DataFrame(word_freq)
            session['filename'] = 'Text Data from Microservice'
            session['data'] = df.to_dict('list')

            # Plot and return figure   
            plot_url = grph.get_plot('pie', df, 'Blues', df.keys()[0], df.keys()[1], 
                                    'Word', 'Frequency', 'Word Frequency Diagram') 
            plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

            return plot
    
        except:        
            return "Text could not be analyzed. Sorry."

    else:
        return "Something went wrong. Sorry."
 

# -------------------------------------------------------------------------------------------------
# Graphing page - create graphs with uploaded data
# ------------------------------------------------------------------------------------------------- 
@app.route('/graph')
def graph():
    # Display a table containing the user data
    if 'data' in session:
        df = pd.DataFrame(session['data'])
        df_html = df.to_html()
        return render_template('graph.html', df_html=df_html)

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

    # Get user selection
    graph_type = request.form.get('graph-type')
    xaxis = request.form.get('x-axis') or None
    yaxis = request.form.get('y-axis') or None

    # Attempt to pass the user selection to graphing functions
    try:
        # Plot figure
        plot_url = grph.get_plot(graph_type, df, 'Greys', xaxis, yaxis, 
                            '', '', '')
        plot = '<img src="data:image/png;base64,{}">'.format(plot_url)

        return plot

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

    # Mean, median, and mode standard deviation form 
    if 'stat-col' in request.form:
        col = request.form.get('stat-col')
        mean, median, mode, stddev = None, None, None, None

        if request.form.get('mean'):
            try:
                mean = df[col].mean(axis=0)
            except:
                mean = 'Mean not calculable'
        
        if request.form.get('median'):
            try:
                median = df[col].median(axis=0)
            except:
                median = 'Median not calculable'

        if request.form.get('mode'):
            try:
                mode = df[col].mode(axis=0)
            except:
                mode = 'Mode not calculable'

        if request.form.get('stddev'):
            try:
                stddev = df[col].std(axis=0)
            except:
                stddev = 'Standard deviation not calculable'

        return 'mean, median, mode'

    # To implement
    if 'form2-submit' in request.form:
        return stats()
    
    return 'hello'

# -------------------------------------------------------------------------------------------------
# Microservice portion - return a graph to external application sending POST request
# -------------------------------------------------------------------------------------------------
@app.route('/graphs_ms', methods=['POST', 'GET'])
def http_graphs():
    if request.method == 'POST':

        try:
            # Get specifications from user
            data = request.get_json()
            colors = data['colors']
            graph_type = data['graph_type']
            xaxis, yaxis = data['xaxis'], data['yaxis']
            xlabel, ylabel = data['xlabel'], data['ylabel']
            title = data['title']
    
            # Convert JSON data to dataframe
            table = pd.io.json.json_normalize(data['table'])
            df = pd.DataFrame(table)

            # Create plot given specifications
            plot = grph.get_plot(graph_type, df, colors, xaxis, yaxis,
                                xlabel, ylabel, title)

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
