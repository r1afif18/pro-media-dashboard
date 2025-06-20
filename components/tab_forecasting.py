import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import timedelta

def show(tab):  # Pastikan nama fungsi adalah show
    with tab:
        st.header("🔮 Forecasting")
        st.info("Fitur forecasting placeholder. Bisa diisi model ARIMA/Prophet dll.")
        
        # Periksa apakah data tersedia
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return
            
        try:
            df = st.session_state.df.copy()
            df['date'] = pd.to_datetime(df['date'])
            df['date_only'] = df['date'].dt.date
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            
            if not daily_counts.empty:
                last_date = daily_counts['date_only'].max()
                future_dates = pd.date_range(
                    start=pd.to_datetime(last_date) + timedelta(days=1),
                    periods=7,
                    freq='D'
                ).date.tolist()
                
                np.random.seed(42)
                mean_count = daily_counts['count'].mean()
                predictions = np.random.randint(
                    int(mean_count * 0.8),
                    int(mean_count * 1.2),
                    size=7
                )
                
                forecast_df = pd.DataFrame({
                    'date_only': daily_counts['date_only'].tolist() + future_dates,
                    'count': daily_counts['count'].tolist() + predictions.tolist(),
                    'type': ['Aktual'] * len(daily_counts) + ['Prediksi'] * 7
                })
                
                forecast_df['date_only'] = pd.to_datetime(forecast_df['date_only'])
                
                fig = px.line(
                    forecast_df,
                    x='date_only',
                    y='count',
                    color='type',
                    title='Contoh Visualisasi Prediksi (Placeholder)',
                    labels={'date_only': 'Tanggal', 'count': 'Jumlah Berita'},
                    line_dash='type'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Tidak ada data untuk ditampilkan")
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam pemrosesan data: {str(e)}")
