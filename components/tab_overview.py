import streamlit as st
import pandas as pd
import plotly.express as px

def tab_overview(tab):
    with tab:
        st.header("📊 Overview")
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Silakan upload data terlebih dahulu di tab 'Upload & Eksplorasi Data'")
            return

        df = st.session_state.df.copy()
        st.subheader("Statistik Umum")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Berita", len(df))
        col2.metric("Sumber Berita", df['source'].nunique())
        col3.metric("Rentang Tanggal",
            f"{df['date'].min().strftime('%d %b %Y')} - {df['date'].max().strftime('%d %b %Y')}")

        st.subheader("Tren Jumlah Berita per Hari")
        df['date_only'] = pd.to_datetime(df['date']).dt.date
        daily_counts = df.groupby('date_only').size().reset_index(name='count')
        fig = px.line(daily_counts, x='date_only', y='count', title='Tren Jumlah Berita Harian')
        st.plotly_chart(fig, use_container_width=True)
