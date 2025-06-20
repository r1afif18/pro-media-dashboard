import streamlit as st
from gemini_engine import gemini_engine
from database import save_ai_history, get_ai_history
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.markdown("""
        <div class="section">
            <h2 class="section-title">🧠 AI Analytics Lab</h2>
            <p>Analisis data berita dengan kecerdasan buatan tingkat lanjut</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Status model
        if not gemini_engine.configured:
            with st.spinner("Mengkonfigurasi model AI..."):
                if gemini_engine.configure():
                    st.success(f"✅ Model {gemini_engine.model_name} siap digunakan!")
                else:
                    st.error("❌ Gagal mengkonfigurasi model. Periksa API key di secrets.")
                    return
        
        # Data status panel
        if 'df' in st.session_state and st.session_state.df is not None:
            profile = st.session_state.get('data_profile', utils.generate_data_profile(st.session_state.df))
            
            st.markdown("""
            <div class="card">
                <div class="card-title">📊 Current Dataset</div>
                <div class="metric-grid">
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{profile['total_news']}</div>
                    <div class="metric-label">Total Berita</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(profile['sources'])}</div>
                    <div class="metric-label">Sumber Berita</div>
                </div>
                """, unsafe_allow_html=True)
                
            with col3:
                if profile['date_range']:
                    date_range = f"{profile['date_range']['min']} - {profile['date_range']['max']}"
                else:
                    date_range = "N/A"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{date_range}</div>
                    <div class="metric-label">Rentang Tanggal</div>
                </div>
                """, unsafe_allow_html=True)
                
            st.markdown("</div></div>", unsafe_allow_html=True)  # Close metric-grid and card
        else:
            st.markdown("""
            <div class="card">
                <div class="warning">📤 Silakan upload data terlebih dahulu di tab Upload Data</div>
            </div>
            """, unsafe_allow_html=True)
            return
        
        # Riwayat analisis
        st.markdown("""
        <div class="card">
            <div class="card-title">📜 Analysis History</div>
        """, unsafe_allow_html=True)
        
        history = get_ai_history(limit=5)
        
        if not history:
            st.info("Belum ada riwayat analisis. Mulailah dengan mengajukan pertanyaan!")
        else:
            for item in history:
                with st.expander(f"{item['created_at']} - {item['prompt'][:50]}..."):
                    st.markdown(f"**Pertanyaan:** {item['prompt']}")
                    st.markdown(f"**Jawaban:** {item['response']}")
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close card
        
        # Input analisis
        st.markdown("""
        <div class="card">
            <div class="card-title">🔍 New Analysis</div>
        """, unsafe_allow_html=True)
        
        question = st.text_area(
            "Apa yang ingin Anda analisis dari data?",
            height=150,
            placeholder="Contoh: Berikan analisis tren topik berita selama 30 hari terakhir"
        )
        
        if st.button("Kirim ke AI", use_container_width=True, disabled=not question):
            if 'df' not in st.session_state or st.session_state.df is None:
                st.warning("Silakan upload data terlebih dahulu di tab Upload Data")
            else:
                with st.spinner("Menganalisis data..."):
                    try:
                        # Ajukan pertanyaan ke Gemini
                        response = gemini_engine.ask(question, st.session_state.df)
                        
                        # Simpan ke database
                        save_ai_history(question, response)
                        
                        # Tampilkan hasil
                        st.markdown("""
                        <div class="card">
                            <div class="card-title">💡 Analysis Result</div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(response)
                        st.markdown("</div>", unsafe_allow_html=True)  # Close card
                        
                    except Exception as e:
                        st.error(f"❌ Error selama analisis: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close card
