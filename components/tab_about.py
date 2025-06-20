import streamlit as st

def tab_about(tab):
    with tab:
        st.header("📝 Tentang ProMedia Insight Hub")
        st.markdown("""
        ### Fitur Utama
        - 📊 **Overview**: Statistik dan visualisasi tren
        - 📤 **Upload & Eksplorasi**: Unggah dan eksplorasi data
        - 🧠 **AI Lab**: Tanya jawab tentang data
        - 🔮 **Forecasting**: Prediksi tren (dalam pengembangan)
        - 💡 **Insights Custom**: Tambahkan insight manual

        ### Teknologi
        - **Streamlit** - Framework dashboard
        - **Google Gemini Pro** - Model AI generatif
        - **Pandas** - Pengolahan data
        - **SQLite** - Penyimpanan data pengguna

        ### Cara Pakai
        1. Login dengan akun yang telah dibuat
        2. Upload file CSV di tab **Upload & Eksplorasi Data**
        3. Pastikan format kolom sesuai (tanggal, judul, sentimen, sumber, isi)
        4. Eksplorasi statistik di tab **Overview**
        5. Ajukan pertanyaan di tab **AI Lab**

        ### Kontak
        - Email: developer@example.com
        - GitHub: [github.com/username](https://github.com/username)
        """)
