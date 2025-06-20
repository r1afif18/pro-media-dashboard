import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from gemini_engine import gemini_engine  # Pastikan modul ini sudah ada

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
            # Konversi tanggal dan buat data harian
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            df['date_only'] = df['date'].dt.strftime('%Y-%m-%d')  # Simpan sebagai string
            daily_counts = df.groupby('date_only').size().reset_index(name='count')
            daily_counts = daily_counts.sort_values('date_only')
            
            # Input parameter forecasting
            st.subheader("⚙️ Parameter Proyeksi")
            col1, col2 = st.columns(2)
            with col1:
                forecast_days = st.slider("Hari ke Depan", 1, 30, 7)
            with col2:
                analysis_depth = st.slider("Kedalaman Analisis", 7, 90, 30)
            
            # Analisis tren real-time
            st.subheader("📈 Analisis Tren Real-Time")
            
            # Hitung moving average
            daily_counts['7_day_avg'] = daily_counts['count'].rolling(window=7, min_periods=1).mean()
            
            # Visualisasi tren
            fig_trend = px.line(
                daily_counts.tail(analysis_depth),
                x='date_only',
                y=['count', '7_day_avg'],
                title=f'Tren Jumlah Berita ({analysis_depth} Hari Terakhir)',
                labels={'date_only': 'Tanggal', 'value': 'Jumlah Berita'},
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
            
            if st.button("Buat Proyeksi & Analisis Strategi", use_container_width=True):
                with st.spinner("Menganalisis data dan membuat proyeksi..."):
                    try:
                        # Ambil data terbaru
                        last_7_days = daily_counts.tail(7)
                        avg_last_7_days = last_7_days['count'].mean()
                        
                        # Buat proyeksi
                        projections = [avg_last_7_days] * forecast_days
                        
                        # Buat tanggal prediksi
                        last_date = datetime.strptime(daily_counts['date_only'].iloc[-1], '%Y-%m-%d')
                        future_dates = [
                            (last_date + pd.DateOffset(days=i)).strftime('%Y-%m-%d') 
                            for i in range(1, forecast_days+1)
                        ]
                        
                        # Buat dataframe untuk visualisasi
                        history_df = daily_counts.tail(30)[['date_only', 'count']].rename(columns={
                            'date_only': 'date',
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
                        
                        # Analisis pola harian
                        st.subheader("📊 Analisis Pola")
                        
                        if len(daily_counts) > 0:
                            # Gunakan kolom tanggal asli untuk analisis pola
                            daily_counts['date_dt'] = pd.to_datetime(daily_counts['date_only'])
                            daily_counts['day_of_week'] = daily_counts['date_dt'].dt.day_name()
                            
                            weekday_avg = daily_counts.groupby('day_of_week')['count'].mean().reset_index()
                            
                            # Urutkan hari secara manual
                            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                            weekday_avg['day_order'] = weekday_avg['day_of_week'].map({day: i for i, day in enumerate(day_order)})
                            weekday_avg = weekday_avg.sort_values('day_order')
                            
                            fig_weekday = px.bar(
                                weekday_avg,
                                x='day_of_week',
                                y='count',
                                title='Rata-rata Jumlah Berita per Hari dalam Minggu',
                                labels={'day_of_week': 'Hari', 'count': 'Rata-rata Berita'},
                                color='count',
                                color_continuous_scale='Blues'
                            )
                            
                            st.plotly_chart(fig_weekday, use_container_width=True)
                        
                        # Rekomendasi strategi oleh AI
                        st.subheader("💡 Rekomendasi Strategi oleh AI")
                        
                        # Siapkan data untuk Gemini
                        trend_data = daily_counts.tail(30).to_dict(orient='records')
                        projection_data = projection_display.to_dict(orient='records')
                        weekday_data = weekday_avg.to_dict(orient='records')
                        
                        # Prompt untuk Gemini
                        prompt = f"""
                        Saya memiliki data berita dengan informasi berikut:
                        - Tren 30 hari terakhir: {trend_data[-3:]}
                        - Proyeksi {forecast_days} hari ke depan: {projection_data}
                        - Rata-rata berita per hari: {weekday_data}
                        
                        Berikan rekomendasi strategi manajemen konten yang spesifik dan dapat ditindaklanjuti 
                        dalam format markdown dengan 4 poin utama, fokus pada:
                        1. Optimalisasi produksi konten
                        2. Strategi distribusi berdasarkan pola harian
                        3. Persiapan untuk fluktuasi permintaan
                        4. Analisis kompetitif
                        
                        Gunakan angka dan data spesifik dari analisis di atas.
                        """
                        
                        # Dapatkan rekomendasi dari Gemini
                        recommendation = gemini_engine.ask(prompt, pd.DataFrame())
                        st.markdown(recommendation)
                        
                        # Simpan rekomendasi di session state
                        st.session_state.last_recommendation = recommendation
                        
                    except Exception as e:
                        st.error(f"Terjadi kesalahan dalam membuat proyeksi: {str(e)}")
            
            # Tampilkan rekomendasi terakhir jika ada
            if 'last_recommendation' in st.session_state:
                st.subheader("💡 Rekomendasi Strategi Terakhir")
                st.markdown(st.session_state.last_recommendation)
            
            # Statistik real-time
            st.subheader("📊 Statistik Real-Time")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Rata-rata Harian", f"{daily_counts['count'].mean():.1f}")
            col2.metric("Maksimum Harian", daily_counts['count'].max())
            col3.metric("Minimum Harian", daily_counts['count'].min())
            
            # Tren 7 hari terakhir
            last_7_days = daily_counts.tail(7)
            fig_last_7 = px.bar(
                last_7_days,
                x='date_only',
                y='count',
                title='7 Hari Terakhir',
                labels={'date_only': 'Tanggal', 'count': 'Jumlah Berita'},
                color='count',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_last_7, use_container_width=True)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam memproses data: {str(e)}")
