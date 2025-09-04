"""
추천 페이지
사용자 입력(연령대, 지역, 차종, 예산) 기반 맞춤형 추천
"""

import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from back.db.kmj.db_config import get_conn

conn = get_conn()
cursor = conn.cursor()

# query = "SELECT * FROM vehicle_reg WHERE 1=1"

st.set_page_config(page_title="맞춤 추천 - DOCHICHA.Inc", page_icon="💡")


def main():
    st.title("💡 맞춤 추천")
    st.markdown("연령대, 지역, 차종, 예산을 입력하여 맞춤형 차량을 추천받으세요.")

    # 사용자 정보 입력
    st.subheader("📝 사용자 정보")

    col1, col2 = st.columns(2)

    with col1:
        age_group = st.selectbox(
            "연령대", ["20대", "30대", "40대", "50대", "60대 이상"]
        )
        region = st.selectbox(
            "지역",
            [
                "서울",
                "경기",
                "인천",
                "부산",
                "대구",
                "광주",
                "대전",
                "울산",
                "세종",
                "기타",
            ],
        )
        budget = st.slider("예산 (만원)", 1000, 10000, 3000)

    with col2:
        car_type = st.selectbox("선호 차종", ["승용차", "SUV", "트럭", "버스"])
        gender = st.selectbox("성별", ["남성", "여성"])
        brand_preference = st.selectbox(
            "선호 브랜드", ["현대", "기아", "쉐보레", "르노삼성", "쌍용"]
        )
    st.text(
        f"{age_group}, {region}, {car_type}, {gender}, {brand_preference}, {budget}"
    )

    # 추천 버튼
    if st.button("🎯 추천받기", type="primary"):
        # TODO: 실제 추천 알고리즘 구현
        st.success("추천 기능이 곧 구현될 예정입니다!")

        # 임시 추천 결과
        st.subheader("🎉 추천 결과")

        recommended_cars = pd.DataFrame(
            {
                "차량명": ["아반떼", "소나타", "투싼"],
                "브랜드": ["현대", "현대", "현대"],
                "가격(만원)": [2000, 3000, 2500],
                "추천 점수": [95, 88, 82],
                "추천 이유": [
                    "예산에 맞고 연령대에 적합",
                    "안전등급이 높고 연비가 우수",
                    "SUV 차종으로 가족용에 적합",
                ],
            }
        )

        st.dataframe(recommended_cars, use_container_width=True)


cursor.close()
conn.close()

if __name__ == "__main__":
    main()
