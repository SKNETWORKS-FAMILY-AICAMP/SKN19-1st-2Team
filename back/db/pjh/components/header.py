"""
DOCHICAR 헤더 컴포넌트
"""
import streamlit as st

def render_header():
    """DOCHICAR 메인 헤더 렌더링"""
    
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 2rem 0;
        text-align: center;
        margin-bottom: 2rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-title {
        color: #000000;
        font-size: 3rem;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.3);
    }
    
    .main-subtitle {
        color: #000000;
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-weight: 500;
    }
    
    .user-info {
        position: absolute;
        top: 1rem;
        right: 1rem;
        color: #000000;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <div class="user-info">👤 Claude</div>
        <h1 class="main-title">도치카 DOCHICAR</h1>
        <p class="main-subtitle">도로 위 새로운 시작, 당신의 첫 차를 만나는 곳</p>
    </div>
    """, unsafe_allow_html=True)

def render_service_cards():
    """서비스 소개 카드들 렌더링"""
    
    st.markdown("""
    <style>
    .service-section {
        margin: 3rem 0;
    }
    
    .section-title {
        color: #000000;
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .service-card {
        background-color: #FFFFFF;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        border: 2px solid #FFD700;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .service-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    .service-icon {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .service-title {
        color: #000000;
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .service-description {
        color: #333333;
        font-size: 1rem;
        text-align: center;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 도치카 브랜드 설명
    st.markdown('<h2 class="section-title">도치카</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon">도</div>
            <div class="service-title">도</div>
            <div class="service-description">도로 위 새로운 시작,<br>당신의 첫 차를 만나는 곳</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon">치</div>
            <div class="service-title">치</div>
            <div class="service-description">치밀하게 모은 데이터로<br>합리적인 선택을 돕고</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon">카</div>
            <div class="service-title">카</div>
            <div class="service-description">카라이프의 즐거움을<br>함께 열어가는 서비스</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 서비스 소개
    st.markdown('<h2 class="section-title">🎯 우리의 서비스</h2>', unsafe_allow_html=True)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon">📊</div>
            <div class="service-title">데이터 기반 추천</div>
            <div class="service-description">연령, 지역, 예산에 맞는<br>최적의 차량을 추천합니다</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon">🔍</div>
            <div class="service-title">상세 비교 분석</div>
            <div class="service-description">최대 3대까지 차량을 비교하여<br>현명한 선택을 도와드립니다</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown("""
        <div class="service-card">
            <div class="service-icon">🔧</div>
            <div class="service-title">정비소 네트워크</div>
            <div class="service-description">전국 정비소 정보를<br>한눈에 확인하세요</div>
        </div>
        """, unsafe_allow_html=True)
