# you will need to install yahoo_fin module
# pip install yahoo_fin
# ref: http://theautomatic.net/yahoo_fin-documentation/

from yahoo_fin.stock_info import get_data
from sqlalchemy import create_engine
from datetime import datetime as dt
import pandas as pd

def get_stock_data(tick_name, start_date, end_date):
    """
    This function scrapes results fro a single stock from yahoo

    tick_name: stock ticker
    start_date: first stock result with format: '01/01/2020'
    end_date: last stock result with format: '01/01/2020'
    """
    df = get_data(ticker=tick_name, start_date=start_date, end_date=end_date)
    df.reset_index(inplace=True)
    df.rename(columns={'index' : 'date'}, inplace=True)
    df['date'] = df['date'].dt.date
    return(df)

def build_stock_df(tickers, start_date, end_date, max_records):
    """
    This function loops through the tickers, runs get_stock_data and 
    returns a combined dataframe with all the results

    tickers : this is a dataframe with the tickers we want with 
    columns for: Sector, Name, and Company

    start_date: first stock result with format: '01/01/2020'
    end_date: last stock result with format: '01/01/2020'

    max_records: integer with the max number of results er stock
    """

    # get the ticker results for the time period
    for record in tickers.index:
        results = get_stock_data(tickers['Ticker'][record], start_date, end_date)
        results['company'] = tickers['Name'][record]
        results['sector'] = tickers['Sector'][record]
        
        # only keep the last 100 records
        results = results.tail(max_records)

        # if a combined dataset exists append these new results
        try:
            combined_results = combined_results.append(results, ignore_index=True)
            
        # if combined dataset doesn't exist make this dataframe  the combined results df
        except:
            combined_results = results

    return combined_results

if __name__ == "__main__":
    # load the tickers we want into a dataframe
    tickers = pd.DataFrame({
        'Sector' : ['Delivery', 'Delivery', 'Delivery', 'Medical Goods', 'Medical Goods', 'Medical Goods', 'Medical Services', 'Medical Services', 'Medical Services', 'Retail', 'Retail', 'Retail', 'Market', 'Market', 'Market'],
        'Name' : ['FedEx', 'UPS', 'DHL', 'Johnson & Johnson', 'Cardinal Health', '3M', 'Medical Imaging Corp', 'Community Health Systems', 'Teladoc Health', 'Walmart', 'Amazon', 'CVS', 'Dow Jones', 'S & P 500', 'Nasdaq'],
        'Ticker' : ['FDX', 'UPS', 'DPSGY', 'JNJ', 'CAH', 'MMM', 'MEDD', 'CYH', 'TDOC', 'WMT', 'AMZN', 'CVS', '^DJI', '^GSPC', '^IXIC'],
    })

    # this is a smaller tickers list that can be used for testing
    test_tickers = pd.DataFrame({
        'Sector' : ['Delivery','Medical Goods', 'Medical Services'],
        'Name' : ['FedEx', 'Johnson & Johnson', 'Community Health Systems'],
        'Ticker' : ['FDX', 'JNJ', 'CYH'],
    })

    prices_df = build_stock_df(tickers=tickers, 
                           start_date='01/01/2020', 
                           end_date = '04/01/2020', 
                           max_records = 100)

    prices_df.to_csv('stock_data.csv',index=False)
    
    print(prices_df)



