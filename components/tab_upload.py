import streamlit as st
import pandas as pd
from datetime import datetime
import data_processor

def show():
    st.header("📤 Upload & Eksplorasi Data")
    
    # Upload file
    uploaded_file = st.file_uploader(
        "Upload file data berita (CSV atau Excel)",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=False
    )
    
    # Template download
    with st.expander("📥 Download Template CSV"):
        st.info("Gunakan template ini untuk memastikan format data sesuai")
        template_df = data_processor.generate_template()
        st.dataframe(template_df)
        st.download_button(
            label="Download Template CSV",
            data=template_df.to_csv(index=False).encode('utf-8'),
            file_name='template_berita.csv',
            mime='text/csv'
        )
    
    if uploaded_file is not None:
        # Proses file
        with st.spinner("Memproses file..."):
            df, error_message = data_processor.process_upload(uploaded_file)
            
        if error_message:
            st.error(f"❌ {error_message}")
            return
            
        # Simpan ke session state
        st.session_state.df = df
        st.session_state.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.success("✅ Data berhasil diupload!")
        
        # Tampilkan preview
        st.subheader("Preview Data")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Tampilkan statistik
        st.subheader("Statistik Data")
        col1, col2, col3 = st.columns(3)
        col1.metric("Jumlah Berita", len(df))
        col2.metric("Rentang Tanggal", 
                    df['date'].min().strftime('%d/%m/%Y'), 
                    df['date'].max().strftime('%d/%m/%Y'))
        col3.metric("Sumber Berita", df['source'].nunique())
        
        # Filter sederhana
        st.subheader("Eksplorasi Data")
        col1, col2 = st.columns(2)
        
        with col1:
            date_range = st.date_input(
                "Rentang Tanggal",
                value=[df['date'].min(), df['date'].max()],
                min_value=df['date'].min(),
                max_value=df['date'].max()
            )
            
        with col2:
            sentiment_options = st.multiselect(
                "Filter Sentimen",
                options=df['sentiment'].unique(),
                default=df['sentiment'].unique()
            )
        
        # Terapkan filter
        filtered_df = df[
            (df['date'].dt.date >= date_range[0]) & 
            (df['date'].dt.date <= date_range[1]) &
            (df['sentiment'].isin(sentiment_options))
        ]
        
        st.metric("Jumlah Berita Terfilter", len(filtered_df))
        st.dataframe(filtered_df, use_container_width=True)
        
    else:
        st.info("Silakan upload file CSV atau Excel untuk memulai analisis")
