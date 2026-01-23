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
import tqdm
import re
from bs4 import BeautifulSoup
from datetime import date
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver import ChromeOptions
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.chrome import ChromeDriverManager


# fetch the articles 

# the output from this script is the extra article saved in data

def init_db(file_name):
    '''
    Initialize the database, which is json and pickle files currently
    '''
    # cold start, first deployment if statement
    if not os.path.exists(file_name):
        # If the file doesn't exist, create an empty dictionary
        urls = set()
        with open(file_name, "wb") as f:
            pickle.dump(urls, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    # load the database 
    with open(file_name, "rb") as f:
        urls = pickle.load(f)
    return urls


def init_articles(file_name):
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


############################# URL RETRIEVAL ####################################
def get_wired_home_url(query):
    return 'https://www.wired.com/search/?q=' + query.replace(' ', '+') + '&sort=score+desc'

def get_techcrunch_home_url(query):
    return "https://search.techcrunch.com/search;_ylc=X3IDMgRncHJpZANZbkF3TWM3eFFvZWhGQkk3TkJHdG5BBG5fc3VnZwM5BHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAMxMgRxdWVyeQNzb2NpYWwlMjBtZWRpYQR0X3N0bXADMTY3OTk0OTA4Nw--?p={}&fr=techcrunch".format(query.replace(' ', '+'))

def get_mit_home_url(query):
    return "https://www.technologyreview.com/tag/{}".format(query.replace(' ', '-'))

def get_the_verge_home_url(query):
    return "https://www.theverge.com/tech"



############################# SCRAPING FROM WEBSITES ###########################
def fetch_wired_article_links(url):
    '''
    Given a url, fetch the article links from the page
    '''
    print("Fetching wired links from {}".format(url))
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    links = ["https://www.wired.com" + a['href'] for a in soup.find_all('a', {'class': ['SummaryItemHedLink-cgaOJy', 'summary-item-tracking__hed-link']}, href=True)]
    return links


def fetch_techcrunch_article_links(url):
    '''
    Given a url, fetch the article links from the page
    '''
    print("Fetching techcrunch links from {}".format(url))
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = set()
    
    for a in soup.select(".compArticleList .d-tc > a[href]"):
        links.add(a['href'])
    return list(links)


def fetch_mit_article_links(url):
    '''
    Given a url, fetch the article links from the page
    '''
    print("Fetching MIT Tech Review links from {}".format(url))
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    links = set()
    for a in soup.select("h3.teaserItem__title--32O7a > a[href]"):
        links.add(a['href'])
    return list(links)


def fetch_the_verge_article_links(url):
    '''
    Given a url, fetch the article links from the page
    '''
    print("Fetching The Verge links from {}".format(url))
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    driver.get(url)

    SCROLL_PAUSE_TIME = 0.5
    n = 5
    last_height = driver.execute_script("return document.body.scrollHeight")

    while n > 0:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        n -= 1

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    links = set()
    for a in soup.select(".duet--content-cards--content-card .max-w-content-block-mobile h2 > a[href]"):
        if not a['href'].startswith('/'):
            continue
        url = a['href'].replace('https://www.theverge.com', '')
        links.add("https://www.theverge.com" + a['href'])
    
    return list(links)


def save_retrieved_links(path, lst): 
    with open(path, "wb") as f:
        pickle.dump(lst, f, protocol=pickle.HIGHEST_PROTOCOL)


def initial_driver():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--incognito")

    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait


def get_redirected_url(driver, wait, url):
    driver.get(url)
    wait.until(lambda driver: driver.current_url != url)
    return driver.current_url


def unpack_urls(path, driver, wait):
    print("Unpacking urls from {}".format(path))
    with open(path, "rb") as f:
        lst = pickle.load(f)
        res = []
        for index, url in enumerate(lst):
            if index % 100 == 0:
                print("Processing " + str(index) + " of " + str(len(lst)))
                driver.quit()

                options = ChromeOptions()
                options.add_argument("--headless=new")
                options.add_argument("--incognito")
                driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
                wait = WebDriverWait(driver, 10)
            try:
                redirect = get_redirected_url(driver, wait, url)
                res.append(redirect)
            except:
                print("Error: {}. {}".format(index, url))
        
    return res

############################# MAIN FUNCTION ####################################

def fetch_links(links, sector, source, data_dir, dic, initial_db, url_db):
    '''
    Given a list of links, fetch the articles and save them to the data folder
    '''
    for link in tqdm.tqdm(links):
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
            'published_at': "" if article.publish_date is None else article.publish_date.strftime("%m/%d/%Y")
        }

        with open(os.path.join(data_dir, article_path + '.json'), "w") as f:
            json.dump(element, f, indent=4, ensure_ascii=False)

        dic[link] = element
        
        # update db
        url_db.add(link)

    return dic, url_db


