import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        hashed_password = hash_password("admin123")
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", hashed_password, "admin")
        )
    conn.commit()
    conn.close()

def register_user(username, password, role="user"):
    init_db()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        hashed_password = hash_password(password)
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        conn.commit()
        return True, "Registrasi berhasil"
    except sqlite3.IntegrityError:
        return False, "Username sudah terdaftar"
    finally:
        conn.close()

def login_user(username, password):
    init_db()
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        "SELECT password, role FROM users WHERE username=?",
        (username,)
    )
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True, result[1]
    else:
        return False, None
