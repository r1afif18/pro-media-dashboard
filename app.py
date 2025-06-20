import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import logging
from components import (
    tab_overview,
    tab_upload,
    tab_ai_lab,
    tab_forecasting,
    tab_insights,
    tab_about
)
from database import init_db, DB_PATH, save_ai_history, get_ai_history, save_custom_insight, get_custom_insights, delete_custom_insight, authenticate_user, create_user, get_user_role

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ProMedia Insight Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
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

# Initialize database
try:
    logger.info(f"Initializing database from app.py at: {DB_PATH}")
    init_db()
    logger.info("Database initialized successfully from app.py")
except Exception as e:
    logger.error(f"Database initialization failed in app.py: {str(e)}")
    st.error(f"Database initialization failed: {str(e)}")

# Custom CSS styling
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
.sidebar-info {
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 15px;
}
@media (max-width: 768px) {
    .stDataFrame { width: 100% !important; }
    .stButton>button { width: 100%; }
    .header-title { font-size: 2rem; }
}
</style>
""", unsafe_allow_html=True)

# Display header
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
        
        st.divider()
        st.subheader("Register")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        
        if st.button("Create Account"):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    if create_user(new_username, new_password):
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists")
                else:
                    st.error("Passwords do not match")
            else:
                st.warning("Please fill all fields")
    else:
        st.write(f"Selamat datang, {st.session_state.username}!")
        st.write(f"Role: {st.session_state.role}")
        
        # Display database info
        st.divider()
        st.subheader("Database Status")
        db_exists = os.path.exists(DB_PATH)
        db_size = os.path.getsize(DB_PATH) if db_exists else 0
        
        st.markdown(f"""
        <div class="sidebar-info">
            <strong>Path:</strong> {DB_PATH}<br>
            <strong>Status:</strong> {"✅ Connected" if db_exists else "❌ Missing"}<br>
            <strong>Size:</strong> {db_size:,} bytes
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Logout"):
            st.session_state.authentication_status = False
            st.session_state.username = None
            st.session_state.role = None
            st.rerun()

# Only show the dashboard if logged in
if not st.session_state.authentication_status:
    st.title("ProMedia Insight Hub")
    st.info("Silakan login di sidebar untuk mengakses dashboard")
    st.stop()

# Tab navigation
tabs = {
    "Overview": tab_overview,
    "Upload & Eksplorasi Data": tab_upload,
    "AI Lab": tab_ai_lab,
    "Forecasting": tab_forecasting,
    "Insights Custom": tab_insights,
    "Tentang": tab_about,
}

# Create tabs
tab_titles = list(tabs.keys())
active_tab = st.sidebar.radio("Navigasi Menu", tab_titles)

# Show active tab
tabs[active_tab].show()
