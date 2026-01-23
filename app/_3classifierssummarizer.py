import sys
sys.dont_write_bytecode = True

import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
from tqdm import tqdm
from _1tempsqlite import TempArticleDB
from helper import llmRequester

class TitleClassifier:
    def __init__(self, temp_db: TempArticleDB, model_path: str):
        self.temp_db = temp_db
        self.tokenizer = AutoTokenizer.from_pretrained("roberta-base")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_path, local_files_only=True
        )
    
    def evaluate(self, text):
        """Classify article title"""
        pipe = TextClassificationPipeline(model=self.model, tokenizer=self.tokenizer)
        res = pipe(text)[0]
        label = f"LABEL_{0 if res['label'] == 'LABEL_0' else 1}_{'irrelevant' if res['label'] == 'LABEL_0' else 'relevant'}"
        return label, res['score']
    
    def process(self):
        """Process all scraped articles"""
        articles = self.temp_db.get_articles_by_stage('scraped')
        logging.info(f"Processing {len(articles)} articles with title classifier")
        
        for article in tqdm(articles):
            prediction, score = self.evaluate(article['title'])
            
            self.temp_db.update_article(article['id'], {
                'prediction': prediction,
                'score': score,
                'processing_stage': 'title_filtered'
            })
        
        logging.info(f"Title classification complete")


class ContentFilter:
    def __init__(self, temp_db: TempArticleDB):
        self.temp_db = temp_db
        self.llm = llmRequester()  # Your LLM helper
    
    def get_filter_prompt(self):
        return "Does the article discuss unintended or undesirable consequences of <domain> on society? Answer only Yes or No.\n\n\"{text}\""
    
    def process(self):
        """Filter articles by content"""
        articles = self.temp_db.get_articles_by_stage('title_filtered')
        # Only process relevant articles
        articles = [a for a in articles if a['prediction'] == 'LABEL_1_relevant']
        
        logging.info(f"Processing {len(articles)} articles with content filter")
        
        for article in tqdm(articles):
            if len(article['text']) > 13000:
                continue
            
            prompt = self.get_filter_prompt().replace("<domain>", article['sector'])
            answer = self.llm.run_llama(prompt=prompt, text=article['text'])
            
            self.temp_db.update_article(article['id'], {
                'gpt3_filter_answer': answer,
                'processing_stage': 'content_filtered'
            })
        
        logging.info("Content filtering complete")


class Summarizer:
    def __init__(self, temp_db: TempArticleDB):
        self.temp_db = temp_db
        self.llm = llmRequester()
    
    def get_summary_prompt(self):
        return '''You goal is to inspire users to be more aware of undesirable consequences of <domain>, using insights from the below input text.
Extract and summarize any undesirable consequence of the technology from the article. Please answer NO_CONSEQUENCE if no undesirable consequence of <domain> technology on society is found.

"{text}"

Answer about the undesirable consequence in 1-3 sentences:'''
    
    def process(self):
        """Summarize filtered articles"""
        articles = self.temp_db.get_articles_by_stage('content_filtered')
        # Only process articles that passed content filter
        articles = [a for a in articles if 'yes' in a['gpt3_filter_answer'].lower()]
        
        logging.info(f"Processing {len(articles)} articles with summarizer")
        
        for article in tqdm(articles):
            if len(article['text']) > 13000:
                continue
            
            prompt = self.get_summary_prompt().replace("<domain>", article['sector'])
            summary = self.llm.run_llama(prompt=prompt, text=article['text'])
            
            # Skip if no consequence found
            if "no_consequence" in summary.lower():
                continue
            
            self.temp_db.update_article(article['id'], {
                'gpt3_summary': summary,
                'processing_stage': 'summarized'
            })
        
        logging.info("Summarization complete")


class AspectClassifier:
    def __init__(self, temp_db: TempArticleDB):
        self.temp_db = temp_db
        self.llm = llmRequester()
    
    def get_aspect_prompt(self):
        return '''List of possible domain: Health & Well-being, Security & Privacy, Equality & Justice, User Experience, Economy, Access to Information & Discourse, Environment & Sustainability, Politics, Power Dynamics, Social Norms & Relationship. 

Which one aspect of life does the following consequence affect? (Please only select one)
    
Summary of the consequence: "{text}"

One Aspect (Please only select one from above):'''
    
    def process(self):
        """Classify aspects of summarized articles"""
        articles = self.temp_db.get_articles_by_stage('summarized')
        
        logging.info(f"Processing {len(articles)} articles with aspect classifier")
        
        for article in tqdm(articles):
            if len(article['text']) > 19000:
                continue
            
            aspect = self.llm.run_llama(
                prompt=self.get_aspect_prompt(),
                text=article['gpt3_summary']
            )
            
            self.temp_db.update_article(article['id'], {
                'gpt3_aspect': aspect,
                'processing_stage': 'classified'
            })
        
        logging.info("Aspect classification complete")