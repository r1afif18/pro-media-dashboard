import streamlit as st
import pandas as pd
import plotly.express as px
import utils
from gemini_engine import gemini_engine

def show(tab):
    with tab:
        st.markdown("""
        <div class="section">
            <h2 class="section-title">📊 Dashboard Overview</h2>
            <p>Ringkasan cerdas dan interaktif data berita terbaru</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ==== Data Cek ====
        if 'df' not in st.session_state or st.session_state.df is None:
            st.markdown("""
            <div class="card">
                <div class="card-title">🚩 Data Required</div>
                <div class="warning">Silakan upload data terlebih dahulu di tab 'Upload Data'</div>
            </div>
            """, unsafe_allow_html=True)
            return
            
        df = st.session_state.df.copy()
        profile = st.session_state.get('data_profile', utils.generate_data_profile(df))

        # ==== Filter Section ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">🔎 Quick Filter</h3>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Filter Data", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("Dari Tanggal", df['date'].min().date() if 'date' in df else None)
            with col2:
                end_date = st.date_input("Sampai Tanggal", df['date'].max().date() if 'date' in df else None)
            if 'source' in df.columns:
                sources = st.multiselect("Filter Sumber", options=df['source'].unique())
                if sources:
                    df = df[df['source'].isin(sources)]
            # Apply date filter
            if 'date' in df.columns:
                df = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
        
        # ==== SMART METRIC CARDS ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">📈 Key Metrics</h3>
            <div class="metric-grid">
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            growth = (df.shape[0] - profile.get('n_news_prev', 0)) / (profile.get('n_news_prev', 1) or 1) * 100
            st.markdown(f"""
            <div class="metric-card" style="border-left:5px solid #1a3c6e;">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">Total Berita</div>
                <div class="metric-insight" style="color:#5eba7d; font-size:13px;">
                    {'↑' if growth>=0 else '↓'} {abs(growth):.1f}% dibanding periode sebelumnya
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            total_source = df['source'].nunique() if 'source' in df.columns else "N/A"
            st.markdown(f"""
            <div class="metric-card" style="border-left:5px solid #4a6fa5;">
                <div class="metric-value">{total_source}</div>
                <div class="metric-label">Sumber Berita</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            if 'date' in df.columns:
                min_date = df['date'].min().strftime('%d %b %Y')
                max_date = df['date'].max().strftime('%d %b %Y')
                date_range = f"{min_date} - {max_date}"
            else:
                date_range = "N/A"
            st.markdown(f"""
            <div class="metric-card" style="border-left:5px solid #d4a76a;">
                <div class="metric-value">{date_range}</div>
                <div class="metric-label">Rentang Tanggal</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            if 'sentiment' in df.columns:
                sentiment_counts = df['sentiment'].value_counts()
                dominant_sentiment = sentiment_counts.idxmax()
                color = "#1a3c6e" if dominant_sentiment == "Positif" else "#e74c3c"
            else:
                dominant_sentiment = "N/A"
                color = "#888"
            st.markdown(f"""
            <div class="metric-card" style="border-left:5px solid {color};">
                <div class="metric-value">{dominant_sentiment}</div>
                <div class="metric-label">Sentimen Dominan</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== MINI INSIGHT SECTION ====
        st.markdown("""
        <div class="section" style="margin-top:2rem;">
            <div class="card" style="background:#f0f7fa;">
                <b>🔥 Hari Teraktif:</b>
        """, unsafe_allow_html=True)
        if 'date' in df.columns:
            busiest_day = df['date'].dt.date.value_counts().idxmax()
            count_busiest = df['date'].dt.date.value_counts().max()
            st.markdown(f"""<span style="font-size:1.1rem;">{busiest_day} — {count_busiest} berita</span>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # ==== NEWS TREND ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">📈 News Trend</h3>
            <div class="card">
                <div class="card-title">Trend Analysis</div>
        """, unsafe_allow_html=True)
        if 'date' in df.columns:
            df['date_only'] = df['date'].dt.date
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            if not daily_counts.empty:
                fig = px.line(
                    daily_counts, 
                    x='date_only', 
                    y='count',
                    title='',
                    labels={'date_only': 'Date', 'count': 'News Count'}
                )
                fig.update_traces(mode='lines+markers')
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for trend analysis")
        else:
            st.info("Date column not available for trend analysis")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== SENTIMENT PIE ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">😊 Sentiment Analysis</h3>
            <div class="card">
                <div class="card-title">Sentiment Distribution</div>
        """, unsafe_allow_html=True)
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts().reset_index()
            sentiment_counts.columns = ['sentiment', 'count']
            if not sentiment_counts.empty:
                fig2 = px.pie(
                    sentiment_counts, 
                    names='sentiment', 
                    values='count',
                    title='',
                    hole=0.35,
                    color_discrete_sequence=px.colors.sequential.Blues
                )
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No sentiment data available")
        else:
            st.info("Sentiment column not available")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== TOP SOURCES WITH CHIPS ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">📰 News Sources</h3>
            <div class="card">
                <div class="card-title">Top News Sources</div>
        """, unsafe_allow_html=True)
        if 'source' in df.columns:
            top_sources = df['source'].value_counts().head(10).reset_index()
            top_sources.columns = ['source', 'count']
            if not top_sources.empty:
                st.markdown("<div style='display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px;'>", unsafe_allow_html=True)
                for _, row in top_sources.iterrows():
                    st.markdown(
                        f"""<span style='background:#e8f1fb;padding:7px 15px;border-radius:20px;font-size:0.97rem;color:#1a3c6e;border:1px solid #b2c5df'>{row["source"]} <b>{row["count"]}</b></span>""",
                        unsafe_allow_html=True
                    )
                st.markdown("</div>", unsafe_allow_html=True)
                fig3 = px.bar(
                    top_sources, 
                    x='source', 
                    y='count',
                    title='',
                    labels={'source': 'Source', 'count': 'Count'},
                    color='count'
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No source data available")
        else:
            st.info("Source column not available")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== AI INSIGHT ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">🤖 AI Insight</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔍 Dapatkan Insight AI", use_container_width=True):
            with st.spinner("Meminta insight AI..."):
                try:
                    prompt = "Buatkan insight utama dan pola menarik dari data tren dan distribusi berita berikut. Singkat, 3-5 poin, bahasa Indonesia, fokus pada insight actionable."
                    ai_insight = gemini_engine.ask(prompt, df)
                    st.markdown(f"""
                    <div class="card" style="background:#e9f4ee;">
                        <div class="card-title">Hasil Insight AI</div>
                        <div style="font-size:1.1rem;">{ai_insight}</div>
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"AI insight gagal: {e}")
