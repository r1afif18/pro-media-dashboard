import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import timedelta

def show():
    st.header("🔮 Forecasting")

    # Placeholder info
    st.info("""
    **Fitur dalam Pengembangan**  
    Versi berikutnya akan menyertakan prediksi tren menggunakan:
    - Analisis deret waktu (Time Series Analysis)
    - Model ARIMA/Prophet
    - Integrasi dengan Gemini untuk prediksi kualitatif
    """)

    # Pastikan data sudah di-upload
    if 'df' not in st.session_state or st.session_state.df is None:
        st.warning("📁 Silakan upload data untuk melihat forecasting", icon="⚠️")
        return

    df = st.session_state.df.copy()

    # --- 1) Pilih kolom tanggal & filter rentang waktu ---
    selected_date_column = st.selectbox('Pilih Kolom Tanggal', df.columns)
    df[selected_date_column] = pd.to_datetime(df[selected_date_column])
    start_date = st.date_input('Tanggal Mulai', value=df[selected_date_column].min())
    end_date   = st.date_input('Tanggal Akhir', value=df[selected_date_column].max())
    mask = (df[selected_date_column] >= pd.to_datetime(start_date)) & (df[selected_date_column] <= pd.to_datetime(end_date))
    df_range = df.loc[mask]
    if df_range.empty:
        st.warning("Rentang tanggal tidak memiliki data")
        return

    # --- 2) Agregasi per hari ---
    df_range['date_only'] = df_range[selected_date_column].dt.date
    daily_counts = df_range.groupby('date_only').size().reset_index(name='count')

    # --- 3) Pilih metrik numerik ---
    metric_cols = [
        col for col in df.columns
        if col != selected_date_column and pd.api.types.is_numeric_dtype(df[col])
    ]
    options = ['Jumlah Data per Hari'] + metric_cols
    selected_metric = st.selectbox("Pilih Kolom Metrik (opsional)", options, index=0)

    # --- 4) Pilih model & parameter ---
    model_type = st.radio('Pilih Model', ['ARIMA', 'Prophet', 'LSTM'])
    if model_type == 'ARIMA':
        p = st.slider('Order ARIMA (p)', 0, 10, 1)
        q = st.slider('Order ARIMA (q)', 0, 10, 1)
    # (Untuk Prophet / LSTM bisa ditambahkan parameter di sini)

    # --- 5) Horizon prediksi & tombol eksekusi ---
    periods = st.number_input('Jumlah Hari Prediksi', min_value=1, max_value=30, value=7)
    if st.button("Jalankan Forecast"):
        with st.spinner("Memprediksi..."):
            last_date = daily_counts['date_only'].max()
            # Dummy prediksi acak (nanti ganti dengan ARIMA/Prophet/LSTM sungguhan)
            future_dates = pd.date_range(
                start=pd.to_datetime(last_date) + timedelta(days=1),
                periods=periods, freq='D'
            ).date.tolist()
            # Pilih data aktual vs prediksi sesuai metrik
            if selected_metric == 'Jumlah Data per Hari':
                actual = daily_counts.copy()
                actual['type'] = 'Aktual'
                mean_val = actual['count'].mean()
                preds = np.random.randint(int(mean_val*0.8), int(mean_val*1.2), size=periods)
                pred_df = pd.DataFrame({
                    'date_only': future_dates,
                    'count': preds,
                    'type': 'Prediksi'
                })
                forecast_df = pd.concat([actual, pred_df], ignore_index=True)
                y_col = 'count'
                y_label = 'Jumlah Data'
            else:
                agg = df_range.groupby('date_only')[selected_metric]\
                              .sum().reset_index(name='count')
                agg['type'] = 'Aktual'
                mean_val = agg['count'].mean()
                preds = np.random.randint(int(mean_val*0.8), int(mean_val*1.2), size=periods)
                pred_df = pd.DataFrame({
                    'date_only': future_dates,
                    'count': preds,
                    'type': 'Prediksi'
                })
                forecast_df = pd.concat([agg, pred_df], ignore_index=True)
                y_col = 'count'
                y_label = selected_metric

            # Plot dengan Plotly
            forecast_df['date_only'] = pd.to_datetime(forecast_df['date_only'])
            fig = px.line(
                forecast_df,
                x='date_only',
                y=y_col,
                color='type',
                title='Forecast vs Actual',
                labels={'date_only': 'Tanggal', y_col: y_label},
                line_dash='type'
            )
            # Garis vertikal pemisah
            fig.add_shape(
                type="line",
                x0=last_date,
                y0=0,
                x1=last_date,
                y1=forecast_df[y_col].max() * 1.1,
                line=dict(color="red", dash="dash"),
            )
            fig.add_annotation(
                x=last_date,
                y=forecast_df[y_col].max() * 1.15,
                text="Mulai Prediksi",
                showarrow=False,
                font=dict(color="red")
            )
            st.plotly_chart(fig, use_container_width=True)

    # --- 6) Visualisasi interaktif bawaan Streamlit ---
    st.subheader("Visualisasi Interaktif (Streamlit)")
    if selected_metric == 'Jumlah Data per Hari':
        chart_series = daily_counts.set_index('date_only')['count']
        st.caption("Jumlah data per hari")
    else:
        agg_series = df_range.groupby(df_range['date_only'])[selected_metric].sum()
        st.caption(f"{selected_metric} per hari")
        chart_series = agg_series
    st.line_chart(chart_series, use_container_width=True)

    # --- 7) Timeline & Feedback ---
    st.divider()
    st.subheader("Timeline Pengembangan")
    timeline_data = {
        "Fitur": ["Integrasi Prediksi Sungguhan", "Optimasi Performa", "UI/UX Improvement", "Testing & Deployment"],
        "Status": ["Dalam Pengembangan", "Belum Dimulai", "Belum Dimulai", "Belum Dimulai"],
        "Progress": [75, 0, 0, 0]
    }
    timeline_df = pd.DataFrame(timeline_data)
    st.dataframe(timeline_df, use_container_width=True)

    with st.expander("Berikan Saran untuk Fitur Forecasting"):
        feedback = st.text_area("Apa yang Anda harapkan dari fitur forecasting?")
        if st.button("Kirim Saran"):
            st.success("Terima kasih atas sarannya! 🙏")

