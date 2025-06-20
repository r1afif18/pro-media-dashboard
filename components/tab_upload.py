import streamlit as st
import pandas as pd
from data_processor import process_upload, generate_template

def show(tab):
    with tab:
        st.header("📤 Upload & Eksplorasi Data")
        
        # Download template button
        template_df = generate_template()
        st.download_button(
            label="📥 Download Template CSV",
            data=template_df.to_csv(index=False).encode('utf-8'),
            file_name="template_berita.csv",
            mime="text/csv"
        )
        
        # File uploader
        uploaded_file = st.file_uploader("Upload file data berita (CSV atau Excel)", type=["csv", "xlsx", "xls"])
        
        if uploaded_file is not None:
            # Process uploaded file
            df, error = process_upload(uploaded_file)
            
            if error:
                st.error(f"Error: {error}")
            else:
                st.session_state.df = df
                st.success("✅ Data berhasil diupload!")
                
                # Show data preview
                st.subheader("Preview Data")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Show data summary
                st.subheader("Statistik Data")
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Berita", len(df))
                col2.metric("Sumber Berita", df['source'].nunique())
                
                if 'date' in df.columns:
                    min_date = df['date'].min().strftime('%d %b %Y')
                    max_date = df['date'].max().strftime('%d %b %Y')
                    col3.metric("Rentang Tanggal", f"{min_date} - {max_date}")
