import sqlite3
import hashlib
import streamlit as st

def init_db():
    """Inisialisasi database user"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Perbaikan: Hapus tabel lama jika ada skema berbeda
    c.execute("DROP TABLE IF EXISTS users")
    
    # Buat tabel baru dengan skema yang diperbarui
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tambahkan user admin default jika belum ada
    c.execute("SELECT * FROM users WHERE username='admin'")
    if not c.fetchone():
        hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", hashed_password, "admin")
        )
    
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    """Autentikasi user"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result:
        stored_password, role = result
        if stored_password == hashlib.sha256(password.encode()).hexdigest():
            return True, role
    return False, None

def register_user(username, password, role='user'):
    """Daftarkan user baru"""
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        
        # Cek apakah username sudah ada
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            return False, "Username sudah digunakan"
        
        # Hash password
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
        # Tambahkan user baru
        c.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_pw, role)
        )
        
        conn.commit()
        conn.close()
        return True, None
    except sqlite3.Error as e:
        return False, str(e)