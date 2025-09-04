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

    # ===== 단위 자동 감지: 평균값이 100,000(=10만원) 이상이면 '원' 단위로 간주 =====
    cursor.execute("SELECT AVG(model_price) FROM car WHERE model_price IS NOT NULL")
    _avg = cursor.fetchone()[0] or 0
    try:
        price_is_won = float(_avg) >= 100_000
    except Exception:
        price_is_won = True  # 안전빵: 원 단위로 처리
    # ========================================================================

    # --- 옵션 로드 ---
    cursor.execute("SELECT DISTINCT age_group FROM vehicle_reg")
    age_options = [row[0] for row in cursor.fetchall()]

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

    cursor.execute("SELECT DISTINCT region FROM vehicle_reg")
    region_options = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT gender FROM vehicle_reg")
    gender_options = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT comp_name FROM car")
    brand_options = [row[0] for row in cursor.fetchall()]

    # --- UI ---
    st.title("💡 맞춤 추천")
    st.markdown("연령대, 지역, 차종, 예산을 입력하여 맞춤형 차량을 추천받으세요.")

    st.subheader("📝 사용자 정보")
    col1, col2 = st.columns(2)

    with col1:
        age_group = st.selectbox("연령대", age_options)
        region = st.selectbox("지역", region_options)
        budget_million = st.slider("예산 (만원)", 2000, 10000, 3000)

    with col2:
        car_type = st.selectbox("선호 차종", car_type_options)
        gender = st.selectbox("성별", gender_options)
        brand_preference = st.selectbox("선호 브랜드", brand_options)

    # ===== 추천 버튼 =====
    if st.button("🎯 추천받기", type="primary"):
        try:
            # ---------- 1) 가격 범위 계산 (DB 단위에 맞춰 변환) ----------
            pads_million = [500, 1000, 2000]  # 단계적 완화
            rows = []
            used_pad = None

            # 부분일치 허용(대소문자 무시); 빈 값이면 전체 매칭
            maker_like = f"%{brand_preference.strip()}%" if brand_preference else "%"
            if car_type:
                car_type_like = (
                    "%suv%" if car_type.upper() == "SUV" else f"%{car_type.strip()}%"
                )
            else:
                car_type_like = "%"

            # ---------- 2) 기본 정렬 쿼리 (가격 > 제조사 > 차종) ----------
            # !! 트레일링 콤마 제거 & 플레이스홀더 8개에 맞춰 params 구성 !!
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
                # 예산(만원) → DB 단위로 변환
                if price_is_won:
                    min_price = max(0, (budget_million - pad) * 10_000)  # 원
                    max_price = (budget_million + pad) * 10_000
                else:
                    min_price = max(0, (budget_million - pad))  # 만원
                    max_price = budget_million + pad

                target_price = (min_price + max_price) // 2

                params = (
                    min_price,  # BETWEEN
                    max_price,  # BETWEEN
                    target_price,  # ABS(...)
                    brand_preference,  # comp_name = %s
                    maker_like,  # comp_name LIKE
                    car_type_like,  # model_type LIKE
                    car_type,  # model_type =
                    30,  # LIMIT
                )

                cursor.execute(base_query, params)
                rows = cursor.fetchall()
                if rows:
                    used_pad = pad
                    break

            # ---------- 3) 스코어링(최종 완화) ----------
            if not rows:
                pad = 2000
                if price_is_won:
                    min_price = max(0, (budget_million - pad) * 10_000)
                    max_price = (budget_million + pad) * 10_000
                else:
                    min_price = max(0, (budget_million - pad))
                    max_price = budget_million + pad
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
                    maker_like,
                    car_type_like,
                    car_type,
                    30,
                )
                cursor.execute(scoring_query, params)
                rows = cursor.fetchall()

            # ---------- 4) 결과 표시 (DB 값 그대로) ----------
            if not rows:
                st.warning(
                    "조건에 맞는 차량이 없습니다. 예산을 넓히거나 브랜드/차종을 조정해보세요."
                )
            else:
                df = pd.DataFrame(rows, columns=[c[0] for c in cursor.description])

                # DB값 그대로 보여주기 (단위 라벨만 분기)
                price_col_label = "가격(원)" if price_is_won else "가격(만원)"
                df[price_col_label] = pd.to_numeric(df["model_price"], errors="coerce")

                # 보기좋게 문자열 표시도 추가(천단위 콤마)
                df[price_col_label + " 표시"] = df[price_col_label].apply(
                    lambda x: f"{int(x):,}" if pd.notnull(x) else ""
                )

                title = "🎉 추천 결과"
                if used_pad is not None:
                    title += f" (예산 ±{used_pad}만원)"
                else:
                    title += " (완화 매칭: 스코어 순)"

                st.subheader(title)
                show_cols = [
                    c
                    for c in [
                        "comp_name",
                        "model_name",
                        "model_type",
                        price_col_label,
                        price_col_label + " 표시",
                        "img_url",
                    ]
                    if c in df.columns
                ]
                st.dataframe(df[show_cols], use_container_width=True)

        except Exception as e:
            st.error(f"추천 중 오류가 발생했습니다: {e}")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
