import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from gemini_engine import gemini_engine
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import logging
import utils

# Setup logging
logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.header("🔮 Forecasting & Strategi - Analisis Tren Berita")
        
        # Cek jika data sudah diupload
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("📤 Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return
            
        df = st.session_state.df.copy()
        
        # Pastikan kolom tanggal ada
        if 'date' not in df.columns:
            st.error("❌ Data tidak memiliki kolom tanggal ('date') untuk forecasting")
            return
            
        try:
            # Konversi tanggal
            df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%Y-%m-%d')
            invalid_dates = df[df['date'].isna()]
            
            if not invalid_dates.empty:
                st.warning(f"⚠️ Ditemukan {len(invalid_dates)} baris dengan format tanggal tidak valid. Baris ini akan diabaikan.")
            
            df = df.dropna(subset=['date'])
            
            # Pastikan ada data yang valid
            if len(df) == 0:
                st.error("❌ Tidak ada data tanggal yang valid untuk dianalisis")
                return
            
            # Siapkan data harian
            df['date_only'] = df['date'].dt.date
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            daily_counts = daily_counts.sort_values('date_only')
            
            # Input parameter forecasting
            st.subheader("⚙️ Parameter Proyeksi")
            col1, col2 = st.columns(2)
            with col1:
                forecast_days = st.slider("Hari ke Depan", 1, 90, 14)
            with col2:
                model_type = st.selectbox("Model Forecasting", 
                                         ["Holt-Winters", "Moving Average"], 
                                         index=0)
            
            # Analisis tren real-time
            st.subheader("📈 Analisis Tren Real-Time")
            
            # Hitung moving average
            daily_counts['7_day_avg'] = daily_counts['count'].rolling(window=7, min_periods=1).mean()
            
            # Visualisasi tren
            fig_trend = px.line(
                daily_counts,
                x='date_only',
                y=['count', '7_day_avg'],
                title='Tren Jumlah Berita Harian',
                labels={'date_only': 'Tanggal', 'value': 'Jumlah Berita'},
                color_discrete_map={'count': '#1f77b4', '7_day_avg': '#ff7f0e'}
            )
            fig_trend.update_layout(legend_title_text='', hovermode='x unified')
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Forecasting section
            st.subheader("🔮 Proyeksi Masa Depan")
            
            if st.button("Buat Proyeksi & Analisis Strategi", key="forecast_btn", use_container_width=True):
                with st.spinner("Menganalisis tren dan membuat proyeksi..."):
                    try:
                        # Pastikan ada cukup data
                        if len(daily_counts) < 7:
                            st.error("❌ Minimal 7 hari data diperlukan untuk membuat proyeksi")
                            return
                            
                        # Ambil data terbaru
                        last_date = daily_counts['date_only'].iloc[-1]
                        
                        if model_type == "Holt-Winters":
                            # Model statistik Holt-Winters
                            model = ExponentialSmoothing(
                                daily_counts['count'],
                                seasonal_periods=7,
                                trend='add',
                                seasonal='add'
                            ).fit()
                            forecast = model.forecast(forecast_days)
                        else:
                            # Simple moving average
                            forecast = [daily_counts['count'].tail(7).mean()] * forecast_days
                        
                        # PERBAIKAN DI SINI: Pastikan last_date adalah datetime.date
                        # Generate future dates
                        future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days + 1)]
                        
                        # Buat dataframe untuk visualisasi
                        history_df = daily_counts.tail(30)[['date_only', 'count']].rename(
                            columns={'date_only': 'date', 'count': 'value'})
                        history_df['type'] = 'Aktual'
                        
                        projection_df = pd.DataFrame({
                            'date': future_dates,
                            'value': forecast,
                            'type': 'Proyeksi'
                        })
                        
                        combined_df = pd.concat([history_df, projection_df])
                        
                        # Buat visualisasi proyeksi
                        fig_projection = px.line(
                            combined_df,
                            x='date',
                            y='value',
                            color='type',
                            title=f'Proyeksi {forecast_days} Hari ke Depan',
                            labels={'date': 'Tanggal', 'value': 'Jumlah Berita'},
                            color_discrete_map={'Aktual': '#1f77b4', 'Proyeksi': '#ff7f0e'}
                        )
                        
                        # Tambahkan garis pembatas
                        fig_projection.add_vline(
                            x=last_date,
                            line_dash="dash",
                            line_color="green",
                            annotation_text="Mulai Proyeksi"
                        )
                        
                        # Confidence interval (untuk Holt-Winters)
                        if model_type == "Holt-Winters":
                            conf_int = model.prediction_intervals(forecast_days)
                            fig_projection.add_traces([
                                go.Scatter(
                                    x=future_dates,
                                    y=conf_int[:, 0],
                                    mode='lines',
                                    line=dict(width=0),
                                    showlegend=False,
                                    name='CI Bawah'
                                ),
                                go.Scatter(
                                    x=future_dates,
                                    y=conf_int[:, 1],
                                    mode='lines',
                                    line=dict(width=0),
                                    fill='tonexty',
                                    fillcolor='rgba(255, 126, 14, 0.2)',
                                    name='95% CI'
                                )
                            ])
                        
                        fig_projection.update_layout(
                            xaxis=dict(tickangle=45),
                            hovermode='x unified'
                        )
                        st.plotly_chart(fig_projection, use_container_width=True)
                        
                        # Tampilkan detail proyeksi
                        st.subheader("Detail Proyeksi")
                        projection_display = projection_df.copy()
                        
                        # Pastikan nilai adalah integer
                        if hasattr(projection_display['value'], 'tolist'):
                            projection_display['value'] = projection_display['value'].round().astype(int)
                        else:
                            projection_display['value'] = [round(v) for v in projection_display['value']]
                            
                        projection_display = projection_display.rename(columns={
                            'date': 'Tanggal',
                            'value': 'Jumlah Berita Proyeksi'
                        }).reset_index(drop=True)
                        
                        st.dataframe(projection_display, use_container_width=True)
                        
                        # Rekomendasi strategi oleh AI
                        st.subheader("💡 Rekomendasi Strategi oleh AI")
                        
                        # Format forecast untuk prompt
                        if hasattr(forecast, 'tolist'):
                            forecast_list = forecast.tolist()
                        else:
                            forecast_list = forecast
                        
                        # Prompt untuk Gemini
                        prompt = f"""
                        Berikan rekomendasi strategi manajemen konten berdasarkan:
                        - Tren historis: {daily_counts.tail(7)['count'].tolist()}
                        - Proyeksi: {forecast_list}
                        - Model: {model_type}
                        
                        Format:
                        1. **Optimalisasi Produksi Konten**
                        - [Analisis & rekomendasi]
                        
                        2. **Strategi Distribusi** 
                        - [Analisis & rekomendasi]
                        
                        3. **Persiapan Fluktuasi**
                        - [Analisis & rekomendasi]
                        
                        Gunakan data spesifik dan berikan saran praktis.
                        """
                        
                        recommendation = gemini_engine.ask(prompt, pd.DataFrame())
                        st.markdown(recommendation)
                        
                    except Exception as e:
                        st.error(f"⚠️ Error forecasting: {str(e)}")
                        logger.exception("Forecasting error")
        
        except Exception as e:
            st.error(f"⚠️ Error pemrosesan: {str(e)}")
            logger.exception("Data processing error")
