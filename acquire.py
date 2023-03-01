# imports

import pandas as pd
import requests
import os

import json

from bs4 import BeautifulSoup




# function to establish BeautifulSoup & link access

def access_codeup_blog():
    
    '''
    this function processes the Codeup
    blog links through BeautifulSoup and
    returns a list of accessible blog links
    '''
    
    # origin url
    url = 'https://codeup.com/blog/'
    
    # access
    headers = {'User-Agent' : 'Codeup Data Science'}
    response = requests.get(url, headers = headers)
    
    # setting to BS
    soup = BeautifulSoup(response.content, 'html.parser')

    # gathering all of the links into one place
    more_links = soup.find_all('a', class_ = 'more-link')

    # EXTRACt the links into sth useful
    links_list = [link['href'] for link in more_links]

    return links_list



# function to collect Codeup blog posts and cache them as a json file

def get_blog_articles(article_list):
    
    '''
    this function takes in a list of links to
    Codeup blog articles and returns a dictionary
    of each blog title, its link, the date 
    published and the post's content and stores 
    it in json format
    '''
    
    file = 'blog_posts.json'
    
    if os.path.exists(file):
        
        # if file exists, then return the file as a json
        with open(file) as f:
            
            return json.load(f)
        
    headers = {'User-Agent' : 'Codeup Data Science'}
    
    article_info = []
    
    for article in article_list:

        response = requests.get(article, headers = headers)

        soup = BeautifulSoup(response.content, 'html.parser')

        info_dict = {'title' : soup.find('h1').text,
                    'link' : link,
                    'date_published' : soup.find('span', class_ = 'published').text,
                    'content' : soup.find('div', class_ = 'entry-content').text}
        
        article_info.append(info_dict)

    # opening file with intent of writing ('w') to it    
    with open(file, 'w') as f:
        
        # dumping info into 'article_info' file
        json.dump(article_info, f)

    return article_info
        
    


# function to scrape a topic

def scrate_one_page(topic):
    
    '''
    this function takes in a news topic 
    and creates a dictionary of the category,
    title and content of each news brief
    for a given news topic on InShorts.
    '''
    
    base_url = 'https://inshorts.com/en/read/'
    
    response = requests.get(base_url + topic)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titles = soup.find_all('span', itemprop = 'headline')
    
    briefs = soup.find_all('div', itemprop = 'articleBody')
    
    summary_list = []
    
    for i in range(len(titles)):
        
        temp_dico = {'category' : topic, 
                     'title' : titles[i].text,
                     'content' : briefs[i].text}
        
        summary_list.append(temp_dico)
    
    return summary_list



# function to scrape info about an array of InShorts topics

def get_news_articles(topic_list):
    
    '''
    this function takes in a list of topics on the 
    InShorts news website and returns a json file 
    of all the news articles in the topic list
    '''
    
    # maintains file name consistency
    file = 'news_articles.json'
    
    if os.path.exists(file):
        with open(file) as f:
            
            return json.load(f)
        
    final_list = []
    
    # loop through topic lost
    for topic in topic_list:
        
        # add to list
        final_list.extend(scrate_one_page(topic))
        
    with open(file, 'w') as f:
        
        json.dump(final_list, f)
        
    return final_list