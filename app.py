# ***************************************************************************
# * CS361 Project - Analytics Application 
# * Spencer Wagner
# * Server-Side functionality for Analytics App
# ***************************************************************************

# Basic Flask functionality, importing modules for parsing results and accessing MySQL. 

from flask import Flask, render_template, json, redirect, url_for, session
from flask import request
import matplotlib as plot
import numpy as np
import pandas as pd
import tempfile

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


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
