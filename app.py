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
from database import init_db as init_app_db

# Load environment variables
load_dotenv()

# Inisialisasi database aplikasi (hanya untuk data utama)
init_app_db()     # Membuat & inisialisasi tabel utama di app_data.db

# Konfigurasi halaman
st.set_page_config(
    page_title="ProMedia Insight Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi session state (tanpa user)
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

# Sidebar tanpa login/register
with st.sidebar:
    st.info("Selamat datang di ProMedia Insight Hub! Semua fitur dapat diakses tanpa login.")

# Tampilkan tab utama
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Upload Data", "AI Lab", "Forecasting", "Insights", "About"
])
tab_overview(tab1)
tab_upload(tab2)
tab_ai_lab(tab3)
tab_forecasting(tab4)
tab_insights(tab5)
tab_about(tab6)
