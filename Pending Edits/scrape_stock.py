# you will need to install yahoo_fin module
# pip install yahoo_fin
# ref: http://theautomatic.net/yahoo_fin-documentation/

from yahoo_fin.stock_info import get_data
from sqlalchemy import create_engine
import datetime
import pandas as pd

def get_stock_data():
    start_date = '01/22/2020'
    today = datetime.datetime.now()
    one_day = datetime.timedelta(days = 1)
    end_date = (today-one_day).strftime('%m-%d-%Y')

    # load the tickers we want into a dataframe
    tickers = pd.DataFrame({
        'Sector' : ['Delivery', 'Delivery', 'Delivery', 'Medical Goods', 'Medical Goods', 'Medical Goods', 'Medical Services', 'Medical Services', 'Medical Services', 'Retail', 'Retail', 'Retail', 'Market', 'Market', 'Market'],
        'Name' : ['FedEx', 'UPS', 'DHL', 'Johnson & Johnson', 'Cardinal Health', '3M', 'Medical Imaging Corp', 'Community Health Systems', 'Teladoc Health', 'Walmart', 'Amazon', 'CVS', 'Dow Jones', 'S & P 500', 'Nasdaq'],
        'Ticker' : ['FDX', 'UPS', 'DPSGY', 'JNJ', 'CAH', 'MMM', 'MEDD', 'CYH', 'TDOC', 'WMT', 'AMZN', 'CVS', '^DJI', '^GSPC', '^IXIC'],
    })

    stock_dict = {}
    for record in tickers.index:
        ticker = tickers['Ticker'][record]

        results= get_data(ticker=ticker, start_date=start_date, end_date=end_date)
        results.reset_index(inplace=True)
        results.rename(columns={'index' : 'date'}, inplace=True)
        results['date'] = results['date']
        results['company'] = tickers['Name'][record]
        results['sector'] = tickers['Sector'][record]


        results['high'] = results.high.round(2)
        results['close'] = results.close.round(2)
        results['low'] = results.low.round(2)

        price_list = []
        for index, row in results.iterrows():
            prices = [row['high'],row['close'],row['low']]
            price_list.append(prices)
        price_list.insert(0,ticker)    


        # if a combined dataset exists append these new results
        try:

            stock_dict.update({ticker : price_list})

        # if combined dataset doesn't exist make this dataframe  the combined results df
        except:
            stock_data = results


    date_list = results['date'].astype(str).tolist()
    date_list.insert(0,'date') 
    stock_dict.update({'date' : date_list})

    results = results[['date']]

    return stock_dict, results