import streamlit as st
from gemini_engine import gemini_engine
from database import save_ai_history, get_ai_history, delete_ai_history
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.markdown("""
        <div class="section">
            <h2 class="section-title">🧠 AI Lab - Analisis Data dengan AI</h2>
            <p>Minta insight, analisis, atau tanya seputar data Anda ke AI!</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # ==== Riwayat Percakapan AI ====
        st.subheader("Riwayat Percakapan")
        history = get_ai_history(limit=30)
        
        if not history:
            st.info("Belum ada riwayat percakapan. Mulailah bertanya di bawah!")
        else:
            # Hapus semua riwayat
            if st.button("🗑️ Hapus Semua Riwayat", use_container_width=True, key="del_all_aihist"):
                delete_ai_history(all_history=True)
                st.success("Semua riwayat percakapan berhasil dihapus!")
                st.rerun()
            
            # Tampilkan percakapan
            for item in history:
                with st.container():
                    with st.expander(f"🕒 {item['created_at']} — {item['prompt'][:48]}...", expanded=False):
                        col_hist, col_del = st.columns([8, 1])
                        with col_hist:
                            st.markdown(f"""
                            <div class="card" style="margin-bottom: 0;">
                                <div class="card-title"><b>Pertanyaan:</b></div>
                                <div style="margin-bottom: 1rem;">{item['prompt']}</div>
                                <div class="card-title"><b>Jawaban AI:</b></div>
                                <div>{item['response']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_del:
                            if st.button("❌", key=f"del_{item['id']}"):
                                delete_ai_history(item['id'])
                                st.success("Riwayat dihapus!")
                                st.rerun()
        
        # ==== Form pertanyaan AI ====
        st.subheader("Ajukan Pertanyaan")
        st.markdown("""
        <div class="form-section">
            <p>Isi pertanyaan/analisis yang ingin ditanyakan ke AI terhadap data yang sudah di-upload.</p>
        </div>
        """, unsafe_allow_html=True)
        question = st.text_area("Apa yang ingin Anda analisis dari data?", height=150)
        
        if st.button("Kirim ke AI", use_container_width=True) and question:
            if 'df' not in st.session_state or st.session_state.df is None:
                st.warning("Silakan upload data terlebih dahulu di tab Upload Data")
            else:
                with st.spinner("Menganalisis data..."):
                    history_context = [(h['prompt'], h['response']) for h in history]
                    response = gemini_engine.ask(question, st.session_state.df, history_context)
                    save_ai_history(question, response)
                    st.rerun()
