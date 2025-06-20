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
        <div class="card">
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
        <div class="card">
            <div class="card-title">✨ Key Features</div>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value">📊</div>
                    <div class="metric-label">Dashboard Overview</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">📤</div>
                    <div class="metric-label">Data Management</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">🧠</div>
                    <div class="metric-label">AI Analytics</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">💡</div>
                    <div class="metric-label">Insights Repository</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">👥</div>
                    <div class="metric-label">Multi-user</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <div class="card-title">🛠️ Technology Stack</div>
            <p>Aplikasi ini dibangun dengan teknologi terkini:</p>
            
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
                <span style="background: #e0f2fe; padding: 0.25rem 0.75rem; border-radius: 50px;">Python</span>
                <span style="background: #e0f2fe; padding: 0.25rem 0.75rem; border-radius: 50px;">Streamlit</span>
                <span style="background: #e0f2fe; padding: 0.25rem 0.75rem; border-radius: 50px;">Google Gemini AI</span>
                <span style="background: #e0f2fe; padding: 0.25rem 0.75rem; border-radius: 50px;">SQLite</span>
                <span style="background: #e0f2fe; padding: 0.25rem 0.75rem; border-radius: 50px;">Plotly</span>
                <span style="background: #e0f2fe; padding: 0.25rem 0.75rem; border-radius: 50px;">Pandas</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="card">
            <div class="card-title">👨‍💻 Development Team</div>
            <p>Platform ini dikembangkan oleh tim profesional:</p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 1rem;">
                <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px;">
                    <h4 style="margin:0; color:#1a3c6e;">John Doe</h4>
                    <p style="margin:0; color:#4a6fa5;">Lead Data Scientist</p>
                </div>
                <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px;">
                    <h4 style="margin:0; color:#1a3c6e;">Jane Smith</h4>
                    <p style="margin:0; color:#4a6fa5;">Full-stack Developer</p>
                </div>
                <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px;">
                    <h4 style="margin:0; color:#1a3c6e;">Robert Johnson</h4>
                    <p style="margin:0; color:#4a6fa5;">UI/UX Designer</p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <p style="text-align: center; color: #95a5a6;">© 2024 ProMedia Insight Hub. Hak Cipta Dilindungi.</p>
        </div>
        """, unsafe_allow_html=True)
