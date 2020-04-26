
from flask import Flask, render_template, jsonify, redirect
import pandas as pd
import get_data

app = Flask(__name__)
app._static_folder = 'static/'

# load the tickers we want into a dataframe
tickers = pd.DataFrame({
    'Sector' : ['Delivery', 'Delivery', 'Delivery', 'Medical Goods', 'Medical Goods', 'Medical Goods', 'Medical Services', 'Medical Services', 'Medical Services', 'Retail', 'Retail', 'Retail', 'Market', 'Market', 'Market'],
    'Name' : ['FedEx', 'UPS', 'DHL', 'Johnson & Johnson', 'Cardinal Health', '3M', 'Medical Imaging Corp', 'Community Health Systems', 'Teladoc Health', 'Walmart', 'Amazon', 'CVS', 'Dow Jones', 'S & P 500', 'Nasdaq'],
    'Ticker' : ['FDX', 'UPS', 'DPSGY', 'JNJ', 'CAH', 'MMM', 'MEDD', 'CYH', 'TDOC', 'WMT', 'AMZN', 'CVS', '^DJI', '^GSPC', '^IXIC'],
})


@app.route("/")
def index():

    stock_data, covid_data = get_data.main()

    return render_template('index.html', covid_data = covid_data, stock_data = stock_data)

if __name__ == "__main__":
    app.run(debug=True)
