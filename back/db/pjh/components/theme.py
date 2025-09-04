"""
DOCHICAR 공통 테마/스타일 유틸리티
- 모든 페이지에서 import하여 동일한 스타일을 적용
"""

import streamlit as st


BRAND_COLORS = {
    "yellow": "#FDB813",
    "yellow_light": "#FFE082",
    "black": "#1F1F1F",
    "text_muted": "#7F8C8D",
}


def inject_base_css():
    """브랜드 컬러와 레이아웃 공통 CSS 주입"""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }}

        .sidebar .sidebar-content {{
            background: linear-gradient(180deg, {BRAND_COLORS['yellow']} 0%, {BRAND_COLORS['yellow_light']} 100%);
            padding: 2rem 1rem;
        }}

        .section-title {{
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 2rem;
            color: {BRAND_COLORS['black']};
        }}

        .card {{
            background: white;
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }}

        .stButton > button {{
            background: {BRAND_COLORS['yellow']};
            color: {BRAND_COLORS['black']};
            border: 0;
            border-radius: 10px;
            font-weight: 700;
        }}

        .stButton > button:hover {{
            filter: brightness(0.95);
        }}
    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str | None = None):
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <h1 style="font-size: 2.5rem; font-weight: 800; color: {BRAND_COLORS['black']}; margin-bottom: .3rem;">{title}</h1>
        {f'<p style="color:{BRAND_COLORS['text_muted']}">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


