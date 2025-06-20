import streamlit as st

def show(tab):
    with tab:
        st.header("ℹ️ Tentang ProMedia Insight Hub")
        
        st.markdown("""
        ## Dashboard Analisis Media Berbasis AI
        
        **ProMedia Insight Hub** adalah platform analitik media yang dirancang untuk membantu Anda:
        - Menganalisis performa konten media
        - Memahami sentimen publik
        - Mengidentifikasi tren berita
        - Membuat prediksi masa depan
        - Menghasilkan insight berbasis AI
        
        ### Fitur Utama
        """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info("📊 **Overview Dashboard**")
            st.caption("Statistik umum dan visualisasi data utama")
            
        with col2:
            st.info("📤 **Upload & Eksplorasi Data**")
            st.caption("Unggah dan eksplorasi dataset berita Anda")
            
        with col3:
            st.info("🧠 **AI Lab**")
            st.caption("Analisis data dengan kecerdasan buatan")
        
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.info("🔮 **Forecasting**")
            st.caption("Prediksi tren berita masa depan")
            
        with col5:
            st.info("💡 **Insights Custom**")
            st.caption("Simpan dan kelola insight analisis Anda")
            
        with col6:
            st.info("👥 **Multi-user**")
            st.caption("Dukungan untuk banyak pengguna dengan peran berbeda")
        
        st.divider()
        st.markdown("""
        ### Teknologi
        
        Aplikasi ini dibangun dengan:
        - Python
        - Streamlit
        - Google Gemini AI
        - SQLite
        - Plotly
        - Scikit-learn
        - Statsmodels
        
        ### Tim Pengembang
        
        - [Nama Pengembang 1]
        - [Nama Pengembang 2]
        - [Nama Pengembang 3]
        
        © 2024 ProMedia Insight Hub. Hak Cipta Dilindungi.
        """)
