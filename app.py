import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from components import (
    tab_overview,
    tab_upload,
    tab_ai_lab,
    tab_forecasting,
    tab_insights,
    tab_about
)
import sqlite3
import hashlib

# Import dua init_db dari dua modul berbeda
from auth import init_db as init_user_db, authenticate_user, register_user
from database import init_db as init_app_db

# Load environment variables
load_dotenv()

# Inisialisasi semua database
init_user_db()    # Membuat & inisialisasi tabel users di users.db
init_app_db()     # Membuat & inisialisasi tabel lain di app_data.db

# Konfigurasi halaman
st.set_page_config(
    page_title="ProMedia Insight Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi session state
if 'authentication_status' not in st.session_state:
    st.session_state.authentication_status = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'ai_history' not in st.session_state:
    st.session_state.ai_history = []

# CSS Custom untuk styling
st.markdown("""
<style>
.header-title {
    font-size: 2.8rem;
    color: #2563EB;
    text-align: center;
    padding: 0.5rem 0;
    border-bottom: 3px solid #FF6B6B;
    margin-bottom: 2rem;
}
@media (max-width: 768px) {
    .stDataFrame { width: 100% !important; }
    .stButton>button { width: 100%; }
    .header-title { font-size: 2rem; }
}
</style>
""", unsafe_allow_html=True)

# Tampilkan header
st.markdown('<h1 class="header-title">📊 ProMedia Insight Hub</h1>', unsafe_allow_html=True)
st.caption("Dashboard Analisis Media Berbasis AI - Eksplorasi, Insight, dan Visualisasi Data Berita")

# Sidebar login
with st.sidebar:
    if not st.session_state.authentication_status:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            if username and password:
                authenticated, role = authenticate_user(username, password)
                if authenticated:
                    st.session_state.authentication_status = True
                    st.session_state.username = username
                    st.session_state.role = role
                    st.rerun()
                else:
                    st.error("Username atau password salah")
            else:
                st.warning("Harap isi username dan password")
    else:
        st.write(f"Selamat datang, {st.session_state.username}!")
        if st.button("Logout"):
            st.session_state.authentication_status = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()

# Hanya tampilkan dashboard jika sudah login
if not st.session_state.authentication_status:
    st.title("ProMedia Insight Hub")
    st.info("Silakan login di sidebar untuk mengakses dashboard")
    st.stop()

# Tab navigasi
tabs = {
    "Overview": tab_overview,
    "Upload & Eksplorasi Data": tab_upload,
    "AI Lab": tab_ai_lab,
    "Forecasting": tab_forecasting,
    "Insights Custom": tab_insights,
    "Tentang": tab_about,
}

# Buat tab
tab_titles = list(tabs.keys())
active_tab = st.sidebar.radio("Navigasi Menu", tab_titles)

# Tampilkan tab aktif
tabs[active_tab].show()
