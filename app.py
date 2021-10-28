# ***************************************************************************
# * CS361 Project - Analytics Application 
# * Spencer Wagner
# * Server-Side functionality for Analytics App
# ***************************************************************************

# Basic Flask functionality, importing modules for parsing results and accessing MySQL. 

from flask import Flask, render_template, request, flash, redirect, url_for, session
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import io
import base64

# Using environment variables on Flip to store our DB credentials. 
import os

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(28)

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
    df = pd.DataFrame({'c1':['apple','banana','orange'],'c2':[10, 34, 22]})
    session['filename'] = 'Text Data from Microservice'
    session['data'] = df.to_dict('list')
    # Plot figure
    img = io.BytesIO()

    df.plot(kind='bar', x='c1', y='c2', rot=0)
    plt.xlabel('')
    plt.ylabel('Word Frequency')
    plt.legend('')
    plt.savefig(img, format='png')
    img.seek(0)

    plot_url = base64.b64encode(img.getvalue()).decode()
    plot = '<img src="data:image/png;base64,{}">'.format(plot_url)
    
    return plot
 
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
    x_axis = request.form.get('x-axis') or None
    y_axis = request.form.get('y-axis') or None

    # Attempt to pass the user selection to matplotlib
    try:
         # Plot figure
        img = io.BytesIO()

        df.plot(kind=graph_type, x=x_axis, y=y_axis, rot=0)
        plt.savefig(img, format='png')
        img.seek(0)

        plot_url = base64.b64encode(img.getvalue()).decode()
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
