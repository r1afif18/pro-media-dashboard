import google.generativeai as genai
import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def generate_time_series_insights(data):
    """
    Meminta Gemini memberikan insight dan prediksi tren 7 hari ke depan
    berdasarkan data deret waktu (format markdown/table).
    """
    prompt = (
        f"Buat prediksi dan insight tren 7 hari ke depan berdasarkan data berikut (format markdown):\n{data}\n"
        "Jawab dalam Bahasa Indonesia, ringkas, dan jika memungkinkan tampilkan prediksi angka per hari."
    )
    return gemini_engine.ask(prompt, pd.DataFrame({'date': [], 'value': []}))

class GeminiEngine:
    def __init__(self):
        self.api_key = st.session_state.get('google_api_key') or os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.model_name = None
        
    def configure(self):
        if not self.api_key:
            st.error("GOOGLE_API_KEY tidak ditemukan")
            return False
            
        try:
            genai.configure(api_key=self.api_key)
            available_models = genai.list_models()
            gemini_models = [
                m.name for m in available_models 
                if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name
            ]
            if not gemini_models:
                st.error("Tidak ada model Gemini yang tersedia")
                return False

            preferred_models = [
                'models/gemini-1.5-flash',
                'models/gemini-1.5-pro',
                'models/gemini-pro'
            ]
            for model in preferred_models:
                if model in gemini_models:
                    self.model = genai.GenerativeModel(model)
                    self.model_name = model.split('/')[-1]
                    return True
            self.model = genai.GenerativeModel(gemini_models[0])
            self.model_name = gemini_models[0].split('/')[-1]
            return True
        except Exception as e:
            st.error(f"Konfigurasi gagal: {str(e)}")
            return False
    
    def ask(self, question, df, history=[]):
        if not self.model and not self.configure():
            return "Tidak dapat mengakses Gemini API"
        try:
            context = f"""
            Anda adalah analis media profesional. Berikut adalah ringkasan data berita:

            Struktur Data:
            - Kolom: {list(df.columns)}
            - Jumlah Baris: {len(df)}
            - Rentang Tanggal: {df['date'].min().strftime('%Y-%m-%d') if 'date' in df.columns and not df.empty else '-'} hingga {df['date'].max().strftime('%Y-%m-%d') if 'date' in df.columns and not df.empty else '-'}
            
            Contoh Data:
            {df.head(2).to_markdown(index=False) if not df.empty else 'Tidak ada data'}
            """
            history_context = ""
            if history:
                history_context = "\nRiwayat Percakapan:\n" + "\n".join(
                    [f"Q: {q}\nA: {a}\n" for q, a in history[-3:]]
                )
            full_prompt = f"""
            {context}
            {history_context}
            
            Pertanyaan: {question}
            
            Instruksi:
            1. Jawab dalam Bahasa Indonesia
            2. Berikan analisis berbasis data
            3. Sertakan insight yang dapat ditindaklanjuti
            4. Jika memungkinkan, berikan angka/metrik spesifik
            """
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
            return f"Error: {str(e)}"

gemini_engine = GeminiEngine()
