import streamlit as st

def show(tab):
    with tab:
        st.markdown("""
        <div class="section">
            <h2 class="section-title">ℹ️ About ProMedia Insight</h2>
            <p>Informasi tentang platform dan tim pengembang</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card about-card">
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
        
        st.markdown("""
        <div class="card about-card">
            <div class="card-title">✨ Key Features</div>
            <div class="metric-grid feature-grid">
                <div class="metric-card feature-card">
                    <div class="metric-value feature-value">📊</div>
                    <div class="metric-label feature-label">Dashboard Overview</div>
                </div>
                <div class="metric-card feature-card">
                    <div class="metric-value feature-value">📤</div>
                    <div class="metric-label feature-label">Data Management</div>
                </div>
                <div class="metric-card feature-card">
                    <div class="metric-value feature-value">🧠</div>
                    <div class="metric-label feature-label">AI Analytics</div>
                </div>
                <div class="metric-card feature-card">
                    <div class="metric-value feature-value">💡</div>
                    <div class="metric-label feature-label">Insights Repository</div>
                </div>
                <div class="metric-card feature-card">
                    <div class="metric-value feature-value">👥</div>
                    <div class="metric-label feature-label">Multi-user</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card about-card">
            <div class="card-title">🛠️ Technology Stack</div>
            <p>Aplikasi ini dibangun dengan teknologi terkini:</p>
            
            <div style="margin-top: 1rem;">
                <span class="tech-tag">Python</span>
                <span class="tech-tag">Streamlit</span>
                <span class="tech-tag">Google Gemini AI</span>
                <span class="tech-tag">SQLite</span>
                <span class="tech-tag">Plotly</span>
                <span class="tech-tag">Pandas</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card about-card">
            <div class="card-title">👨‍💻 Development Team</div>
            <p>Platform ini dikembangkan oleh tim profesional:</p>
            
            <div class="team-grid">
                <div class="team-member">
                    <h4>John Doe</h4>
                    <p>Lead Data Scientist</p>
                </div>
                <div class="team-member">
                    <h4>Jane Smith</h4>
                    <p>Full-stack Developer</p>
                </div>
                <div class="team-member">
                    <h4>Robert Johnson</h4>
                    <p>UI/UX Designer</p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <p style="text-align: center; color: #95a5a6;">© 2024 ProMedia Insight Hub. Hak Cipta Dilindungi.</p>
        </div>
        """, unsafe_allow_html=True)
