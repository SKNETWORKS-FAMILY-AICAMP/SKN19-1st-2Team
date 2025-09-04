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


st.set_page_config(page_title="맞춤 추천 - DOCHICHA.Inc", page_icon="💡")


def main():
    conn = get_conn()
    cursor = conn.cursor()

    # 연령대 옵션
    age_query = "SELECT DISTINCT age_group FROM vehicle_reg"
    cursor.execute(age_query)
    age_options = [row[0] for row in cursor.fetchall()]

    # 차종 옵션
    car_type_query = """
        SELECT DISTINCT
        CASE
            WHEN LOWER(model_type) LIKE '%suv%' THEN 'SUV'
            WHEN model_type LIKE '%준형%' THEN '준형'
            WHEN model_type LIKE '%대형%' THEN '대형'
            WHEN model_type LIKE '%중형%' THEN '중형'
            ELSE model_type
        END AS model_type
        FROM car
        """
    cursor.execute(car_type_query)
    car_type_options = [row[0] for row in cursor.fetchall()]

    # 지역 옵션
    region_query = "SELECT DISTINCT region FROM vehicle_reg"
    cursor.execute(region_query)
    region_options = [row[0] for row in cursor.fetchall()]

    # 성별 옵션
    gender_query = "SELECT DISTINCT gender FROM vehicle_reg"
    cursor.execute(gender_query)
    gender_options = [row[0] for row in cursor.fetchall()]

    # 제조사 옵션
    brand_query = "SELECT DISTINCT comp_name FROM car"
    cursor.execute(brand_query)
    brand_options = [row[0] for row in cursor.fetchall()]

    st.title("💡 맞춤 추천")
    st.markdown("연령대, 지역, 차종, 예산을 입력하여 맞춤형 차량을 추천받으세요.")

    # 사용자 정보 입력
    st.subheader("📝 사용자 정보")

    col1, col2 = st.columns(2)

    with col1:
        age_group = st.selectbox("연령대", age_options)
        region = st.selectbox(
            "지역",
            region_options,
        )
        budget = st.slider("예산 (만원)", 2000, 10000, 3000)

    with col2:
        car_type = st.selectbox("선호 차종", car_type_options)
        gender = st.selectbox("성별", gender_options)
        brand_preference = st.selectbox("선호 브랜드", brand_options)

    st.text(
        f"연령대 : {age_group}, 지역 : {region}, 차종 : {car_type}, 성별 : {gender}, 브랜드 : {brand_preference}, 예산 : {budget}"
    )
    # 등록현황 테이블에서
    # 사용자가 원하는 제조사와 가격 범위, 차종에 맞는 차량 추천
    # query = "SELECT DISTINCT comp_name FROM car WHERE age_group = %s AND region = %s AND car_type = %s AND gender = %s AND brand_preference = %s AND budget = %s"
    # cursor.execute(
    #     query, (age_group, region, car_type, gender, brand_preference, budget)
    # )

    # # 조회한 결과 값
    # result = cursor.fetchall()
    # st.text(f"{result}")

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
