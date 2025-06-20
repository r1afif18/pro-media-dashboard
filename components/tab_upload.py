import streamlit as st
import pandas as pd
from datetime import datetime

def tab_upload(tab):
    with tab:
        st.header("📤 Upload & Eksplorasi Data")
        uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, parse_dates=['date'])
            st.session_state.df = df
            st.success("Data berhasil diupload!")
            st.dataframe(df.head(10), use_container_width=True)
