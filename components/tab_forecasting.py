# forecasting.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import warnings

# Konfigurasi halaman
st.set_page_config(page_title="🔮 Forecasting Sentimen Berita", layout="wide")
st.title("🔮 Forecasting Tren Sentimen Berita")

# Fungsi untuk memproses data
def process_data(df):
    # Konversi tipe data
    df['sentiment_score'] = pd.to_numeric(df['sentiment_score'], errors='coerce')
    df['count'] = pd.to_numeric(df['count'], errors='coerce')
    df = df.fillna({'sentiment_score': 0, 'count': 0})
    
    # Konversi tanggal
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    
    # Hitung weighted sentiment
    df['weighted_sentiment'] = df['sentiment_score'] * df['count']
    
    # Agregasi harian
    daily_df = df.groupby('date').agg({
        'weighted_sentiment': 'sum',
        'count': 'sum'
    }).reset_index()
    daily_df['avg_sentiment'] = daily_df['weighted_sentiment'] / daily_df['count']
    
    return daily_df

# Fungsi forecasting ARIMA
def arima_forecast(data, steps=7):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = ARIMA(data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=steps)
    return forecast

# Upload file
uploaded_file = st.file_uploader("Upload file CSV berita", type="csv")

if uploaded_file is not None:
    try:
        # Baca dan proses data
        df = pd.read_csv(uploaded_file)
        processed_df = process_data(df)
        
        # Tampilkan data
        st.subheader("Data Sentimen Harian")
        st.dataframe(processed_df, height=300)
        
        # Visualisasi tren historis
        st.subheader("📈 Tren Sentimen Historis")
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(processed_df['date'], processed_df['avg_sentiment'], 'b-', label='Aktual')
        ax.set_title('Rata-Rata Sentimen Harian')
        ax.set_xlabel('Tanggal')
        ax.set_ylabel('Skor Sentimen')
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Forecasting
        st.subheader("🔮 Proyeksi Masa Depan")
        
        # Input parameter forecasting
        col1, col2 = st.columns(2)
        with col1:
            forecast_days = st.slider("Jumlah Hari ke Depan", 1, 30, 7)
        with col2:
            model_type = st.selectbox("Model Forecasting", ["ARIMA", "Moving Average"])
        
        # Lakukan forecasting
        if model_type == "ARIMA":
            # Gunakan ARIMA
            forecast = arima_forecast(processed_df['avg_sentiment'], steps=forecast_days)
        else:
            # Moving Average
            forecast = processed_df['avg_sentiment'].rolling(window=3).mean().iloc[-forecast_days:]
        
        # Generate future dates
        last_date = processed_df['date'].iloc[-1]
        future_dates = [last_date + timedelta(days=i) for i in range(1, forecast_days+1)]
        
        # Plot hasil
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(processed_df['date'], processed_df['avg_sentiment'], 'b-', label='Historis')
        ax.plot(future_dates, forecast, 'r--', label='Proyeksi')
        ax.set_title(f'Proyeksi Sentimen {forecast_days} Hari ke Depan')
        ax.set_xlabel('Tanggal')
        ax.set_ylabel('Skor Sentimen')
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        
        # Tampilkan data proyeksi
        forecast_df = pd.DataFrame({
            'Tanggal': future_dates,
            'Proyeksi Skor Sentimen': forecast
        })
        st.subheader("Detail Proyeksi")
        st.dataframe(forecast_df.style.format({
            'Proyeksi Skor Sentimen': '{:.2f}'
        }))
        
        # Evaluasi model
        if len(processed_df) > 5:
            st.subheader("Evaluasi Model")
            
            # Split data train-test
            train = processed_df['avg_sentiment'].iloc[:-3]
            test = processed_df['avg_sentiment'].iloc[-3:]
            
            # Training model
            model = ARIMA(train, order=(1,1,1))
            model_fit = model.fit()
            
            # Forecasting test
            test_forecast = model_fit.forecast(steps=3)
            
            # Hitung RMSE
            rmse = np.sqrt(mean_squared_error(test, test_forecast))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("RMSE (3 Hari Terakhir)", f"{rmse:.4f}")
            
            with col2:
                st.metric("Akurasi Model", f"{(1 - rmse):.2%}")
            
            # Plot evaluasi
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(test.index, test, 'bo-', label='Aktual')
            ax.plot(test.index, test_forecast, 'ro--', label='Prediksi')
            ax.set_title('Evaluasi Prediksi vs Aktual')
            ax.set_xlabel('Hari')
            ax.set_ylabel('Skor Sentimen')
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
        st.error("Pastikan format file sesuai. Kolom wajib: date, sentiment_score, count")

else:
    st.info("Silakan upload file CSV untuk memulai forecasting")
    
    # Tampilkan contoh data
    st.subheader("Contoh Format Data")
    example_data = {
        'date': ['2024-06-10', '2024-06-11', '2024-06-12'],
        'title': ['Contoh Berita 1', 'Contoh Berita 2', 'Contoh Berita 3'],
        'sentiment_score': [0.85, -0.62, 0.76],
        'count': [10, 8, 12]
    }
    st.dataframe(pd.DataFrame(example_data))
