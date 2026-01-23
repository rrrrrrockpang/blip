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
    
    # Step 1: Fetch articles
    logging.info("=== Step 1: Fetching Articles ===")
    fetcher = ArticleRequester(temp_db)
    fetcher.fetch_all_sources()
    


if __name__ == "__main__":
    load_dotenv()
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    model_path = "./model"
    main(supabase_url, supabase_key, model_path)