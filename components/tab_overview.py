import streamlit as st
import pandas as pd
import plotly.express as px
import utils

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

        # ==== Key Metrics with Soft Background ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">📈 Key Metrics</h3>
            <div class="metric-grid" style="margin-top:1.3rem;">
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            growth = (df.shape[0] - profile.get('n_news_prev', 0)) / (profile.get('n_news_prev', 1) or 1) * 100
            st.markdown(f"""
            <div class="metric-card" style="background:#f4f6fb;border-left:5px solid #1a3c6e;box-shadow:0 4px 18px 0 #e2e8f0;">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">Total Berita</div>
                <div class="metric-insight" style="color:#43aa8b; font-size:13px;">
                    {'↑' if growth>=0 else '↓'} {abs(growth):.1f}% dibanding periode sebelumnya
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            total_source = df['source'].nunique() if 'source' in df.columns else "N/A"
            st.markdown(f"""
            <div class="metric-card" style="background:#f4f6fb;border-left:5px solid #4a6fa5;box-shadow:0 4px 18px 0 #e2e8f0;">
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
            <div class="metric-card" style="background:#f4f6fb;border-left:5px solid #d4a76a;box-shadow:0 4px 18px 0 #e2e8f0;">
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
            <div class="metric-card" style="background:#f4f6fb;border-left:5px solid {color};box-shadow:0 4px 18px 0 #e2e8f0;">
                <div class="metric-value">{dominant_sentiment}</div>
                <div class="metric-label">Sentimen Dominan</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== Hari Teraktif Card ====
        st.markdown("""
        <div class="section" style="margin-top:2rem;">
            <div class="card" style="background:#f3f7fa;border-left:5px solid #43aa8b;">
                <b>🔥 Hari Teraktif:</b>
        """, unsafe_allow_html=True)
        if 'date' in df.columns:
            busiest_day = df['date'].dt.date.value_counts().idxmax()
            count_busiest = df['date'].dt.date.value_counts().max()
            st.markdown(f"""<span style="font-size:1.1rem;">{busiest_day} — {count_busiest} berita</span>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== News Trend Card ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">📈 News Trend</h3>
            <div class="card" style="background:#f5f7fa;">
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
                    labels={'date_only': 'Date', 'count': 'News Count'},
                    template='simple_white'
                )
                fig.update_traces(mode='lines+markers')
                fig.update_layout(
                    plot_bgcolor='#f4f6fb',
                    paper_bgcolor='#f4f6fb',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for trend analysis")
        else:
            st.info("Date column not available for trend analysis")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== Sentiment Pie Card ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">😊 Sentiment Analysis</h3>
            <div class="card" style="background:#f5f7fa;">
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
                    color_discrete_sequence=["#dae6f6", "#c9d8ee", "#b1cbe3"]
                )
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No sentiment data available")
        else:
            st.info("Sentiment column not available")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== Top Sources Card ====
        st.markdown("""
        <div class="section">
            <h3 class="section-title">📰 News Sources</h3>
            <div class="card" style="background:#f5f7fa;">
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
                    color='count',
                    color_continuous_scale=["#34618c", "#a3c9e2"]
                )
                fig3.update_layout(
                    plot_bgcolor='#f5f7fa',
                    paper_bgcolor='#f5f7fa'
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No source data available")
        else:
            st.info("Source column not available")
        st.markdown("</div></div>", unsafe_allow_html=True)
