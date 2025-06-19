import pandas as pd
import streamlit as st

COLUMN_MAPPING = {
    'tanggal': 'date',
    'judul': 'title',
    'sentimen': 'sentiment',
    'sumber': 'source',
    'isi': 'content',
    'kategori': 'category'
}

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