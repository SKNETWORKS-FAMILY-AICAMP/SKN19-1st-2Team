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
    cursor.execute("SELECT DISTINCT age_group FROM vehicle_reg")
    age_options = [row[0] for row in cursor.fetchall()]

    # 차종 옵션 (간단 매핑 포함)
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
    cursor.execute("SELECT DISTINCT region FROM vehicle_reg")
    region_options = [row[0] for row in cursor.fetchall()]

    # 성별 옵션
    cursor.execute("SELECT DISTINCT gender FROM vehicle_reg")
    gender_options = [row[0] for row in cursor.fetchall()]

    # 제조사 옵션
    cursor.execute("SELECT DISTINCT comp_name FROM car")
    brand_options = [row[0] for row in cursor.fetchall()]

    st.title("💡 맞춤 추천")
    st.markdown("연령대, 지역, 차종, 예산을 입력하여 맞춤형 차량을 추천받으세요.")

    # 사용자 입력
    st.subheader("📝 사용자 정보")

    col1, col2 = st.columns(2)

    with col1:
        age_group = st.selectbox("연령대", age_options)
        region = st.selectbox("지역", region_options)
        budget_million = st.slider("예산 (만원)", 2000, 10000, 3000)  # 만원 단위

    with col2:
        car_type = st.selectbox("선호 차종", car_type_options)
        gender = st.selectbox("성별", gender_options)
        brand_preference = st.selectbox("선호 브랜드", brand_options)

    st.text(
        f"연령대 : {age_group}, 지역 : {region}, 차종 : {car_type}, 성별 : {gender}, 브랜드 : {brand_preference}, 예산 : {budget_million}만원"
    )

    # ====== 핵심: 추천 쿼리 ======
    # 1) 가격 범위(만원 → 원 변환): 예산 ±500만원을 기본 범위로
    price_pad_million = 500
    min_price = max(0, (budget_million - price_pad_million) * 10000)  # 원
    max_price = (budget_million + price_pad_million) * 10000  # 원
    target_price = (min_price + max_price) // 2  # 중앙값

    # 2) 우선순위: 가격(가까울수록) > 제조사 일치 > 차종 일치
    #    - car_type 매핑이 단순화되어 있을 수 있으므로, 일치 비교는 그대로 둡니다.
    query = """
        SELECT car_id, comp_name, model_name, model_price, model_type, img_url
        FROM car
        WHERE model_price BETWEEN %s AND %s
        ORDER BY
            ABS(model_price - %s) ASC,
            CASE WHEN comp_name = %s THEN 0 ELSE 1 END,
            CASE WHEN model_type = %s THEN 0 ELSE 1 END,
            STR_TO_DATE(launch_date, '%%Y%%m%%d') DESC
        LIMIT %s
    """

    # 3) 파라미터 바인딩 (필수!)
    params = (min_price, max_price, target_price, brand_preference, car_type, 30)

    # 추천 버튼
    if st.button("🎯 추천받기", type="primary"):
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()

            if not rows:
                st.warning(
                    "조건에 맞는 차량이 없습니다. 예산 범위를 넓혀보세요 (슬라이더 조정)."
                )
            else:
                # 표로 가공
                df = pd.DataFrame(
                    rows,
                    columns=[
                        "car_id",
                        "브랜드",
                        "차량명",
                        "가격(원)",
                        "차종",
                        "이미지",
                    ],
                )
                # 보기 좋게 만원 단위로 변환 컬럼 추가
                df["가격(만원)"] = (df["가격(원)"] // 10000).astype(int)
                st.subheader("🎉 추천 결과")
                st.dataframe(
                    df[["브랜드", "차량명", "차종", "가격(만원)", "이미지"]],
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"쿼리 실행 중 오류가 발생했습니다: {e}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
