import streamlit as st  # Pastikan impor ini ada
from datetime import datetime
from database import save_custom_insight, get_custom_insights, delete_custom_insight

def show():
    st.header("💡 Insights Custom")
    
    # Inisialisasi jika belum ada
    if 'custom_insights' not in st.session_state:
        st.session_state.custom_insights = []
    
    # Form tambah insight
    with st.form("insight_form"):
        insight_title = st.text_input("Judul Insight*", placeholder="Contoh: Tren Topik Politik Q3 2024")
        insight_content = st.text_area("Deskripsi Insight*", placeholder="Jelaskan insight secara detail...", height=150)
        insight_tags = st.multiselect("Tag/Kategori", ["Politik", "Ekonomi", "Teknologi", "Kesehatan", "Lainnya"])
        submitted = st.form_submit_button("Simpan Insight")
        
        if submitted:
            if insight_title and insight_content:
                # Simpan ke session_state dulu
                new_insight = {
                    "title": insight_title,
                    "content": insight_content,
                    "tags": insight_tags,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.custom_insights.append(new_insight)

                # Simpan ke database jika username tersedia
                if 'username' in st.session_state:
                    save_custom_insight(
                        st.session_state.username,
                        insight_title,
                        insight_content,
                        insight_tags
                    )

                st.success("Insight berhasil disimpan!")
            else:
                st.error("Judul dan deskripsi harus diisi!")
    
    # Ambil insights dari database jika user login
    if 'username' in st.session_state:
        insights = get_custom_insights(st.session_state.username)
    else:
        insights = None
    
    # Tampilkan insights yang diambil dari database atau dari session_state
    if insights:
        st.subheader("Insights dari Database")
        # Filter berdasarkan tag
        all_tags = set()
        for insight in insights:
            all_tags.update(insight.get('tags', []))
        selected_tags = st.multiselect("Filter berdasarkan Tag", list(all_tags))

        for insight in insights:
            if not selected_tags or any(tag in selected_tags for tag in insight.get('tags', [])):
               with st.expander(f"{insight.get('title', 'Untitled')} - {insight.get('timestamp', 'No date')}"):
                    st.markdown("**Deskripsi:**")
                    st.write(insight.get('content', 'No content'))
                    if insight.get('tags'):
                        st.markdown(f"**Tags:** {', '.join(insight['tags'])}")
                    st.caption(f"Ditambahkan pada: {insight.get('timestamp', 'No date')}")
                    if st.button("Hapus", key=f"delete_{insight['id']}"):
                        delete_custom_insight(insight['id'])
                        st.experimental_rerun()
    elif st.session_state.custom_insights:
        st.subheader("Insights dari Session")
        all_tags = set()
        for insight in st.session_state.custom_insights:
            all_tags.update(insight.get('tags', []))
        selected_tags = st.multiselect("Filter berdasarkan Tag", list(all_tags))

        for i, insight in enumerate(reversed(st.session_state.custom_insights)):
            if not selected_tags or any(tag in selected_tags for tag in insight.get('tags', [])):
                with st.expander(f"{insight['title']} - {insight['timestamp']}"):
                    st.markdown("**Deskripsi:**")
                    st.write(insight['content'])
                    if insight.get('tags'):
                        st.markdown(f"**Tags:** {', '.join(insight['tags'])}")
                    st.caption(f"Ditambahkan pada: {insight['timestamp']}")
                    if st.button("Hapus", key=f"delete_session_{i}"):
                        st.session_state.custom_insights.remove(insight)
                        st.experimental_rerun()
    else:
        st.info("Belum ada insights yang disimpan. Tambahkan insight menggunakan form di atas.")
