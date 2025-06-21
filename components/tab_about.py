import streamlit as st

def show(tab):
    with tab:
        st.markdown("""
        <style>
            .about-header { text-align: center; padding: 1.5rem 0 0.7rem 0; border-bottom: 2px solid #1a3c6e; margin-bottom: 2.1rem; }
            .about-title { font-size: 2.2rem; color: #1a3c6e; margin-bottom: 0.5rem; }
            .about-subtitle { font-size: 1.13rem; color: #374151; max-width: 800px; margin: 0 auto; }
            .about-card { background: #fff; border-radius: 13px; padding: 2rem 1.5rem; margin-bottom: 1.45rem; box-shadow: 0 5px 18px 0 #e2e8f0; border: 1px solid #e5e7eb; }
            .card-title { font-size: 1.32rem; font-weight: 700; color: #1a3c6e; margin-bottom: 1.1rem; display: flex; align-items: center; gap: 12px; }
            .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(175px, 1fr)); gap: 1.13rem; margin-top: 1rem; }
            .feature-card { background: linear-gradient(120deg, #f4f6fb 60%, #eaf2fa 100%); border-radius: 10px; padding: 1.23rem 1rem; text-align: center; border: 1px solid #e3e8ee; }
            .feature-value { font-size: 2.1rem; margin-bottom: 0.65rem; }
            .feature-label { font-weight: 500; color: #1a3c6e; font-size:1.07rem; }
            .tech-tag-container { display: flex; flex-wrap: wrap; gap: 0.53rem; margin-top: 1.13rem; }
            .tech-tag { background: #e0f2fe; color: #0369a1; padding: 0.45rem 1.12rem; border-radius: 18px; font-weight: 500; font-size: 0.97rem; box-shadow: 0 2px 6px rgba(0,0,0,0.05);}
            .dev-profile { display: flex; flex-direction: column; align-items: center; gap: 0.45rem; margin-top: 0.3rem; margin-bottom: 0.7rem;}
            .dev-avatar { width: 74px; height: 74px; border-radius: 50%; object-fit: cover; margin-bottom: 0.5rem; border: 3px solid #c6dbf5;}
            .dev-name { font-size: 1.17rem; font-weight: 700; color: #15386a; margin-bottom: 0.16rem;}
            .dev-links { display: flex; gap: 1.3rem; margin-top: 0.44rem;}
            .dev-link { color: #1a3c6e; font-weight: 500; font-size: 1.01rem; text-decoration: none; background: #e8f1fb; padding: 0.41rem 1.03rem; border-radius: 19px; border: 1px solid #b2c5df;}
            .dev-link:hover { background: #e0eaff; color: #356aad;}
            .dev-email {margin-top:0.45rem;font-size:1.01rem; color:#1a3c6e; background:#f3f7fa; padding:0.49rem 1.18rem; border-radius:22px; border:1px solid #e3e8ee; text-decoration:none; display:inline-block;}
            .footer { text-align: center; padding: 1.08rem 1.1rem 1.1rem 1.2rem; color: #64748b; font-size: 0.93rem; margin-top: 1.1rem; background: #f8fafc; border-radius: 13px; border: 1px solid #e2e8f0;}
            .platform-overview ul { padding-left: 1.55rem; margin-top: 0.88rem;}
            .platform-overview li { margin-bottom: 0.56rem; line-height: 1.6; position: relative;}
            .platform-overview li:before { content: "•"; color: #1a3c6e; font-weight: bold; display: inline-block; width: 1em; margin-left: -1em;}
        </style>
        """, unsafe_allow_html=True)

        # ===== HEADER =====
        st.markdown("""
        <div class="about-header">
            <div class="about-title">ℹ️ About ProMedia Insight Hub</div>
            <div class="about-subtitle">
                Platform dashboard analisis media berbasis AI untuk insight strategis dari data berita — upload, analisis, prediksi, dan manajemen insight media secara modern & efisien.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== PLATFORM OVERVIEW =====
        st.markdown("""
        <div class="about-card platform-overview">
            <div class="card-title">📊 Platform Overview</div>
            <p><b>ProMedia Insight Hub</b> adalah platform dashboard analisis media berbasis AI yang memungkinkan pengguna untuk mengelola, menganalisis, dan mendapatkan insight strategis dari data berita secara efisien.</p>
            <p>Platform ini mengintegrasikan teknologi data analytics dan kecerdasan buatan (AI) untuk visualisasi interaktif, analisis sentimen otomatis, identifikasi topik/sumber terpopuler, serta prediksi tren masa depan.</p>
        </div>
        """, unsafe_allow_html=True)

        # ===== KEY FEATURES =====
        st.markdown("""
        <div class="about-card">
            <div class="card-title">✨ Key Features</div>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-value">📊</div>
                    <div class="feature-label">Dashboard Overview</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Rangkuman data, distribusi berita, tren & insight interaktif.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">📤</div>
                    <div class="feature-label">Upload & Manajemen Data</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Upload & kelola dataset berita dengan template standar.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">📈</div>
                    <div class="feature-label">Visualisasi & Tren Data</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Distribusi, tren sentimen, topik & sumber terpopuler.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">😊</div>
                    <div class="feature-label">Analisis Sentimen Otomatis</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Deteksi sentimen publik terhadap isu/topik otomatis.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">📰</div>
                    <div class="feature-label">Topik & Sumber Terpopuler</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Identifikasi topik & sumber paling berpengaruh.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">🔮</div>
                    <div class="feature-label">Forecasting Tren Masa Depan</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Prediksi tren media berbasis data historis.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">🧠</div>
                    <div class="feature-label">AI Data Lab / Chat AI</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Tanya jawab & insight otomatis dengan AI Gemini.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">💡</div>
                    <div class="feature-label">Insight & Rekomendasi Strategis</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Simpan insight penting dan rekomendasi AI.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">🔐</div>
                    <div class="feature-label">Multi-user & Authentication</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Sistem login, admin/user, & manajemen role.
                    </div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">⚡</div>
                    <div class="feature-label">Interface Modern & Responsive</div>
                    <div style="font-size:12px;margin-top:0.3rem;color:#65708a;">
                        Dashboard modern, profesional, & scalable.
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== TECHNOLOGY STACK =====
        st.markdown("""
        <div class="about-card">
            <div class="card-title">🛠️ Technology Stack</div>
            <p><b>Bahasa & Framework:</b></p>
            <div class="tech-tag-container">
                <span class="tech-tag">Python</span>
                <span class="tech-tag">Streamlit</span>
                <span class="tech-tag">HTML & CSS</span>
            </div>
            <p style="margin-top:1rem;"><b>Data Science & Analytics:</b></p>
            <div class="tech-tag-container">
                <span class="tech-tag">pandas</span>
                <span class="tech-tag">numpy</span>
                <span class="tech-tag">plotly</span>
                <span class="tech-tag">matplotlib</span>
                <span class="tech-tag">openpyxl</span>
                <span class="tech-tag">networkx</span>
                <span class="tech-tag">scikit-learn</span>
                <span class="tech-tag">statsmodels</span>
                <span class="tech-tag">tabulate</span>
                <span class="tech-tag">fpdf2</span>
            </div>
            <p style="margin-top:1rem;"><b>AI & ML Integration:</b></p>
            <div class="tech-tag-container">
                <span class="tech-tag">google-generativeai</span>
                <span class="tech-tag">textblob</span>
                <span class="tech-tag">NLP</span>
                <span class="tech-tag">Machine Learning</span>
            </div>
            <p style="margin-top:1rem;"><b>Database & Auth:</b></p>
            <div class="tech-tag-container">
                <span class="tech-tag">SQLite</span>
                <span class="tech-tag">sqlite3</span>
                <span class="tech-tag">sqlalchemy</span>
                <span class="tech-tag">streamlit-authenticator</span>
                <span class="tech-tag">hashlib</span>
            </div>
            <p style="margin-top:1rem;"><b>Environment & Deployment:</b></p>
            <div class="tech-tag-container">
                <span class="tech-tag">Docker</span>
                <span class="tech-tag">docker-compose</span>
                <span class="tech-tag">python-dotenv</span>
                <span class="tech-tag">Devcontainer</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== DEVELOPER =====
        st.markdown("""
        <div class="about-card">
            <div class="card-title">👨‍💻 Developer</div>
            <div class="dev-profile">
                <img src="https://ui-avatars.com/api/?name=Rafif+Sudanta&background=e8f1fb&color=1a3c6e&size=256" class="dev-avatar"/>
                <div class="dev-name">Rafif Sudanta</div>
                <div class="dev-links">
                    <a class="dev-link" href="https://github.com/r1afif18/pro-media-dashboard" target="_blank">GitHub Repo</a>
                    <a class="dev-link" href="https://www.linkedin.com/in/rafifsudanta/" target="_blank">LinkedIn</a>
                </div>
                <a class="dev-email" href="mailto:rafifsudanta1@gmail.com">📧 rafifsudanta1@gmail.com</a>
            </div>
            <div style="margin-top:1rem;font-size:0.99rem;color:#4b5563;text-align:center;">
                Untuk kolaborasi, proyek bersama, atau konsultasi dashboard & AI, silakan hubungi saya via LinkedIn atau email.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== FOOTER =====
        st.markdown("""
        <div class="footer">
            <p>© 2024 ProMedia Insight Hub. Developed by Rafif Sudanta.</p>
            <p style="margin-top: 0.5rem;">Versi 2.0 | <a href="https://github.com/r1afif18/pro-media-dashboard" style="color: #3b82f6; text-decoration: none;" target="_blank">GitHub Repo</a> | <a href="https://www.linkedin.com/in/rafifsudanta/" style="color: #3b82f6; text-decoration: none;" target="_blank">LinkedIn</a></p>
        </div>
        """, unsafe_allow_html=True)
