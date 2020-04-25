
import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_stock, scrape_covid
from yahoo_fin.stock_info import get_data
from sqlalchemy import create_engine
import datetime
import pandas as pd

'''sys.setrecursionlimit(2000)
app = Flask(__name__)


client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts'''
app = Flask(__name__)
app._static_folder = 'static/'

@app.route("/")
def index():
    
    covid_data = scrape_covid.get_covid_data()
    stock_return = scrape_stock.get_stock_data()
    stock_data = stock_return[0]   

    return render_template('index.html', covid_data = covid_data, stock_data = stock_data)

'''@app.route("/delivery")
def delivery():

    return render_template()  

@app.route("/retail")
def retail():

    return render_template()

@app.route("/medical_goods")
def medical_goods():

    return render_template()

 @app.route("/medical_services")
def medical_service():

    return render_template()'''

if __name__ == "__main__":
    app.run(debug=True)
