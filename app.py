import streamlit as st
from dotenv import load_dotenv
from auth import login_user, register_user, init_db as init_auth_db
from database import init_db as init_app_db
from components import (
    tab_overview,
    tab_upload,
    tab_ai_lab,
    tab_forecasting,
    tab_insights,
    tab_about
)
import logging
import os
import sys
from contextlib import contextmanager

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Global Exception Handler
@contextmanager
def st_exception_handler():
    try:
        yield
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error(f"CRITICAL ERROR [{exc_tb.tb_lineno}]: {str(e)}")
        st.error(f"🚨 Sistem mengalami gangguan: {str(e)}")
        st.error("Silakan refresh halaman atau hubungi administrator")
        st.stop()

# Initialize databases
init_auth_db()
init_app_db()

# Initialize session state
DEFAULT_STATE = {
    'df': None,
    'data_profile': None,
    'ai_history': [],
    'authenticated': False,
    'user': "",
    'role': "",
    'custom_insights': [],
    'google_api_key': os.getenv("GOOGLE_API_KEY", "")
}

for k, v in DEFAULT_STATE.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ========== UI Components ==========
def registration_ui():
    """UI for user registration (admin only)"""
    with st.expander("🛡️ Admin: Registrasi User Baru", expanded=True):
        new_username = st.text_input("Username Baru", key="reg_username")
        new_password = st.text_input("Password Baru", type="password", key="reg_password")
        confirm_password = st.text_input("Konfirmasi Password", type="password", key="reg_confirm")
        user_role = st.selectbox("Peran", ["user", "admin"], index=0, key="reg_role")
        
        if st.button("Daftarkan Pengguna"):
            if len(new_password) < 6:
                st.error("Password minimal 6 karakter")
            elif new_password != confirm_password:
                st.error("Password tidak cocok")
            else:
                success, message = register_user(new_username, new_password, user_role)
                if success:
                    st.success("Registrasi berhasil! Pengguna dapat login dengan akun baru")
                else:
                    st.error(f"Registrasi gagal: {message}")

