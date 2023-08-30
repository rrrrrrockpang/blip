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

    def get_links(self, soup):
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
        links = set(self.get_links(soup))

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
            new_links = self.get_links(soup)
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
    
    




fetcher = Fetcher("voice assistant")
links = fetcher.retrieve_from_wired()
