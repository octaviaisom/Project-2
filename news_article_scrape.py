# Import rependencies
from bs4 import BeautifulSoup
import requests


#All topics that need to be searched
topics = {'Virus': ['covid-19'],
        'Industries': ['covid-19 delivery industry', 'covid-19 retail industry', 'covid-19 medical industry'],
        'Retail Companies':['amazon','walmart','cvs'],
        'Delivery Companies': ['fedex', 'ups', 'dhl'],
        'Medical Companies': ['johnson and johnson', '3m', 'cardinal health'],
        'Medical Service Companies':  ['teladoc','medical imaging corp', 'community health system']}


#Create Google News url for all the above topics
urls = {}
for key in topics:
    
    objects = len(topics[key]) #number of objects per key
    
    value = 0
    while value < objects:
        query = topics[key][value]
        url = f'https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US%3Aen'
        urls.update({query : url}) #append full url to dictionary
        value +=1


#Scrape article info from the above links
articles_dict = {} #Will store all article info for all topics
article_count = 8 #Number of articles to be scrapped per topic

for topic in urls:
    
    url = urls[topic]
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find_all('article', class_='MQsxIb xTewfe R7GTQ keNKEd j7vNaf Cc0Z5d EjqUne')
    images = soup.find_all('img', class_='tvs3Id QwxBBf')
    
    article_list = [] #Will store all article info for a single topic
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
            print(f'Unable to retrieve all {topic} data...skipping')
            
    articles_dict.update({topic : article_list}) #append topic's articles to 

topics = list(articles_dict.keys())