def login_ui():
    """UI for user login"""
    st.title("Login ProMedia Insight Hub")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        with st.spinner("Memverifikasi..."):
            success, role = login_user(username, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.user = username
                st.session_state.role = role
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Username atau password salah!")

# ========== Main App Flow ==========
if not st.session_state.authenticated:
    st.info("Silakan login terlebih dahulu.")
    with st_exception_handler():
        login_ui()
    st.stop()

# Show dashboard if authenticated
else:
    with st.sidebar:
        st.success(f"Halo, {st.session_state.user}!")
        st.info("Selamat datang di ProMedia Insight Hub!")
        st.caption(f"Role: {st.session_state.role}")
        
        if st.session_state.role == "admin":
            registration_ui()
        
        if st.button("Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key not in DEFAULT_STATE:
                    del st.session_state[key]
            st.session_state.update(DEFAULT_STATE)
            st.rerun()

    # Corporate Professional CSS
    st.markdown("""
    <style>
    /* Corporate Color Palette */
    :root {
        --primary: #1a3c6e;
        --secondary: #4a6fa5;
        --accent: #d4a76a;
        --light: #f5f7fa;
        --dark: #2c3e50;
        --success: #27ae60;
        --warning: #f39c12;
        --danger: #e74c3c;
        --gray: #95a5a6;
    }
    
    /* Global Styles */
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp {
        background-color: #f9fafc;
    }
    
    /* Header */
    .header-title {
        font-size: 2.1rem;
        color: var(--primary);
        text-align: center;
        padding: 0.5rem 0;
        margin-bottom: 1.5rem;
        font-weight: 600;
        border-bottom: 1px solid #e0e6ed;
        padding-bottom: 0.8rem;
        letter-spacing: -0.5px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: #ffffff;
        border-bottom: 1px solid #e0e6ed;
        padding: 0 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.8rem 1.8rem;
        border: none;
        border-radius: 0;
        background: transparent;
        margin: 0;
        font-weight: 500;
        color: #7f8fa4;
        transition: all 0.3s;
        letter-spacing: -0.2px;
    }
    
    .stTabs [aria-selected="true"] {
        background: #ffffff;
        color: var(--primary);
        border-bottom: 3px solid var(--primary);
        box-shadow: none;
        font-weight: 600;
    }
    
    /* Cards */
    .card {
        background: #ffffff;
        border-radius: 8px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.03);
        border: 1px solid #e6eaf0;
        margin-bottom: 1.5rem;
    }
    
    .card-title {
        font-size: 1.15rem;
        color: var(--primary);
        margin-bottom: 1.2rem;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid #f0f2f5;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        letter-spacing: -0.2px;
    }
    
    /* Metrics */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.2rem;
        margin-bottom: 1.8rem;
    }
    
    .metric-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        border-left: 4px solid var(--primary);
        text-align: left;
    }
    
    .metric-value {
        font-size: 1.65rem;
        font-weight: 700;
        color: var(--dark);
        margin: 0.5rem 0 0.2rem;
        letter-spacing: -0.5px;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: var(--gray);
        text-transform: uppercase;
        letter-spacing: 0.8px;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 6px;
        padding: 0.6rem 1.5rem;
        background: var(--primary);
        border: none;
        transition: background 0.3s;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .stButton>button:hover {
        background: #142a4e;
        box-shadow: 0 2px 8px rgba(26, 60, 110, 0.15);
    }
    
    .stButton>button:focus {
        box-shadow: 0 0 0 2px rgba(26, 60, 110, 0.2);
    }
    
    /* Inputs */
    .stTextInput>div>div>input, 
    .stTextArea>div>textarea,
    .stSelectbox>div>div>div {
        border-radius: 6px;
        border: 1px solid #dde3e9;
        padding: 0.8rem;
        background: #ffffff;
    }
    
    .stTextInput>div>div>input:focus, 
    .stTextArea>div>textarea:focus,
    .stSelectbox>div>div>div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 2px rgba(26, 60, 110, 0.1);
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 8px;
        border: 1px solid #e6eaf0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    /* Charts */
    .stPlotlyChart {
        border-radius: 8px;
        border: 1px solid #e6eaf0;
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }
    
    /* Forms */
    .form-section {
        background: white;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
        border: 1px solid #e6eaf0;
    }
    
    /* Status Colors */
    .success {
        color: var(--success);
    }
    
    .warning {
        color: var(--warning);
    }
    
    .error {
        color: var(--danger);
    }
    
    /* Layout */
    .section {
        margin-bottom: 2.2rem;
    }
    
    .section-title {
        font-size: 1.4rem;
        color: var(--primary);
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        letter-spacing: -0.3px;
    }
    
    /* Expander */
    .stExpander {
        border: 1px solid #e6eaf0;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .stExpander summary {
        padding: 1rem 1.5rem;
        font-weight: 500;
    }
    
    .stExpander div[data-baseweb="collapse"] {
        padding: 0 1.5rem 1.5rem;
    }
    
    /* File Uploader */
    .stFileUploader {
        border: 1px dashed #dde3e9;
        border-radius: 8px;
        padding: 1.5rem;
        background: #f9fbfd;
    }
    
    /* Warning Messages */
    .warning {
        background: #fef6e6;
        border-left: 4px solid var(--warning);
        padding: 1rem;
        border-radius: 0 4px 4px 0;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header aplikasi
    st.markdown('<h1 class="header-title">📊 ProMedia Insight Hub</h1>', unsafe_allow_html=True)
    st.caption("Dashboard Analisis Media Berbasis AI - Eksplorasi, Insight, dan Visualisasi Data Berita")

    # Create main tabs
    tabs = st.tabs([
        "📊 Overview", "📤 Upload Data", "🧠 AI Lab", "💡 Insights", "ℹ️ About"
    ])
    
    # Display tab content with global error handling
    with st_exception_handler():
        tab_overview.show(tabs[0])
        tab_upload.show(tabs[1])
        tab_ai_lab.show(tabs[2])
        tab_insights.show(tabs[3])
        tab_about.show(tabs[4])
