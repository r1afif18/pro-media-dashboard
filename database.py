import sqlite3
import os
import logging

DB_PATH = os.path.join(os.path.dirname(__file__), "app_data.db")
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Table for custom insights
        c.execute("""
            CREATE TABLE IF NOT EXISTS custom_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Table for AI Lab history
        c.execute("""
            CREATE TABLE IF NOT EXISTS ai_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_custom_insight(title, content, tags):
    """Save custom insight to database"""
    tag_str = ','.join(tags) if tags else ''
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO custom_insights (title, content, tags) VALUES (?, ?, ?)",
            (title, content, tag_str)
        )
        conn.commit()

def get_custom_insights():
    """Get all custom insights"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT id, title, content, tags, created_at FROM custom_insights ORDER BY created_at DESC")
        rows = c.fetchall()
        insights = []
        for row in rows:
            insights.append({
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'tags': row[3].split(',') if row[3] else [],
                'created_at': row[4]
            })
        return insights

def delete_custom_insight(insight_id):
    """Delete custom insight"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM custom_insights WHERE id=?", (insight_id,))
        conn.commit()

def save_ai_history(prompt, response):
    """Save AI conversation history"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO ai_history (prompt, response) VALUES (?, ?)",
            (prompt, response)
        )
        conn.commit()

def get_ai_history(limit=20):
    """Get AI conversation history"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "SELECT id, prompt, response, created_at FROM ai_history ORDER BY created_at DESC LIMIT ?",
            (limit,)
        )
        rows = c.fetchall()
        history = []
        for row in rows:
            history.append({
                'id': row[0],
                'prompt': row[1],
                'response': row[2],
                'created_at': row[3]
            })
        return history

def delete_ai_history(history_id):
    """Delete AI history"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM ai_history WHERE id=?", (history_id,))
        conn.commit()
