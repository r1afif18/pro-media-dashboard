import streamlit as st

def show(tab):
    with tab:
        # ===== STYLE =====
        st.markdown("""
        <style>
            .about-header {
                text-align: center;
                padding: 1.5rem 0 0.7rem 0;
                border-bottom: 2px solid #1a3c6e;
                margin-bottom: 2.1rem;
            }
            .about-title {
                font-size: 2.2rem;
                color: #1a3c6e;
                margin-bottom: 0.5rem;
            }
            .about-subtitle {
                font-size: 1.13rem;
                color: #374151;
                max-width: 800px;
                margin: 0 auto;
            }
            .about-card {
                background: #fff;
                border-radius: 13px;
                padding: 2rem 1.5rem;
                margin-bottom: 1.45rem;
                box-shadow: 0 5px 18px 0 #e2e8f0;
                border: 1px solid #e5e7eb;
                transition: all 0.2s;
            }
            .about-card:hover {
                transform: translateY(-2px) scale(1.011);
                box-shadow: 0 8px 20px 0 #dde7f2;
            }
            .card-title {
                font-size: 1.32rem;
                font-weight: 700;
                color: #1a3c6e;
                margin-bottom: 1.1rem;
                display: flex;
                align-items: center;
                gap: 12px;
            }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 1.15rem;
                margin-top: 1rem;
            }
            .feature-card {
                background: linear-gradient(120deg, #f4f6fb 60%, #eaf2fa 100%);
                border-radius: 10px;
                padding: 1.25rem 0.9rem;
                text-align: center;
                transition: all 0.22s;
                border: 1px solid #e3e8ee;
            }
            .feature-card:hover {
                transform: scale(1.035);
                box-shadow: 0 3px 10px rgba(26, 60, 110, 0.11);
            }
            .feature-value {
                font-size: 2rem;
                margin-bottom: 0.7rem;
            }
            .feature-label {
                font-weight: 500;
                color: #1a3c6e;
                font-size:1.07rem;
            }
            .tech-tag-container {
                display: flex;
                flex-wrap: wrap;
                gap: 0.53rem;
                margin-top: 1.3rem;
            }
            .tech-tag {
                background: #e0f2fe;
                color: #0369a1;
                padding: 0.45rem 1.12rem;
                border-radius: 18px;
                font-weight: 500;
                font-size: 0.97rem;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                transition: all 0.17s;
            }
            .tech-tag:hover {
                transform: translateY(-2px) scale(1.045);
                box-shadow: 0 5px 14px rgba(0,0,0,0.08);
                background: #bae6fd;
            }
            .dev-profile {
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.47rem;
                margin-top: 0.3rem;
                margin-bottom: 0.7rem;
            }
            .dev-avatar {
                width: 74px;
                height: 74px;
                border-radius: 50%;
                object-fit: cover;
                margin-bottom: 0.5rem;
                border: 3px solid #c6dbf5;
            }
            .dev-name {
                font-size: 1.19rem;
                font-weight: 700;
                color: #15386a;
                margin-bottom: 0.18rem;
            }
            .dev-role {
                font-size: 1.03rem;
                color: #1a3c6e;
                font-weight: 500;
                margin-bottom: 0.19rem;
            }
            .dev-links {
                display: flex;
                gap: 1.4rem;
                margin-top: 0.5rem;
            }
            .dev-link {
                color: #1a3c6e;
                font-weight: 500;
                font-size: 1.01rem;
                text-decoration: none;
                background: #e8f1fb;
                padding: 0.41rem 1.03rem;
                border-radius: 19px;
                border: 1px solid #b2c5df;
                transition: all 0.16s;
            }
            .dev-link:hover {
                background: #e0eaff;
                color: #356aad;
            }
            .footer {
                text-align: center;
                padding: 1.2rem 1.1rem 1.1rem 1.2rem;
                color: #64748b;
                font-size: 0.94rem;
                margin-top: 1.1rem;
                background: #f8fafc;
                border-radius: 13px;
                border: 1px solid #e2e8f0;
            }
            .platform-overview ul {
                padding-left: 1.5rem;
                margin-top: 0.88rem;
            }
            .platform-overview li {
                margin-bottom: 0.56rem;
                line-height: 1.6;
                position: relative;
            }
            .platform-overview li:before {
                content: "•";
                color: #1a3c6e;
                font-weight: bold;
                display: inline-block; 
                width: 1em;
                margin-left: -1em;
            }
        </style>
        """, unsafe_allow_html=True)

        # ===== HEADER =====
        st.markdown("""
        <div class="about-header">
            <div class="about-title">ℹ️ About ProMedia Insight</div>
            <div class="about-subtitle">
                Platform media analytics berbasis AI & ML untuk insight konten, sentimen, dan proyeksi tren media secara real-time.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== PLATFORM OVERVIEW =====
        st.markdown("""
        <div class="about-card platform-overview">
            <div class="card-title">📊 Platform Overview</div>
            <p><b>ProMedia Insight Hub</b> adalah solusi dashboard <b>end-to-end</b> untuk pemantauan, analisis, dan proyeksi data media berbasis AI/ML — cocok untuk organisasi, brand, maupun individu yang ingin:</p>
            <ul>
                <li>Melihat <b>tren & distribusi konten</b> dari berbagai sumber</li>
                <li>Memahami <b>sentimen publik</b> terhadap isu/topik</li>
                <li>Identifikasi <b>sumber, topik, dan periode paling berpengaruh</b></li>
                <li>Mendapatkan <b>analisis & insight otomatis</b> dari AI</li>
                <li>Melakukan <b>forecast & prediksi tren masa depan</b></li>
            </ul>
            <div style="margin-top:1.25rem;color:#3b466b;font-size:1.04rem;">
                Semua fitur didesain mudah digunakan, tampilan <b>profesional dan modern</b> (cocok portofolio/magang), dan dapat dikembangkan lebih lanjut.
            </div>
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
                </div>
                <div class="feature-card">
                    <div class="feature-value">📤</div>
                    <div class="feature-label">Upload & Manajemen Data</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">📈</div>
                    <div class="feature-label">Distribusi & Tren Berita</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">😊</div>
                    <div class="feature-label">Analisis Sentimen Otomatis</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">📰</div>
                    <div class="feature-label">Topik & Sumber Terpopuler</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">🔮</div>
                    <div class="feature-label">Forecasting Tren Masa Depan</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">🧠</div>
                    <div class="feature-label">AI Data Lab / Chat AI</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">💡</div>
                    <div class="feature-label">Insight & Rekomendasi Strategis</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">🔐</div>
                    <div class="feature-label">Multi-user & Authentication</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== TECHNOLOGY STACK =====
        st.markdown("""
        <div class="about-card">
            <div class="card-title">🛠️ Technology Stack</div>
            <p>Dikembangkan dengan teknologi modern, modular, dan scalable:</p>
            <div class="tech-tag-container">
                <span class="tech-tag">Python 3.11</span>
                <span class="tech-tag">Streamlit</span>
                <span class="tech-tag">Plotly Express</span>
                <span class="tech-tag">Pandas</span>
                <span class="tech-tag">Numpy</span>
                <span class="tech-tag">Scikit-learn</span>
                <span class="tech-tag">SQLite</span>
                <span class="tech-tag">Gemini AI</span>
                <span class="tech-tag">OpenAI</span>
                <span class="tech-tag">NLP & ML</span>
                <span class="tech-tag">Responsive UI</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== DEVELOPER PROFILE =====
        st.markdown("""
        <div class="about-card">
            <div class="card-title">👨‍💻 Developer</div>
            <div class="dev-profile">
                <img src="https://ui-avatars.com/api/?name=Rafif+Sudanta&background=e8f1fb&color=1a3c6e&size=256" class="dev-avatar"/>
                <div class="dev-name">Rafif Sudanta</div>
                <div class="dev-role">Data & AI Application Developer</div>
                <div class="dev-links">
                    <a class="dev-link" href="https://github.com/rafifsudanta/promedia-insight" target="_blank">GitHub Repo</a>
                    <a class="dev-link" href="https://www.linkedin.com/in/rafifsudanta/" target="_blank">LinkedIn</a>
                </div>
            </div>
            <div style="margin-top:1rem;font-size:0.99rem;color:#4b5563;text-align:center;">
                Untuk kolaborasi, magang, atau konsultasi dashboard & AI, silakan hubungi saya via LinkedIn!
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===== FOOTER =====
        st.markdown("""
        <div class="footer">
            <p>© 2024 ProMedia Insight Hub. Developed by Rafif Sudanta.</p>
            <p style="margin-top: 0.5rem;">Versi 2.0 | <a href="https://github.com/rafifsudanta/promedia-insight" style="color: #3b82f6; text-decoration: none;" target="_blank">GitHub Repo</a> | <a href="https://www.linkedin.com/in/rafifsudanta/" style="color: #3b82f6; text-decoration: none;" target="_blank">LinkedIn</a></p>
        </div>
        """, unsafe_allow_html=True)
