import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from gemini_engine import gemini_engine
import logging
import io
import re

logger = logging.getLogger(__name__)

def extract_markdown_table(text):
    # Ambil bagian tabel markdown dari respons AI
    match = re.search(r'(\|.*\|\n\|[-\s|]+\|\n[\s\S]+?)(\n\n|$)', text)
    if match:
        return match.group(1)
    else:
        # Jika tidak ada tabel, hapus blok kode python atau blok triple-backtick
        text_no_code = re.sub(r'```[\s\S]+?```', '', text)
        return text_no_code.strip()

def show(tab):
    with tab:
        st.header("🔮 AI Forecasting & Strategi - Analisis Tren Berita")
        st.info("Forecasting menggunakan Google Gemini AI untuk memproyeksikan tren masa depan dari data historis. Data minimum: 10 baris.")

        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("📤 Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return

        df = st.session_state.df.copy()

        st.subheader("1. Pilih Data untuk Analisis")
        col1, col2 = st.columns(2)

        with col1:
            date_cols = [col for col in df.columns if 'date' in col.lower()]
            if not date_cols:
                st.error("❌ Tidak ditemukan kolom tanggal di dataset")
                return
            date_column = st.selectbox("Kolom Tanggal", date_cols)

            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            if not numeric_cols:
                st.error("❌ Tidak ditemukan kolom numerik di dataset")
                return
            metric_column = st.selectbox("Kolom Metrik", numeric_cols)

        with col2:
            category_cols = [''] + [col for col in df.columns if col != date_column and col != metric_column]
            category_column = st.selectbox("Kelompokkan Berdasarkan (opsional)", category_cols)
            time_window = st.selectbox("Rentang Waktu", ["Harian", "Mingguan", "Bulanan"])
            forecast_periods = st.slider("Jumlah Periode ke Depan", 1, 14, 7)

        try:
            df_clean = df.copy()
            df_clean[date_column] = pd.to_datetime(df_clean[date_column], errors='coerce')
            df_clean = df_clean.dropna(subset=[date_column])

            if time_window == "Harian":
                df_clean['period'] = df_clean[date_column].dt.normalize()
                freq = 'D'
            elif time_window == "Mingguan":
                df_clean['period'] = df_clean[date_column].dt.to_period('W').dt.start_time
                freq = 'W'
            else:
                df_clean['period'] = df_clean[date_column].dt.to_period('M').dt.start_time
                freq = 'M'

            group_cols = ['period']
            if category_column:
                group_cols.append(category_column)
            df_agg = df_clean.groupby(group_cols)[metric_column].sum().reset_index()
            df_agg = df_agg.sort_values('period').reset_index(drop=True)

            st.subheader("📈 Data Historis")
            if category_column:
                fig_hist = px.line(
                    df_agg,
                    x='period',
                    y=metric_column,
                    color=category_column,
                    title=f'Tren {metric_column}'
                )
            else:
                fig_hist = px.line(
                    df_agg,
                    x='period',
                    y=metric_column,
                    title=f'Tren {metric_column}'
                )
            st.plotly_chart(fig_hist, use_container_width=True)

            # ====== AI Forecast (Hanya Jika Data Cukup) ======
            MIN_HISTORICAL_ROWS = 10
            if len(df_agg) < MIN_HISTORICAL_ROWS:
                st.warning(f"Data historis terlalu sedikit untuk prediksi AI. Minimal upload {MIN_HISTORICAL_ROWS} baris data agar hasil lebih bermakna.")
                return

            st.subheader("🔮 Proyeksi Masa Depan (AI)")
            st.info("Forecast dihasilkan otomatis oleh Gemini AI. Hasil prediksi hanya berupa tabel (tanpa kode python).")

            ringkas = df_agg[['period', metric_column]].copy()
            ringkas['period'] = ringkas['period'].astype(str)
            data_table = ringkas.tail(30).to_csv(index=False)

            prompt = f"""
Data berikut adalah tren '{metric_column}' dari dataset media.
Kolom 'period' = tanggal, '{metric_column}' = nilainya.

Tampilkan prediksi {forecast_periods} periode ke depan ({time_window.lower()}):
- Jawab HANYA dalam bentuk tabel markdown tanpa kode python, tanpa narasi tambahan.
- Kolom tabel: periode_prediksi, nilai_prediksi.
- Periode awal prediksi = setelah data terakhir berikut:

