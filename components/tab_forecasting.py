import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import timedelta

def show():
    st.header("🔮 Forecasting")
    
    # Placeholder yang lebih menarik
    st.info("""
    **Fitur dalam Pengembangan**  
    Versi berikutnya akan menyertakan prediksi tren menggunakan:
    - Analisis deret waktu (Time Series Analysis)
    - Model ARIMA/Prophet
    - Integrasi dengan Gemini untuk prediksi kualitatif
    """)
    
    # Tampilkan grafik placeholder jika data tersedia
    if 'df' in st.session_state and st.session_state.df is not None:
        df = st.session_state.df.copy()
        
        # Siapkan data untuk contoh visualisasi
        df['date'] = pd.to_datetime(df['date'])
        df['date_only'] = df['date'].dt.date
        
        try:
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            
            # Pastikan daily_counts memiliki setidaknya satu baris data
            if not daily_counts.empty:
                # PERBAIKAN: Gunakan pendekatan yang lebih kompatibel
                last_date = daily_counts['date_only'].max()
                
                # Buat rentang tanggal untuk prediksi
                future_dates = pd.date_range(
                    start=pd.to_datetime(last_date) + timedelta(days=1),
                    periods=7,
                    freq='D'
                ).date.tolist()
                
                # Generate random data untuk prediksi
                np.random.seed(42)
                mean_count = daily_counts['count'].mean()
                predictions = np.random.randint(
                    int(mean_count * 0.8),
                    int(mean_count * 1.2),
                    size=7
                )
                
                # Gabungkan data aktual dan prediksi
                forecast_df = pd.DataFrame({
                    'date_only': daily_counts['date_only'].tolist() + future_dates,
                    'count': daily_counts['count'].tolist() + predictions.tolist(),
                    'type': ['Aktual'] * len(daily_counts) + ['Prediksi'] * 7
                })
                
                # Konversi ke datetime untuk Plotly
                forecast_df['date_only'] = pd.to_datetime(forecast_df['date_only'])
                
                # Buat visualisasi
                fig = px.line(
                    forecast_df, 
                    x='date_only', 
                    y='count', 
                    color='type',
                    title='Contoh Visualisasi Prediksi (Placeholder)',
                    labels={'date_only': 'Tanggal', 'count': 'Jumlah Berita'},
                    line_dash='type'
                )
                
                # Tambahkan garis vertikal untuk memisahkan aktual dan prediksi
                # PERBAIKAN: Gunakan pendekatan yang berbeda untuk vline
                fig.add_shape(
                    type="line",
                    x0=last_date,
                    y0=0,
                    x1=last_date,
                    y1=forecast_df['count'].max() * 1.1,
                    line=dict(color="red", width=2, dash="dash"),
                )
                
                # Tambahkan anotasi
                fig.add_annotation(
                    x=last_date,
                    y=forecast_df['count'].max() * 1.15,
                    text="Mulai Prediksi",
                    showarrow=False,
                    font=dict(color="red")
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tambahkan penjelasan
                st.markdown("""
                **Keterangan:**
                - Garis biru: Data aktual
                - Garis oranye: Prediksi (contoh acak)
                - Garis putus-putus merah: Titik awal prediksi
                """)
            else:
                st.warning("Data tidak memiliki cukup entri untuk membuat prediksi")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat membuat prediksi: {str(e)}")
            st.warning("Silakan coba dengan dataset yang berbeda")
    else:
        st.warning("Silakan upload data untuk melihat contoh visualisasi prediksi")
        st.image("https://via.placeholder.com/800x400?text=Upload+Data+Untuk+Melihat+Contoh+Prediksi", 
                 use_column_width=True)
    
    # Progress bar dan timeline
    st.divider()
    st.subheader("Timeline Pengembangan")
    
    timeline_data = {
        "Fitur": ["Integrasi Model Prediksi", "Optimasi Performa", "UI/UX Improvement", "Testing & Deployment"],
        "Status": ["Dalam Pengembangan", "Belum Dimulai", "Belum Dimulai", "Belum Dimulai"],
        "Progress": [75, 0, 0, 0]
    }
    
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True)
    
    # Tombol untuk memberikan feedback
    with st.expander("Berikan Saran untuk Fitur Forecasting"):
        feedback = st.text_area("Apa yang Anda harapkan dari fitur forecasting?")
        if st.button("Kirim Saran"):
            st.success("Terima kasih atas sarannya! Kami akan mempertimbangkan untuk pengembangan fitur ini.")