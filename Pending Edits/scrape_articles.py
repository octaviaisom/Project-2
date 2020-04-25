# Dependencies
from bs4 import BeautifulSoup
import requests

def get_article_data():

    queries = {'Virus': ['covid-19'],
        'Industries': ['covid-19 delivery industry', 'covid-19 retail industry', 'covid-19 medical industry'],
        'Retail Companies':['amazon','walmart','cvs'],
        'Delivery Companies': ['fedex', 'ups', 'dhl'],
        'Medical Companies': ['johnson and johnson', '3m', 'cardinal health'],
        'Medical Service Companies':  ['teladoc','medical imaging corp', 'community health system']}

    urls = {}
    for key in queries:
        
        objects = len(queries[key])
        
        value = 0
        while value < objects:
            query = queries[key][value]
            url = f'https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US%3Aen'
            urls.update({query : url})
            value +=1

    article_data = {}
    article_count = 5

    for key in urls:
        
        url = urls[key]
        
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        articles = soup.find_all('article', class_='MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne')
        images = soup.find_all('img', class_='tvs3Id QwxBBf')
        
        
        article_list = []
        iterator = 0
        while iterator < article_count:

            try: 
                title = articles[iterator].find('a', class_='DY5T1d').text
                link = "https://news.google.com/" + articles[iterator].find('a', class_='DY5T1d')['href']
                source = articles[iterator].find('a', class_='wEwyrc AVN2gc uQIVzc Sksgp').text
                post_date = articles[iterator].find('time', class_='WW6dff uQIVzc Sksgp').text
                image = images[0]['src']

                article_info = {'title' : title,
                            'link' : link,
                            'source' : source,
                            'post_date' : post_date,
                            'image' : image}

                article_list.append(article_info)

                iterator +=1

            except:
                print(f'Unable to retrieve all {key} data...skipping')
                
        article_data.update({key : article_list})

    return article_data