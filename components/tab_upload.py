import streamlit as st
import pandas as pd
import utils
from io import BytesIO

def show(tab):
    with tab:
        st.header("📤 Upload & Eksplorasi Data")
        
        # Download template
        st.subheader("Template Data")
        st.markdown("Download template untuk memastikan format data sesuai")
        template_df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'title': ['Contoh Judul Berita 1', 'Contoh Judul Berita 2'],
            'sentiment': ['Positif', 'Netral'],
            'source': ['Media Satu', 'Media Dua'],
            'content': ['Isi berita pertama...', 'Isi berita kedua...']
        })
        
        # Download button
        csv_data = template_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Template CSV",
            data=csv_data,
            file_name="template_berita.csv",
            mime="text/csv"
        )
        
        # File uploader
        st.subheader("Upload Data")
        uploaded_file = st.file_uploader(
            "Upload file data berita (CSV atau Excel)",
            type=["csv", "xlsx", "xls"],
            help="Maksimal ukuran file: 200MB"
        )
        
        if uploaded_file is not None:
            try:
                # Read file
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # Clean and validate data
                df = utils.validate_and_clean_data(df)
                
                # Save to session
                st.session_state.df = df
                st.session_state.data_profile = utils.generate_data_profile(df)
                st.success("✅ Data berhasil diupload dan divalidasi!")
                
                # Data preview
                st.subheader("Preview Data")
                st.dataframe(df.head(10), 
                            use_container_width=True,
                            column_config={
                                "date": st.column_config.DateColumn("Tanggal"),
                                "title": "Judul",
                                "source": "Sumber",
                                "sentiment": "Sentimen"
                            })
                
                # Data profile
                st.subheader("Profil Data")
                profile = st.session_state.data_profile
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Berita", profile['total_news'])
                col2.metric("Sumber Unik", len(profile['sources']))
                if profile['date_range']:
                    col3.metric("Rentang Tanggal", 
                               f"{profile['date_range']['min']} - {profile['date_range']['max']}")
                
                # Show top sources
                if profile['sources']:
                    st.markdown("**Top Sumber Berita**")
                    source_df = pd.DataFrame({
                        'Sumber': list(profile['sources'].keys()),
                        'Jumlah': list(profile['sources'].values())
                    })
                    st.dataframe(source_df, hide_index=True, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.df = None
