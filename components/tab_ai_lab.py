import streamlit as st
from gemini_engine import gemini_engine
from database import save_ai_history, get_ai_history, delete_ai_history
import logging
import time
import pandas as pd
import utils

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def show(tab):
    with tab:
        st.header("🧠 AI Lab - Analisis Data Cerdas")
        st.caption("Analisis data berita dengan kecerdasan buatan tingkat lanjut")
        
        # Status model
        if not gemini_engine.configured:
            with st.spinner("Mengkonfigurasi model AI..."):
                if gemini_engine.configure():
                    st.success(f"✅ Model {gemini_engine.model_name} siap digunakan!")
                else:
                    st.error("❌ Gagal mengkonfigurasi model. Periksa API key di secrets.")
                    return
        
        # Data status panel
        if 'df' in st.session_state and st.session_state.df is not None:
            profile = st.session_state.get('data_profile', utils.generate_data_profile(st.session_state.df))
            col1, col2, col3 = st.columns(3)
            col1.markdown(utils.create_metric_card("Total Berita", profile['total_news'], "📰", "#4C78A8"), 
                         unsafe_allow_html=True)
            col2.markdown(utils.create_metric_card("Sumber Berita", len(profile['sources']), "📡", "#E45756"), 
                         unsafe_allow_html=True)
            
            if profile['date_range']:
                date_range = f"{profile['date_range']['min']} - {profile['date_range']['max']}"
                col3.markdown(utils.create_metric_card("Rentang Tanggal", date_range, "📅", "#54A24B"), 
                             unsafe_allow_html=True)
        else:
            st.warning("📤 Silakan upload data terlebih dahulu di tab Upload Data")
        
        # Riwayat analisis
        st.subheader("📜 Riwayat Analisis")
        history = get_ai_history(limit=8)
        
        if not history:
            st.info("Belum ada riwayat analisis. Mulailah dengan mengajukan pertanyaan!")
        else:
            # Fitur pencarian riwayat
            search_query = st.text_input("Cari riwayat...", key="history_search")
            
            # Tampilkan riwayat dengan tabs
            tab_labels = [f"#{i+1}" for i in range(len(history))]
            tabs = st.tabs(tab_labels)
            
            for i, item in enumerate(history):
                with tabs[i]:
                    # Highlight jika sesuai pencarian
                    if search_query and (search_query.lower() in item['prompt'].lower() or 
                                        search_query.lower() in item['response'].lower()):
                        st.markdown("🔍 **Hasil Pencarian**")
                    
                    st.markdown(f"**🗓️ {item['created_at']}**")
                    with st.expander(f"**❓ {item['prompt'][:80]}...**", expanded=False):
                        st.markdown(f"**Pertanyaan:** {item['prompt']}")
                        st.markdown("---")
                        st.markdown(f"**Jawaban:** {item['response']}")
                    
                    # Tombol aksi
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("Gunakan Ulang", key=f"reuse_{item['id']}"):
                            st.session_state.reuse_prompt = item['prompt']
                            st.experimental_rerun()
                    with col2:
                        if st.button("Hapus", key=f"delete_{item['id']}"):
                            delete_ai_history(item['id'])
                            st.success("Riwayat dihapus!")
                            time.sleep(0.5)
                            st.experimental_rerun()
        
        # Input analisis
        st.subheader("🔍 Ajukan Analisis")
        
        # Template pertanyaan
        template_options = {
            "Pilih template...": "",
            "Analisis Tren Topik": "Analisis tren topik berita selama periode tertentu",
            "Sentimen per Sumber": "Bandingkan sentimen berita antar sumber media",
            "Deteksi Anomali": "Identifikasi hari dengan aktivitas berita tidak biasa",
            "Korelasi Variabel": "Analisis hubungan antara variabel dalam dataset"
        }
        
        selected_template = st.selectbox("Template Analisis", list(template_options.keys()))
        
        # Input pertanyaan
        question = st.text_area(
            "Rumuskan pertanyaan analisis Anda:",
            height=150,
            value=st.session_state.get("reuse_prompt", template_options[selected_template]),
            placeholder="Contoh: Berikan analisis mendalam tentang pola sentimen selama 30 hari terakhir"
        )
        
        # Opsi lanjutan
        with st.expander("⚙️ Pengaturan Lanjutan"):
            col1, col2 = st.columns(2)
            with col1:
                temperature = st.slider("Kreativitas AI", 0.0, 1.0, 0.7, 
                                        help="Nilai lebih tinggi = lebih kreatif, lebih rendah = lebih fokus")
            with col2:
                history_context = st.slider("Riwayat Konteks", 0, 5, 3, 
                                           help="Jumlah riwayat percakapan yang digunakan sebagai konteks")
        
        # Tombol aksi
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🔄 Reset Input", use_container_width=True):
                if "reuse_prompt" in st.session_state:
                    del st.session_state.reuse_prompt
                st.experimental_rerun()
        with col2:
            if st.button("🚀 Kirim ke AI", type="primary", use_container_width=True, 
                        disabled=not question or 'df' not in st.session_state):
                if 'df' not in st.session_state or st.session_state.df is None:
                    st.warning("Silakan upload data terlebih dahulu")
                else:
                    with st.spinner("Menganalisis data. Ini mungkin memakan waktu beberapa detik..."):
                        try:
                            # Dapatkan riwayat untuk konteks
                            history_context_data = [(h['prompt'], h['response']) 
                                                  for h in history[:history_context]]
                            
                            # Ajukan pertanyaan ke Gemini
                            start_time = time.time()
                            response = gemini_engine.ask(question, st.session_state.df, history_context_data)
                            processing_time = time.time() - start_time
                            
                            # Simpan ke database
                            save_ai_history(question, response)
                            
                            # Tampilkan hasil
                            st.success(f"✅ Analisis selesai dalam {processing_time:.2f} detik")
                            st.markdown("### Hasil Analisis")
                            st.markdown(response)
                            
                            # Tampilkan metrik performa
                            st.caption(f"Model: {gemini_engine.model_name} | Token: ~{len(response.split()) * 1.33:.0f}")
                            
                            # Auto-refresh riwayat
                            st.experimental_rerun()
                            
                        except Exception as e:
                            st.error(f"❌ Error selama analisis: {str(e)}")
                            logger.exception("AI Lab error")
