import streamlit as st
from gemini_engine import gemini_engine
from database import save_ai_history, get_ai_history

def show(tab):
    with tab:
        st.header("🧠 AI Lab - Analisis Data dengan AI")
        
        # API key configuration
        if not st.session_state.get('google_api_key'):
            st.warning("Masukkan Google API Key untuk menggunakan fitur AI")
        
        api_key = st.text_input("Google API Key", 
                               value=st.session_state.get('google_api_key', ''),
                               type="password",
                               help="Dapatkan API Key dari Google AI Studio")
        
        if api_key:
            st.session_state.google_api_key = api_key
            gemini_engine.api_key = api_key
            
            if st.button("Konfigurasi Model AI"):
                if gemini_engine.configure():
                    st.success(f"Model {gemini_engine.model_name} siap digunakan!")
                else:
                    st.error("Gagal mengkonfigurasi model. Periksa API key Anda.")
        
        # Display AI history
        st.subheader("Riwayat Percakapan")
        history = get_ai_history(limit=10)
        
        if not history:
            st.info("Belum ada riwayat percakapan. Mulailah bertanya di bawah!")
        else:
            for item in reversed(history):
                with st.expander(f"{item['created_at']} - {item['prompt'][:30]}..."):
                    st.markdown(f"**Pertanyaan:** {item['prompt']}")
                    st.markdown(f"**Jawaban:** {item['response']}")
        
        # User input
        st.subheader("Ajukan Pertanyaan")
        question = st.text_area("Apa yang ingin Anda analisis dari data?")
        
        if st.button("Kirim ke AI") and question:
            if not gemini_engine.model:
                st.warning("Silakan konfigurasi model AI terlebih dahulu")
            elif 'df' not in st.session_state or st.session_state.df is None:
                st.warning("Silakan upload data terlebih dahulu di tab Upload Data")
            else:
                with st.spinner("Menganalisis data..."):
                    response = gemini_engine.ask(question, st.session_state.df)
                    save_ai_history(question, response)
                    st.rerun()
