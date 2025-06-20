import sqlite3
import logging

DB_PATH = "app_data.db"
logger = logging.getLogger(__name__)

def init_db():
    """Inisialisasi database utama untuk aplikasi (tanpa tabel user)"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS custom_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

def save_custom_insight(title, content, tags):
    try:
        tag_str = ','.join(tags) if tags else None
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO custom_insights (title, content, tags) VALUES (?, ?, ?)",
                (title, content, tag_str)
            )
            conn.commit()
            logger.info(f"Saved custom insight: {title}")
    except Exception as e:
        logger.error(f"Error saving custom insight: {str(e)}")

def get_custom_insights():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, title, content, tags, created_at FROM custom_insights ORDER BY created_at DESC"
            )
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
    except Exception as e:
        logger.error(f"Error retrieving custom insights: {str(e)}")
        return []
