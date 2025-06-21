import streamlit as st

def show(tab):
    with tab:
        # CSS styling
        st.markdown("""
        <style>
            .about-header {
                text-align: center;
                padding: 1.5rem 0;
                border-bottom: 2px solid #1e3a8a;
                margin-bottom: 2rem;
            }
            .about-title {
                font-size: 2.2rem;
                color: #1e3a8a;
                margin-bottom: 0.5rem;
            }
            .about-subtitle {
                font-size: 1.1rem;
                color: #4b5563;
                max-width: 800px;
                margin: 0 auto;
            }
            .about-card {
                background: white;
                border-radius: 12px;
                padding: 1.8rem;
                margin-bottom: 1.5rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
                border: 1px solid #e5e7eb;
                transition: all 0.3s ease;
            }
            .about-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 6px 16px rgba(0,0,0,0.08);
            }
            .card-title {
                font-size: 1.5rem;
                font-weight: 600;
                color: #1e3a8a;
                margin-bottom: 1.2rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 1.2rem;
                margin-top: 1rem;
            }
            .feature-card {
                background: linear-gradient(135deg, #f9fafb, #f0f4f8);
                border-radius: 10px;
                padding: 1.5rem 1rem;
                text-align: center;
                transition: all 0.3s ease;
            }
            .feature-card:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 10px rgba(30, 58, 138, 0.15);
            }
            .feature-value {
                font-size: 2.5rem;
                margin-bottom: 0.8rem;
            }
            .feature-label {
                font-weight: 500;
                color: #1e3a8a;
            }
            .tech-tag {
                display: inline-block;
                background: #e0f2fe;
                color: #0369a1;
                padding: 0.4rem 1rem;
                border-radius: 20px;
                margin: 0.3rem;
                font-weight: 500;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            .team-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-top: 1.5rem;
            }
            .team-member {
                background: #f8fafc;
                border-radius: 12px;
                padding: 1.5rem;
                text-align: center;
                border: 1px solid #e2e8f0;
            }
            .team-member h4 {
                margin-top: 0;
                margin-bottom: 0.5rem;
                color: #1e3a8a;
            }
            .team-member p {
                color: #4b5563;
                margin-bottom: 0;
            }
            .footer {
                text-align: center;
                padding: 1.5rem;
                color: #64748b;
                font-size: 0.9rem;
                margin-top: 1rem;
                background: #f8fafc;
                border-radius: 12px;
            }
            ul {
                padding-left: 1.5rem;
                margin-top: 0.8rem;
            }
            li {
                margin-bottom: 0.6rem;
                line-height: 1.6;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Header section
        st.markdown("""
        <div class="about-header">
            <div class="about-title">ℹ️ About ProMedia Insight</div>
            <div class="about-subtitle">Platform analitik media profesional untuk membantu organisasi memahami performa konten media dan sentimen publik</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Platform Overview
        st.markdown("""
        <div class="about-card">
            <div class="card-title">📊 Platform Overview</div>
            <p><strong>ProMedia Insight Hub</strong> adalah platform analitik media profesional yang dirancang untuk membantu organisasi:</p>
            
            <ul>
                <li>Menganalisis performa konten media</li>
                <li>Memahami sentimen publik</li>
                <li>Mengidentifikasi tren berita</li>
                <li>Membuat prediksi masa depan</li>
                <li>Menghasilkan insight berbasis AI</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Key Features
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
                    <div class="feature-label">Data Management</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">🧠</div>
                    <div class="feature-label">AI Analytics</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">💡</div>
                    <div class="feature-label">Insights Repository</div>
                </div>
                <div class="feature-card">
                    <div class="feature-value">👥</div>
                    <div class="feature-label">Multi-user</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Technology Stack
        st.markdown("""
        <div class="about-card">
            <div class="card-title">🛠️ Technology Stack</div>
            <p>Aplikasi ini dibangun dengan teknologi terkini:</p>
            
            <div style="margin-top: 1.5rem;">
                <span class="tech-tag">Python</span>
                <span class="tech-tag">Streamlit</span>
                <span class="tech-tag">Google Gemini AI</span>
                <span class="tech-tag">SQLite</span>
                <span class="tech-tag">Plotly</span>
                <span class="tech-tag">Pandas</span>
                <span class="tech-tag">NLP</span>
                <span class="tech-tag">Machine Learning</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Development Team
        st.markdown("""
        <div class="about-card">
            <div class="card-title">👨‍💻 Development Team</div>
            <p>Platform ini dikembangkan oleh tim profesional:</p>
            
            <div class="team-grid">
                <div class="team-member">
                    <h4>John Doe</h4>
                    <p>Lead Data Scientist</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">PhD in Machine Learning, 10+ years experience</p>
                </div>
                <div class="team-member">
                    <h4>Jane Smith</h4>
                    <p>Full-stack Developer</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">Specialized in data applications, 8+ years experience</p>
                </div>
                <div class="team-member">
                    <h4>Robert Johnson</h4>
                    <p>UI/UX Designer</p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">Award-winning designer, 12+ years experience</p>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2024 ProMedia Insight Hub. Hak Cipta Dilindungi.</p>
            <p style="margin-top: 0.5rem;">Versi 2.0 | <a href="#" style="color: #3b82f6; text-decoration: none;">Kebijakan Privasi</a> | <a href="#" style="color: #3b82f6; text-decoration: none;">Syarat Penggunaan</a></p>
        </div>
        """, unsafe_allow_html=True)
