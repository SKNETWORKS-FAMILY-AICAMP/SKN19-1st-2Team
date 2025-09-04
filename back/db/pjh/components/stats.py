"""
DOCHICAR 통계 컴포넌트
"""
import streamlit as st

def render_stats():
    """DOCHICAR 현황 통계 렌더링"""
    
    st.markdown("""
    <style>
    .stats-section {
        margin: 3rem 0;
    }
    
    .stats-title {
        color: #000000;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    .stat-number {
        color: #000000;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.3);
    }
    
    .stat-label {
        color: #000000;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="stats-title">📊 DOCHICAR 현황</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">2,847</div>
            <div class="stat-label">등록 차량</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">15,234</div>
            <div class="stat-label">활성 사용자</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">8,921</div>
            <div class="stat-label">정비소 파트너</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">98%</div>
            <div class="stat-label">만족도</div>
        </div>
        """, unsafe_allow_html=True)

def render_footer():
    """푸터 렌더링"""
    
    st.markdown("""
    <style>
    .footer {
        background-color: #000000;
        color: #FFFFFF;
        padding: 2rem 0;
        text-align: center;
        margin-top: 4rem;
        border-radius: 20px 20px 0 0;
    }
    
    .footer-content {
        color: #FFFFFF;
        font-size: 1rem;
        margin: 0;
    }
    
    .footer-tagline {
        color: #FFD700;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <p class="footer-content">© 2025 DOCHICAR Inc. | 팀 따봉도치</p>
        <p class="footer-tagline">도로 위 새로운 시작, 당신의 첫 차를 만나는 곳</p>
    </div>
    """, unsafe_allow_html=True)
