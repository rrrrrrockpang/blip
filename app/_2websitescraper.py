import sys
sys.dont_write_bytecode = True

from datetime import datetime, timedelta

import requests
from newspaper import Article
import logging
from _1tempsqlite import TempArticleDB
import time
import feedparser
import os
from dotenv import load_dotenv


class ArticleRequester:
    def __init__(self, temp_db: TempArticleDB):
        self.temp_db = temp_db
        self.current_date = datetime.now()
        self.seven_days_ago = self.current_date - timedelta(days=7)
        self.queries = ['social media', 'voice assistants', 'virtual reality', 
                        'computer vision', 'robotics', 'mobile technology',
                        'ai decision-making', 'neuroscience', 'computational biology',
                        'ubiquitous computing']
        
    def get_article(self, article):
        """Download and parse article"""
        try:
            newspaperArticle = Article(article["url"])
            newspaperArticle.download()
            newspaperArticle.parse()

            return {
                'title': article["title"],
                'text': newspaperArticle.text,
                'source': article["source"]["name"],
                'url': article["url"],
                'published_at': article.get("publishedAt", "")
            }
        except Exception as e:
            logging.error(f"Error fetching article: {e}")
            return None
    
    def fetch_from_arxiv(self, keyword: str, max_results: int = 100):
        """
        Fetch articles from arXiv API
        arXiv categories relevant to tech: cs.AI, cs.CY (Computers and Society), cs.HC (Human-Computer Interaction)
        """
        logging.info(f"Fetching arXiv articles for: {keyword}")
        
        # arXiv API base URL
        base_url = 'http://export.arxiv.org/api/query'
        
        # Build search query - search in title
        search_query = f'ti:"{keyword}"'
        
        # Calculate date range for filtering
        from_date = self.seven_days_ago.strftime('%Y%m%d')
        to_date = self.current_date.strftime('%Y%m%d')
        
        params = {
            'search_query': search_query,
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        try:
            # Use urllib.parse to properly encode parameters
            from urllib.parse import urlencode
            query_url = f"{base_url}?{urlencode(params)}"
            
            # Parse the Atom feed response
            feed = feedparser.parse(query_url)
            
            articles_added = 0
            for entry in feed.entries:
                # Parse submission date
                published_date = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ')
                
                # Only include articles from the past week
                if published_date < self.seven_days_ago:
                    continue
                
                # Extract arXiv ID and construct URL
                arxiv_id = entry.id.split('/abs/')[-1]
                arxiv_url = f'https://arxiv.org/abs/{arxiv_id}'
                
                # Check if already exists
                if self.temp_db.article_exists(arxiv_url):
                    continue
                
                # Extract abstract (arXiv's "text" content)
                abstract = entry.summary.replace('\n', ' ').strip()
                
                # Get primary category
                primary_category = entry.tags[0]['term'] if entry.tags else 'cs.CY'
                
                article_data = {
                    'title': entry.title,
                    'text': abstract,
                    'source': 'arXiv',
                    'url': arxiv_url,
                    'sector': keyword,
                    'published_at': published_date.strftime('%Y-%m-%d')
                }
                
                self.temp_db.insert_article(article_data)
                articles_added += 1
            
            logging.info(f"Added {articles_added} articles from arXiv for '{keyword}'")
            time.sleep(3)  # Be respectful to arXiv API
            return articles_added
            
        except Exception as e:
            logging.error(f"Error fetching from arXiv: {e}")
            return 0
    
    def fetch_from_guardian(self, guardian_api_key: str, keyword: str, page_size: int = 50):
        """
        Fetch articles from The Guardian API
        API Documentation: https://open-platform.theguardian.com/documentation/
        """
        logging.info(f"Fetching Guardian articles for: {keyword}")
        
        base_url = 'https://content.guardianapis.com/search'
        
        # Calculate date range
        from_date = self.seven_days_ago.strftime('%Y-%m-%d')
        to_date = self.current_date.strftime('%Y-%m-%d')
        
        params = {
            'q': keyword,
            'from-date': from_date,
            'to-date': to_date,
            'page-size': page_size,
            'show-fields': 'bodyText,trailText',  # Get article body and summary
            'show-tags': 'keyword',
            'order-by': 'relevance',
            'section': 'technology',  # Focus on technology section
            'api-key': guardian_api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['response']['status'] != 'ok':
                logging.error(f"Guardian API error: {data['response']['status']}")
                return 0
            
            articles_added = 0
            for item in data['response']['results']:
                # Check if already exists
                if self.temp_db.article_exists(item['webUrl']):
                    continue
                
                # Get full article body if available, otherwise use trail text
                article_text = item.get('fields', {}).get('bodyText', '')
                if not article_text:
                    article_text = item.get('fields', {}).get('trailText', '')
                
                # Skip if no substantial text
                if len(article_text) < 100:
                    continue
                
                article_data = {
                    'title': item['webTitle'],
                    'text': article_text,
                    'source': 'The Guardian',
                    'url': item['webUrl'],
                    'sector': keyword,
                    'published_at': item['webPublicationDate'][:10]  # Format: YYYY-MM-DD
                }
                
                self.temp_db.insert_article(article_data)
                articles_added += 1
            
            logging.info(f"Added {articles_added} articles from The Guardian for '{keyword}'")
            time.sleep(1)  # Rate limiting
            return articles_added
            
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching from Guardian API: {e}")
            return 0
        except Exception as e:
            logging.error(f"Unexpected error with Guardian API: {e}")
            return 0
    
    def fetch_from_nyt(self, nyt_api_key: str,  keyword: str, page_limit: int = 5):
        """
        Fetch articles from New York Times Article Search API
        API Documentation: https://developer.nytimes.com/docs/articlesearch-product/1/overview
        Note: NYT API has rate limit of 5 requests per minute and 500 per day
        """
        logging.info(f"Fetching NYT articles for: {keyword}")
        
        base_url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
        
        # Calculate date range (NYT format: YYYYMMDD)
        from_date = self.seven_days_ago.strftime('%Y%m%d')
        to_date = self.current_date.strftime('%Y%m%d')
        
        articles_added = 0
        
        # NYT API paginates with pages of 10 articles
        for page in range(page_limit):
            params = {
                'q': keyword,
                'begin_date': from_date,
                'end_date': to_date,
                'fq': 'news_desk:("Technology")',  # Filter to technology desk
                'sort': 'relevance',
                'page': page,
                'api-key': nyt_api_key
            }
            
            try:
                response = requests.get(base_url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data['status'] != 'OK':
                    logging.error(f"NYT API error: {data.get('status')}")
                    break
                
                articles = data['response']['docs']
                
                if not articles:
                    break  # No more articles
                
                for item in articles:
                    article_url = item['web_url']
                    
                    # Check if already exists
                    if self.temp_db.article_exists(article_url):
                        continue
                    
                    # Try to get full article text using newspaper library
                    try:
                        article = Article(article_url)
                        article.download()
                        article.parse()
                        article_text = article.text
                    except:
                        # Fallback to lead paragraph and snippet
                        article_text = item.get('lead_paragraph', '')
                        if item.get('snippet'):
                            article_text = item['snippet'] + '\n\n' + article_text
                    
                    # Skip if no substantial text
                    if len(article_text) < 100:
                        continue
                    
                    # Parse publication date
                    pub_date = datetime.strptime(
                        item['pub_date'], 
                        '%Y-%m-%dT%H:%M:%S%z'
                    ).strftime('%Y-%m-%d')
                    
                    article_data = {
                        'title': item['headline']['main'],
                        'text': article_text,
                        'source': 'New York Times',
                        'url': article_url,
                        'sector': keyword,
                        'published_at': pub_date
                    }
                    
                    self.temp_db.insert_article(article_data)
                    articles_added += 1
                
                # NYT rate limit: 5 requests per minute
                time.sleep(12)  # Wait 12 seconds between requests
                
            except requests.exceptions.RequestException as e:
                logging.error(f"Error fetching from NYT API (page {page}): {e}")
                if response.status_code == 429:  # Rate limit exceeded
                    logging.warning("Rate limit exceeded, waiting 60 seconds...")
                    time.sleep(60)
                break
            except Exception as e:
                logging.error(f"Unexpected error with NYT API: {e}")
                break
        
        logging.info(f"Added {articles_added} articles from NYT for '{keyword}'")
        return articles_added
    
    def fetch_all_sources(self):
        """
        Fetch articles from all sources (NewsAPI, arXiv, Guardian, NYT)
        """
        logging.info("Starting comprehensive article fetch from all sources")
        
        total_added = 0

            
        for query in self.queries:
            logging.info(f"\n=== Processing query: {query} ===")
            # arXiv
            logging.info("Fetching from arXiv...")
            tot_arxiv = self.fetch_from_arxiv(query, max_results=50)
            total_added += tot_arxiv
            logging.info(f"total found from arxiv: {tot_arxiv}")
            
            # The Guardian
            logging.info("Fetching from The Guardian...")

            guardian_api_key = os.getenv("GUARDIAN_API_KEY")
            tot_guardian = self.fetch_from_guardian(guardian_api_key, query, page_size=50)
            total_added += tot_guardian
            logging.info(f"total found from The Guardian: {tot_guardian}")
            
            # New York Times
            logging.info("Fetching from New York Times...")

            nyt_api_key = os.getenv("NYT_API_KEY")
            tot_nyt = self.fetch_from_nyt(nyt_api_key, query, page_limit=5)
            total_added += tot_nyt
            logging.info(f"total found from the NYT: {tot_nyt}")
            
            logging.info(f"Completed query: {query}")
        
        logging.info(f"\n=== Total articles added across all sources: {total_added} ===")
        return total_added