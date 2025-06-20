import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from gemini_engine import gemini_engine

def show(tab):
    with tab:
        st.header("🔮 Forecasting & Strategi - Analisis Tren Berita")
        
        # Cek jika data sudah diupload
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return
            
        df = st.session_state.df.copy()
        
        # Pastikan kolom tanggal ada
        if 'date' not in df.columns:
            st.error("Data tidak memiliki kolom tanggal ('date') untuk forecasting")
            return
            
        try:
            # Konversi tanggal dengan penanganan error yang lebih ketat
            df['date'] = pd.to_datetime(df['date'], errors='coerce', format='%Y-%m-%d')
            invalid_dates = df[df['date'].isna()]
            
            if not invalid_dates.empty:
                st.warning(f"Ditemukan {len(invalid_dates)} baris dengan format tanggal tidak valid. Baris ini akan diabaikan.")
            
            df = df.dropna(subset=['date'])
            
            # Pastikan ada data yang valid
            if len(df) == 0:
                st.error("Tidak ada data tanggal yang valid untuk dianalisis")
                return
            
            # Ekstrak tanggal sebagai string dengan format konsisten
            df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
            daily_counts = df.groupby('date_str').size().reset_index(name='count')
            daily_counts = daily_counts.sort_values('date_str')
            
            # Debug: Tampilkan tipe data
            st.session_state.daily_counts = daily_counts
            
            # Input parameter forecasting
            st.subheader("⚙️ Parameter Proyeksi")
            col1, col2 = st.columns(2)
            with col1:
                forecast_days = st.slider("Hari ke Depan", 1, 30, 7)
            with col2:
                analysis_depth = st.slider("Kedalaman Analisis (hari)", 7, 90, 30)
            
            # Analisis tren real-time
            st.subheader("📈 Analisis Tren Real-Time")
            
            # Hitung moving average
            daily_counts['7_day_avg'] = daily_counts['count'].rolling(window=7, min_periods=1).mean()
            
            # Visualisasi tren
            fig_trend = px.line(
                daily_counts.tail(analysis_depth),
                x='date_str',
                y=['count', '7_day_avg'],
                title=f'Tren Jumlah Berita ({analysis_depth} Hari Terakhir)',
                labels={'date_str': 'Tanggal', 'value': 'Jumlah Berita'},
                color_discrete_map={'count': '#1f77b4', '7_day_avg': '#ff7f0e'}
            )
            
            fig_trend.update_layout(
                legend_title_text='',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis=dict(tickangle=45)
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Proyeksi sederhana
            st.subheader("🔮 Proyeksi Masa Depan")
            
            if st.button("Buat Proyeksi & Analisis Strategi", use_container_width=True, key="forecast_btn"):
                with st.spinner("Menganalisis data dan membuat proyeksi..."):
                    try:
                        # Pastikan ada cukup data
                        if len(daily_counts) < 7:
                            st.error("Minimal 7 hari data diperlukan untuk membuat proyeksi")
                            return
                            
                        # Ambil data terbaru
                        last_7_days = daily_counts.tail(7)
                        avg_last_7_days = last_7_days['count'].mean()
                        
                        # SOLUSI UTAMA: Tangani tanggal dengan sangat hati-hati
                        # Dapatkan tanggal terakhir sebagai string
                        last_date_str = daily_counts['date_str'].iloc[-1]
                        
                        # Konversi ke objek datetime dengan format eksplisit
                        last_date = datetime.strptime(last_date_str, '%Y-%m-%d')
                        
                        # Buat tanggal prediksi
                        future_dates = []
                        for i in range(1, forecast_days + 1):
                            # Gunakan timedelta dari modul datetime
                            next_date = last_date + pd.DateOffset(days=i)
                            
                            # Konversi ke string dengan format konsisten
                            future_dates.append(next_date.strftime('%Y-%m-%d'))
                        
                        # Buat proyeksi
                        projections = [avg_last_7_days] * forecast_days
                        
                        # Buat dataframe untuk visualisasi
                        history_df = daily_counts.tail(30)[['date_str', 'count']].rename(columns={
                            'date_str': 'date',
                            'count': 'value'
                        })
                        history_df['type'] = 'Aktual'
                        
                        projection_df = pd.DataFrame({
                            'date': future_dates,
                            'value': projections,
                            'type': 'Proyeksi'
                        })
                        
                        combined_df = pd.concat([history_df, projection_df])
                        
                        # Buat visualisasi proyeksi
                        fig_projection = px.line(
                            combined_df,
                            x='date',
                            y='value',
                            color='type',
                            title=f'Proyeksi Jumlah Berita {forecast_days} Hari ke Depan',
                            labels={'date': 'Tanggal', 'value': 'Jumlah Berita'},
                            color_discrete_map={'Aktual': '#1f77b4', 'Proyeksi': '#ff7f0e'}
                        )
                        
                        # Tambahkan garis pembatas
                        fig_projection.add_vline(
                            x=history_df['date'].iloc[-1],
                            line_dash="dash",
                            line_color="green",
                            annotation_text="Mulai Proyeksi"
                        )
                        
                        # Tambahkan anotasi
                        fig_projection.add_annotation(
                            x=0.05,
                            y=0.95,
                            xref="paper",
                            yref="paper",
                            text=f"Proyeksi: {int(avg_last_7_days)} berita/hari",
                            showarrow=False,
                            bgcolor="white",
                            bordercolor="black",
                            borderwidth=1
                        )
                        
                        fig_projection.update_layout(xaxis=dict(tickangle=45))
                        st.plotly_chart(fig_projection, use_container_width=True)
                        
                        # Tampilkan detail proyeksi
                        st.subheader("Detail Proyeksi")
                        projection_display = projection_df.copy()
                        projection_display['value'] = projection_display['value'].round().astype(int)
                        projection_display = projection_display.rename(columns={
                            'date': 'Tanggal',
                            'value': 'Jumlah Berita Proyeksi'
                        }).reset_index(drop=True)
                        
                        st.dataframe(projection_display, use_container_width=True)
                        
                        # Rekomendasi strategi oleh AI
                        st.subheader("💡 Rekomendasi Strategi oleh AI")
                        
                        # Siapkan data untuk Gemini
                        data_for_ai = {
                            "tren_terakhir": daily_counts.tail(7).to_dict('records'),
                            "proyeksi": projection_display.to_dict('records'),
                            "rata_harian": daily_counts['count'].mean(),
                            "max_harian": daily_counts['count'].max(),
                            "min_harian": daily_counts['count'].min()
                        }
                        
                        # Prompt untuk Gemini
                        prompt = f"""
                        [INSTRUKSI]
                        Berikan rekomendasi strategi manajemen konten berdasarkan data berikut:
                        {data_for_ai}
                        
                        [FORMAT]
                        1. 🎯 Optimalisasi Produksi Konten
                        2. 📊 Strategi Distribusi 
                        3. ⚠️ Persiapan Fluktuasi
                        4. 🔍 Analisis Kompetitif
                        
                        Gunakan data spesifik dan berikan saran praktis.
                        """
                        
                        # Dapatkan rekomendasi dari Gemini
                        recommendation = gemini_engine.ask(prompt, pd.DataFrame())
                        st.markdown(recommendation)
                        
                        # Simpan rekomendasi
                        st.session_state.last_recommendation = recommendation
                        
                    except Exception as e:
                        st.error(f"Terjadi kesalahan dalam membuat proyeksi: {str(e)}")
                        # Tampilkan informasi debugging
                        st.error("Informasi Debugging:")
                        st.error(f"Tipe last_date_str: {type(last_date_str)}")
                        st.error(f"Nilai last_date_str: {last_date_str}")
                        if 'last_date' in locals():
                            st.error(f"Tipe last_date: {type(last_date)}")
        
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam memproses data: {str(e)}")
