# ***************************************************************************
# * CS361 Project - Analytics Application 
# * Spencer Wagner
# * Server-Side functionality for Analytics App
# ***************************************************************************

# Basic Flask functionality, importing modules for parsing results and accessing MySQL. 

from flask import Flask, render_template, json, redirect, url_for
from flask_mysqldb import MySQL
from flask import request

# Using environment variables on Flip to store our DB credentials. 
import os

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = os.environ.get("CS340DBUSER")
app.config['MYSQL_PASSWORD'] = os.environ.get("CS340DBPW")
app.config['MYSQL_DB'] = os.environ.get("CS340DB")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
 
# -------------------------------------------------------------------------------------------------
# Main Index page 
# -------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')   

    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 61557))
    app.run(port=port, debug=True)