import streamlit as st
import pandas as pd
from datetime import datetime

def tab_upload(tab):
    with tab:
        st.header("📤 Upload & Eksplorasi Data")
        uploaded_file = st.file_uploader("Upload file data berita (CSV atau Excel)", type=["csv", "xlsx", "xls"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, parse_dates=['date'])
            else:
                df = pd.read_excel(uploaded_file, parse_dates=['date'])
            st.session_state.df = df
            st.session_state.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success("✅ Data berhasil diupload!")
            st.subheader("Preview Data")
            st.dataframe(df.head(10), use_container_width=True)
