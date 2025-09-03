import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="DOCHICAR - 홈",
    page_icon="🦔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일 (HTML 디자인 기반)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    
    /* 사이드바 스타일 */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #FDB813 0%, #FFE082 100%);
        padding: 2rem 1rem;
    }
    
    /* 브랜드 헤더 */
    .brand-header {
        background: linear-gradient(135deg, #FDB813 0%, #FFE082 100%);
        padding: 4rem 3rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(253,184,19,0.3);
    }
    
    .brand-title {
        font-size: 4.5rem;
        font-weight: 900;
        color: #1F1F1F;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -2px;
    }
    
    .brand-subtitle {
        font-size: 1.3rem;
        color: #1F1F1F;
        font-weight: 500;
    }
    
    /* 슬로건 카드 */
    .slogan-card {
        background: white;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #FDB813;
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .slogan-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(253,184,19,0.3);
    }
    
    .slogan-number {
        font-size: 3rem;
        font-weight: 900;
        color: #FDB813;
        margin-bottom: 1rem;
    }
    
    .slogan-text {
        font-size: 1.1rem;
        color: #2C3E50;
        line-height: 1.8;
    }
    
    /* 서비스 카드 */
    .service-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        border: 2px solid transparent;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .service-card:hover {
        border-color: #FDB813;
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(253,184,19,0.3);
    }
    
    .service-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .service-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #1F1F1F;
        margin-bottom: 0.5rem;
    }
    
    .service-desc {
        font-size: 0.95rem;
        color: #7F8C8D;
        line-height: 1.6;
    }
    
    /* 통계 카드 */
    .stat-card {
        background: linear-gradient(135deg, #FDB813 0%, #FFE082 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 15px rgba(253,184,19,0.3);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(253,184,19,0.4);
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 1rem;
        opacity: 0.95;
    }
    
    /* 섹션 타이틀 */
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 2rem;
        color: #1F1F1F;
    }
    
    /* Footer */
    .footer {
        background: #1F1F1F;
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 3rem;
    }
    
    /* 네비게이션 아이템 */
    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        background: rgba(255,255,255,0.2);
        border-radius: 8px;
        color: #1F1F1F;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        background: rgba(255,255,255,0.4);
        transform: translateX(5px);
    }
    
    .nav-item.active {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 사이드바 네비게이션
st.sidebar.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <div style="font-size: 4rem; margin-bottom: 1rem;">🦔</div>
    <div style="font-size: 1.8rem; font-weight: 900; color: #1F1F1F; margin-bottom: 0.5rem;">DOCHICAR</div>
    <div style="font-size: 0.9rem; color: #444;">당신의 첫 차를 만나는 곳</div>
</div>
""", unsafe_allow_html=True)

# 네비게이션 메뉴
nav_items = [
    ("🏠", "Home", True),
    ("🚗", "신차 정보", False),
    ("💡", "맞춤 추천", False),
    ("⚖️", "차량 비교", False),
    ("🗺️", "정비소 찾기", False),
    ("❓", "FAQ", False)
]

for icon, name, active in nav_items:
    active_class = "active" if active else ""
    st.sidebar.markdown(f"""
    <div class="nav-item {active_class}">
        <span style="margin-right: 10px;">{icon}</span>
        <span>{name}</span>
    </div>
    """, unsafe_allow_html=True)

# 메인 콘텐츠
# 브랜드 헤더
st.markdown("""
<div class="brand-header">
    <h1 class="brand-title">도치카 DOCHICAR</h1>
    <p class="brand-subtitle">도로 위 새로운 시작, 당신의 첫 차를 만나는 곳</p>
</div>
""", unsafe_allow_html=True)

# 슬로건 섹션
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="slogan-card">
        <div class="slogan-number">도</div>
        <div class="slogan-text">
            도로 위 새로운 시작,<br>
            당신의 첫 차를 만나는 곳
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="slogan-card">
        <div class="slogan-number">치</div>
        <div class="slogan-text">
            치밀하게 모은 데이터로<br>
            합리적인 선택을 돕고
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="slogan-card">
        <div class="slogan-number">카</div>
        <div class="slogan-text">
            카라이프의 즐거움을<br>
            함께 열어가는 서비스
        </div>
    </div>
    """, unsafe_allow_html=True)

# 서비스 섹션
st.markdown('<h2 class="section-title">🎯 우리의 서비스</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="service-card">
        <div class="service-icon">📊</div>
        <div class="service-title">데이터 기반 추천</div>
        <div class="service-desc">연령, 지역, 예산에 맞는 최적의 차량을 추천합니다</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("맞춤 추천 바로가기", key="svc_recommend", use_container_width=True):
        try:
            st.switch_page("pages/02_Recommend_Beta.py")
        except Exception:
            st.switch_page("pages/02_Recommend.py")

with col2:
    st.markdown("""
    <div class="service-card">
        <div class="service-icon">🔍</div>
        <div class="service-title">상세 비교 분석</div>
        <div class="service-desc">최대 3대까지 차량을 비교하여 현명한 선택을 도와드립니다</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("차량 비교 바로가기", key="svc_compare", use_container_width=True):
        st.switch_page("pages/03_Compare.py")

with col3:
    st.markdown("""
    <div class="service-card">
        <div class="service-icon">🛠️</div>
        <div class="service-title">정비소 네트워크</div>
        <div class="service-desc">전국 정비소 정보를 한눈에 확인하세요</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("정비소 찾기 바로가기", key="svc_repair", use_container_width=True):
        try:
            st.switch_page("pages/04_Service_Centers_Beta.py")
        except Exception:
            st.switch_page("pages/04_Service_Centers.py")

# 통계 섹션
st.markdown('<h2 class="section-title">📈 DOCHICAR 현황</h2>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">2,847</div>
        <div class="stat-label">등록 차량</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">15,234</div>
        <div class="stat-label">활성 사용자</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">8,921</div>
        <div class="stat-label">정비소 파트너</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-value">98%</div>
        <div class="stat-label">만족도</div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>© 2025 DOCHICAR Inc. | 팀 따봉도치 🦔👍</p>
    <p style="opacity: 0.8; font-size: 0.9rem;">도로 위 새로운 시작, 당신의 첫 차를 만나는 곳</p>
</div>
""", unsafe_allow_html=True)
