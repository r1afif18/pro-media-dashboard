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

        # ==== KEY METRICS ====
        st.markdown("""
        <div class="section" style="margin-bottom: 1.5rem;">
            <h3 class="section-title">📈 Key Metrics</h3>
        </div>
        """, unsafe_allow_html=True)

        growth = (df.shape[0] - profile.get('n_news_prev', 0)) / (profile.get('n_news_prev', 1) or 1) * 100
        total_source = df['source'].nunique() if 'source' in df.columns else "N/A"
        if 'date' in df.columns:
            min_date = df['date'].min().strftime('%d %b %Y')
            max_date = df['date'].max().strftime('%d %b %Y')
            date_range = f"{min_date} - {max_date}"
        else:
            date_range = "N/A"
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()
            dominant_sentiment = sentiment_counts.idxmax()
            color = "#1a3c6e" if dominant_sentiment == "Positif" else "#e74c3c"
        else:
            dominant_sentiment = "N/A"
            color = "#e74c3c"

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div style="
                background: #eef2fa;
                border-left:5px solid #1a3c6e;
                box-shadow:0 6px 20px 0 #d1dbec3d;
                border-radius: 16px;
                width:100%;
                padding: 1.3rem 1.1rem 1.1rem 1.2rem;
                margin-bottom: 0.7rem;">
                <div style="font-size:2.15rem;font-weight:700;">{len(df)}</div>
                <div style="font-size:1.02rem;">Total Berita</div>
                <div style="color:#43aa8b; font-size:13px; margin-top:5px;">
                    {'↑' if growth>=0 else '↓'} {abs(growth):.1f}% dibanding periode sebelumnya
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="
                background: #eef2fa;
                border-left:5px solid #4a6fa5;
                box-shadow:0 6px 20px 0 #d1dbec3d;
                border-radius: 16px;
                width:100%;
                padding: 1.3rem 1.1rem 1.1rem 1.2rem;
                margin-bottom: 0.7rem;">
                <div style="font-size:2.15rem;font-weight:700;">{total_source}</div>
                <div style="font-size:1.02rem;">Sumber Berita</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="
                background: #eef2fa;
                border-left:5px solid #d4a76a;
                box-shadow:0 6px 20px 0 #d1dbec3d;
                border-radius: 16px;
                width:100%;
                padding: 1.3rem 1.1rem 1.1rem 1.2rem;
                margin-bottom: 0.7rem;">
                <div style="font-size:1.11rem;font-weight:600;">{date_range}</div>
                <div style="font-size:1.02rem;">Rentang Tanggal</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div style="
                background: #eef2fa;
                border-left:5px solid {color};
                box-shadow:0 6px 20px 0 #d1dbec3d;
                border-radius: 16px;
                width:100%;
                padding: 1.3rem 1.1rem 1.1rem 1.2rem;
                margin-bottom: 0.7rem;">
                <div style="font-size:2rem;font-weight:600;">{dominant_sentiment}</div>
                <div style="font-size:1.02rem;">Sentimen Dominan</div>
            </div>
            """, unsafe_allow_html=True)

        # ==== HARI TERAKTIF CARD ====
        st.markdown("""
        <div class="section" style="margin-top:2rem;">
            <div class="card" style="background:#f3f7fa;border-left:5px solid #43aa8b;box-shadow:0 3px 14px 0 #d1dbec24;">
                <b>🔥 Hari Teraktif:</b>
        """, unsafe_allow_html=True)
        if 'date' in df.columns:
            busiest_day = df['date'].dt.date.value_counts().idxmax()
            count_busiest = df['date'].dt.date.value_counts().max()
            st.markdown(f"""<span style="font-size:1.13rem;">{busiest_day} — {count_busiest} berita</span>""", unsafe_allow_html=True)
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== NEWS TREND ====
        st.markdown("""
        <div class="section" style="margin-top: 1.3rem;">
            <h3 class="section-title">📈 News Trend</h3>
            <div class="card" style="background:#f5f7fa;box-shadow:0 3px 14px 0 #d1dbec24;">
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
                    plot_bgcolor='#f5f7fa',
                    paper_bgcolor='#f5f7fa',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#f0f0f0')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for trend analysis")
        else:
            st.info("Date column not available for trend analysis")
        st.markdown("</div></div>", unsafe_allow_html=True)

        # ==== SENTIMENT PIE CARD ====
        st.markdown("""
        <div class="section" style="margin-top: 1.3rem;">
            <h3 class="section-title">😊 Sentiment Analysis</h3>
            <div class="card" style="background:#f5f7fa;box-shadow:0 3px 14px 0 #d1dbec24;">
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

        # ==== TOP SOURCES CARD ====
        st.markdown("""
        <div class="section" style="margin-top: 1.3rem;">
            <h3 class="section-title">📰 News Sources</h3>
            <div class="card" style="background:#f5f7fa;box-shadow:0 3px 14px 0 #d1dbec24;">
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
