import sys
sys.dont_write_bytecode = True

from supabase import create_client
from _1tempsqlite import TempArticleDB
import logging
import tqdm


class SupabaseUploader:
    def __init__(self, supabase_url: str, supabase_key: str, temp_db: TempArticleDB):
        self.supabase = create_client(supabase_url, supabase_key)
        self.temp_db = temp_db
    
    def upload_final_articles(self):
        """Upload only fully processed articles to Supabase"""
        articles = self.temp_db.get_final_articles()
        
        logging.info(f"Uploading {len(articles)} final articles to Supabase")
        
        uploaded = 0
        skipped = 0
        
        for article in tqdm.tqdm(articles):
            try:
                # Check if already exists in production
                existing = self.supabase.table('data')\
                    .select('url')\
                    .eq('url', article['url'])\
                    .execute()
                
                if len(existing.data) > 0:
                    skipped += 1
                    continue
                
                # Map to your production schema
                data = {
                    'title': article['title'],
                    'text': article['text'],
                    'magazine': article['source'],  # maps to source
                    'url': article['url'],
                    'label': article['sector'],      # maps to sector
                    'gpt_summary': article['gpt3_summary'],
                    'sector': article['gpt3_aspect']  # the classified aspect
                }
                
                self.supabase.table('data').insert(data).execute()
                uploaded += 1
                
            except Exception as e:
                logging.error(f"Error uploading article {article['url']}: {e}")
        
        logging.info(f"Upload complete: {uploaded} uploaded, {skipped} skipped (already exist)")
        return uploaded, skipped