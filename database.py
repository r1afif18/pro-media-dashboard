import sqlite3

DB_PATH = "app_data.db"

def init_db():
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
    tag_str = ','.join(tags) if tags else ''
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO custom_insights (title, content, tags) VALUES (?, ?, ?)",
            (title, content, tag_str)
        )
        conn.commit()

def get_custom_insights():
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
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("DELETE FROM custom_insights WHERE id=?", (insight_id,))
        conn.commit()
