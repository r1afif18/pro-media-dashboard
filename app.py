import logging
import os
import sys
from contextlib import contextmanager
import streamlit as st
from dotenv import load_dotenv

# Setup logging harus setelah impor logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Impor modul aplikasi SETELAH setup logging
from auth import login_user, register_user, init_db as init_auth_db
from database import init_db as init_app_db
from components.tab_about import show as show_about
from components.tab_ai_lab import show as show_ai_lab
from components.tab_forecasting import show as show_forecasting
from components.tab_insights import show as show_insights
from components.tab_overview import show as show_overview
from components.tab_upload import show as show_upload

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
        
        if st.button("Logout"):
            for key in list(st.session_state.keys()):
                if key not in DEFAULT_STATE:
                    del st.session_state[key]
            st.session_state.update(DEFAULT_STATE)
            st.rerun()

    # Enhanced CSS
    st.markdown("""
    <style>
    .header-title {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #2563EB 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 0.5rem 0;
        margin-bottom: 2rem;
        font-weight: 800;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 4px solid #2563EB;
        transition: transform 0.3s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 8px 8px 0 0;
        transition: all 0.3s;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2563EB20;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #4f46e5, #7c3aed);
    }
    </style>
    """, unsafe_allow_html=True)

    # Header aplikasi
    st.markdown('<h1 class="header-title">📊 ProMedia Insight Hub</h1>', unsafe_allow_html=True)
    st.caption("Dashboard Analisis Media Berbasis AI - Eksplorasi, Insight, dan Visualisasi Data Berita")

    # Create main tabs
    tabs = st.tabs([
        "📊 Overview", "📤 Upload Data", "🧠 AI Lab", "🔮 Forecasting", 
        "💡 Insights", "ℹ️ About"
    ])
    
    # Display tab content with global error handling
    with st_exception_handler():
        show_overview(tabs[0])
        show_upload(tabs[1])
        show_ai_lab(tabs[2])
        show_forecasting(tabs[3])
        show_insights(tabs[4])
        show_about(tabs[5])
