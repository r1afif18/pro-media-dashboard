# components/tab_insights.py
import streamlit as st
import pandas as pd
# Hapus import ini karena kita akan pakai gemini_engine:
# from pandasai import SmartDataframe
# from pandasai.llm import GoogleGenerativeAI
import os
from dotenv import load_dotenv

# Impor gemini_engine, sama seperti di tab_ai_lab.py
from gemini_engine import gemini_engine
import time 

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
    st.info("Catatan manual di sini tidak akan tersimpan secara persisten jika aplikasi di-refresh tanpa backend.")

    st.markdown("---")

    st.subheader("🤖 AI-Generated Insights")
    st.info("Gunakan AI untuk mendapatkan ringkasan otomatis, temuan menarik, atau pola dari data Anda.")

    # Validasi API Key dan inisialisasi model dari gemini_engine
    if not gemini_engine.api_key:
        st.error(
            "🔐 API Key tidak ditemukan! Silakan buat file `.env` dengan:",
            icon="❌"
        )
        st.code("GOOGLE_API_KEY=your_api_key_here", language="bash")
        st.markdown("Dapatkan API key dari [Google AI Studio](https://aistudio.google.com/)")
        return

    # Tampilkan info model (opsional, tapi bagus untuk konsistensi)
    if gemini_engine.model_name:
        st.success(f"Model Gemini aktif: **{gemini_engine.model_name}**")
    else:
        if gemini_engine.configure():
            st.success(f"Model Gemini aktif: **{gemini_engine.model_name}**")
        else:
            st.error("Tidak ada model Gemini yang tersedia")
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
                    # Panggil gemini_engine.ask() seperti di tab_ai_lab.py
                    response = gemini_engine.ask(prompt, df) # Tidak perlu riwayat untuk insight sekali pakai
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
                    response = gemini_engine.ask(prompt, df)
                    st.success("Analisis Sentimen Utama:")
                    st.write(response)
                except Exception as e:
                    st.error(f"Gagal mendapatkan analisis sentimen: {e}")

    with col_insight_3:
        if st.button("Topik Berita Populer (via Kolom 'title' atau 'category')", key="insight_topics"):
            with st.spinner("Mengidentifikasi topik populer dari AI..."):
                try:
                    if 'category' in df.columns:
                        prompt = "Berdasarkan kolom 'category', identifikasi 3 kategori berita paling populer. Jelaskan alasannya."
                    elif 'title' in df.columns:
                        prompt = "Identifikasi 3 kata kunci atau topik paling sering muncul dari kolom 'title'. Jelaskan singkat mengapa itu relevan."
                    else:
                        st.warning("Kolom 'category' atau 'title' tidak ditemukan untuk analisis topik.")
                        return

                    response = gemini_engine.ask(prompt, df)
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
                    # Panggil gemini_engine.ask() untuk pertanyaan kustom
                    response = gemini_engine.ask(custom_insight_query, df)
                    st.subheader("Insight AI Kustom:")
                    # Ini adalah bagian yang perlu penyesuaian jika gemini_engine mengembalikan tipe data spesifik
                    # Untuk sementara, asumsikan respons teks, atau perlu modifikasi di gemini_engine untuk menangani DataFrame/Plot
                    st.write(response) # Asumsi gemini_engine.ask() mengembalikan string
                    # Jika gemini_engine.ask() bisa mengembalikan DataFrame/Plot, logika ini perlu diadaptasi di gemini_engine
                    # agar konsisten
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat mendapatkan insight kustom: {e}")
                    st.warning("Pastikan pertanyaan Anda relevan dengan data dan API Key berfungsi.")
        else:
            st.warning("Silakan masukkan pertanyaan untuk insight kustom.")
