"""
DOCHICAR 사이드바 컴포넌트
"""
import streamlit as st

def render_sidebar():
    """DOCHICAR 브랜딩과 네비게이션이 포함된 사이드바 렌더링"""
    
    # 사이드바 스타일링
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #FFD700;
        padding: 1rem;
    }
    
    .sidebar .sidebar-content .block-container {
        padding-top: 0;
    }
    
    .brand-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .brand-logo h1 {
        color: #000000;
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
    }
    
    .brand-tagline {
        color: #000000;
        font-size: 0.9rem;
        margin-top: 0.5rem;
        text-align: center;
    }
    
    .nav-item {
        display: flex;
        align-items: center;
        padding: 0.8rem 1rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        color: #000000;
        text-decoration: none;
        transition: background-color 0.3s;
    }
    
    .nav-item:hover {
        background-color: rgba(255, 255, 255, 0.3);
    }
    
    .nav-item.active {
        background-color: #FFFFFF;
        color: #000000;
        font-weight: bold;
    }
    
    .nav-icon {
        margin-right: 0.8rem;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 브랜드 로고
    st.markdown("""
    <div class="brand-logo">
        <h1>🦔 DOCHICAR</h1>
        <div class="brand-tagline">당신의 첫 차를 만나는 곳</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 네비게이션 메뉴
    nav_items = [
        ("🏠", "Home", "home"),
        ("🚗", "신차 정보", "search"),
        ("⭐", "맞춤 추천", "recommend"),
        ("⚖️", "차량 비교", "compare"),
        ("🔧", "정비소 찾기", "repair"),
        ("❓", "FAQ", "faq")
    ]
    
    # 현재 페이지 확인 (URL 파라미터 또는 세션 상태로)
    current_page = st.session_state.get('current_page', 'home')
    
    for icon, title, page_key in nav_items:
        is_active = current_page == page_key
        active_class = "active" if is_active else ""
        
        if st.button(f"{icon} {title}", key=f"nav_{page_key}", use_container_width=True):
            if page_key == "home":
                st.switch_page("streamlit_app.py")
            elif page_key == "search":
                st.switch_page("pages/01_Search.py")
            elif page_key == "recommend":
                st.switch_page("pages/02_Recommend.py")
            elif page_key == "compare":
                st.switch_page("pages/03_Compare.py")
            elif page_key == "repair":
                st.switch_page("pages/04_Service_Centers.py")
            elif page_key == "faq":
                st.switch_page("pages/05_FAQ.py")
            
            st.session_state.current_page = page_key
            st.rerun()
