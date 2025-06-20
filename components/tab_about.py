import streamlit as st

def show():
    st.header("📝 Tentang ProMedia Insight Hub")
    
    # Form registrasi
    if st.session_state.get('role') == 'admin':
        with st.expander("🔐 Admin: Registrasi Pengguna Baru", expanded=False):
            new_username = st.text_input("Username Baru", key="reg_username")
            new_password = st.text_input("Password Baru", type="password", key="reg_password")
            confirm_password = st.text_input("Konfirmasi Password", type="password", key="reg_confirm")
            user_role = st.selectbox("Peran", ["user", "admin"], index=0, key="reg_role")
            
            if st.button("Daftarkan Pengguna"):
                if not new_username or not new_password:
                    st.error("Username dan password harus diisi")
                elif new_password != confirm_password:
                    st.error("Password tidak cocok")
                else:
                    success, message = register_user(new_username, new_password, user_role)
                    if success:
                        st.success("Registrasi berhasil! Pengguna dapat login dengan akun baru")
                    else:
                        st.error(f"Registrasi gagal: {message}")
    
    # Informasi aplikasi
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
