import streamlit as st
import pandas as pd
from datetime import datetime
from database import save_custom_insight, get_custom_insights, delete_custom_insight
from gemini_engine import gemini_engine
import utils
import time

def show(tab):
    with tab:
        st.header("💡 Insights Custom")
        st.markdown("Simpan, kelola, dan hasilkan insight dari data berita")
        
        # Data status
        if 'df' not in st.session_state or st.session_state.df is None:
            st.warning("Upload data terlebih dahulu untuk menghasilkan insights")
            df = None
        else:
            df = st.session_state.df
            profile = st.session_state.get('data_profile', utils.generate_data_profile(df))
            
            # Auto generate insights panel
            st.subheader("AI-Powered Insights")
            st.markdown("Hasilkan insight otomatis menggunakan AI")
            
            insight_types = {
                "Analisis Tren Topik": "Analisis topik yang sedang tren dalam periode tertentu",
                "Perbandingan Sentimen": "Bandingkan sentimen berita antar sumber media",
                "Deteksi Pola Harian": "Identifikasi pola aktivitas harian/mingguan"
            }
            
            col1, col2 = st.columns([3,1])
            with col1:
                insight_topic = st.selectbox(
                    "Pilih jenis insight:",
                    list(insight_types.keys()))
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Generate", key="generate_insight"):
                    with st.spinner("Membuat insight..."):
                        prompt = f"""
                        Buatkan insight tentang '{insight_topic}' berdasarkan data berita dengan karakteristik:
                        - Rentang: {profile['date_range']['min']} hingga {profile['date_range']['max']}
                        - Jumlah berita: {profile['total_news']}
                        - Top sumber: {list(profile['sources'].keys())[:3]}
                        
                        Format:
                        1. **Judul Insight**
                        2. **Deskripsi** (minimal 3 kalimat)
                        3. **Rekomendasi Strategis**
                        """
                        response = gemini_engine.ask(prompt, df)
                        st.session_state.generated_insight = response
            
            if 'generated_insight' in st.session_state:
                st.markdown("### Generated Insight")
                st.markdown(st.session_state.generated_insight)
                
                if st.button("Simpan Insight", key="save_insight"):
                    # Extract title from response
                    lines = st.session_state.generated_insight.split('\n')
                    title = lines[0].replace('**', '').strip() if len(lines) > 0 else "AI Generated Insight"
                    
                    save_custom_insight(
                        title=title,
                        content=st.session_state.generated_insight,
                        tags=["AI Generated", insight_topic]
                    )
                    st.success("Insight disimpan!")
                    del st.session_state.generated_insight
                    st.experimental_rerun()
        
        # Custom insights form
        st.subheader("Buat Insight Custom")
        with st.form("insight_form", clear_on_submit=True):
            title = st.text_input("Judul Insight*", placeholder="Contoh: Peningkatan Topik Politik Q3 2024")
            content = st.text_area("Deskripsi Insight*", height=200, 
                                 placeholder="Deskripsi lengkap insight...")
            tags = st.text_input("Tags (pisahkan dengan koma)", 
                                placeholder="politik, tren, 2024")
            
            submitted = st.form_submit_button("Simpan Insight")
            if submitted:
                if not title or not content:
                    st.error("Judul dan deskripsi wajib diisi")
                else:
                    tag_list = [tag.strip() for tag in tags.split(",")] if tags else []
                    save_custom_insight(title, content, tag_list)
                    st.success("Insight disimpan!")
        
        # Saved insights
        st.subheader("Insights Tersimpan")
        insights = get_custom_insights()
        
        if not insights:
            st.info("Belum ada insight yang disimpan")
        else:
            # Filter by tags
            all_tags = set(tag for insight in insights for tag in insight['tags'])
            selected_tags = st.multiselect("Filter berdasarkan tags", list(all_tags))
            
            # Apply filter
            if selected_tags:
                insights = [i for i in insights if any(tag in selected_tags for tag in i['tags'])]
            
            for insight in insights:
                with st.expander(f"{insight['title']} - {insight['created_at']}"):
                    st.markdown(f"**{insight['title']}**")
                    st.markdown(insight['content'])
                    
                    if insight['tags']:
                        st.caption(f"Tags: {', '.join(insight['tags'])}")
                    
                    if st.button("Hapus", key=f"delete_{insight['id']}"):
                        delete_custom_insight(insight['id'])
                        st.success("Insight dihapus!")
                        time.sleep(0.5)
                        st.experimental_rerun()
