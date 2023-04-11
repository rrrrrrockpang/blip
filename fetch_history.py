import newspaper
import requests
import sqlite3
import os
import pickle
import json
import uuid
import time
import argparse
import unicodedata
import re
from bs4 import BeautifulSoup
from datetime import date
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# fetch the articles 

def init_db(file_name):
     # cold start, first deployment if statement
    if not os.path.exists(file_name):
        # If the file doesn't exist, create an empty dictionary
        articles = {}
        with open(file_name, "wb") as f:
            pickle.dump(articles, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    # load the database 
    with open(file_name, "rb") as f:
        articles = pickle.load(f)
    return articles


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def update_db(file_name, db):
    '''
    Update the database
    '''
    with open(file_name, "wb") as f:
        pickle.dump(db, f, protocol=pickle.HIGHEST_PROTOCOL)



def fetch_wired_article_links(url):
    '''
    Given a url, fetch the article links from the page
    '''
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    links = ["https://www.wired.com" + a['href'] for a in soup.find_all('a', {'class': ['SummaryItemHedLink-cgaOJy', 'summary-item-tracking__hed-link']}, href=True)]
    return links


def get_wired_home_url(query):
    return 'https://www.wired.com/search/?q=' + query.replace(' ', '+') + '&sort=score+desc'


def fetch_from_links(links, sector, source, data_dir, dic, initial_db, url_db):
    '''
    Given a list of links, fetch the articles and save them to the data folder
    '''
    for link in links:
        if link in initial_db: continue
        print("### Adding article {}".format(link))
        # add and dump to data
        article = Article(link)
        article.download()
        article.parse()

        # clean title
        title = article.title
        if len(title) <= 1: 
            continue
        # remove techcrunch from title
        if "techcrunch" in title:
            title = title.replace("techcrunch", "")

        article_path = slugify(article.title.strip())

        element = {
            'title': title,
            'text': article.text,
            'sector': sector,
            'source': source,
            'url': link,
            'published_at': article.publish_date.strftime("%m/%d/%Y")
        }

        with open(os.path.join(data_dir, article_path + '.json'), "w") as f:
            json.dump(element, f, indent=4, ensure_ascii=False)

        dic[link] = element
        
        # update db
        url_db.add(link)

    return dic, url_db


def fetch_wired_article_links_from_history(url, k):
    '''
    Given a url, fetch the article links from the page in history
    '''
    BUTTON_SELECTOR = ".SummaryListCallToActionWrapper-zjlBs.jEQOrB.summary-list__call-to-action-wrapper .ButtonLabel-eAHUfq.bCFzBu.button__label"
    driver = webdriver.Chrome(ChromeDriverManager().install())  # or use any other webdriver
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = set(["https://www.wired.com" + a['href'] for a in soup.find_all('a', {'class': ['SummaryItemHedLink-cgaOJy', 'summary-item-tracking__hed-link']}, href=True)])

    # find the "More Stories" button
    button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, BUTTON_SELECTOR)))
    
    while button and k > 0:
        # simulate a click on the button
        button.click()
        print("clicked")
        
        # wait for the new page to load
        time.sleep(2)
        new_button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)

        print(new_button.text)
        while(new_button.text == 'LOADING...'):
            time.sleep(2)
            new_button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)
            
        # get the new articles on the page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        new_links = ["https://www.wired.com" + a['href'] for a in soup.find_all('a', {'class': ['SummaryItemHedLink-cgaOJy', 'summary-item-tracking__hed-link']}, href=True)]
        for nl in new_links:
            if nl not in links:
                links.add(nl)
        
        k -= 1

        button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)
        time.sleep(1)
            
    driver.quit()
    return list(links)



def main(article_dic_path, data_dir):
    '''
    article_set_pickle: article_set.pkl file path that contains all the article urls read
    data_dir: data_dir is the folder to save the data
    '''
    QUERIES = ['social media'] # , 'voice assistants', 'virtual reality']
    article_db = init_db(article_dic_path) # dictionary
    initial_db = article_db 
    
    # wired
    wired_article_links = []
    for query in QUERIES:
        wired_article_links.extend(
            fetch_wired_article_links_from_history(
                get_wired_home_url(query), 
                k=1
            )
        )
    print(wired_article_links)
    print(len(wired_article_links))
    
    # # TODO: add other resources
    
    # links = wired_article_links

    # fetch_from_links(wired_article_links, 'social media', 'WIRED', data_dir, dic, initial_db, url_db)

    # assert url_db >= initial_db
    # update_db(article_set_pickle, url_db)
    # with open(articles, "wb") as file:
    #     pickle.dump(dic, file, protocol=pickle.HIGHEST_PROTOCOL)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--articles', required=True)
    parser.add_argument('--data_dir', required=True)
    parser.add_argument('--history', required=True, type=int)
    args = parser.parse_args()

    print("### Fetching ###")
    if args.history == 1:
        main(
            args.articles,
            args.data_dir
        )