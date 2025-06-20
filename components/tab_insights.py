import streamlit as st
from datetime import datetime
from database import save_custom_insight, get_custom_insights, delete_custom_insight

def show(tab):
    with tab:
        st.header("💡 Insights Custom")
        
        # Form to create new insight
        with st.form("insight_form", clear_on_submit=True):
            st.subheader("Buat Insight Baru")
            insight_title = st.text_input("Judul Insight*")
            insight_content = st.text_area("Deskripsi Insight*", height=200)
            tags = st.text_input("Tags (pisahkan dengan koma)")
            
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
        
        # Display saved insights
        st.subheader("Insights Tersimpan")
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
                        st.rerun()
