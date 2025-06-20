import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def show(tab):
    with tab:
        st.header("🔮 Forecasting - Proyeksi Tren Berita")
        
        # Cek jika data sudah diupload
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Silakan upload data terlebih dahulu di tab 'Upload Data'")
            return
            
        df = st.session_state.df.copy()
        
        try:
            # Hitung jumlah berita per hari tanpa operasi datetime
            date_counts = df['date'].value_counts().reset_index()
            date_counts.columns = ['date', 'count']
            date_counts = date_counts.sort_values('date')
            
            # Input parameter forecasting
            st.subheader("⚙️ Parameter Proyeksi")
            forecast_days = st.slider("Hari ke Depan yang Diproyeksikan", 1, 30, 7)
            
            # Analisis tren sederhana
            st.subheader("📈 Analisis Tren")
            
            # Hitung moving average 7 hari
            date_counts['7_day_avg'] = date_counts['count'].rolling(window=7, min_periods=1).mean()
            
            # Visualisasi tren
            fig_trend = px.line(
                date_counts,
                x='date',
                y=['count', '7_day_avg'],
                title='Tren Jumlah Berita Harian',
                labels={'date': 'Tanggal', 'value': 'Jumlah Berita'},
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
                        # Ambil data terbaru
                        last_7_days = date_counts.tail(7)
                        avg_last_7_days = last_7_days['count'].mean()
                        
                        # Buat tanggal prediksi sebagai urutan numerik
                        last_idx = len(date_counts) - 1
                        future_idxs = list(range(last_idx + 1, last_idx + forecast_days + 1))
                        
                        # Buat proyeksi
                        projections = [avg_last_7_days] * forecast_days
                        
                        # Buat dataframe untuk visualisasi
                        history_df = date_counts[['date', 'count']].rename(columns={
                            'date': 'Tanggal',
                            'count': 'value'
                        })
                        history_df['type'] = 'Aktual'
                        history_df['index'] = range(len(history_df))
                        
                        projection_df = pd.DataFrame({
                            'Tanggal': [f"Proyeksi Hari {i+1}" for i in range(forecast_days)],
                            'value': projections,
                            'type': 'Proyeksi',
                            'index': future_idxs
                        })
                        
                        combined_df = pd.concat([history_df, projection_df])
                        
                        # Buat visualisasi
                        fig_projection = px.line(
                            combined_df,
                            x='index',
                            y='value',
                            color='type',
                            title=f'Proyeksi Jumlah Berita {forecast_days} Hari ke Depan',
                            labels={'index': 'Urutan Hari', 'value': 'Jumlah Berita'},
                            color_discrete_map={'Aktual': '#1f77b4', 'Proyeksi': '#ff7f0e'}
                        )
                        
                        # Tambahkan garis pembatas
                        fig_projection.add_vline(
                            x=last_idx,
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
                        
                        st.plotly_chart(fig_projection, use_container_width=True)
                        
                        # Tampilkan detail proyeksi
                        st.subheader("Detail Proyeksi")
                        projection_display = projection_df.copy()
                        projection_display['value'] = projection_display['value'].round().astype(int)
                        projection_display = projection_display[['Tanggal', 'value']].rename(columns={
                            'value': 'Jumlah Berita Proyeksi'
                        }).reset_index(drop=True)
                        
                        st.dataframe(projection_display, use_container_width=True)
                        
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
            
            # Analisis pola
            st.subheader("📊 Analisis Pola")
            
            if len(date_counts) > 0:
                # Analisis distribusi
                fig_dist = px.histogram(
                    date_counts,
                    x='count',
                    title='Distribusi Jumlah Berita Harian',
                    labels={'count': 'Jumlah Berita per Hari'},
                    nbins=20
                )
                st.plotly_chart(fig_dist, use_container_width=True)
                
                # Statistik sederhana
                col1, col2, col3 = st.columns(3)
                col1.metric("Rata-rata Harian", f"{date_counts['count'].mean():.1f}")
                col2.metric("Maksimum Harian", date_counts['count'].max())
                col3.metric("Minimum Harian", date_counts['count'].min())
            
            # Rekomendasi strategi
            st.subheader("💡 Rekomendasi Strategi")
            st.markdown("""
            1. **Stabilkan produksi konten** pada level rata-rata harian
            2. **Siapkan konten cadangan** untuk hari dengan aktivitas tinggi
            3. **Analisis penyimpangan** pada hari dengan jumlah berita ekstrim
            4. **Monitor tren mingguan** untuk perencanaan yang lebih baik
            """)
            
        except Exception as e:
            st.error(f"Terjadi kesalahan dalam memproses data: {str(e)}")
