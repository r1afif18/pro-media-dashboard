import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from gemini_engine import gemini_engine
import logging

logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.header("🔮 AI Forecasting & Strategi - Analisis Tren Berita")
        st.info("Forecasting di sini menggunakan Google Gemini AI untuk memproyeksikan tren masa depan dari data historis!")

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

        # Proses & visualisasi data historis
        try:
            df_clean = df.copy()
            df_clean[date_column] = pd.to_datetime(df_clean[date_column], errors='coerce')
            df_clean = df_clean.dropna(subset=[date_column])

            # Generate period column
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

            # Forecasting dengan AI
            st.subheader("🔮 Proyeksi Masa Depan (AI)")
            st.info("Forecast dihasilkan otomatis oleh Gemini AI, berbasis data historis.")

            # Build prompt data ringkas (biar AI tidak overload token)
            ringkas = df_agg[[ 'period', metric_column ]].copy()
            ringkas['period'] = ringkas['period'].astype(str)
            data_table = ringkas.tail(30).to_csv(index=False)

            prompt = f"""
Data berikut adalah tren '{metric_column}' dari dataset media. 
Kolom 'period' menyatakan tanggal, '{metric_column}' adalah nilainya.

Tampilkan prediksi {forecast_periods} periode ke depan ({time_window.lower()}), 
berikan nilai estimasi tiap periode dalam bentuk tabel.
- Kolom: periode_prediksi, nilai_prediksi
- Prediksi berbasis pola historis data.
- Hanya tampilkan tabel tanpa penjelasan narasi.
- Periode awal proyeksi = setelah data terakhir berikut:

{data_table}
            
             """

            if st.button("Buat Prediksi AI", use_container_width=True):
                with st.spinner("Meminta prediksi ke Google Gemini..."):
                    result = gemini_engine.ask(prompt, df_agg)
                    # Gemini akan membalas tabel markdown, konversi ke DataFrame jika bisa
                    # Coba auto-parse markdown tabel
                    import re
                    import io

                    # Ambil tabel markdown saja dari result
                    md_table = None
                    match = re.search(r"\|.*\|\n\|[-\s|]+\|\n([\s\S]+?)\n\n", result)
                    if match:
                        md_table = "|periode_prediksi|nilai_prediksi|\n|---|---|\n" + match.group(1)
                    else:
                        md_table = result

                    try:
                        import pandas as pd
                        df_pred = pd.read_csv(io.StringIO(md_table.replace('|', ',')), header=1)
                        st.dataframe(df_pred, use_container_width=True)
                        # Plot proyeksi AI
                        if 'periode_prediksi' in df_pred.columns and 'nilai_prediksi' in df_pred.columns:
                            st.line_chart(
                                df_pred.set_index('periode_prediksi')['nilai_prediksi']
                            )
                    except Exception:
                        st.markdown(result)

                    # AI STRATEGY RECOMMENDATION
                    st.subheader("💡 Rekomendasi Strategi oleh AI")
                    prompt2 = f"""
Berdasarkan data historis dan hasil proyeksi AI, berikan saran singkat (maks 5 poin) strategi untuk manajemen dan distribusi konten media, berbasis tren {metric_column} ke depan.
"""
                    rekomendasi = gemini_engine.ask(prompt2, df_agg)
                    st.markdown(rekomendasi)

        except Exception as e:
            st.error("⚠️ Terjadi kesalahan dalam analisis: {}".format(str(e)))
            logger.exception("Forecasting error")
