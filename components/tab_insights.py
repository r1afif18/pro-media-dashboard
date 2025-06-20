# components/tab_insights.py
import streamlit as st
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import GoogleGenerativeAI
import os
from dotenv import load_dotenv

# Muat variabel lingkungan dari .env
load_dotenv()

def show_insights_tab(df):
    """
    Menampilkan tab Insights Custom, dengan fokus pada AI-generated insights.
    """
    st.header("💡 Insights Penting")

    if df is None or df.empty:
        st.info("Unggah data CSV di tab 'Upload & Eksplorasi Data' untuk melihat potensi insights.")
        return

    st.subheader("Insights Manual/Kurasi (Placeholder)")
    st.write("""
    Bagian ini dapat digunakan untuk mencatat temuan penting manual atau ringkasan kurasi yang tidak dihasilkan secara otomatis.
    """)
    # Anda bisa menambahkan st.text_area di sini jika ingin pengguna bisa menulis notes
    # Tetapi ingat, tanpa backend, catatan ini tidak akan persisten saat aplikasi di-refresh.
    st.info("Catatan manual di sini tidak akan tersimpan secara persisten jika aplikasi di-refresh tanpa backend.")

    st.markdown("---")

    st.subheader("🤖 AI-Generated Insights")
    st.info("Gunakan AI untuk mendapatkan ringkasan otomatis, temuan menarik, atau pola dari data Anda.")

    # Inisialisasi Gemini Pro LLM
    try:
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not gemini_api_key:
            st.error("API Key Gemini tidak ditemukan. Pastikan Anda telah mengatur GEMINI_API_KEY di file .env Anda.")
            return

        llm = GoogleGenerativeAI(api_key=gemini_api_key)
        # Inisialisasi SmartDataframe hanya jika belum ada atau data berubah
        if 'smart_df_insights' not in st.session_state or st.session_state['smart_df_insights'].dataframe_hash() != SmartDataframe(df, config={"llm": llm}).dataframe_hash():
            st.session_state['smart_df_insights'] = SmartDataframe(df, config={"llm": llm})

        smart_df = st.session_state['smart_df_insights']

    except Exception as e:
        st.error(f"Gagal menginisialisasi Google Gemini Pro untuk Insights: {e}")
        st.warning("Pastikan API Key Anda valid dan koneksi internet stabil.")
        return

    st.markdown("---")
    st.markdown("**Coba Dapatkan Insights Cepat:**")

    # Tombol untuk menghasilkan berbagai jenis insight otomatis
    col_insight_1, col_insight_2, col_insight_3 = st.columns(3)

    with col_insight_1:
        if st.button("Ringkasan Statistik Umum", key="insight_general"):
            with st.spinner("Meminta ringkasan statistik dari AI..."):
                try:
                    # Contoh prompt untuk ringkasan umum
                    prompt = "Berikan ringkasan statistik kunci dari data ini, seperti jumlah total baris, jumlah kolom, dan nilai unik di beberapa kolom kategorikal penting (jika ada seperti 'source', 'sentiment', 'category'). Jelaskan singkat."
                    response = smart_df.chat(prompt)
                    st.success("Ringkasan Statistik:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Gagal mendapatkan ringkasan statistik: {e}")

    with col_insight_2:
        if st.button("Analisis Sentimen Utama", key="insight_sentiment"):
            with st.spinner("Menganalisis sentimen dari AI..."):
                try:
                    # Contoh prompt untuk analisis sentimen
                    prompt = "Berdasarkan kolom 'sentiment' (jika ada), identifikasi sentimen paling dominan, berikan persentasenya. Jelaskan juga jika ada sentimen minoritas yang signifikan."
                    response = smart_df.chat(prompt)
                    st.success("Analisis Sentimen Utama:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Gagal mendapatkan analisis sentimen: {e}")

    with col_insight_3:
        if st.button("Topik Berita Populer (via Kolom 'title' atau 'category')", key="insight_topics"):
            with st.spinner("Mengidentifikasi topik populer dari AI..."):
                try:
                    # Contoh prompt untuk topik populer
                    # Ini akan lebih efektif jika ada kolom 'content' atau 'description' yang lebih panjang
                    # Asumsi 'title' atau 'category' bisa memberikan gambaran
                    if 'category' in df.columns:
                        prompt = "Berdasarkan kolom 'category', identifikasi 3 kategori berita paling populer. Jelaskan alasannya."
                    elif 'title' in df.columns:
                         prompt = "Identifikasi 3 kata kunci atau topik paling sering muncul dari kolom 'title'. Jelaskan singkat mengapa itu relevan."
                    else:
                        st.warning("Kolom 'category' atau 'title' tidak ditemukan untuk analisis topik.")
                        return

                    response = smart_df.chat(prompt)
                    st.success("Topik Berita Populer:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Gagal mendapatkan topik berita populer: {e}")


    st.markdown("---")
    st.markdown("**Atau Ajukan Pertanyaan Insight Kustom Anda:**")
    custom_insight_query = st.text_area("Tulis pertanyaan Anda untuk mendapatkan insight dari AI:", height=100, key="custom_insight_input")

    if st.button("Dapatkan Insight Kustom", key="get_custom_insight_button"):
        if custom_insight_query:
            with st.spinner("Menghasilkan insight kustom dari AI..."):
                try:
                    response = smart_df.chat(custom_insight_query)
                    st.subheader("Insight AI Kustom:")
                    if isinstance(response, pd.DataFrame):
                        st.dataframe(response)
                    elif hasattr(response, 'show'):
                        # Coba tampilkan sebagai plot, jika memungkinkan
                        import matplotlib.pyplot as plt
                        if isinstance(response, plt.Figure):
                            st.pyplot(response)
                        else:
                            st.write(response)
                    else:
                        st.write(response)
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat mendapatkan insight kustom: {e}")
                    st.warning("Pastikan pertanyaan Anda relevan dengan data dan API Key berfungsi.")
        else:
            st.warning("Silakan masukkan pertanyaan untuk insight kustom.")
