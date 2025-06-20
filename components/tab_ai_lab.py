import streamlit as st

def tab_ai_lab(tab):
    with tab:
        st.subheader("AI Lab")
        st.info("Eksperimen dengan fitur AI di sini. (Anda dapat menambahkan logika AI sesuai kebutuhan portfolio Anda!)")
        # Contoh interaksi AI sederhana (dummy):
        prompt = st.text_area("Coba prompt ke AI (dummy):")
        if st.button("Kirim"):
            if prompt.strip():
                st.write(f"Output AI (dummy): {prompt[::-1]}")
            else:
                st.warning("Masukkan prompt terlebih dahulu.")
