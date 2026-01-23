import sqlite3
import os
from contextlib import contextmanager


class TempArticleDB:
    def __init__(self, db_path='temp_processing.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize temporary SQLite database with all processing fields"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                text TEXT,
                sector TEXT,
                source TEXT,
                published_at TEXT,
                
                -- Processing fields
                prediction TEXT,
                score REAL,
                gpt3_filter_answer TEXT,
                gpt3_summary TEXT,
                gpt3_aspect TEXT,
                processing_stage TEXT DEFAULT 'scraped',
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_url ON articles(url)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_stage ON articles(processing_stage)')
        
        conn.commit()
        conn.close()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        try:
            yield conn
        finally:
            conn.close()
    
    def article_exists(self, url):
        """Check if article already exists"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM articles WHERE url = ?', (url,))
            return cursor.fetchone() is not None
    
    def insert_article(self, article_data):
        """Insert new article into temp database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO articles (url, title, text, sector, source, published_at, processing_stage)
                VALUES (?, ?, ?, ?, ?, ?, 'scraped')
            ''', (
                article_data['url'],
                article_data['title'],
                article_data['text'],
                article_data['sector'],
                article_data['source'],
                article_data.get('published_at', '')
            ))
            conn.commit()
    
    def get_articles_by_stage(self, stage, limit=None):
        """Get articles at a specific processing stage"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            query = 'SELECT * FROM articles WHERE processing_stage = ?'
            if limit:
                query += f' LIMIT {limit}'
            cursor.execute(query, (stage,))
            return [dict(row) for row in cursor.fetchall()]
    
    def update_article(self, article_id, updates):
        """Update article fields"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            set_clause = ', '.join([f'{k} = ?' for k in updates.keys()])
            values = list(updates.values()) + [article_id]
            cursor.execute(f'UPDATE articles SET {set_clause} WHERE id = ?', values)
            conn.commit()
    
    def get_final_articles(self):
        """Get all fully processed articles ready for Supabase"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT url, title, text, sector, source, gpt3_summary, gpt3_aspect
                FROM articles 
                WHERE processing_stage = 'classified'
                AND gpt3_summary IS NOT NULL
                AND gpt3_summary != ''
                AND gpt3_summary NOT LIKE '%NO_CONSEQUENCE%'
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    def cleanup(self):
        """Delete the temporary database file"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"Deleted temporary database: {self.db_path}")