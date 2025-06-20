import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import logging

logger = logging.getLogger(__name__)

# Define COLUMN_MAPPING as a constant
COLUMN_MAPPING = {
    'tanggal': 'date',
    'judul': 'title',
    'sentimen': 'sentiment',
    'sumber': 'source',
    'isi': 'content',
    'kategori': 'category'
}

def create_metric_card(title, value, icon, color):
    """Create modern metric card with hover effect"""
    return f"""
    <div style="
        background: #ffffff;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid {color};
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    ">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 28px; color: {color};">{icon}</div>
            <div>
                <div style="font-size: 14px; color: #666;">{title}</div>
                <div style="font-size: 24px; font-weight: bold; color: {color};">{value}</div>
            </div>
        </div>
    </div>
    """

def validate_and_clean_data(df):
    """Validate and clean the news data"""
    # Use the defined COLUMN_MAPPING
    column_mapping = COLUMN_MAPPING
    
    # Rename columns
    df.columns = [col.strip().lower() for col in df.columns]
    df.rename(columns=column_mapping, inplace=True)
    
    # Check required columns
    required_columns = ['date', 'title', 'source', 'content']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        raise ValueError(f"Kolom wajib tidak ditemukan: {', '.join(missing_columns)}")
    
    # Clean date
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%Y-%m-%d')
        invalid_dates = df[df['date'].isna()]
        if not invalid_dates.empty:
            logger.warning(f"Ditemukan {len(invalid_dates)} baris dengan tanggal tidak valid")
    
    # Clean sentiment
    if 'sentiment' in df.columns:
        valid_sentiments = ['positif', 'negatif', 'netral']
        df['sentiment'] = df['sentiment'].str.lower()
        invalid_sentiments = ~df['sentiment'].isin(valid_sentiments)
        if invalid_sentiments.any():
            logger.warning(f"Ditemukan {invalid_sentiments.sum()} sentimen tidak valid")
    
    return df

def generate_data_profile(df):
    """Generate comprehensive data profile"""
    profile = {
        'total_news': len(df),
        'sources': {},
        'date_range': None,
        'sentiment_dist': {}
    }
    
    if 'date' in df.columns and not df.empty:
        min_date = df['date'].min()
        max_date = df['date'].max()
        if pd.notnull(min_date) and pd.notnull(max_date):
            profile['date_range'] = {
                'min': min_date.strftime('%Y-%m-%d'),
                'max': max_date.strftime('%Y-%m-%d')
            }
    
    if 'source' in df.columns and not df.empty:
        profile['sources'] = df['source'].value_counts().head(5).to_dict()
    
    if 'sentiment' in df.columns and not df.empty:
        sentiment_counts = df['sentiment'].value_counts(normalize=True)
        profile['sentiment_dist'] = sentiment_counts.to_dict()
    
    return profile

def plot_sentiment_timeseries(df):
    """Plot sentiment over time"""
    if 'date' not in df.columns or 'sentiment' not in df.columns:
        return None
    
    # Resample by week
    df_weekly = df.set_index('date').resample('W')['sentiment'].value_counts().unstack().fillna(0)
    df_weekly = df_weekly.div(df_weekly.sum(axis=1), axis=0)
    
    fig = px.area(
        df_weekly,
        title='Proporsi Sentimen Mingguan',
        labels={'value': 'Proporsi', 'date': 'Tanggal'},
        color_discrete_map={
            'positif': '#2ca02c',
            'netral': '#7f7f7f',
            'negatif': '#d62728'
        }
    )
    fig.update_layout(yaxis_tickformat=".0%")
    return fig

def process_upload(uploaded_file):
    """Proses file CSV yang diupload"""
    try:
        # Deteksi format file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Format file tidak didukung. Gunakan CSV atau Excel."
        
        # Auto rename columns
        df.columns = [col.strip().lower() for col in df.columns]
        # Use the defined COLUMN_MAPPING
        df.rename(columns=lambda x: COLUMN_MAPPING.get(x, x), inplace=True)
        
        # Validasi kolom wajib
        required_columns = ['date', 'title', 'sentiment', 'source', 'content']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return None, f"Kolom wajib tidak ditemukan: {', '.join(missing_columns)}"
        
        # Konversi tanggal
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Validasi sentimen
        valid_sentiments = ['positif', 'negatif', 'netral']
        invalid_sentiments = df[~df['sentiment'].str.lower().isin(valid_sentiments)]
        if not invalid_sentiments.empty:
            st.warning(f"Terdapat {len(invalid_sentiments)} sentimen tidak valid. Hanya gunakan: Positif, Negatif, Netral")
        
        return df, None
        
    except Exception as e:
        return None, f"Error memproses file: {str(e)}"

def generate_template():
    """Generate sample CSV template"""
    data = {
        'date': ['2024-01-01', '2024-01-02'],
        'title': ['Contoh Judul Berita 1', 'Contoh Judul Berita 2'],
        'sentiment': ['Positif', 'Netral'],
        'source': ['Media Satu', 'Media Dua'],
        'content': ['Isi berita pertama...', 'Isi berita kedua...']
    }
    return pd.DataFrame(data)
