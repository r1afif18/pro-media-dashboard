import streamlit as st
from dotenv import load_dotenv
from auth import login_user, register_user, init_db

from components import (
    tab_overview,
    tab_upload,
    tab_ai_lab,
    tab_forecasting,
    tab_insights,
    tab_about
)

# Load .env jika ada
load_dotenv()

# Inisialisasi session state
for k, v in {
    'df': None,
    'ai_history': [],
    'authenticated': False,
    'user': "",
    'role': "",
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------- Login & Registration UI ----------

def registration_ui():
    st.subheader("Registrasi Pengguna Baru (oleh admin)")
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
            st.experimental_rerun()
        else:
            st.error("Username atau password salah!")

# ---------- MAIN APP ----------

init_db()

if not st.session_state.authenticated:
    st.info("Silakan login terlebih dahulu.")
    login_ui()
    st.stop()
else:
    with st.sidebar:
        st.success(f"Halo, {st.session_state.user}!")
        st.info("Selamat datang di ProMedia Insight Hub!")
        st.caption(f"Role: {st.session_state.role}")
        if st.session_state.role == "admin":
            with st.expander("🛡️ Admin: Registrasi User Baru"):
                registration_ui()
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.user = ""
            st.session_state.role = ""
            st.experimental_rerun()

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

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Overview", "Upload Data", "AI Lab", "Forecasting", "Insights", "About"
    ])
    tab_overview(tab1)
    tab_upload(tab2)
    tab_ai_lab(tab3)
    tab_forecasting(tab4)
    tab_insights(tab5)
    tab_about(tab6)
