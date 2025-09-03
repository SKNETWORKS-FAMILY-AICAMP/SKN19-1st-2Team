"""
신차 검색 페이지
차량명, 가격, 차종, 출시일 기준으로 신차를 검색합니다.
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="신차 검색 - DOCHICHA.Inc",
    page_icon="🔍"
)

def main():
    st.title("🔍 신차 검색")
    st.markdown("차량명, 가격, 차종, 출시일 기준으로 신차를 검색하세요.")
    
    # 검색 필터
    col1, col2 = st.columns(2)
    
    with col1:
        car_name = st.text_input("차량명", placeholder="예: 아반떼, 소나타")
        car_type = st.selectbox("차종", ["전체", "승용차", "SUV", "트럭", "버스"])
        price_min = st.number_input("최소 가격 (만원)", min_value=0, value=0)
    
    with col2:
        brand = st.selectbox("브랜드", ["전체", "현대", "기아", "쉐보레", "르노삼성", "쌍용"])
        fuel_type = st.selectbox("연료", ["전체", "가솔린", "디젤", "하이브리드", "전기"])
        price_max = st.number_input("최대 가격 (만원)", min_value=0, value=50000)
    
    # 검색 버튼
    if st.button("🔍 검색", type="primary"):
        # TODO: 실제 검색 로직 구현
        st.success("검색 기능이 곧 구현될 예정입니다!")
        
        # 임시 데이터 표시
        sample_data = pd.DataFrame({
            "차량명": ["아반떼", "소나타", "투싼"],
            "브랜드": ["현대", "현대", "현대"],
            "가격(만원)": [2000, 3000, 2500],
            "차종": ["승용차", "승용차", "SUV"],
            "연료": ["가솔린", "가솔린", "가솔린"]
        })
        st.dataframe(sample_data, use_container_width=True)

if __name__ == "__main__":
    main()
