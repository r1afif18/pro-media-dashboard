import streamlit as st
import pandas as pd
import plotly.express as px
import utils

def show(tab):
    with tab:
        st.markdown("""
        <div class="section">
            <h2 class="section-title">📊 Dashboard Overview</h2>
            <p>Ringkasan analisis data berita secara keseluruhan</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if data is uploaded
        if 'df' not in st.session_state or st.session_state.df is None:
            st.markdown("""
            <div class="card">
                <div class="card-title">Data Required</div>
                <div class="warning">Silakan upload data terlebih dahulu di tab 'Upload Data'</div>
            </div>
            """, unsafe_allow_html=True)
            return
            
        df = st.session_state.df.copy()
        profile = st.session_state.get('data_profile', utils.generate_data_profile(df))
        
        # Metrics cards
        st.markdown("""
        <div class="section">
            <h3 class="section-title">📈 Key Metrics</h3>
            <div class="metric-grid">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(df)}</div>
                <div class="metric-label">Total Berita</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{df['source'].nunique()}</div>
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
            <div class="metric-card">
                <div class="metric-value">{date_range}</div>
                <div class="metric-label">Rentang Tanggal</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if 'sentiment' in df.columns:
                sentiment_counts = df['sentiment'].value_counts()
                dominant_sentiment = sentiment_counts.idxmax()
            else:
                dominant_sentiment = "N/A"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{dominant_sentiment}</div>
                <div class="metric-label">Sentimen Dominan</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)  # Close metric-grid and section
        
        # News trend over time
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
            
        st.markdown("</div></div>", unsafe_allow_html=True)  # Close card and section
        
        # Sentiment distribution
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
                    hole=0.3
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No sentiment data available")
        else:
            st.info("Sentiment column not available")
            
        st.markdown("</div></div>", unsafe_allow_html=True)  # Close card and section
        
        # Top news sources
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
            
        st.markdown("</div></div>", unsafe_allow_html=True)  # Close card and section
