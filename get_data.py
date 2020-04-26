import sys
from flask import Flask, render_template, jsonify, redirect
# import pymongo
# import scrape_stock, scrape_covid
from yahoo_fin.stock_info import get_data
# from sqlalchemy import create_engine
import datetime
import pandas as pd
import requests

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

tickers = pd.DataFrame({
    'Sector' : ['Delivery', 'Delivery', 'Delivery', 'Medical Goods', 'Medical Goods', 'Medical Goods', 'Medical Services', 'Medical Services', 'Medical Services', 'Retail', 'Retail', 'Retail', 'Market', 'Market', 'Market'],
    'Name' : ['FedEx', 'UPS', 'DHL', 'Johnson & Johnson', 'Cardinal Health', '3M', 'Medical Imaging Corp', 'Community Health Systems', 'Teladoc Health', 'Walmart', 'Amazon', 'CVS', 'Dow Jones', 'S & P 500', 'Nasdaq'],
    'Ticker' : ['FDX', 'UPS', 'DPSGY', 'JNJ', 'CAH', 'MMM', 'MEDD', 'CYH', 'TDOC', 'WMT', 'AMZN', 'CVS', '^DJI', '^GSPC', '^IXIC'],
})

def scrape_stock_data(tick_name, start_date, end_date):
    df = get_data(ticker=tick_name, start_date=start_date, end_date=end_date)
    df.reset_index(inplace=True)
    df.rename(columns={'index' : 'date'}, inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    #df['date'] = df['date'].dt.date
    return(df)

def build_stock_df(tickers, start_date, end_date):

    # get the ticker results for the time period
    for record in tickers.index:
        results = scrape_stock_data(tickers['Ticker'][record], start_date, end_date)
        results['company'] = tickers['Name'][record]
        results['sector'] = tickers['Sector'][record]
        
        #organize data for d3 use
        results['high'] = results.high.round(2)
        results['close'] = results.close.round(2)
        results['low'] = results.low.round(2)
        results['open'] = results.open.round(2)
        results['adjclose'] = results.adjclose.round(2)

        # if a combined dataset exists append these new results
        try:
            combined_results = combined_results.append(results, ignore_index=True)
            
        # if combined dataset doesn't exist make this dataframe  the combined results df
        except:
            combined_results = results

    return combined_results

def load_stock_data(tickers):
    """
    This functions chekcs the dates and gets new data if needed
    """
    
    # covid data starts on 1/22/20
    start_date = '01-22-2020'
    end_date = datetime.datetime.now().strftime('%m-%d-%Y')
    
    #end_date = '03-31-2020'
    
    # connect to the database
    connection_string = "postgres:postgres@localhost:5432/Project-2_db"
    engine = create_engine(f'postgresql://{connection_string}')
    
    # if the table exists set the start date to one day past the last date in the db
    if engine.has_table('stocks'):
        result = engine.execute('SELECT MAX (date) FROM stocks;')
        for row in result:
            start_date = (row[0] + datetime.timedelta(days = 1))
        
        # stock data is only available for weekdays
        while start_date.weekday() > 4:
            start_date = start_date + datetime.timedelta(days = 1)
        
        start_date = start_date.strftime('%m-%d-%Y')

    if start_date < end_date:
        stock_df = build_stock_df(tickers=tickers, 
                               start_date=start_date, 
                               end_date = end_date)
        
    
        stock_df.to_sql(name='stocks', con=engine, if_exists='append')

def get_covid_data(get_dates):
    
    stock_dates = pd.DataFrame(get_dates, columns=['date'])
    stock_dates['date'] = pd.to_datetime(stock_dates['date'])
    
    url  = 'https://pomber.github.io/covid19/timeseries.json'
    response = requests.get(url).json()
    
    dateList = []
    confirmedList = []
    for i in response:

        #all records for a simgle country
        country_data = response[i]

        country_records = len(response[i])    
        for j in range(0, country_records):

            #pull and append each country's daily stats to lists
            date = country_data[j]['date']
            confirmed = country_data[j]['confirmed']

            dateList.append(date)
            confirmedList.append(confirmed)
    
    #consolidate list into a ditionary
    covid_dict = {'date': dateList,
                'confirmed': confirmedList}

    #convert dictionary into dataframe
    covid_df = pd.DataFrame.from_dict(covid_dict)

    #convert 'date' format
    covid_df['date'] = pd.to_datetime(covid_df['date'])

    #consolidate all records into a worlwide dataset
    covid_grouped = covid_df.groupby(['date'], as_index=False).sum()

    #sort date column
    covid_grouped = covid_grouped.sort_values(by=['date'])

    #calculate daily rate of change
    covid_grouped['delta'] = covid_grouped['confirmed'] - covid_grouped['confirmed'].shift(1)

    #convert NaN value to '0'
    covid_confirmed = covid_grouped.fillna(0)

    #remove columns that will not be used
    covid_data = covid_confirmed[['date','delta']]

    covid_data = pd.merge(stock_dates, covid_confirmed, on='date',how='inner')


    return covid_data

def load_covid_data():
    """
    This functions chekcs the dates and gets new covid data if needed
    """
    
    # connect to the database
    connection_string = "postgres:postgres@localhost:5432/Project-2_db"
    engine = create_engine(f'postgresql://{connection_string}')
    
    try:
        stock_dates = set([date[0] for date in engine.execute('SELECT date FROM stocks;')])
    except:
        print('no stock data')
        return
    
    # if the table exists get the dates we need
    if engine.has_table('covid'):
        covid_dates = set([date[0] for date in engine.execute('SELECT date FROM covid;')])
        need_dates = stock_dates.difference(covid_dates)
        if len(need_dates) == 0:
            return
    else:
        need_dates = stock_dates

    covid_df = get_covid_data(need_dates)
    covid_df.to_sql(name='covid', con=engine, if_exists='append')

def get_stock_from_db(tickers):
    connection_string = "postgres:postgres@localhost:5432/Project-2_db"
    engine = create_engine(f'postgresql://{connection_string}')
    
    # get the results from the datframe
    stock_df = pd.read_sql(sql='stocks', con=engine)
#     covid_df = pd.read_sql(sql='covid', con=engine)
    
    # build the stock data
    stock_dict = {}
    for ticker in tickers['Ticker'].iteritems():
        ticker_df = stock_df[stock_df['ticker'] == ticker[1]].sort_values('date')
   
        price_list = []
        for index, row in ticker_df.iterrows():
            prices = [row['high'],row['close'],row['low']]
            price_list.append(prices)
        price_list.insert(0,ticker[1])
        
        stock_dict.update({ticker[1] : price_list})
    
    date_list = ticker_df['date'].astype(str).tolist()
    date_list.insert(0,'date') 
    stock_dict.update({'date' : date_list})

    
    return(stock_dict)

def get_covid_from_db():
    connection_string = "postgres:postgres@localhost:5432/Project-2_db"
    engine = create_engine(f'postgresql://{connection_string}')
    covid_df = pd.read_sql(sql='covid', con=engine).sort_values('date')
    
    covid_confirmed_list = covid_df['delta'].tolist()
    covid_confirmed_list.insert(0,"No. of New Cases")
    
    return([covid_confirmed_list])

def main():
    load_stock_data(tickers)
    load_covid_data()
    stock_data = get_stock_from_db(tickers)
    covid_data = get_covid_from_db()
    return([stock_data, covid_data])