import sqlite3
from typing import Optional
from app.config import settings


class Database:
    """Data layer for SQLite database operations."""
    
    def __init__(self) -> None:
        self.db_path: str = settings.database_url.replace("sqlite:///./", "")
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self) -> None:
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume TEXT NOT NULL,
                job_description TEXT NOT NULL,
                compatibility_score INTEGER NOT NULL,
                strengths TEXT NOT NULL,
                weaknesses TEXT NOT NULL,
                suggestions TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_analysis(
        self,
        resume: str,
        job_description: str,
        compatibility_score: int,
        strengths: str,
        weaknesses: str,
        suggestions: str,
        **kwargs
    ) -> int:
        """Save analysis result to database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO analyses (resume, job_description, compatibility_score, strengths, weaknesses, suggestions)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (resume, job_description, compatibility_score, strengths, weaknesses, suggestions))
        
        conn.commit()
        analysis_id = cursor.lastrowid
        conn.close()
        
        return analysis_id


db = Database()
