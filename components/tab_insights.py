import streamlit as st
from datetime import datetime

def tab_insights(tab):
    with tab:
        st.header("💡 Insights Custom")
        if 'custom_insights' not in st.session_state:
            st.session_state.custom_insights = []
        with st.form("insight_form"):
            insight_title = st.text_input("Judul Insight*", key="insight_title")
            insight_content = st.text_area("Deskripsi Insight*", key="insight_content")
            submitted = st.form_submit_button("Simpan Insight")
            if submitted and insight_title and insight_content:
                st.session_state.custom_insights.append({
                    "title": insight_title,
                    "content": insight_content,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("Insight berhasil disimpan!")
        if st.session_state.custom_insights:
            st.subheader("Daftar Insight")
            for insight in reversed(st.session_state.custom_insights):
                with st.expander(f"{insight['title']} - {insight['timestamp']}"):
                    st.write(insight['content'])
        else:
            st.info("Belum ada insight.")
