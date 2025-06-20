import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import timedelta
from gemini_engine import generate_time_series_insights

def show():
    st.header("🔮 Forecasting")

    st.info("""
    **Fitur dalam Pengembangan**  
    Versi berikutnya akan menyertakan prediksi tren menggunakan:
    - Analisis deret waktu (Time Series Analysis)
    - Model ARIMA/Prophet
    - Integrasi dengan Gemini untuk prediksi kualitatif
    """)

    if 'df' in st.session_state and st.session_state.df is not None:
        df = st.session_state.df.copy()
        
        # Pilih kolom tanggal dan metrik (misal, count berita/sentimen)
        date_columns = [c for c in df.columns if 'date' in c.lower()]
        if not date_columns:
            st.warning("Data tidak memiliki kolom bertipe tanggal.")
            return

        selected_date_column = st.selectbox('Pilih Kolom Tanggal', date_columns)
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_columns:
            st.warning("Data tidak memiliki kolom numerik untuk prediksi.")
            return

        selected_metric = st.selectbox('Pilih Kolom Metrik/Target', numeric_columns)
        
        # Kontrol rentang waktu
        df[selected_date_column] = pd.to_datetime(df[selected_date_column])
        start_date = st.date_input('Tanggal Mulai', value=df[selected_date_column].min().date())
        end_date = st.date_input('Tanggal Akhir', value=df[selected_date_column].max().date())
        mask = (df[selected_date_column].dt.date >= start_date) & (df[selected_date_column].dt.date <= end_date)
        df_range = df.loc[mask]

        if df_range.empty:
            st.warning("Tidak ada data dalam rentang waktu ini.")
            return

        # Agregasi harian (atau sesuai granularity)
        daily_counts = (
            df_range.groupby(df_range[selected_date_column].dt.date)[selected_metric]
            .sum()
            .reset_index(name=selected_metric)
        )

        # Visualisasi interaktif
        st.line_chart(
            daily_counts.set_index(selected_date_column)[selected_metric],
            use_container_width=True
        )

        # Pilihan model (dummy parameter untuk UI)
        model_type = st.radio('Pilih Model', ['ARIMA', 'Prophet', 'LSTM'])
        if model_type == 'ARIMA':
            p = st.slider('Order (p)', 0, 10, 5)
            q = st.slider('Order (q)', 0, 10, 5)
            st.caption(f'ARIMA Order dipilih: p={p}, q={q}')
        elif model_type == 'Prophet':
            st.caption("Prophet default setting (belum diimplementasi).")
        elif model_type == 'LSTM':
            st.caption("LSTM (deep learning) coming soon!")

        # Tombol AI Insight
        if st.button("Minta Insight Prediksi AI (Gemini)"):
            preview_data = daily_counts.tail(14).to_markdown(index=False)
            with st.spinner("Meminta insight ke Gemini..."):
                insight = generate_time_series_insights(preview_data)
                st.markdown("### 📊 Insight Gemini:")
                st.write(insight)
        
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
        
        # Feedback
        with st.expander("Berikan Saran untuk Fitur Forecasting"):
            feedback = st.text_area("Apa yang Anda harapkan dari fitur forecasting?")
            if st.button("Kirim Saran"):
                st.success("Terima kasih atas sarannya! Kami akan mempertimbangkan untuk pengembangan fitur ini.")

    else:
        st.warning("Silakan upload data untuk melihat contoh visualisasi prediksi")
        st.image("https://via.placeholder.com/800x400?text=Upload+Data+Untuk+Melihat+Contoh+Prediksi", use_column_width=True)
