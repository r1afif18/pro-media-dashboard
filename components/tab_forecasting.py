import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta
from gemini_engine import gemini_engine
import logging

logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.header("🔮 Forecasting & Strategi - Analisis Tren Berita")
        st.info("Fitur ini membantu memproyeksikan tren berita berdasarkan data historis")
        
        # Step 1: Pilih kolom yang akan dianalisis
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("📤 Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return
            
        df = st.session_state.df.copy()
        
        st.subheader("1. Pilih Data untuk Analisis")
        col1, col2 = st.columns(2)
        
        with col1:
            # Pilih kolom tanggal
            date_cols = [col for col in df.columns if 'date' in col.lower()]
            if not date_cols:
                st.error("❌ Tidak ditemukan kolom tanggal di dataset")
                return
            date_column = st.selectbox("Kolom Tanggal", date_cols)
            
            # Pilih kolom numerik
            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            if not numeric_cols:
                st.error("❌ Tidak ditemukan kolom numerik di dataset")
                return
            metric_column = st.selectbox("Kolom Metrik", numeric_cols)
            
        with col2:
            # Pilih kategori untuk grouping (opsional)
            category_cols = [''] + [col for col in df.columns if col != date_column and col != metric_column]
            category_column = st.selectbox("Kelompokkan Berdasarkan (opsional)", category_cols)
            
            # Pilih rentang waktu
            time_window = st.selectbox("Rentang Waktu", ["Harian", "Mingguan", "Bulanan"])
        
        st.subheader("2. Parameter Forecasting")
        col1, col2 = st.columns(2)
        with col1:
            forecast_periods = st.slider("Jumlah Periode ke Depan", 1, 30, 7)
        with col2:
            method = st.selectbox("Metode Forecasting", 
                                 ["Rata-rata Bergerak", "Pola Terakhir", "Sederhana"])
        
        # Tombol analisis
        if st.button("Buat Proyeksi & Analisis Strategi", use_container_width=True):
            with st.spinner("Menganalisis data dan membuat proyeksi..."):
                try:
                    # Proses data
                    df_clean = df.copy()
                    
                    # Konversi tanggal - lebih toleran
                    try:
                        df_clean[date_column] = pd.to_datetime(df_clean[date_column], errors='coerce')
                        df_clean = df_clean.dropna(subset=[date_column])
                    except Exception as e:
                        st.error(f"❌ Gagal mengonversi kolom tanggal: {str(e)}")
                        return
                    
                    # Agregasi data berdasarkan periode
                    df_clean['period'] = pd.to_datetime(df_clean[date_column])
                    
                    if time_window == "Mingguan":
                        df_clean['period'] = df_clean['period'].dt.to_period('W').dt.start_time
                    elif time_window == "Bulanan":
                        df_clean['period'] = df_clean['period'].dt.to_period('M').dt.start_time
                    
                    # Grouping data
                    group_cols = ['period']
                    if category_column:
                        group_cols.append(category_column)
                    
                    df_agg = df_clean.groupby(group_cols)[metric_column].sum().reset_index()
                    
                    # Visualisasi data historis
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
                    
                    # Forecasting sederhana
                    st.subheader("🔮 Proyeksi Masa Depan")
                    
                    # Metode rata-rata sederhana
                    last_value = df_agg[metric_column].iloc[-1]
                    avg_value = df_agg[metric_column].mean()
                    
                    # Buat data proyeksi
                    last_date = df_agg['period'].iloc[-1]
                    
                    # PERBAIKAN UTAMA: Gunakan objek datetime untuk operasi tanggal
                    if time_window == "Harian":
                        delta = timedelta(days=1)
                    elif time_window == "Mingguan":
                        delta = timedelta(weeks=1)
                    else:  # Bulanan
                        delta = timedelta(days=30)  # Perkiraan
                    
                    # Buat tanggal proyeksi
                    future_dates = []
                    for i in range(1, forecast_periods + 1):
                        next_date = last_date + i * delta
                        future_dates.append(next_date)
                    
                    if method == "Rata-rata Bergerak":
                        proj_values = [avg_value] * forecast_periods
                    elif method == "Pola Terakhir":
                        proj_values = [last_value] * forecast_periods
                    else:
                        # Metode sederhana: rata-rata 3 periode terakhir
                        last_values = df_agg[metric_column].tail(3)
                        avg_last = last_values.mean()
                        proj_values = [avg_last] * forecast_periods
                    
                    # Buat dataframe proyeksi
                    proj_df = pd.DataFrame({
                        'Periode': future_dates,
                        metric_column: proj_values,
                        'Tipe': 'Proyeksi'
                    })
                    
                    # Gabungkan dengan data historis untuk visualisasi
                    hist_df = df_agg[['period', metric_column]].copy()
                    hist_df['Tipe'] = 'Historis'
                    hist_df = hist_df.rename(columns={'period': 'Periode'})
                    
                    combined_df = pd.concat([hist_df, proj_df])
                    
                    # Visualisasi proyeksi
                    fig_forecast = px.line(
                        combined_df,
                        x='Periode',
                        y=metric_column,
                        color='Tipe',
                        title=f'Proyeksi {metric_column}',
                        color_discrete_map={'Historis': '#1f77b4', 'Proyeksi': '#ff7f0e'}
                    )
                    fig_forecast.add_vline(
                        x=last_date,
                        line_dash="dash",
                        line_color="green",
                        annotation_text="Mulai Proyeksi"
                    )
                    st.plotly_chart(fig_forecast, use_container_width=True)
                    
                    # Tampilkan tabel proyeksi
                    st.subheader("Detail Proyeksi")
                    proj_df = proj_df.rename(columns={'Periode': 'Tanggal', metric_column: 'Nilai Proyeksi'})
                    st.dataframe(proj_df, use_container_width=True)
                    
                    # Rekomendasi strategi oleh AI
                    st.subheader("💡 Rekomendasi Strategi oleh AI")
                    
                    # Siapkan prompt untuk AI
                    prompt = f"""
                    Berikan rekomendasi strategi manajemen konten berita berdasarkan proyeksi berikut:
                    
                    - Metrik: {metric_column}
                    - Metode proyeksi: {method}
                    - Periode proyeksi: {forecast_periods} {time_window}
                    - Nilai rata-rata historis: {avg_value:.2f}
                    - Nilai terakhir: {last_value:.2f}
                    - Proyeksi: {', '.join([str(round(v, 2)) for v in proj_values])}
                    
                    Format rekomendasi:
                    1. **Optimalisasi Produksi Konten**
                    2. **Strategi Distribusi** 
                    3. **Persiapan Fluktuasi**
                    
                    Berikan saran praktis.
                    """
                    
                    recommendation = gemini_engine.ask(prompt, pd.DataFrame())
                    st.markdown(recommendation)
                    
                except Exception as e:
                    st.error(f"⚠️ Terjadi kesalahan dalam analisis: {str(e)}")
                    logger.exception("Forecasting error")
