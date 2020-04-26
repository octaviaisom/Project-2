# you will need to install yahoo_fin module
# pip install yahoo_fin
# ref: http://theautomatic.net/yahoo_fin-documentation/

from yahoo_fin.stock_info import get_data
from sqlalchemy import create_engine
import datetime
import pandas as pd


def get_stock_data(tickers, start_date, end_date):

    """
    This function loops through the tickers, runs get_stock_data and 
    returns a combined dataframe with all the results
    tickers : this is a dataframe with the tickers we want with 
    columns for: Sector, Name, and Company
    start_date: first stock result with format: '01/01/2020'
    end_date: last stock result with format: '01/01/2020'
    max_records: integer with the max number of results er stock
    """
    #Covid data starts on 1/22/20
    today = datetime.datetime.now()
    one_day = datetime.timedelta(days = 1)
    end_date = (today-one_day).strftime('%m-%d-%Y')

    stock_dict = {}
    for record in tickers.index:
        ticker = tickers['Ticker'][record]

        # get the ticker results for the time period
        results= get_data(ticker=ticker, start_date=start_date, end_date=end_date)
        results.reset_index(inplace=True)
        results.rename(columns={'index' : 'date'}, inplace=True)
        results['date'] = results['date']
        results['company'] = tickers['Name'][record]
        results['sector'] = tickers['Sector'][record]

        #organize data for d3 use
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

    #Addt'l formatting for d3 use
    date_list = results['date'].astype(str).tolist()
    date_list.insert(0,'date') 
    stock_dict.update({'date' : date_list})

    #to be used in covid data
    results = results[['date']]

    return stock_dict, results
