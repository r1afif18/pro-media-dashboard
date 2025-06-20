import streamlit as st
import pandas as pd
import plotly.express as px

def show(tab):  # Ganti nama fungsi dari tab_overview menjadi show
    with tab:
        st.header("📊 Overview")
        
        # Cek jika data sudah diupload
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Silakan upload data terlebih dahulu di tab 'Upload & Eksplorasi Data'")
            return
            
        df = st.session_state.df.copy()
        
        # Statistik umum
        st.subheader("Statistik Umum")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Berita", len(df))
        col2.metric("Sumber Berita", df['source'].nunique())
        
        # Pastikan kolom 'date' ada dan dalam format datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            min_date = df['date'].min()
            max_date = df['date'].max()
            
            if pd.notna(min_date) and pd.notna(max_date):
                col3.metric("Rentang Tanggal",
                            f"{min_date.strftime('%d %b %Y')} - {max_date.strftime('%d %b %Y')}")
            else:
                col3.metric("Rentang Tanggal", "Data tidak valid")
        else:
            col3.metric("Rentang Tanggal", "Kolom tidak ditemukan")
        
        # Tren jumlah berita per hari
        if 'date' in df.columns:
            st.subheader("Tren Jumlah Berita per Hari")
            df['date_only'] = df['date'].dt.date
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            
            if not daily_counts.empty:
                fig = px.line(daily_counts, x='date_only', y='count', 
                              title='Tren Jumlah Berita Harian',
                              labels={'date_only': 'Tanggal', 'count': 'Jumlah Berita'})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Tidak ada data untuk ditampilkan")
        
        # Distribusi sentimen
        if 'sentiment' in df.columns:
            st.subheader("Distribusi Sentimen")
            sentiment_counts = df['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['sentiment', 'count']
            
            if not sentiment_counts.empty:
                fig2 = px.pie(sentiment_counts, names='sentiment', values='count',
                              title='Proporsi Sentimen Berita', hole=0.3)
                st.plotly_chart(fig2, use_container_width=True)
        
        # Top sumber berita
        if 'source' in df.columns:
            st.subheader("Top 10 Sumber Berita")
            top_sources = df['source'].value_counts().head(10).reset_index()
            top_sources.columns = ['source', 'count']
            
            if not top_sources.empty:
                fig3 = px.bar(top_sources, x='source', y='count',
                              title='Sumber Berita Terbanyak',
                              labels={'source': 'Sumber Berita', 'count': 'Jumlah Berita'})
                st.plotly_chart(fig3, use_container_width=True)
        
        st.divider()
        st.subheader("Analisis Lanjutan")
        
        # Buat tab untuk analisis lanjutan
        tab1, tab2, tab3 = st.tabs([
            "Analisis Sentimen Mendalam",
            "Topic Modeling",
            "Jaringan Sumber"
        ])
        
        with tab1:
            st.write("Analisis sentimen lebih detail berdasarkan konten berita")
            # Implementasi analisis sentimen mendalam di sini
            
        with tab2:
            st.write("Identifikasi topik utama dalam berita")
            # Implementasi topic modeling di sini
            
        with tab3:
            st.write("Analisis hubungan antar sumber berita")
            # Implementasi analisis jaringan di sini
