import streamlit as st

def tab_overview(tab):
    with tab:
        st.subheader("Overview")
        st.write(
            "Selamat datang di ProMedia Insight Hub! Dashboard ini menampilkan analisis media berbasis AI, eksplorasi data, insight, dan visualisasi berita."
        )
