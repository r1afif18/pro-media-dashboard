import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.header("🔮 Forecasting - Prediksi Tren Berita")
        
        # Cek jika data sudah diupload
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return
            
        df = st.session_state.df.copy()
        
        # Perbaikan 1: Pastikan kolom tanggal ada dan dalam format yang benar
        if 'date' not in df.columns:
            st.error("Data tidak memiliki kolom tanggal ('date') untuk forecasting")
            return
            
        try:
            # Konversi tanggal dan buat data harian
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])  # Hapus baris dengan tanggal tidak valid
            
            # Buat kolom tanggal saja (tanpa waktu)
            df['date_only'] = df['date'].dt.date
            
            # Hitung jumlah berita per hari
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            daily_counts['date_only'] = pd.to_datetime(daily_counts['date_only'])
            
            # Set index sebagai DateTimeIndex dengan frekuensi harian
            daily_counts = daily_counts.set_index('date_only').asfreq('D')
            daily_counts['count'] = daily_counts['count'].fillna(0)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam memproses tanggal: {str(e)}")
            logger.error(f"Date processing error: {str(e)}")
            return
            
        # Input parameter forecasting
        st.subheader("⚙️ Parameter Forecasting")
        col1, col2 = st.columns(2)
        
        with col1:
            forecast_days = st.slider("Hari ke Depan yang Diprediksi", 1, 90, 14)
            test_size = st.slider("Ukuran Data Testing (%)", 10, 50, 20)
        
        with col2:
            model_type = st.selectbox("Model Forecasting", 
                                     ['Holt-Winters', 'Exponential Smoothing'])
            seasonality = st.selectbox("Musiman", 
                                      ['Harian (7 hari)', 'Mingguan (4 minggu)', 'Bulanan (12 bulan)'])
        
        # Analisis data time series
        st.subheader("📈 Analisis Deret Waktu")
        
        try:
            # Tentukan periode berdasarkan pilihan musiman
            period_map = {
                'Harian (7 hari)': 7,
                'Mingguan (4 minggu)': 28,
                'Bulanan (12 bulan)': 365  # Pendekatan untuk musiman bulanan
            }
            period = period_map[seasonality]
            
            # Decompose time series
            decomposition = seasonal_decompose(
                daily_counts['count'], 
                period=period,
                model='additive'
            )
            
            # Plot decomposition
            fig_decompose = go.Figure()
            
            # Original data
            fig_decompose.add_trace(go.Scatter(
                x=daily_counts.index,
                y=daily_counts['count'],
                name='Data Asli',
                line=dict(color='#1f77b4')
            ))
            
            # Trend
            fig_decompose.add_trace(go.Scatter(
                x=decomposition.trend.index,
                y=decomposition.trend,
                name='Tren',
                line=dict(color='#ff7f0e')
            ))
            
            # Seasonal
            fig_decompose.add_trace(go.Scatter(
                x=decomposition.seasonal.index,
                y=decomposition.seasonal,
                name='Musiman',
                line=dict(color='#2ca02c')
            ))
            
            # Residual
            fig_decompose.add_trace(go.Scatter(
                x=decomposition.resid.index,
                y=decomposition.resid,
                name='Residual',
                line=dict(color='#d62728')
            ))
            
            fig_decompose.update_layout(
                title='Dekomposisi Deret Waktu',
                xaxis_title='Tanggal',
                yaxis_title='Jumlah Berita',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                height=500
            )
            
            st.plotly_chart(fig_decompose, use_container_width=True)
            
        except Exception as e:
            st.warning(f"Tidak dapat melakukan dekomposisi deret waktu: {str(e)}")
            logger.warning(f"Decomposition error: {str(e)}")
        
        # Forecasting section
        st.subheader("🔮 Prediksi Masa Depan")
        
        if st.button("Buat Prediksi", use_container_width=True):
            with st.spinner("Melatih model dan membuat prediksi..."):
                try:
                    # Prepare data
                    ts_data = daily_counts['count']
                    
                    # Split data into train/test
                    test_size_int = int(len(ts_data) * test_size / 100)
                    train = ts_data[:-test_size_int]
                    test = ts_data[-test_size_int:]
                    
                    # Model selection
                    if model_type == 'Holt-Winters':
                        model = ExponentialSmoothing(
                            train,
                            seasonal='add',
                            seasonal_periods=7
                        )
                        model_fit = model.fit()
                        forecast = model_fit.forecast(forecast_days)
                        
                    elif model_type == 'Exponential Smoothing':
                        model = ExponentialSmoothing(
                            train,
                            trend='add',
                            seasonal='add',
                            seasonal_periods=7
                        )
                        model_fit = model.fit()
                        forecast = model_fit.forecast(forecast_days)
                    
                    # Evaluate model
                    predictions = model_fit.forecast(len(test))
                    mae = mean_absolute_error(test, predictions)
                    rmse = np.sqrt(mean_squared_error(test, predictions))
                    
                    # PERBAIKAN 2: Tangani pembuatan tanggal prediksi dengan benar
                    last_date = ts_data.index[-1]
                    
                    # Gunakan pd.date_range dengan freq='D'
                    forecast_dates = pd.date_range(
                        start=last_date + timedelta(days=1),
                        periods=forecast_days,
                        freq='D'
                    )
                    
                    # Create dataframes for plotting
                    history_df = pd.DataFrame({
                        'date': ts_data.index,
                        'count': ts_data.values,
                        'type': 'Aktual'
                    })
                    
                    forecast_df = pd.DataFrame({
                        'date': forecast_dates,
                        'count': forecast,
                        'type': 'Prediksi'
                    })
                    
                    # Combine data
                    result_df = pd.concat([history_df, forecast_df])
                    
                    # Create plot
                    fig = px.line(
                        result_df,
                        x='date',
                        y='count',
                        color='type',
                        title=f'Prediksi Jumlah Berita {forecast_days} Hari ke Depan',
                        labels={'date': 'Tanggal', 'count': 'Jumlah Berita'},
                        color_discrete_map={'Aktual': '#1f77b4', 'Prediksi': '#ff7f0e'}
                    )
                    
                    # Add confidence interval (placeholder)
                    fig.add_trace(go.Scatter(
                        x=forecast_df['date'],
                        y=forecast_df['count'] * 0.9,
                        fill=None,
                        mode='lines',
                        line=dict(width=0),
                        showlegend=False
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=forecast_df['date'],
                        y=forecast_df['count'] * 1.1,
                        fill='tonexty',
                        mode='lines',
                        line=dict(width=0),
                        fillcolor='rgba(255, 127, 14, 0.2)',
                        name='Interval Kepercayaan'
                    ))
                    
                    # Add vertical line for forecast start
                    fig.add_vline(
                        x=last_date,
                        line_dash="dash",
                        line_color="green",
                        annotation_text="Mulai Prediksi"
                    )
                    
                    # Add metrics
                    fig.add_annotation(
                        x=0.05,
                        y=0.95,
                        xref="paper",
                        yref="paper",
                        text=f"MAE: {mae:.2f}, RMSE: {rmse:.2f}",
                        showarrow=False,
                        bgcolor="white",
                        bordercolor="black",
                        borderwidth=1
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show forecast details
                    st.subheader("Detail Prediksi")
                    forecast_df_display = forecast_df.copy()
                    forecast_df_display['date'] = forecast_df_display['date'].dt.strftime('%Y-%m-%d')
                    forecast_df_display['count'] = forecast_df_display['count'].round().astype(int)
                    forecast_df_display = forecast_df_display.rename(columns={
                        'date': 'Tanggal',
                        'count': 'Jumlah Berita Prediksi'
                    })
                    
                    st.dataframe(forecast_df_display, use_container_width=True)
                    
                    # Interpretation
                    st.subheader("Interpretasi Prediksi")
                    avg_prediction = forecast_df['count'].mean().round()
                    max_prediction = forecast_df['count'].max().round()
                    min_prediction = forecast_df['count'].min().round()
                    
                    st.markdown(f"""
                    Berdasarkan model forecasting **{model_type}**:
                    - Rata-rata jumlah berita harian yang diprediksi: **{int(avg_prediction)} berita/hari**
                    - Puncak prediksi: **{int(max_prediction)} berita** pada **{forecast_df.loc[forecast_df['count'].idxmax(), 'date'].strftime('%d %b %Y')}**
                    - Prediksi terendah: **{int(min_prediction)} berita** pada **{forecast_df.loc[forecast_df['count'].idxmin(), 'date'].strftime('%d %b %Y')}**
                    """)
                    
                except Exception as e:
                    st.error(f"Terjadi kesalahan dalam membuat prediksi: {str(e)}")
                    logger.error(f"Forecasting error: {str(e)}")
        
        # Additional analysis
        st.subheader("📊 Analisis Tren Lanjutan")
        
        # PERBAIKAN 3: Analisis korelasi sentimen dengan penanganan error
        if 'sentiment' in df.columns:
            try:
                st.markdown("**Korelasi Sentimen dengan Volume Berita**")
                
                # Create daily sentiment average
                sentiment_map = {
                    'positif': 1,
                    'netral': 0,
                    'negatif': -1,
                    'positive': 1,  # Handle English versions
                    'neutral': 0,
                    'negative': -1
                }
                
                # Normalisasi sentimen
                df['sentiment'] = df['sentiment'].str.strip().str.lower()
                df['sentiment_score'] = df['sentiment'].map(sentiment_map)
                
                # Hapus baris dengan sentimen tidak valid
                df = df.dropna(subset=['sentiment_score'])
                
                # Group by date_only (yang sudah kita buat sebelumnya)
                daily_sentiment = df.groupby('date_only')['sentiment_score'].mean().reset_index()
                daily_sentiment.columns = ['date_only', 'sentiment_avg']
                
                # PERBAIKAN 4: Pastikan tipe data konsisten untuk merge
                daily_sentiment['date_only'] = pd.to_datetime(daily_sentiment['date_only'])
                
                # Merge dengan daily counts
                analysis_df = daily_counts.reset_index()
                analysis_df = analysis_df.rename(columns={'date_only': 'date'})
                
                # Gabungkan berdasarkan kolom tanggal
                analysis_df = pd.merge(
                    analysis_df, 
                    daily_sentiment, 
                    left_on='date', 
                    right_on='date_only',
                    how='left'
                )
                
                # Hapus kolom duplikat
                analysis_df = analysis_df.drop(columns=['date_only'])
                
                # Hitung korelasi
                correlation = analysis_df[['count', 'sentiment_avg']].corr().iloc[0,1]
                
                st.markdown(f"Koefisien korelasi: **{correlation:.2f}**")
                
                # Create scatter plot jika ada data yang cukup
                if not analysis_df.empty:
                    fig_scatter = px.scatter(
                        analysis_df,
                        x='sentiment_avg',
                        y='count',
                        title='Hubungan Sentimen dan Volume Berita',
                        labels={'sentiment_avg': 'Rata-rata Sentimen', 'count': 'Jumlah Berita'},
                        trendline='ols'
                    )
                    
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    
                    # Interpretation
                    if correlation > 0.3:
                        st.info("Terdapat korelasi positif: Hari dengan sentimen lebih positif cenderung memiliki lebih banyak berita")
                    elif correlation < -0.3:
                        st.info("Terdapat korelasi negatif: Hari dengan sentimen lebih negatif cenderung memiliki lebih banyak berita")
                    else:
                        st.info("Tidak ada korelasi yang signifikan antara sentimen dan volume berita")
                else:
                    st.warning("Tidak ada data yang cukup untuk analisis korelasi")
                    
            except Exception as e:
                st.error(f"Terjadi kesalahan dalam analisis korelasi: {str(e)}")
                logger.error(f"Correlation analysis error: {str(e)}")
        
        # Future development note
        st.divider()
        st.markdown("""
        ### Fitur Mendatang
        Kami terus meningkatkan kemampuan forecasting:
        - **Integrasi dengan Gemini AI**: Untuk analisis prediktif berbasis NLP
        - **Model SARIMA**: Untuk penanganan musiman yang lebih kompleks
        - **Prediksi Sentimen**: Memperkirakan sentimen berita masa depan
        - **Analisis Topik**: Prediksi topik berita yang akan dominan
        """)
