import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show(tab):
    with tab:
        st.header("🔮 Forecasting - Proyeksi Tren Berita")
        
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
            # Konversi tanggal dan buat data harian (tanpa operasi timestamp kompleks)
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            
            # Ekstrak tanggal saja sebagai string (YYYY-MM-DD)
            df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
            daily_counts = df.groupby('date_str').size().reset_index(name='count')
            daily_counts = daily_counts.sort_values('date_str')
            
            # Input parameter forecasting
            st.subheader("⚙️ Parameter Proyeksi")
            forecast_days = st.slider("Hari ke Depan yang Diproyeksikan", 1, 30, 7)
            
            # Analisis tren sederhana
            st.subheader("📈 Analisis Tren")
            
            # Hitung moving average 7 hari (tanpa operasi tanggal)
            daily_counts['7_day_avg'] = daily_counts['count'].rolling(window=7, min_periods=1).mean()
            
            # Visualisasi tren
            fig_trend = px.line(
                daily_counts,
                x='date_str',
                y=['count', '7_day_avg'],
                title='Tren Jumlah Berita Harian',
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
            
            if st.button("Buat Proyeksi", use_container_width=True):
                with st.spinner("Membuat proyeksi tren..."):
                    try:
                        # Ambil data terbaru (tanpa operasi timestamp)
                        last_7_days = daily_counts.tail(7)
                        avg_last_7_days = last_7_days['count'].mean()
                        
                        # Buat tanggal prediksi sebagai string
                        last_date = pd.to_datetime(daily_counts['date_str'].iloc[-1])
                        future_dates = [
                            (last_date + pd.DateOffset(days=i)).strftime('%Y-%m-%d') 
                            for i in range(1, forecast_days+1)
                        ]
                        
                        # Buat proyeksi
                        projections = [avg_last_7_days] * forecast_days
                        
                        # Buat dataframe untuk visualisasi
                        history_df = daily_counts[['date_str', 'count']].rename(columns={
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
                        
                        # Buat visualisasi
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
                        last_actual_date = history_df['date'].iloc[-1]
                        fig_projection.add_vline(
                            x=last_actual_date,
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
                        projection_df['value'] = projection_df['value'].round().astype(int)
                        projection_df = projection_df.rename(columns={
                            'date': 'Tanggal',
                            'value': 'Jumlah Berita Proyeksi'
                        }).reset_index(drop=True)
                        
                        st.dataframe(projection_df, use_container_width=True)
                        
                        # Interpretasi
                        st.subheader("Interpretasi Proyeksi")
                        st.markdown(f"""
                        Berdasarkan analisis tren sederhana:
                        - **Rata-rata 7 hari terakhir**: {int(avg_last_7_days)} berita/hari
                        - **Proyeksi harian**: {int(avg_last_7_days)} berita
                        - **Total proyeksi {forecast_days} hari**: {int(avg_last_7_days * forecast_days)} berita
                        
                        Proyeksi ini didasarkan pada rata-rata jumlah berita dalam 7 hari terakhir. 
                        """)
                        
                    except Exception as e:
                        st.error(f"Terjadi kesalahan dalam membuat proyeksi: {str(e)}")
            
            # Analisis pola harian (tanpa operasi timestamp)
            st.subheader("📊 Analisis Pola")
            
            if len(daily_counts) > 0:
                # Gunakan kolom tanggal asli untuk analisis pola
                daily_counts['date'] = pd.to_datetime(daily_counts['date_str'])
                daily_counts['day_of_week'] = daily_counts['date'].dt.day_name()
                
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
            
            # Rekomendasi strategi
            st.subheader("💡 Rekomendasi Strategi")
            st.markdown("""
            1. **Fokus pada hari aktif**: Tingkatkan produksi konten di hari Senin-Jumat
            2. **Analisis akhir pekan**: Pantau perbedaan pola berita di hari Sabtu/Minggu
            3. **Siapkan konten cadangan**: Untuk hari dengan aktivitas tinggi
            4. **Bandkan dengan periode sebelumnya**: Lihat pola minggu ke minggu
            """)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam memproses data: {str(e)}")
