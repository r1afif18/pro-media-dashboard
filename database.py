import sqlite3
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine the base directory and set the database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app_data.db')

def init_db():
    """Initialize the database and create tables if they don't exist."""
    try:
        logger.info(f"Initializing database at: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Create ai_history table
        c.execute('''
            CREATE TABLE IF NOT EXISTS ai_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create custom_insights table
        c.execute('''
            CREATE TABLE IF NOT EXISTS custom_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create datasets table
        c.execute('''
            CREATE TABLE IF NOT EXISTS datasets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create users table if not exists
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT DEFAULT 'user'
            )
        ''')
        
        # Check if tables were created
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in c.fetchall()]
        logger.info(f"Database tables: {tables}")
        
        conn.commit()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
    finally:
        if conn:
            conn.close()

def save_ai_history(username, query, response):
    """Save an AI interaction to the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO ai_history (username, query, response) VALUES (?, ?, ?)",
                (username, query, response)
            )
            conn.commit()
            logger.info(f"Saved AI history for {username}")
    except Exception as e:
        logger.error(f"Error saving AI history: {str(e)}")

def get_ai_history(username, limit=10):
    """Retrieve AI interaction history for a user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            
            # Check if the table exists
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ai_history'")
            table_exists = c.fetchone()
            
            if not table_exists:
                # If the table doesn't exist, initialize the database and return empty list
                logger.warning("ai_history table not found, initializing database")
                init_db()
                return []
            
            c.execute(
                "SELECT query, response, timestamp FROM ai_history WHERE username = ? ORDER BY timestamp DESC LIMIT ?",
                (username, limit)
            )
            return c.fetchall()
    except Exception as e:
        logger.error(f"Error retrieving AI history: {str(e)}")
        return []

def save_custom_insight(username, title, content, tags):
    """Save a custom insight to the database."""
    try:
        tag_str = ','.join(tags) if tags else None
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO custom_insights (username, title, content, tags) VALUES (?, ?, ?, ?)",
                (username, title, content, tag_str)
            )
            conn.commit()
            logger.info(f"Saved custom insight for {username}")
    except Exception as e:
        logger.error(f"Error saving custom insight: {str(e)}")

def get_custom_insights(username):
    """Retrieve custom insights for a user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            
            # Check if the table exists
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='custom_insights'")
            table_exists = c.fetchone()
            
            if not table_exists:
                init_db()
                return []
            
            c.execute(
                "SELECT id, title, content, tags, created_at FROM custom_insights WHERE username = ? ORDER BY created_at DESC",
                (username,)
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

def delete_custom_insight(insight_id):
    """Delete a custom insight by ID."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM custom_insights WHERE id = ?", (insight_id,))
            conn.commit()
            logger.info(f"Deleted insight ID: {insight_id}")
    except Exception as e:
        logger.error(f"Error deleting custom insight: {str(e)}")

def create_user(username, password, role='user'):
    """Create a new user in the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            conn.commit()
            logger.info(f"Created user: {username}")
            return True
    except sqlite3.IntegrityError:
        logger.warning(f"Username {username} already exists")
        return False
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        return False

def authenticate_user(username, password):
    """Authenticate a user."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT role FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            result = c.fetchone()
            if result:
                logger.info(f"User authenticated: {username}")
                return True, result[0]  # Return authentication status and role
            return False, None
    except Exception as e:
        logger.error(f"Error authenticating user: {str(e)}")
        return False, None

def get_user_role(username):
    """Get a user's role."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT role FROM users WHERE username = ?",
                (username,)
            )
            result = c.fetchone()
            return result[0] if result else 'user'
    except Exception as e:
        logger.error(f"Error getting user role: {str(e)}")
        return 'user'

# Initialize the database when this module is imported
init_db()
