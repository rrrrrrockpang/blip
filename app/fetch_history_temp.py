import newspaper
import requests
import glob
import sqlite3
import os
import pickle
import json
import tqdm
import time
import argparse
import unicodedata
import re
import concurrent.futures
from bs4 import BeautifulSoup
from selenium import webdriver
from newspaper import Article
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote

chrome_options = Options()
# chrome_options.add_argument("--headless")

class Fetcher():
    def __init__(self, keyword, domain_folder):
        self.keyword = keyword
        self.domain_folder = domain_folder
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    def get_wired_links(self, soup):
        links = []
        for a in soup.find_all('a', {'class': ['SummaryItemHedLink-civMjp', 'summary-item-tracking__hed-link']}, href=True):
            if a['href'] not in links:
                if a['href'].startswith('https://www.wired.com'):
                    links.append(a['href'])
                elif a['href'].startswith('/'):
                    links.append('https://www.wired.com' + a['href'])
        return links
    
    def save_to_db(self, stuff, source):
        file_name = self.keyword.replace(" ", "_")
        with open("./{}/{}_{}.pkl".format(file_name, file_name, source), "wb") as f:
            pickle.dump(stuff, f, protocol=pickle.HIGHEST_PROTOCOL)

    def retrieve_from_wired(self, k=50):
        print("Retrieving from Wired... : {}".format(self.keyword))
        # get url
        query = self.keyword
        url = 'https://www.wired.com/search/?q=' + query.replace(' ', '+') + '&sort=score+desc'

        # initialize the driver
        print("initializing driver")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = set(self.get_wired_links(soup))

        # find the "More Stories" button
        BUTTON_SELECTOR = ".SummaryListCallToActionWrapper-fngYcb.bXdTPE.summary-list__call-to-action-wrapper .ButtonLabel-cjAuJN.hzwRuG.button__label"
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, BUTTON_SELECTOR)))
        print("Retrieving from Wired...")
        try:
            while button and k > 0:
                print("Wired Progress: {}, {}".format(query, len(links)))
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)
                new_button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)

                print(new_button.text)
                while(new_button.text == 'LOADING...'):
                    time.sleep(2)
                    new_button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)
                    
                # get the new articles on the page
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                new_links = self.get_wired_links(soup)
                for nl in new_links:
                    if nl not in links:
                        links.add(nl)
                
                k -= 1
                self.save_to_db(links, "wired")
                button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)
                time.sleep(1)
        except:
            print("Error retrieving from Wired")
        driver.quit()
        print("Done retrieving from Wired: {} links".format(len(links)))
        return list(links)
    
    def process_fetched_techcrunch(self, links):

        # helper functions for techcrunch
        def extract_final_url(yahoo_url):
            # Find the start position of 'RU='
            start_pos = yahoo_url.find("RU=")
            
            if start_pos == -1:
                return None
            
            # Add 3 to skip 'RU='
            start_pos += 3
            
            # Find the next '/' after 'RU='
            end_pos = yahoo_url.find("/", start_pos)
            
            if end_pos == -1:
                return None
            
            # Extract and decode the final URL
            final_url_encoded = yahoo_url[start_pos:end_pos]
            final_url = unquote(final_url_encoded)
            
            return final_url

        def fetch_url(link):
            try:
                with requests.Session() as s:
                    # If the website uses JavaScript for redirection, we won't be able to capture it with 'requests'
                    r = s.get(link, allow_redirects=True, timeout=10)
                    # This gives you the final URL after following all redirects
                    final_url = r.url
                    # print(f"Initial URL: {link}, Final URL: {final_url}")
                    return extract_final_url(final_url)
            except Exception as e:
                print(f"Error fetching {link}: {e}")
                return None
        
        final_links = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for link, result in zip(links, executor.map(fetch_url, links)):
                if result is not None:
                    # print(f"Success: {link} => {result}")
                    final_links.append(result)
                else:
                    print(f"Error fetching {link}")

        return final_links
    
    def retrieve_from_techcrunch(self, url, k=100):
        print("Retrieving from TechCrunch... : {}".format(self.keyword))
        # has to input url since techcrunch website includes a random string
        query = self.keyword

        # initialize the driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = set([a['href'] for a in soup.select('.compArticleList a.thmb')])
        
        # find the "Next" button
        BUTTON_SELECTOR = ".next"
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, BUTTON_SELECTOR)))
        print("Retrieving from TechCrunch...")
        try: 
            while button and k > 0:
                print("Techcrunch Progress: {}".format(len(links)))
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)

                # get the new articles on the page
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                new_links = [a['href'] for a in soup.select('.compArticleList a.thmb')]

                for nl in new_links:
                    if nl not in links:
                        links.add(nl)
                
                k -= 1
                self.save_to_db(links, "techcrunch")
                button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)
                time.sleep(1)
        except:
            print("Error retrieving from TechCrunch")
        
        driver.quit()
        print("Done retrieving from TechCrunch: {} links".format(len(links)))

        # techcrunch needs additional redirecting
        # links is a set at this step
        links = self.process_fetched_techcrunch(list(links))
        return links
    

    def retrieve_from_mit_tech_review(self, k=100):
        print("Retrieving from MIT Tech Review... : {}".format(self.keyword))
        # get url
        query = self.keyword
        url = 'https://www.technologyreview.com/search/?s=' + query.replace(' ', '%20') 

        # initialize the driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # links = set([a['href'] for a in soup.find_all('a', {'class': ['teaserItem__title--32O7a']}, href=True)])
        links = set([a['href'] for a in soup.select('.teaserItem__title--32O7a a')])

        # find the "View More" button
        BUTTON_SELECTOR = "button#content-list__load-more-btn"
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, BUTTON_SELECTOR)))
        print("Retrieving from MIT Tech Review...")

        try:
            while button and k > 0:
                print("MIT Tech Review Progress: {}, {}".format(query, len(links)))
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)

                # get the new articles on the page
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # new_links = [a['href'] for a in soup.find_all('a', {'class': ['teaserItem__title--32O7a']}, href=True)]
                new_links = [a['href'] for a in soup.select('.teaserItem__title--32O7a a')]
                for nl in new_links:
                    if nl not in links:
                        links.add(nl)
                
                k -= 1
                self.save_to_db(links, "mit_tech_review")
                button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)
                time.sleep(1)
        except:
            print("Error retrieving from MIT Tech Review")

        driver.quit()
        print("Done retrieving from MIT Tech Review: {} links".format(len(links)))
        return list(links)
    

    def retreive_from_the_verge(self, k=100):
        print("Retrieving from The Verge... : {}".format(self.keyword))
        query = self.keyword
        url = 'https://www.theverge.com/search?q=' + query.replace(' ', '%20')

        # initialize the driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')


        # links = set([a['href'] for a in soup.find_all('a', {'class': ['w-full', 'max-w-content-block-standard']}, href=True)])
        links = set(["https://www.theverge.com" + a['href'] for a in soup.select('.w-full.max-w-content-block-standard h2 a')])

        # find the "Next" button   
        # hover:border-b-text-gray-13 border-b border-b-blurple font-polysans text-12 uppercase leading-120 tracking-15 text-blurple hover:text-gray-13 dark:border-b-franklin dark:text-franklin dark:hover:border-white dark:hover:text-white md:text-15
        BUTTON_XPATH = "//button[text()='Next']"
        button = wait.until(EC.presence_of_element_located((By.XPATH, BUTTON_XPATH)))
        print("Retrieving from The Verge...")

        try:
            while button and k > 0:
                print("The Verge Progress: {}, {}".format(query, len(links)))
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)

                # get the new articles on the page
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # new_links = [a['href'] for a in soup.find_all('a', {'class': ['max-w-content-block-standard']}, href=True)]
                new_links = ["https://www.theverge.com" + a['href'] for a in soup.select('.w-full.max-w-content-block-standard h2 a')]
                for nl in new_links:
                    if nl not in links:
                        links.add(nl)
                
                k -= 1
                self.save_to_db(links, "the_verge")
                button = driver.find_element(By.XPATH, BUTTON_XPATH)
                time.sleep(1)
        except:
            print("Error retrieving from The Verge")

        driver.quit()
        print("Done retrieving from The Verge: {} links".format(len(links)))
        return list(links)
    

    def download_and_parse(self, link, sector, source):
        try:
            article = Article(link)
            article.download()
            article.parse()

            title = article.title
            if len(title) <= 1:
                time.sleep(2)
                article = Article(link)
                article.download()
                article.parse()
                title = article.title
                if len(title) <= 1:
                    return None

            if "techcrunch" in title:
                title = title.replace("techcrunch", "")

            # source = os.path.basename(file).replace(sector.replace(" ", "_"), "").replace(".pkl", "").replace("_", " ")

            element = {
                'title': title,
                'text': article.text,
                'sector': sector,
                'source': source,
                'url': link,
                'published_at': article.publish_date.strftime("%m/%d/%Y") if article.publish_date else 'Unknown'
            }

            return element
        except Exception as e:
            print(f"Error processing link {link}. Error: {e}")
            return None
        
    def parse_articles(self):
        elements = []
        
        for file in glob.glob("{}/*.pkl".format(self.domain_folder)):
            try:
                with open(file, "rb") as f:
                    links = pickle.load(f, encoding='utf-8')
                print("#### File: {}; Number of links: {}".format(file, len(links)))

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    sector = self.keyword
                    if "techcrunch" in file:
                        source = "techcrunch"
                    elif "mit_tech_review" in file:
                        source = "MIT Tech Review"
                    elif "the_verge" in file:
                        source = "The Verge"
                    elif "wired" in file:
                        source = "Wired"
                    else:
                        source = "Unknown"
                    
                    results = list(tqdm.tqdm(executor.map(self.download_and_parse, links, [sector] * len(links), [source] * len(links)), total=len(links)))
                elements.extend([result for result in results if result is not None])

                print("#### File: {}; Number of elements: {}".format(file, len(elements)))
                with open("./{}/articles.pkl".format(domain_folder), "wb") as f:
                    pickle.dump(elements, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            except Exception as e:
                print(f"Error processing file {file}. Error: {e}")

    
    def format(self):
        with open("{}/articles.pkl".format(self.domain_folder), "rb") as f:
            articles = pickle.load(f)
            dic = {a["url"]: a for a in articles}

        with open("{}/articles_dic.pkl".format(self.domain_folder), "wb") as f:
            pickle.dump(dic, f, protocol=pickle.HIGHEST_PROTOCOL)

        


if __name__ == "__main__":
    # Fetch articles
    domain_name = "natural language processing"
    domain_folder = "natural_language_processing"

    fetcher = Fetcher(domain_name, domain_folder)
    # fetcher.retreive_from_the_verge()
    fetcher.retrieve_from_wired()
    # fetcher.retrieve_from_mit_tech_review()
    fetcher.retrieve_from_techcrunch("https://search.techcrunch.com/search;_ylt=Awr99Tzr3fdkGCEFqh.nBWVH;_ylc=X1MDMTE5NzgwMjkxOQRfcgMyBGZyAwRncHJpZAN1VXhXUVlzWlR2RzlCSEhxMmxvT21BBG5fcnNsdAMwBG5fc3VnZwM5BG9yaWdpbgNzZWFyY2gudGVjaGNydW5jaC5jb20EcG9zAzAEcHFzdHIDBHBxc3RybAMwBHFzdHJsAzI3BHF1ZXJ5A25hdHVyYWwlMjBsYW5ndWFnZSUyMHByb2Nlc3NpbmcEdF9zdG1wAzE2OTM5NjU4MDc-?p=natural+language+processing&fr2=sb-top")
    
    # Parse articles
    fetcher.parse_articles()
    fetcher.format()
    



# import glob
# import tqdm
# import pickle
# from newspaper import Article
# import concurrent.futures
# import time
# import os

# def download_and_parse(link):
#     try:
#         article = Article(link)
#         article.download()
#         article.parse()

#         title = article.title
#         if len(title) <= 1:
#             time.sleep(2)
#             article = Article(link)
#             article.download()
#             article.parse()
#             title = article.title
#             if len(title) <= 1:
#                 return None

#         if "techcrunch" in title:
#             title = title.replace("techcrunch", "")

#         sector = "AI decision making"
#         source = os.path.basename(file).replace(sector.replace(" ", "_"), "").replace(".pkl", "").replace("_", " ")

#         element = {
#             'title': title,
#             'text': article.text,
#             'sector': sector,
#             'source': source,
#             'url': link,
#             'published_at': article.publish_date.strftime("%m/%d/%Y") if article.publish_date else 'Unknown'
#         }

#         return element
#     except Exception as e:
#         print(f"Error processing link {link}. Error: {e}")
#         return None

# elements = []
# for file in glob.glob("{}/*.pkl".format(domain_folder)):
#     print(file)
    
#     try:
#         with open(file, "rb") as f:
#             links = pickle.load(f, encoding='utf-8')
#         print("#### File: {}; Number of links: {}".format(file, len(links)))

#         with concurrent.futures.ThreadPoolExecutor() as executor:
#             results = list(tqdm.tqdm(executor.map(download_and_parse, links), total=len(links)))
#         elements.extend([result for result in results if result is not None])

#         print("#### File: {}; Number of elements: {}".format(file, len(elements)))
#         with open("./{}/articles.pkl".format(domain_folder), "wb") as f:
#             pickle.dump(elements, f, protocol=pickle.HIGHEST_PROTOCOL)

#     except Exception as e:
#         print(f"Error processing file {file}. Error: {e}")


# with open("{}/articles.pkl".format(domain_folder), "rb") as f:
#     articles = pickle.load(f)
#     dic = {a["url"]: a for a in articles}

# with open("{}/articles_dic.pkl".format(domain_folder), "wb") as f:
#     pickle.dump(dic, f, protocol=pickle.HIGHEST_PROTOCOL)