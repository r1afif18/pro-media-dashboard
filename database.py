import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    
    # Buat tabel untuk menyimpan history query AI
    c.execute('''
        CREATE TABLE IF NOT EXISTS ai_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Buat tabel untuk menyimpan insights custom
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
    
    # Buat tabel untuk menyimpan data yang diupload
    c.execute('''
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_ai_history(username, query, response):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO ai_history (username, query, response) VALUES (?, ?, ?)",
        (username, query, response)
    )
    conn.commit()
    conn.close()

def get_ai_history(username, limit=10):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute(
        "SELECT query, response, timestamp FROM ai_history WHERE username = ? ORDER BY timestamp DESC LIMIT ?",
        (username, limit)
    )
    history = c.fetchall()
    conn.close()
    return history

def save_custom_insight(username, title, content, tags):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute(
        "INSERT INTO custom_insights (username, title, content, tags) VALUES (?, ?, ?, ?)",
        (username, title, content, ','.join(tags) if tags else None)
    )
    conn.commit()
    conn.close()

def get_custom_insights(username):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute(
        "SELECT id, title, content, tags, created_at FROM custom_insights WHERE username = ? ORDER BY created_at DESC",
        (username,)
    )
    insights = []
    for row in c.fetchall():
        insights.append({
            'id': row[0],
            'title': row[1],
            'content': row[2],
            'tags': row[3].split(',') if row[3] else [],
            'created_at': row[4]
        })
    conn.close()
    return insights

def delete_custom_insight(insight_id):
    conn = sqlite3.connect('app_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM custom_insights WHERE id = ?", (insight_id,))
    conn.commit()
    conn.close()