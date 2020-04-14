from scrape_stock_data import build_stock_df
import pandas as pd

tickers = pd.DataFrame({
        'Sector' : ['Delivery', 'Delivery', 'Delivery', 'Medical Goods', 'Medical Goods', 'Medical Goods', 'Medical Services', 'Medical Services', 'Medical Services', 'Retail', 'Retail', 'Retail', 'Market', 'Market', 'Market'],
        'Name' : ['FedEx', 'UPS', 'DHL', 'Johnson & Johnson', 'Cardinal Health', '3M', 'Medical Imaging Corp', 'Community Health Systems', 'Teladoc Health', 'Walmart', 'Amazon', 'CVS', 'Dow Jones', 'S & P 500', 'Nasdaq'],
        'Ticker' : ['FDX', 'UPS', 'DPSGY', 'JNJ', 'CAH', 'MMM', 'MEDD', 'CYH', 'TDOC', 'WMT', 'AMZN', 'CVS', '^DJI', '^GSPC', '^IXIC'],
    })


stock_df = build_stock_df(tickers=tickers, 
                        start_date='01/01/2020', 
                        end_date = '04/01/2020', 
                        max_records = 100)

print(stock_df)