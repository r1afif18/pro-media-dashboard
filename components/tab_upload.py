import streamlit as st
import pandas as pd

def show():
    st.header("📁 Upload & Eksplorasi Data")

    # Upload CSV
    uploaded_file = st.file_uploader(
        "Upload file data (.csv)", type=["csv"], key="uploader_main"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("File berhasil diupload!")
            
            # Auto-detect kolom tanggal
            date_cols = [col for col in df.columns if 'date' in col.lower() or 'tanggal' in col.lower()]
            if not date_cols:
                st.error("Tidak ditemukan kolom bertipe tanggal! Pastikan ada kolom seperti 'date' atau 'tanggal'.")
                return
            date_col = st.selectbox("Pilih kolom tanggal", date_cols)
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

            # Deteksi kolom numerik
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            # Jika tidak ada kolom numerik, auto-generate 'count'
            if not numeric_cols:
                st.warning(
                    "Tidak ada kolom numerik! Sistem akan otomatis membuat kolom `count` (jumlah data per tanggal)."
                )
                daily_counts = df.groupby(date_col).size().reset_index(name='count')
                df = daily_counts
                numeric_cols = ['count']

            # Simpan ke session_state
            st.session_state.df = df
            st.session_state.date_col = date_col
            st.session_state.numeric_cols = numeric_cols

            # Preview data
            st.subheader("Preview Data")
            st.dataframe(df.head(10), use_container_width=True)

            st.markdown(f"**Kolom Tanggal:** {date_col}")
            st.markdown(f"**Kolom Numerik:** {', '.join(numeric_cols)}")

        except Exception as e:
            st.error(f"Terjadi error saat upload/parse file: {e}")
    else:
        st.info("Silakan upload file CSV untuk mulai analisis data.")

