import streamlit as st
from dotenv import load_dotenv
import os
from components import (
    tab_overview,
    tab_upload,
    tab_ai_lab,
    tab_forecasting,
    tab_insights,
    tab_about
)
from database import init_db as init_app_db

# Load environment variables
load_dotenv()

# Inisialisasi database aplikasi (jika perlu)
init_app_db()

# Konfigurasi halaman
st.set_page_config(
    page_title="ProMedia Insight Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi session state
if 'df' not in st.session_state:
    st.session_state.df = None
if 'ai_history' not in st.session_state:
    st.session_state.ai_history = []
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user' not in st.session_state:
    st.session_state.user = ""

# Login UI
def login_ui():
    st.title("Login ProMedia Insight Hub")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Ganti sesuai kebutuhan atau hubungkan ke DB User
        if username == "admin" and password == "admin123":
            st.session_state.authenticated = True
            st.session_state.user = username
            st.success("Login berhasil!")
            st.experimental_rerun()
        else:
            st.error("Username atau password salah!")

# Cek status login
if not st.session_state.authenticated:
    login_ui()
    st.stop()
else:
    with st.sidebar:
        st.success(f"Halo, {st.session_state.user}!")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = ""
            st.experimental_rerun()
        st.info("Selamat datang di ProMedia Insight Hub!")

    # CSS custom
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

    st.markdown('<h1 class="header-title">📊 ProMedia Insight Hub</h1>', unsafe_allow_html=True)
    st.caption("Dashboard Analisis Media Berbasis AI - Eksplorasi, Insight, dan Visualisasi Data Berita")

    # Definisi tab utama dan pemanggilan fungsi
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Overview", "Upload Data", "AI Lab", "Forecasting", "Insights", "About"
    ])
    tab_overview(tab1)
    tab_upload(tab2)
    tab_ai_lab(tab3)
    tab_forecasting(tab4)
    tab_insights(tab5)
    tab_about(tab6)
