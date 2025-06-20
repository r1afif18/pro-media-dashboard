import streamlit as st
import pandas as pd
import utils

def show(tab):
    with tab:
        st.markdown("""
        <div class="section">
            <h2 class="section-title">📤 Data Management</h2>
            <p>Upload dan kelola dataset berita untuk analisis</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Download template
        st.markdown("""
        <div class="card">
            <div class="card-title">📥 Data Template</div>
            <p>Download template berikut untuk memastikan format data sesuai</p>
        """, unsafe_allow_html=True)
        
        template_df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'title': ['Contoh Judul Berita 1', 'Contoh Judul Berita 2'],
            'sentiment': ['Positif', 'Netral'],
            'source': ['Media Satu', 'Media Dua'],
            'content': ['Isi berita pertama...', 'Isi berita kedua...']
        })
        
        csv_data = template_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Template CSV",
            data=csv_data,
            file_name="template_berita.csv",
            mime="text/csv"
        )
        st.markdown("</div>", unsafe_allow_html=True)  # Close card
        
        # File uploader
        st.markdown("""
        <div class="card">
            <div class="card-title">📁 Upload Data</div>
            <p>Upload file data berita (CSV atau Excel)</p>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Pilih file",
            type=["csv", "xlsx", "xls"],
            help="Maksimal ukuran file: 200MB",
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Process uploaded file
            df, error = utils.process_upload(uploaded_file)
            
            if error:
                st.error(f"❌ Error: {error}")
            else:
                st.session_state.df = df
                st.session_state.data_profile = utils.generate_data_profile(df)
                st.success("✅ Data berhasil diupload!")
                
                # Show data preview
                st.markdown("""
                <div class="card">
                    <div class="card-title">👀 Data Preview</div>
                """, unsafe_allow_html=True)
                
                st.dataframe(df.head(10), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)  # Close card
                
                # Show data summary
                st.markdown("""
                <div class="card">
                    <div class="card-title">📊 Data Summary</div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Berita", len(df))
                col2.metric("Sumber Berita", df['source'].nunique())
                
                if 'date' in df.columns:
                    min_date = df['date'].min().strftime('%d %b %Y')
                    max_date = df['date'].max().strftime('%d %b %Y')
                    col3.metric("Rentang Tanggal", f"{min_date} - {max_date}")
                
                st.markdown("</div>", unsafe_allow_html=True)  # Close card
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close card
