from dotenv import load_dotenv
from components.db import init_app_db
from components.tab_about import show as tab_about
from components.tab_overview import tab_overview
from components.tab_upload import tab_upload
from components.tab_ai_lab import tab_ai_lab
from components.tab_forecasting import tab_forecasting
from components.tab_insights import tab_insights

load_dotenv()
init_app_db()

st.set_page_config(
    page_title="ProMedia Insight Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'df' not in st.session_state:
    st.session_state.df = None
if 'ai_history' not in st.session_state:
    st.session_state.ai_history = []

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

with st.sidebar:
    st.info("Selamat datang di ProMedia Insight Hub! Semua fitur dapat diakses tanpa login.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Upload Data", "AI Lab", "Forecasting", "Insights", "About"
])
tab_overview(tab1)
tab_upload(tab2)
tab_ai_lab(tab3)
tab_forecasting(tab4)
tab_insights(tab5)
tab_about(tab6)
