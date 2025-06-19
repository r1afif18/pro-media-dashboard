import streamlit as st
import pandas as pd
from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime
from database import get_custom_insights, get_ai_history

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'ProMedia Insight Hub - Laporan Analisis', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, body)
        self.ln()

def generate_pdf_report(username):
    pdf = PDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Laporan Analisis Media', 0, 1, 'C')
    pdf.ln(10)
    
    # Informasi dasar
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f"Tanggal: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
    pdf.cell(0, 6, f"Pengguna: {username}", 0, 1)
    pdf.ln(10)
    
    # Insights custom
    pdf.chapter_title("Insights Custom")
    insights = get_custom_insights(username)
    for insight in insights:
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, insight['title'], 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, insight['content'])
        pdf.ln(3)
    
    # History AI
    pdf.chapter_title("Riwayat Analisis AI")
    history = get_ai_history(username, limit=10)
    for i, (query, response, timestamp) in enumerate(history):
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, f"Pertanyaan {i+1}: {query}", 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, response)
        pdf.ln(3)
    
    # Simpan file
    filename = f"report_{username}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def send_email(report_file, recipient_email):
    # Konfigurasi email (ganti dengan konfigurasi Anda)
    sender_email = "reports@promedia.com"
    password = "email_password"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Laporan ProMedia Insight Hub"
    
    body = "Berikut terlampir laporan analisis media terbaru Anda."
    msg.attach(MIMEText(body, 'plain'))
    
    with open(report_file, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=report_file)
        msg.attach(attach)
    
    try:
        server = smtplib.SMTP('smtp.example.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"Gagal mengirim email: {str(e)}")
        return False