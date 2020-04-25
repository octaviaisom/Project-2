import requests
import pandas as pd
import datetime
import scrape_stock

def get_covid_data():


    stock_return = scrape_stock.get_stock_data()
    stock_dates = stock_return[1] 
        
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



    #format data for js visual
    covid_data = pd.merge(stock_dates, covid_confirmed, on='date',how='inner')

    covid_confirmed_list = covid_data['delta'].tolist()
    covid_confirmed_list.insert(0,"No. of New Cases")

    covid_data = [covid_confirmed_list]

    return covid_data