import streamlit as st
import pandas as pd
import plotly.express as px
import utils
from datetime import datetime

def show(tab):
    with tab:
        st.header("📊 Overview Dashboard")
        
        # Check data
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return
            
        df = st.session_state.df.copy()
        profile = st.session_state.get('data_profile', utils.generate_data_profile(df))
        
        # Metric cards
        st.subheader("Statistik Utama")
        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(utils.create_metric_card("Total Berita", profile['total_news'], "📰", "#4C78A8"), 
                     unsafe_allow_html=True)
        col2.markdown(utils.create_metric_card("Sumber Berita", len(profile['sources']), "📡", "#E45756"), 
                     unsafe_allow_html=True)
        
        if profile['date_range']:
            date_range = f"{profile['date_range']['min']} - {profile['date_range']['max']}"
            col3.markdown(utils.create_metric_card("Rentang Tanggal", date_range, "📅", "#54A24B"), 
                         unsafe_allow_html=True)
        
        if profile['sentiment_dist']:
            dominant_sentiment = max(profile['sentiment_dist'], key=profile['sentiment_dist'].get)
            col4.markdown(utils.create_metric_card("Sentimen Dominan", dominant_sentiment.capitalize(), "😊", "#F58518"), 
                         unsafe_allow_html=True)
        
        # News trend
        st.subheader("Tren Jumlah Berita")
        if 'date' in df.columns:
            df['date_only'] = df['date'].dt.date
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            
            fig = px.line(
                daily_counts, 
                x='date_only', 
                y='count',
                title='Jumlah Berita per Hari',
                labels={'date_only': 'Tanggal', 'count': 'Jumlah Berita'}
            )
            fig.update_traces(line=dict(width=2.5))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Data tidak memiliki kolom tanggal untuk analisis tren")
        
        # Sentiment distribution
        st.subheader("Distribusi Sentimen")
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['sentiment', 'count']
            
            fig2 = px.pie(
                sentiment_counts, 
                names='sentiment', 
                values='count',
                title='Proporsi Sentimen',
                hole=0.35,
                color='sentiment',
                color_discrete_map={
                    'positif': '#2ca02c',
                    'netral': '#7f7f7f',
                    'negatif': '#d62728'
                }
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Data tidak memiliki kolom sentimen")
        
        # Advanced analysis
        st.divider()
        st.subheader("Analisis Lanjutan")
        
        tab1, tab2, tab3 = st.tabs(["Trend Sentimen", "Topik Populer", "Jaringan Media"])
        
        with tab1:
            if 'date' in df.columns and 'sentiment' in df.columns:
                fig = utils.plot_sentiment_timeseries(df)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Tidak cukup data untuk analisis trend sentimen")
            else:
                st.info("Data tidak memiliki kolom tanggal atau sentimen")
        
        with tab2:
            st.info("Fitur analisis topik akan segera hadir!")
            # Placeholder for topic modeling
        
        with tab3:
            st.info("Fitur analisis jaringan media akan segera hadir!")
            # Placeholder for media network
