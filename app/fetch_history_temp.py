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
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument("--headless")

class Fetcher():
    def __init__(self, keyword):
        self.keyword = keyword
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
        with open("{}_{}.pkl".format(self.keyword.replace(" ", "_"), source), "wb") as f:
            pickle.dump(stuff, f, protocol=pickle.HIGHEST_PROTOCOL)

    def retrieve_from_wired(self, k=50):
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
        while button and k > 0:
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
        driver.quit()
        print("Done retrieving from Wired: {} links".format(len(links)))
        return list(links)
    
    def retrieve_from_techcrunch(self, url, k=100):
        # has to input url since techcrunch website includes a random string
        query = self.keyword

        # initialize the driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = set([a['href'] for a in soup.find_all('a', {'class': ['compArticleList', "thmb"]}, href=True)])
        
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
                new_links = [a['href'] for a in soup.find_all('a', {'class': ['compArticleList', "thmb"]}, href=True)]
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
        return list(links)
    

    def retrieve_from_mit_tech_review(self, k=100):
        # get url
        query = self.keyword
        url = 'https://www.technologyreview.com/search/?s=' + query.replace(' ', '%20') 

        # initialize the driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        links = set([a['href'] for a in soup.find_all('a', {'class': ['teaserItem__title--32O7a']}, href=True)])

        # find the "View More" button
        BUTTON_SELECTOR = ".content-list__load-more-btn"
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, BUTTON_SELECTOR)))
        print("Retrieving from MIT Tech Review...")

        try:
            while button and k > 0:
                print("MIT Tech Review Progress: {}, {}".format(query, len(links)))
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)

                # get the new articles on the page
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                new_links = [a['href'] for a in soup.find_all('a', {'class': ['teaserItem__title--32O7a']}, href=True)]
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
        query = self.keyword
        url = 'https://www.theverge.com/search?q=' + query.replace(' ', '%20')

        # initialize the driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        links = set([a['href'] for a in soup.find_all('a', {'class': ['max-w-content-block-standard']}, href=True)])

        # find the "Next" button   
        # hover:border-b-text-gray-13 border-b border-b-blurple font-polysans text-12 uppercase leading-120 tracking-15 text-blurple hover:text-gray-13 dark:border-b-franklin dark:text-franklin dark:hover:border-white dark:hover:text-white md:text-15
        BUTTON_SELECTOR = "button.hover:border-b-text-gray-13.border-b.border-b-blurple.font-polysans.text-12.uppercase.leading-120.tracking-15.text-blurple.hover:text-gray-13.dark:border-b-franklin.dark:text-franklin.dark:hover:border-white.dark:hover:text-white.md:text-15"
        button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, BUTTON_SELECTOR)))
        print("Retrieving from The Verge...")

        try:
            while button and k > 0:
                print("The Verge Progress: {}, {}".format(query, len(links)))
                driver.execute_script("arguments[0].click();", button)
                time.sleep(2)

                # get the new articles on the page
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                new_links = [a['href'] for a in soup.find_all('a', {'class': ['max-w-content-block-standard']}, href=True)]
                for nl in new_links:
                    if nl not in links:
                        links.add(nl)
                
                k -= 1
                self.save_to_db(links, "the_verge")
                button = driver.find_element(By.CSS_SELECTOR, BUTTON_SELECTOR)
                time.sleep(1)
        except:
            print("Error retrieving from The Verge")

        driver.quit()
        print("Done retrieving from The Verge: {} links".format(len(links)))
        return list(links)
    

# with open("voice_assistant_techcrunch.pkl", "rb") as f:
#     links = pickle.load(f)
#     print(links)
#     print(len(links))


fetcher = Fetcher("mobile technology")
try:
    fetcher.retrieve_from_techcrunch("https://search.techcrunch.com/search;_ylt=AwrgxQYiy.5kqvICdjenBWVH;_ylc=X1MDMTE5NzgwMjkxOQRfcgMyBGZyA3RlY2hjcnVuY2gEZ3ByaWQDa3ZMZ0dYQk9RSnlCMW5zRkU0MVdmQQRuX3JzbHQDMARuX3N1Z2cDOARvcmlnaW4Dc2VhcmNoLnRlY2hjcnVuY2guY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAMxNwRxdWVyeQNtb2JpbGUlMjB0ZWNobm9sb2d5BHRfc3RtcAMxNjkzMzcxMjA1?p=mobile+technology&fr2=sb-top&fr=techcrunch")
except:
    pass

try: 
    fetcher.retrieve_from_wired()
except:
    pass

try:
    fetcher.retrieve_from_mit_tech_review()
except:
    pass

try:
    fetcher.retreive_from_the_verge()
except:
    pass


# fetcher = Fetcher("accessibility")
# try:
#     fetcher.retrieve_from_techcrunch("https://search.techcrunch.com/search;_ylt=AwrOs9jLte5kiKkBHMWnBWVH;_ylc=X1MDMTE5NzgwMjkxOQRfcgMyBGZyA3RlY2hjcnVuY2gEZ3ByaWQDVzBicUtCcHdSZzY3MXFUVFdMVDBNQQRuX3JzbHQDMARuX3N1Z2cDMQRvcmlnaW4Dc2VhcmNoLnRlY2hjcnVuY2guY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAMxOARxdWVyeQNhaSUyMGRlY2lzaW9uJTIwbWFraW5nBHRfc3RtcAMxNjkzMzY1NzEx?p=ai+decision+making&fr2=sb-top&fr=techcrunch")
# except:
#     pass

# fetcher = Fetcher("computer vision")
# try:
#     fetcher.retrieve_from_techcrunch("https://search.techcrunch.com/search;_ylc=X3IDMgRncHJpZAM2SmtZNExleVNscUV2emEzNnhjUmpBBG5fc3VnZwM5BHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAMxNQRxdWVyeQNjb21wdXRlciUyMHZpc2lvbgR0X3N0bXADMTY5MzM2NTY5NQ--?p=computer+vision&fr=techcrunch")
# except:
#     pass
