import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.linear_model import LinearRegression
from gemini_engine import gemini_engine
import logging

logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.header("🔮 Forecasting & Strategi - Analisis Tren Berita")
        st.info(
        """
        Tab ini memungkinkan Anda memproyeksikan tren jumlah dan sentimen berita ke depan menggunakan metode statistik (Moving Average & Linear Regression) berbasis data historis yang telah diupload.  
        Hasil prediksi dapat digunakan untuk mengantisipasi perubahan tren, mengambil keputusan strategis, serta mendapatkan insight otomatis dari AI (Gemini).
    
        Pastikan data sudah lengkap dan terstruktur agar hasil prediksi lebih akurat.
        """
        )

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
            method = st.selectbox("Metode Forecasting", ["Moving Average", "Linear Regression"])

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

            MIN_HISTORICAL_ROWS = 8
            if len(df_agg) < MIN_HISTORICAL_ROWS:
                st.warning(f"Data historis terlalu sedikit untuk forecast. Minimal upload {MIN_HISTORICAL_ROWS} baris data.")
                return

            st.subheader("🔮 Proyeksi Masa Depan (Non-AI)")

            last_date = pd.to_datetime(df_agg['period'].iloc[-1])
            if freq == 'D':
                start_date = last_date + pd.Timedelta(days=1)
            elif freq == 'W':
                start_date = last_date + pd.Timedelta(weeks=1)
            else:
                start_date = (last_date + pd.DateOffset(months=1)).normalize()
            future_dates = pd.date_range(start=start_date, periods=forecast_periods, freq=freq)

            if method == "Moving Average":
                window = min(5, len(df_agg))
                avg = df_agg[metric_column].rolling(window=window).mean().iloc[-1]
                predictions = [avg]*forecast_periods
                note = f"Moving average {window}-periode terakhir."
            else:
                # Linear regression time series (period to int)
                df_agg_reset = df_agg.copy()
                df_agg_reset = df_agg_reset.reset_index(drop=True)
                df_agg_reset['t'] = np.arange(len(df_agg_reset))
                X = df_agg_reset['t'].values.reshape(-1,1)
                y = df_agg_reset[metric_column].values
                lr = LinearRegression()
                lr.fit(X, y)
                future_X = np.arange(len(df_agg_reset), len(df_agg_reset)+forecast_periods).reshape(-1,1)
                predictions = lr.predict(future_X)
                note = "Linear Regression pada urutan waktu."

            pred_df = pd.DataFrame({
                'periode_prediksi': future_dates,
                'nilai_prediksi': predictions
            })

            st.info(f"Prediksi ({method}): {note}")
            st.dataframe(pred_df, use_container_width=True)
            # Gabung untuk visualisasi
            chart_df = pd.concat([
                pd.DataFrame({'periode': df_agg['period'], 'nilai': df_agg[metric_column], 'tipe': 'Historis'}),
                pd.DataFrame({'periode': pred_df['periode_prediksi'], 'nilai': pred_df['nilai_prediksi'], 'tipe': 'Prediksi'})
            ])
            fig_forecast = px.line(
                chart_df,
                x='periode',
                y='nilai',
                color='tipe',
                markers=True,
                title=f"Forecasting {metric_column} ({method})"
            )
            st.plotly_chart(fig_forecast, use_container_width=True)

            # AI hanya untuk strategi, bukan prediksi numerik
            st.subheader("💡 Rekomendasi Strategi oleh AI")
            prompt = f"""
Berdasarkan data historis (dan hasil prediksi {method} pada grafik di atas), 
berikan saran maksimal 5 poin strategi manajemen dan distribusi konten media, berbasis tren {metric_column} ke depan. 
Jawab hanya dalam bullet point.
"""
            rekomendasi = gemini_engine.ask(prompt, df_agg)
            import re
            rekomendasi_clean = re.sub(r'```[\s\S]+?```', '', rekomendasi)
            st.markdown(rekomendasi_clean)

        except Exception as e:
            st.error(f"⚠️ Terjadi kesalahan dalam analisis: {str(e)}")
            logger.exception("Forecasting error")