def main(article_set_pickle, articles, data_dir):
    '''
    article_set_pickle: article_set.pkl file path that contains all the article urls read
    data_dir: data_dir is the folder to save the data
    '''
    QUERIES = ['social media']# , 'voice assistants', 'virtual reality']
    url_db = init_db(article_set_pickle)
    initial_db = url_db

    dic = init_articles(articles)
    
    # wired
    wired_article_links = []
    techcrunch_article_links = []
    mit_article_links = []
    the_verge_article_links = []

    for query in QUERIES:
        wired_article_links.extend(fetch_wired_article_links(get_wired_home_url(query)))
        techcrunch_article_links.extend(fetch_techcrunch_article_links(get_techcrunch_home_url(query)))
        mit_article_links.extend(fetch_mit_article_links(get_mit_home_url(query)))
        the_verge_article_links.extend(fetch_the_verge_article_links(get_the_verge_home_url(query)))
    
        save_retrieved_links("./urls/wired_article_{}_links.pkl".format(query), wired_article_links)
        save_retrieved_links("./urls/techcrunch_article_{}_links_raw.pkl".format(query), techcrunch_article_links)
        save_retrieved_links("./urls/mit_article_{}_links.pkl".format(query), mit_article_links)
        save_retrieved_links("./urls/the_verge_article_{}_links.pkl".format(query), the_verge_article_links)

        # for techcrunch, we need to get the redirected url
        driver, wait = initial_driver()
        techcrunch_article_links = unpack_urls("./urls/techcrunch_article_{}_links_raw.pkl".format(query), driver, wait)
        save_retrieved_links("./urls/techcrunch_article_{}_links.pkl".format(query), techcrunch_article_links)
        
        # links = wired_article_links + techcrunch_article_links
        fetch_links(wired_article_links, query, 'WIRED', data_dir, dic, initial_db, url_db)
        fetch_links(techcrunch_article_links, query, 'TechCrunch', data_dir, dic, initial_db, url_db)
        fetch_links(mit_article_links, query, 'MIT', data_dir, dic, initial_db, url_db)
        fetch_links(the_verge_article_links, query, 'Verge', data_dir, dic, initial_db, url_db)

    assert url_db >= initial_db
    update_db(article_set_pickle, url_db)
    with open(articles, "wb") as file:
        pickle.dump(dic, file, protocol=pickle.HIGHEST_PROTOCOL)

import logging
from newsapi import NewsApiClient
from typing import Dict
from datetime import datetime, timedelta

class ArticleRequester():
    def __init__(self, data_dir:str):
        """Initialize the article requester with the data directory"""
        logging.info("Article Requester initialized with data directory: {}".format(data_dir))
        self.data_dir = data_dir
        self.article_pickle = os.path.join(data_dir, "articles.pkl")
        self.articles = self.init_db(self.article_pickle)

        # Figure out dates
        self.current_date = datetime.now()
        self.seven_days_ago = self.current_date - timedelta(days=7)
        logging.info("Current date: {}; Seven days ago: {}".format(self.current_date.strftime("%Y-%m-%d"), self.seven_days_ago.strftime("%Y-%m-%d")))
        
        self.queries = ['social media', 'voice assistants', 'virtual reality']

        
    def init_db(self, file_name):
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
    
    def fetch_from_news_api(self, keyword:str, from_date=str, to_date=str) -> Dict[str, str]:
        """Fetch articles from newsapi.org"""
        newsapi = NewsApiClient(api_key='12b234aeee694320a9feec1a38734663')
        articles = all_articles = newsapi.get_everything(q=keyword, 
                                                         domains='theverge.com,axios.com,wired.com,techcrunch.com,engadget.com,futurism.com',
                                                         from_param=from_date,
                                                         to=to_date,
                                                         language='en',
                                                         sort_by='relevancy')
        return articles["articles"]

    def get_article(self, article:Dict[str,str]) -> Dict[str, str]:
        """Get the article from the returned article object from newsapi"""
        # download and parse an article
        try:
            newspaperArticle = Article(article["url"])
            newspaperArticle.download()
            newspaperArticle.parse()

            return {
                'title': article["title"],
                'text': newspaperArticle.text,
                'source': article["source"]["name"],
                'url': article["url"],
                'published_at': "" if len(article["publishedAt"]) == 0 else article["publishedAt"]
            }
        
        except Exception as e:
            logging.error("Fetching Article Error: {}".format(e))
            return None


    def fetch(self):
        """Fetch articles in the past week"""
        logging.info("Fetching articles from {} to {}".format(self.seven_days_ago.strftime("%Y-%m-%d"), self.current_date.strftime("%Y-%m-%d")))

        for query in self.queries:
            logging.info("Fetching articles for {}".format(query))
            articles = self.fetch_from_news_api(query, 
                                                self.current_date.strftime("%Y-%m-%d"), 
                                                self.seven_days_ago.strftime("%Y-%m-%d"))
            
            for article in articles:
                if article["url"] in self.articles: 
                    continue
                # add and dump to data
                article_path = slugify(article['title'].strip())
                # update the article and get the sector namespace
                element = self.get_article(article)
                if element is None: continue
                element["sector"] = query

                with open(os.path.join(self.data_dir, article_path + '.json'), "w") as f:
                    json.dump(element, f, indent=4, ensure_ascii=False)

                self.articles[element["url"]] = element

            self.update_db()

    def update_db(self):
        """Update the database"""
        with open(self.article_pickle, "wb") as file:
            pickle.dump(self.articles, file, protocol=pickle.HIGHEST_PROTOCOL)
            


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--article_set_pickle', required=True)
    # parser.add_argument('--articles', required=True)
    parser.add_argument('--data_dir', required=True)
    args = parser.parse_args()
    logging.getLogger().setLevel(logging.INFO)

    logging.info("### Fetching ###")
    # main(
    #     args.article_set_pickle,
    #     args.articles,
    #     args.data_dir
    # )
    ar = ArticleRequester(args.data_dir)
    ar.fetch()