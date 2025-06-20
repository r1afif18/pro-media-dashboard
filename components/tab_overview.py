import streamlit as st
import pandas as pd
import plotly.express as px

def show(tab):
    with tab:
        st.header("📊 Overview Dashboard")
        
        # Check if data is uploaded
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return
            
        df = st.session_state.df.copy()
        
        # Stats cards
        st.subheader("Statistik Umum")
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown('<div class="metric-card">Total Berita<br><h3>{}</h3></div>'.format(len(df)), unsafe_allow_html=True)
        col2.markdown('<div class="metric-card">Sumber Berita<br><h3>{}</h3></div>'.format(df['source'].nunique()), unsafe_allow_html=True)
        
        # Date range
        if 'date' in df.columns:
            min_date = df['date'].min().strftime('%d %b %Y')
            max_date = df['date'].max().strftime('%d %b %Y')
            col3.markdown('<div class="metric-card">Rentang Tanggal<br><h3>{} - {}</h3></div>'.format(min_date, max_date), unsafe_allow_html=True)
        else:
            col3.markdown('<div class="metric-card">Rentang Tanggal<br><h3>N/A</h3></div>', unsafe_allow_html=True)
        
        # Sentiment distribution
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()
            col4.markdown('<div class="metric-card">Sentimen Dominan<br><h3>{}</h3></div>'.format(sentiment_counts.idxmax()), unsafe_allow_html=True)
        
        # News trend over time
        if 'date' in df.columns:
            st.subheader("Tren Jumlah Berita per Hari")
            df['date_only'] = df['date'].dt.date
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            
            if not daily_counts.empty:
                fig = px.line(daily_counts, x='date_only', y='count', 
                              title='Tren Jumlah Berita Harian',
                              labels={'date_only': 'Tanggal', 'count': 'Jumlah Berita'})
                st.plotly_chart(fig, use_container_width=True)
        
        # Sentiment distribution
        if 'sentiment' in df.columns:
            st.subheader("Distribusi Sentimen")
            sentiment_counts = df['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['sentiment', 'count']
            
            if not sentiment_counts.empty:
                fig2 = px.pie(sentiment_counts, names='sentiment', values='count',
                              title='Proporsi Sentimen Berita', hole=0.3)
                st.plotly_chart(fig2, use_container_width=True)
        
        # Top news sources
        if 'source' in df.columns:
            st.subheader("Top 10 Sumber Berita")
            top_sources = df['source'].value_counts().head(10).reset_index()
            top_sources.columns = ['source', 'count']
            
            if not top_sources.empty:
                fig3 = px.bar(top_sources, x='source', y='count',
                              title='Sumber Berita Terbanyak',
                              labels={'source': 'Sumber Berita', 'count': 'Jumlah Berita'},
                              color='count')
                st.plotly_chart(fig3, use_container_width=True)
        
        # Advanced analysis
        st.divider()
        st.subheader("Analisis Lanjutan")
        
        tab1, tab2, tab3 = st.tabs(["Analisis Sentimen Mendalam", "Topic Modeling", "Jaringan Sumber"])
        
        with tab1:
            st.info("Fitur analisis sentimen mendalam akan segera hadir!")
            # Placeholder for sentiment analysis
            
        with tab2:
            st.info("Fitur topic modeling akan segera hadir!")
            # Placeholder for topic modeling
            
        with tab3:
            st.info("Fitur analisis jaringan sumber akan segera hadir!")
            # Placeholder for source network analysis
