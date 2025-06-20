import google.generativeai as genai
import streamlit as st
import os
import pandas as pd
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiEngine:
    def __init__(self):
        self.api_key = st.secrets.get("GOOGLE_API_KEY")
        self.model = None
        self.model_name = None
        self.configured = False
        self.last_request_time = 0
        self.RATE_LIMIT = 1.0  # 1 request per second
        
    def configure(self):
        if not self.api_key:
            logger.error("GOOGLE_API_KEY tidak ditemukan di secrets")
            return False
            
        try:
            genai.configure(api_key=self.api_key)
            available_models = genai.list_models()
            
            # Prioritas model
            model_priority = [
                'models/gemini-1.5-flash-latest',
                'models/gemini-1.5-pro-latest',
                'models/gemini-pro'
            ]
            
            for model in model_priority:
                if any(m.name == model for m in available_models):
                    self.model = genai.GenerativeModel(model)
                    self.model_name = model.split('/')[-1]
                    logger.info(f"Model {self.model_name} berhasil dikonfigurasi")
                    self.configured = True
                    return True
            
            # Fallback ke model pertama yang tersedia
            for m in available_models:
                if 'generateContent' in m.supported_generation_methods:
                    self.model = genai.GenerativeModel(m.name)
                    self.model_name = m.name.split('/')[-1]
                    logger.info(f"Fallback model {self.model_name} berhasil dikonfigurasi")
                    self.configured = True
                    return True
                    
            logger.error("Tidak ada model yang kompatibel ditemukan")
            return False
            
        except Exception as e:
            logger.error(f"Konfigurasi gagal: {str(e)}")
            return False
    
    def ask(self, question, df, history=[]):
        """Ajukan pertanyaan ke model Gemini dengan konteks data"""
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_request_time < self.RATE_LIMIT:
            time.sleep(self.RATE_LIMIT - (current_time - self.last_request_time))
        self.last_request_time = time.time()
        
        if not self.configured and not self.configure():
            return "⚠️ Sistem AI belum terkonfigurasi. Periksa API key Anda."
            
        try:
            # Data profiling
            data_profile = f"""
            **Profil Data:**
            - Dimensi: {df.shape[0]} baris × {df.shape[1]} kolom
            - Rentang Tanggal: {df['date'].min().strftime('%d %b %Y') if 'date' in df.columns and not df.empty else 'N/A'} - {df['date'].max().strftime('%d %b %Y') if 'date' in df.columns and not df.empty else 'N/A'}
            - Sumber Unik: {df['source'].nunique() if 'source' in df.columns else 'N/A'}
            - Distribusi Sentimen: 
              {df['sentiment'].value_counts(normalize=True).to_dict() if 'sentiment' in df.columns and not df.empty else 'N/A'}
            """
            
            # Contoh data - menggunakan to_html sebagai fallback
            sample_data = ""
            if not df.empty:
                try:
                    # Coba gunakan to_markdown jika tersedia
                    sample_data = df.head(2).to_markdown(index=False)
                except Exception:
                    # Fallback ke HTML jika tabulate tidak terinstall
                    sample_data = df.head(2).to_html(index=False)
            
            # Build context
            context = f"""
            # PERINTAH ANALISIS DATA MEDIA
            
            ## KONTEKS DATA
            {data_profile}
            
            ## CONTOH DATA:
            {sample_data if not df.empty else 'Tidak ada data'}
            
            ## RIWAYAT PERCAKAPAN:
            {self._format_history(history)}
            """
            
            # Prompt engineering
            full_prompt = f"""
            {context}
            
            ## PERMINTAAN USER:
            {question}
            
            ## INSTRUKSI RESPONS:
            1. Berikan analisis berbasis data konkret
            2. Sertakan metrik kuantitatif
            3. Berikan 3 insight utama
            4. Rekomendasi strategis berbasis temuan
            5. Format respons dalam Markdown
            
            ## STRUKTUR RESPONS:
            ### 📊 Analisis Data
            [Analisis mendalam dengan data pendukung]
            
            ### 💡 Key Insights
            1. [Insight 1]
            2. [Insight 2]
            3. [Insight 3]
            
            ### 🚀 Rekomendasi Strategis
            - [Rekomendasi 1]
            - [Rekomendasi 2]
            """
            
            logger.info(f"Mengajukan pertanyaan ke Gemini: {question[:100]}...")
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.95,
                    candidate_count=1
                )
            )
            
            if response.candidates:
                return response.text
            elif response.prompt_feedback:
                return f"⚠️ Respons diblokir: {response.prompt_feedback}"
            else:
                return "⚠️ Tidak mendapatkan respons yang valid"
                
        except genai.types.BlockedPromptException:
            return "⚠️ Pertanyaan mengandung konten yang diblokir"
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            return f"⚠️ Error: {str(e)}"
    
    def _format_history(self, history):
        """Format riwayat percakapan"""
        if not history:
            return "Tidak ada riwayat percakapan"
            
        return "\n\n".join(
            [f"### Pertanyaan {i+1}:\n**Q:** {q}\n**A:** {a[:200]}..."
            for i, (q, a) in enumerate(history[-3:])]
        )

# Singleton instance
gemini_engine = GeminiEngine()
