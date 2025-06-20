import streamlit as st
from database import save_custom_insight, get_custom_insights, delete_custom_insight
import utils

def show(tab):
    with tab:
        st.markdown("""
        <div class="section">
            <h2 class="section-title">💡 Insights Repository</h2>
            <p>Simpan dan kelola insight analitis dari data berita</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form to create new insight
        st.markdown("""
        <div class="card">
            <div class="card-title">➕ Create New Insight</div>
        """, unsafe_allow_html=True)
        
        with st.form("insight_form", clear_on_submit=True):
            insight_title = st.text_input("Judul Insight*", placeholder="Contoh: Tren Topik Politik Q3 2024")
            insight_content = st.text_area("Deskripsi Insight*", height=200, 
                                         placeholder="Deskripsi lengkap insight...")
            tags = st.text_input("Tags (pisahkan dengan koma)", 
                                placeholder="politik, tren, 2024")
            
            submitted = st.form_submit_button("Simpan Insight")
            if submitted:
                if insight_title and insight_content:
                    # Save to database
                    save_custom_insight(
                        title=insight_title,
                        content=insight_content,
                        tags=[tag.strip() for tag in tags.split(",")] if tags else []
                    )
                    st.success("Insight berhasil disimpan!")
                else:
                    st.error("Judul dan deskripsi harus diisi")
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close card
        
        # Display saved insights
        st.markdown("""
        <div class="card">
            <div class="card-title">📚 Saved Insights</div>
        """, unsafe_allow_html=True)
        
        insights = get_custom_insights()
        
        if not insights:
            st.info("Belum ada insight yang disimpan")
        else:
            for insight in insights:
                with st.expander(f"{insight['title']} - {insight['created_at']}"):
                    st.markdown(f"**{insight['title']}**")
                    st.write(insight['content'])
                    
                    if insight['tags']:
                        st.caption(f"Tags: {', '.join(insight['tags'])}")
                    
                    if st.button("Hapus", key=f"delete_{insight['id']}"):
                        delete_custom_insight(insight['id'])
                        st.success("Insight dihapus!")
                        st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close card
