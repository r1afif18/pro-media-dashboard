import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import timedelta

def show():
    st.header("🔮 Forecasting")

    st.info("""
    **Fitur dalam Pengembangan**  
    Versi berikutnya akan menyertakan prediksi tren menggunakan:
    - Analisis deret waktu (Time Series Analysis)
    - Model ARIMA/Prophet
    - Integrasi dengan Gemini untuk prediksi kualitatif
    """)

    if 'df' in st.session_state and st.session_state.df is not None and not st.session_state.df.empty:
        df = st.session_state.df.copy()

        # ==== PILIHAN KOLUM TANGGAL SECARA OTOMATIS ====
        date_columns = df.select_dtypes(include=['datetime', 'datetime64[ns]', 'object']).columns.tolist()
        # Deteksi kolom yg mengandung kata 'date'
        suggested = [col for col in date_columns if 'date' in col.lower() or 'tanggal' in col.lower()]
        if suggested:
            default_col = suggested[0]
        else:
            default_col = date_columns[0] if date_columns else None

        selected_date_column = st.selectbox(
            "Pilih Kolom Tanggal",
            options=date_columns,
            index=date_columns.index(default_col) if default_col else 0
        ) if date_columns else None

        if selected_date_column is None:
            st.error("Tidak ditemukan kolom bertipe tanggal di dataset Anda.")
            return

        # Pastikan kolom bertipe datetime
        df[selected_date_column] = pd.to_datetime(df[selected_date_column], errors="coerce")
        if df[selected_date_column].isnull().all():
            st.error("Semua nilai di kolom tanggal tidak valid. Cek format datanya.")
            return

        # ==== KONTROL RENTANG WAKTU ====
        min_date = df[selected_date_column].min().date()
        max_date = df[selected_date_column].max().date()

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input('Tanggal Mulai', value=min_date, min_value=min_date, max_value=max_date)
        with col2:
            end_date = st.date_input('Tanggal Akhir', value=max_date, min_value=min_date, max_value=max_date)

        # Filter data sesuai range
        df_range = df[(df[selected_date_column].dt.date >= start_date) & (df[selected_date_column].dt.date <= end_date)]

        if df_range.empty:
            st.warning("Tidak ada data dalam rentang waktu yang dipilih.")
            return

        # === AGGREGASI DATA (misal: jumlah berita per hari) ===
        daily_counts = df_range.groupby(df_range[selected_date_column].dt.date).size().reset_index(name='count')

        if not daily_counts.empty:
            last_date = daily_counts[selected_date_column].max()
            # Buat rentang tanggal untuk prediksi
            future_dates = pd.date_range(
                start=pd.to_datetime(last_date) + timedelta(days=1),
                periods=7,
                freq='D'
            ).date.tolist()

            # Generate random data untuk prediksi (NANTI diganti Prophet)
            np.random.seed(42)
            mean_count = daily_counts['count'].mean()
            predictions = np.random.randint(
                int(mean_count * 0.8),
                int(mean_count * 1.2),
                size=7
            )

            # Gabungkan data aktual dan prediksi
            forecast_df = pd.DataFrame({
                'date_only': daily_counts[selected_date_column].tolist() + future_dates,
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
                labels={'date_only': 'Tanggal', 'count': 'Jumlah'},
                line_dash='type'
            )

            # Garis vertikal pembatas prediksi
            fig.add_shape(
                type="line",
                x0=last_date,
                y0=0,
                x1=last_date,
                y1=forecast_df['count'].max() * 1.1,
                line=dict(color="red", width=2, dash="dash"),
            )
            fig.add_annotation(
                x=last_date,
                y=forecast_df['count'].max() * 1.15,
                text="Mulai Prediksi",
                showarrow=False,
                font=dict(color="red")
            )

            st.plotly_chart(fig, use_container_width=True)
            st.markdown("""
            **Keterangan:**
            - Garis biru: Data aktual
            - Garis oranye: Prediksi (placeholder/acak)
            - Garis merah: Titik awal prediksi
            """)
        else:
            st.warning("Data tidak memiliki cukup entri untuk membuat prediksi.")

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

    with st.expander("Berikan Saran untuk Fitur Forecasting"):
        feedback = st.text_area("Apa yang Anda harapkan dari fitur forecasting?")
        if st.button("Kirim Saran"):
            st.success("Terima kasih atas sarannya! Kami akan mempertimbangkan untuk pengembangan fitur ini.")

