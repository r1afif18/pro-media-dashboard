import streamlit as st
import pandas as pd

def tab_upload(tab):
    with tab:
        st.subheader("Upload Data")
        uploaded_file = st.file_uploader("Pilih file CSV untuk dianalisis", type=["csv"])
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.success("File berhasil diupload!")
                st.dataframe(df)
            except Exception as e:
                st.error(f"File tidak valid: {e}")
        else:
            st.info("Silakan upload file data untuk mulai eksplorasi.")
