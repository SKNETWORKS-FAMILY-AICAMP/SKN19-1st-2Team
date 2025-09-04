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

    # st.text(
    #     f"연령대 : {age_group}, 지역 : {region}, 차종 : {car_type}, 성별 : {gender}, 브랜드 : {brand_preference}, 예산 : {budget_million}만원"
    # )

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
            # ---------- 1) 가격 범위 단계적 완화 ----------
            pads_million = [500, 1000, 2000]  # ±50/100/2000만원
            rows = []
            used_pad = None

            # 부분일치 허용(대소문자 무시)
            maker_like = f"%{brand_preference.strip()}%" if brand_preference else "%"

            ## SUV 등 간단 매칭
            if car_type:
                car_type_like = (
                    "%suv%" if car_type.upper() == "SUV" else f"%{car_type.strip()}%"
                )
            else:
                car_type_like = "%"

            base_query = """
                SELECT car_id, comp_name, model_name, model_price, model_type, img_url
                FROM car
                WHERE model_price BETWEEN %s AND %s
                ORDER BY
                    ABS(model_price - %s) ASC,
                    CASE WHEN comp_name = %s OR LOWER(comp_name) LIKE LOWER(%s) THEN 0 ELSE 1 END,
                    CASE WHEN LOWER(model_type) LIKE LOWER(%s) OR model_type = %s THEN 0 ELSE 1 END,
                    STR_TO_DATE(launch_date, '%%Y%%m%%d') DESC
                LIMIT %s
            """

            for pad in pads_million:
                min_price = max(0, (budget_million - pad) * 10000)
                max_price = (budget_million + pad) * 10000
                target_price = (min_price + max_price) // 2

                # ✅ 플레이스홀더 8개에 정확히 맞춘 순서
                params = (
                    min_price,  # WHERE BETWEEN %s
                    max_price,  # WHERE BETWEEN %s
                    target_price,  # ABS(model_price - %s)
                    brand_preference,  # comp_name = %s
                    maker_like,  # LOWER(comp_name) LIKE LOWER(%s)
                    car_type_like,  # LOWER(model_type) LIKE LOWER(%s)
                    car_type,  # model_type = %s
                    30,  # LIMIT %s
                )

                cursor.execute(base_query, params)
                rows = cursor.fetchall()
                if rows:
                    used_pad = pad
                    break

            # ---------- 2) 스코어링(마지막 완화 단계) ----------
            if not rows:
                # 가격 범위 밖도 점수 페널티로 하단에 노출
                # - 가격: 범위 안 0점 / 밖이면 100 + 차이
                # - 제조사 불일치 +10, 차종 불일치 +5
                # - maker/type 부분일치도 인정
                pad = 2000  # 기준 범위(±2000만원)로 점수화 지표
                min_price = max(0, (budget_million - pad) * 10000)
                max_price = (budget_million + pad) * 10000
                target_price = (min_price + max_price) // 2

                scoring_query = """
                    SELECT
                        c.car_id,
                        c.comp_name,
                        c.model_name,
                        c.model_price,
                        c.model_type,
                        c.img_url,
                        (CASE
                            WHEN c.model_price BETWEEN %s AND %s THEN 0
                            ELSE 100 + ABS(c.model_price - %s)
                        END)
                        + (CASE WHEN c.comp_name = %s OR LOWER(c.comp_name) LIKE LOWER(%s) THEN 0 ELSE 10 END)
                        + (CASE WHEN LOWER(c.model_type) LIKE LOWER(%s) OR c.model_type = %s THEN 0 ELSE 5 END)
                        AS score
                    FROM car c
                    ORDER BY score ASC, STR_TO_DATE(c.launch_date, '%%Y%%m%%d') DESC
                    LIMIT %s
                """
                params = (
                    min_price,
                    max_price,
                    target_price,
                    brand_preference,
                    maker_like or "",
                    car_type_like or "",
                    car_type,
                    30,
                )
                cursor.execute(scoring_query, params)
                rows = cursor.fetchall()

            # ---------- 3) 결과 출력 ----------
            if not rows:
                st.warning(
                    "조건에 맞는 차량이 없습니다. 예산 슬라이더를 조금 더 넓혀보거나, 브랜드/차종을 바꿔보세요."
                )
            else:
                df = pd.DataFrame(
                    rows,
                    columns=[col[0] for col in cursor.description],  # 컬럼 자동 반영
                )

                # 보기 좋게 가공
                if "model_price" in df.columns:
                    df["가격(만원)"] = (
                        pd.to_numeric(df["model_price"], errors="coerce") // 10000
                    ).astype("Int64")

                title = "🎉 추천 결과"
                if used_pad is not None:
                    title += f"  (예산 ±{used_pad}만원 범위)"
                else:
                    title += "  (완화 매칭: 스코어 순)"

                st.subheader(title)
                display_cols = [
                    c
                    for c in [
                        "comp_name",
                        "model_name",
                        "model_type",
                        "가격(만원)",
                        "img_url",
                    ]
                    if c in df.columns
                ]
                st.dataframe(df[display_cols], use_container_width=True)

        except Exception as e:
            st.error(f"추천 중 오류가 발생했습니다: {e}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
