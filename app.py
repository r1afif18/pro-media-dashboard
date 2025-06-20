import streamlit as st
from dotenv import load_dotenv
from auth import login_user, register_user, init_db as init_auth_db
from database import init_db as init_app_db
import logging
import os
import sys
from contextlib import contextmanager

# Impor fungsi show dari masing-masing tab
from components.tab_overview import show as show_overview
from components.tab_upload import show as show_upload
from components.tab_ai_lab import show as show_ai_lab
from components.tab_insights import show as show_insights
from components.tab_about import show as show_about

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
    /* ... (CSS sebelumnya tetap sama) ... */

    /* Perbaikan untuk tampilan About */
    .about-card ul {
        padding-left: 1.5rem;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .about-card li {
        margin-bottom: 0.5rem;
    }
    
    .about-card .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .about-card .feature-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        border: 1px solid #e6eaf0;
    }
    
    .about-card .feature-value {
        font-size: 1.75rem;
        margin-bottom: 0.5rem;
    }
    
    .about-card .feature-label {
        font-size: 0.85rem;
        color: var(--gray);
    }
    
    .about-card .tech-tag {
        background: #e0f2fe;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        display: inline-block;
        margin: 0.15rem;
    }
    
    .about-card .team-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .about-card .team-member {
        background: #f0f9ff;
        padding: 1rem;
        border-radius: 8px;
    }
    
    .about-card .team-member h4 {
        margin:0; 
        color:#1a3c6e;
    }
    
    .about-card .team-member p {
        margin:0; 
        color:#4a6fa5;
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
        show_overview(tabs[0])
        show_upload(tabs[1])
        show_ai_lab(tabs[2])
        show_insights(tabs[3])
        show_about(tabs[4])
