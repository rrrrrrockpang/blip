import sys
sys.dont_write_bytecode = True

import argparse
import logging
import os
from dotenv import load_dotenv
from _1tempsqlite import TempArticleDB
from _2websitescraper import ArticleRequester
from _3classifierssummarizer import TitleClassifier
from _3classifierssummarizer import ContentFilter
from _3classifierssummarizer import Summarizer
from _3classifierssummarizer import AspectClassifier
from _4supabase import SupabaseUploader


def main(supabase_url, supabase_key, model_path):
    logging.basicConfig(level=logging.INFO)
    
    # Initialize temporary database
    temp_db = TempArticleDB('temp_processing.db')
    
    try:
        # Step 1: Fetch articles
        logging.info("=== Step 1: Fetching Articles ===")
        fetcher = ArticleRequester(temp_db)
        fetcher.fetch_all_sources()
        
        # Step 2: Title classification
        logging.info("=== Step 2: Title Classification ===")
        title_classifier = TitleClassifier(temp_db, model_path)
        title_classifier.process()
        
        # Step 3: Content filtering
        logging.info("=== Step 3: Content Filtering ===")
        content_filter = ContentFilter(temp_db)
        content_filter.process()
        
        # Step 4: Summarization
        logging.info("=== Step 4: Summarization ===")
        summarizer = Summarizer(temp_db)
        summarizer.process()
        
        # Step 5: Aspect classification
        logging.info("=== Step 5: Aspect Classification ===")
        aspect_classifier = AspectClassifier(temp_db)
        aspect_classifier.process()

        # Step 6: Upload to Supabase
        logging.info("=== Step 6: Uploading to Supabase ===")
        uploader = SupabaseUploader(supabase_url, supabase_key, temp_db)
        uploaded, skipped = uploader.upload_final_articles()
        
        logging.info(f"Pipeline complete! {uploaded} new articles added to production")
        
    finally:
        # Always cleanup temp database
        logging.info("=== Cleanup ===")
        temp_db.cleanup()


if __name__ == "__main__":
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    model_path = "./model"
    main(supabase_url, supabase_key, model_path)