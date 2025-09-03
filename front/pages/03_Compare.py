"""
차량 비교 페이지
최대 3개 차량 비교 (제원·가격·안전등급 등)
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="차량 비교 - DOCHICHA.Inc",
    page_icon="⚖️"
)

def main():
    st.title("⚖️ 차량 비교")
    st.markdown("최대 3개 차량을 비교하여 최적의 선택을 하세요.")
    
    # 차량 선택
    st.subheader("🚗 비교할 차량 선택")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**차량 1**")
        car1_brand = st.selectbox("브랜드", ["현대", "기아", "쉐보레", "르노삼성", "쌍용"], key="car1_brand")
        car1_model = st.text_input("차량명", key="car1_model", placeholder="예: 아반떼")
    
    with col2:
        st.markdown("**차량 2**")
        car2_brand = st.selectbox("브랜드", ["현대", "기아", "쉐보레", "르노삼성", "쌍용"], key="car2_brand")
        car2_model = st.text_input("차량명", key="car2_model", placeholder="예: 소나타")
    
    with col3:
        st.markdown("**차량 3**")
        car3_brand = st.selectbox("브랜드", ["현대", "기아", "쉐보레", "르노삼성", "쌍용"], key="car3_brand")
        car3_model = st.text_input("차량명", key="car3_model", placeholder="예: 투싼")
    
    # 비교 버튼
    if st.button("⚖️ 비교하기", type="primary"):
        # TODO: 실제 비교 로직 구현
        st.success("비교 기능이 곧 구현될 예정입니다!")
        
        # 임시 비교 결과
        st.subheader("📊 비교 결과")
        
        comparison_data = pd.DataFrame({
            "항목": ["가격(만원)", "연비(km/L)", "안전등급", "배기량(cc)", "연료", "출시년도"],
            "차량 1": [2000, 15.2, "5성급", 1600, "가솔린", 2023],
            "차량 2": [3000, 12.8, "5성급", 2000, "가솔린", 2023],
            "차량 3": [2500, 13.5, "4성급", 1800, "디젤", 2022]
        })
        
        st.dataframe(comparison_data, use_container_width=True)
        
        # 좋아요 기능
        st.subheader("👍 선호도")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👍 차량 1 좋아요", key="like1"):
                st.success("차량 1에 좋아요를 눌렀습니다!")
        
        with col2:
            if st.button("👍 차량 2 좋아요", key="like2"):
                st.success("차량 2에 좋아요를 눌렀습니다!")
        
        with col3:
            if st.button("👍 차량 3 좋아요", key="like3"):
                st.success("차량 3에 좋아요를 눌렀습니다!")

if __name__ == "__main__":
    main()
