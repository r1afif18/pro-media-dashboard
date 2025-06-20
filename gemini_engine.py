import google.generativeai as genai
import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiEngine:
    def __init__(self):
        # Mengambil API key langsung dari secrets
        self.api_key = st.secrets.get("GOOGLE_API_KEY")
        self.model = None
        self.model_name = None
        self.configured = False
        
    def configure(self):
        """Konfigurasi model Gemini dengan API key dari secrets"""
        if not self.api_key:
            logger.error("GOOGLE_API_KEY tidak ditemukan di secrets")
            return False
            
        try:
            genai.configure(api_key=self.api_key)
            available_models = genai.list_models()
            gemini_models = [
                m.name for m in available_models 
                if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name
            ]
            
            if not gemini_models:
                logger.error("Tidak ada model Gemini yang tersedia")
                return False

            # Prioritas model: 1.5 Flash > 1.5 Pro > Pro
            preferred_models = [
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro',
                'models/gemini-pro'
            ]
            
            for model in preferred_models:
                if model in gemini_models:
                    self.model = genai.GenerativeModel(model)
                    self.model_name = model.split('/')[-1]
                    logger.info(f"Model {self.model_name} berhasil dikonfigurasi")
                    self.configured = True
                    return True
            
            # Gunakan model pertama yang tersedia jika tidak ada yang di-prefer
            self.model = genai.GenerativeModel(gemini_models[0])
            self.model_name = gemini_models[0].split('/')[-1]
            logger.info(f"Model {self.model_name} berhasil dikonfigurasi")
            self.configured = True
            return True
            
        except Exception as e:
            logger.error(f"Konfigurasi gagal: {str(e)}")
            return False
    
    def ask(self, question, df, history=[]):
        """Ajukan pertanyaan ke model Gemini dengan konteks data"""
        if not self.configured and not self.configure():
            return "Tidak dapat mengakses Gemini API. Periksa konfigurasi."
            
        try:
            # Siapkan konteks dari data
            context = f"""
            Anda adalah analis media profesional. Berikut adalah ringkasan data berita:

            Struktur Data:
            - Kolom: {list(df.columns)}
            - Jumlah Baris: {len(df)}
            - Rentang Tanggal: {df['date'].min().strftime('%Y-%m-%d') if 'date' in df.columns and not df.empty else '-'} hingga {df['date'].max().strftime('%Y-%m-%d') if 'date' in df.columns and not df.empty else '-'}
            
            Contoh Data:
            {df.head(2).to_markdown(index=False) if not df.empty else 'Tidak ada data'}
            """
            
            # Tambahkan riwayat percakapan jika ada
            history_context = ""
            if history:
                history_context = "\nRiwayat Percakapan:\n" + "\n".join(
                    [f"Q: {q}\nA: {a}\n" for q, a in history[-3:]]
                )
                
            # Bangun prompt lengkap
            full_prompt = f"""
            {context}
            {history_context}
            
            Pertanyaan: {question}
            
            Instruksi:
            1. Jawab dalam Bahasa Indonesia
            2. Berikan analisis berbasis data
            3. Sertakan insight yang dapat ditindaklanjuti
            4. Jika memungkinkan, berikan angka/metrik spesifik
            5. Gunakan format Markdown untuk struktur yang jelas
            """
            
            logger.info(f"Mengajukan pertanyaan ke Gemini: {question[:50]}...")
            response = self.model.generate_content(full_prompt)
            
            if response.candidates:
                return response.text
            elif response.prompt_feedback:
                return "Respons diblokir: " + str(response.prompt_feedback)
            else:
                return "Tidak mendapatkan respons yang valid"
                
        except genai.types.BlockedPromptException:
            return "Pertanyaan Anda mengandung konten yang diblokir"
        except Exception as e:
            logger.error(f"Error dalam menghasilkan respons: {str(e)}")
            return f"Error: {str(e)}"

# Buat instance engine yang akan digunakan di seluruh aplikasi
gemini_engine = GeminiEngine()
