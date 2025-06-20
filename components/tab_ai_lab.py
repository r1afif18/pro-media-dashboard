import streamlit as st
from gemini_engine import gemini_engine
import time
from database import save_ai_history, get_ai_history
from pandasai.llm.google_generative_ai import GoogleGenerativeAI

def show():
    st.header("🧠 AI Lab")
    
    # Validasi API Key
    if not gemini_engine.api_key:
        st.error(
            "🔐 API Key tidak ditemukan! Silakan buat file `.env` dengan:",
            icon="❌"
        )
        st.code("GOOGLE_API_KEY=your_api_key_here", language="bash")
        st.markdown("Dapatkan API key dari [Google AI Studio](https://aistudio.google.com/)")
        return
        
    if 'df' not in st.session_state or st.session_state.df is None or st.session_state.df.empty:
        st.warning("📁 Silakan upload data di tab 'Upload & Eksplorasi Data' terlebih dahulu", icon="⚠️")
        return
        
    df = st.session_state.df
    
    # Tampilkan info model
    if gemini_engine.model_name:
        st.success(f"Model Gemini aktif: **{gemini_engine.model_name}**")
    else:
        # Coba konfigurasi model jika belum
        if gemini_engine.configure():
            st.success(f"Model Gemini aktif: **{gemini_engine.model_name}**")
        else:
            st.error("Tidak ada model Gemini yang tersedia")
            return
    
    with st.expander("🔍 Struktur Data", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.json({
                "columns": list(df.columns),
                "total_rows": len(df),
                "date_range": [str(df['date'].min().date()), str(df['date'].max().date())]
            })
        with col2:
            st.write("Contoh Data:")
            st.dataframe(df.head(2), use_container_width=True)
    
    # Input pertanyaan
    question = st.text_area(
        "Ajukan pertanyaan tentang data Anda:", 
        placeholder="Contoh: Apa topik yang paling sering muncul di berita dengan sentimen negatif?",
        height=150,
        key="ai_question"
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Analisis dengan Gemini", type="primary", use_container_width=True):
            st.session_state.ask_ai = True
    
    # Tampilkan hasil jika tombol ditekan
    if st.session_state.get('ask_ai', False) and question.strip():
        with st.spinner(f"🔍 Menganalisis dengan Gemini ({gemini_engine.model_name})..."):
            start_time = time.time()
            
            # Panggil Gemini engine
            response = gemini_engine.ask(
                question, 
                df,
                st.session_state.get('ai_history', [])
            )
            
            response_time = time.time() - start_time
            
            if response:
                # Simpan ke history di session_state
                if 'ai_history' not in st.session_state:
                    st.session_state.ai_history = []
                st.session_state.ai_history.append((question, response))
                
                # Simpan ke database
                if 'username' in st.session_state:
                    save_ai_history(
                        st.session_state.username,
                        question,
                        response
                    )
                
                # Tampilkan hasil
                st.subheader("📝 Hasil Analisis")
                st.write(response)
                
                # Tampilkan info performa
                st.caption(f"Waktu respons: {response_time:.2f} detik | Model: {gemini_engine.model_name}")
                
                # Reset flag
                st.session_state.ask_ai = False
            else:
                st.error("Tidak mendapatkan respons dari Gemini")
    
    # Tampilkan history dari database atau session_state
    if st.session_state.get('username'):
        history = get_ai_history(st.session_state.username, limit=10)
        if history:
            st.divider()
            st.subheader("📚 Riwayat Analisis")
            for i, (q, a, timestamp) in enumerate(reversed(history)):
                with st.expander(f"{timestamp}: {q[:50]}..."):
                    st.markdown(f"**Q:** {q}")
                    st.markdown(f"**A:** {a}")
    
    elif st.session_state.get('ai_history'):
        st.divider()
        st.subheader("📚 Riwayat Percakapan (Session)")
        for i, (q, a) in enumerate(reversed(st.session_state.ai_history)):
            with st.expander(f"Pertanyaan #{len(st.session_state.ai_history)-i}: {q[:50]}..."):
                st.markdown(f"**Pertanyaan:** {q}")
                st.divider()
                st.markdown(f"**Jawaban:** {a}")
                
                # Tombol untuk mengulang pertanyaan
                if st.button("Gunakan Kembali", key=f"reuse_{i}", use_container_width=True):
                    st.session_state.ai_question = q
                    st.experimental_rerun()
    
    # Debug section
    if st.button("Debug Model Info", type="secondary"):
        st.write("### Informasi Debugging")
        st.write("API Key:", gemini_engine.api_key[:8] + "..." if gemini_engine.api_key else "None")
        st.write("Model Name:", gemini_engine.model_name)
        
        try:
            # List available models
            import genai
            genai.configure(api_key=gemini_engine.api_key)
            models = genai.list_models()
            gemini_models = [
                (m.name, m.supported_generation_methods) 
                for m in models if 'gemini' in m.name
            ]
            
            st.write("Model Gemini yang Tersedia:")
            for model in gemini_models:
                st.write(f"- {model[0]} (Methods: {', '.join(model[1])})")
        except Exception as e:
            st.error(f"Error fetching models: {str(e)}")
