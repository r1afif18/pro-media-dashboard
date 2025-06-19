import google.generativeai as genai
import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class GeminiEngine:
    def __init__(self):
        self.api_key = st.session_state.get('google_api_key') or os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.model_name = None
        
    def configure(self):
        """Konfigurasi model Gemini"""
        if not self.api_key:
            st.error("GOOGLE_API_KEY tidak ditemukan")
            return False
            
        try:
            genai.configure(api_key=self.api_key)
            
            # Cari model yang tersedia
            available_models = genai.list_models()
            gemini_models = [
                m.name for m in available_models 
                if 'generateContent' in m.supported_generation_methods and 'gemini' in m.name
            ]
            
            if not gemini_models:
                st.error("Tidak ada model Gemini yang tersedia")
                return False
                
            # Pilih model terbaru yang tersedia
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
            
            # Gunakan model pertama yang tersedia sebagai fallback
            self.model = genai.GenerativeModel(gemini_models[0])
            self.model_name = gemini_models[0].split('/')[-1]
            return True
            
        except Exception as e:
            st.error(f"Konfigurasi gagal: {str(e)}")
            return False
    
    def ask(self, question, df, history=[]):
        """Mengajukan pertanyaan menggunakan library resmi"""
        if not self.model and not self.configure():
            return "Tidak dapat mengakses Gemini API"
            
        try:
            # Format konteks data
            context = f"""
            Anda adalah analis media profesional. Berikut adalah ringkasan data berita:

            Struktur Data:
            - Kolom: {list(df.columns)}
            - Jumlah Baris: {len(df)}
            - Rentang Tanggal: {df['date'].min().strftime('%Y-%m-%d')} hingga {df['date'].max().strftime('%Y-%m-%d')}
            
            Contoh Data:
            {df.head(2).to_markdown(index=False)}
            """
            
            # Format riwayat percakapan
            history_context = ""
            if history:
                history_context = "\nRiwayat Percakapan:\n" + "\n".join(
                    [f"Q: {q}\nA: {a}\n" for q, a in history[-3:]]
                )
            
            # Buat prompt lengkap
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
            
            # Generate respons
            response = self.model.generate_content(full_prompt)
            
            # Handle respons
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

# Global instance
gemini_engine = GeminiEngine()