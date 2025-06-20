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

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize databases
init_auth_db()  # Initialize authentication database
init_app_db()   # Initialize application database

# Initialize session state
session_vars = {
    'df': None,
    'ai_history': [],
    'authenticated': False,
    'user': "",
    'role': "",
    'custom_insights': [],
    'google_api_key': os.getenv("GOOGLE_API_KEY", "")
}

for k, v in session_vars.items():
    if k not in st.session_state:
        st.session_state[k] = v

def registration_ui():
    """UI for user registration (admin only)"""
    with st.expander("🛡️ Admin: Registrasi User Baru", expanded=True):
        new_username = st.text_input("Username Baru", key="reg_username")
        new_password = st.text_input("Password Baru", type="password", key="reg_password")
        confirm_password = st.text_input("Konfirmasi Password", type="password", key="reg_confirm")
        user_role = st.selectbox("Peran", ["user", "admin"], index=0, key="reg_role")
        
        if st.button("Daftarkan Pengguna"):
            if not new_username or not new_password:
                st.error("Username dan password harus diisi")
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
        success, role = login_user(username, password)
        if success:
            st.session_state.authenticated = True
            st.session_state.user = username
            st.session_state.role = role
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Username atau password salah!")

# Show login UI if not authenticated
if not st.session_state.authenticated:
    st.info("Silakan login terlebih dahulu.")
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
            st.session_state.authenticated = False
            st.session_state.user = ""
            st.session_state.role = ""
            st.rerun()

    # Custom CSS
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
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    @media (max-width: 768px) {
        .stDataFrame { width: 100% !important; }
        .stButton>button { width: 100%; }
        .header-title { font-size: 2rem; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Header aplikasi
    st.markdown('<h1 class="header-title">📊 ProMedia Insight Hub</h1>', unsafe_allow_html=True)
    st.caption("Dashboard Analisis Media Berbasis AI - Eksplorasi, Insight, dan Visualisasi Data Berita")

    # Create main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", "📤 Upload Data", "🧠 AI Lab", "🔮 Forecasting", "💡 Insights", "ℹ️ About"
    ])
    
    # Display tab content
    try:
        tab_overview.show(tab1)
        tab_upload.show(tab2)
        tab_ai_lab.show(tab3)
        tab_forecasting.show(tab4)
        tab_insights.show(tab5)
        tab_about.show(tab6)
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
        logger.error(f"Error in tab navigation: {str(e)}")
