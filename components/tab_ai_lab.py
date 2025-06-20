import streamlit as st
from gemini_engine import gemini_engine
from database import save_ai_history, get_ai_history
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.header("🧠 AI Lab - Analisis Data dengan AI")
        
        # Konfigurasi otomatis menggunakan API key dari secrets
        if gemini_engine.api_key:
            if not gemini_engine.configured:
                with st.spinner("Mengkonfigurasi model AI..."):
                    if gemini_engine.configure():
                        st.success(f"Model {gemini_engine.model_name} siap digunakan!")
                    else:
                        st.error("Gagal mengkonfigurasi model. Periksa log untuk detail.")
        else:
            st.error("Google API Key tidak ditemukan di secrets. Pastikan Anda sudah menyetel GOOGLE_API_KEY di Streamlit secrets.")
            return
        
        # Display AI history
        st.subheader("Riwayat Percakapan")
        history = get_ai_history(limit=10)
        
        if not history:
            st.info("Belum ada riwayat percakapan. Mulailah bertanya di bawah!")
        else:
            for item in history:
                with st.expander(f"{item['created_at']} - {item['prompt'][:30]}..."):
                    st.markdown(f"**Pertanyaan:** {item['prompt']}")
                    st.markdown(f"**Jawaban:** {item['response']}")
        
        # User input
        st.subheader("Ajukan Pertanyaan")
        question = st.text_area("Apa yang ingin Anda analisis dari data?", height=150)
        
        if st.button("Kirim ke AI", use_container_width=True) and question:
            if 'df' not in st.session_state or st.session_state.df is None:
                st.warning("Silakan upload data terlebih dahulu di tab Upload Data")
            else:
                with st.spinner("Menganalisis data..."):
                    # Dapatkan riwayat untuk konteks
                    history_context = [(h['prompt'], h['response']) for h in history]
                    
                    # Ajukan pertanyaan ke Gemini
                    response = gemini_engine.ask(question, st.session_state.df, history_context)
                    
                    # Simpan ke database
                    save_ai_history(question, response)
                    
                    # Perbarui UI
                    st.rerun()
