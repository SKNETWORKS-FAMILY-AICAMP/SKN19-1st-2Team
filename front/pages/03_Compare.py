"""
차량 비교 페이지
최대 3개 차량 비교
"""
import mysql.connector
import streamlit as st
import pandas as pd
from sqlalchemy import text
from pathlib import Path
from datetime import date
import sys

from dotenv import load_dotenv
load_dotenv()
import os
# ------import


#DB 커넥트 객체 생성
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

#STREAMLIT 페이지
st.set_page_config(
    page_title="차량 비교 - DOCHICHA.Inc",
    page_icon="⚖️",
    layout="wide",
)


def main():
    #comparison_data = pd.read_sql("SELECT * FROM car", con=conn)
    # st.dataframe(comparison_data, use_container_width=True)
    
    # fig = comparison_data.plot.pie(
    #     y='model_name',
    #     labels=comparison_data['항목'],
    #     # autopct='%1.1f%%',
    #     figsize=(10,10),
    #     legend = False
    # ).get_figure()      #호출해야 만들어진 pie 차트가 반환이 됨

    # st.pyplot(fig)

    #랜더링
    ensure_session()
    sel = list(st.session_state.favorites)
    sel = [2, 6, 12]

    st.title("⚖️ 차량 비교")
    st.caption("열람 페이지에서 ⭐로 담은 모델을 불러와 비교합니다.")

    top_l, top_r = st.columns([1, 1])
    with top_l:
        st.markdown(f"**담긴 모델:** {len(sel)}대")
        try:
            st.page_link("pages/02_Recommend.py", label="← 열람 페이지로 돌아가기")
        except Exception:
            pass
    with top_r:
        c1, _ = st.columns([1, 1])   # CSV 다운로드 제거 → 오른쪽 칸 비움
        with c1:
            if st.button("🧹 전체 비우기", use_container_width=True):
                st.session_state.favorites.clear()
                st.rerun()

    if len(sel) == 0:
        st.info("열람 페이지에서 '☆ 비교 담기'를 눌러 모델을 먼저 담아주세요.")
        st.stop()

    placeholders = ','.join(['%s'] * len(sel))
    query = f"""SELECT c.car_id, c.model_name, c.img_url, c.launch_date, model_type, model_price, resrc_amount, efficiency_amount, wait_period, GROUP_CONCAT(f.fuel_type SEPARATOR ', ') AS fuel_types
                FROM car c
                LEFT JOIN fuel f ON c.model_name = f.model_name
                WHERE c.car_id IN ({placeholders})
                GROUP BY c.car_id, c.model_name, c.img_url, launch_date, model_type, model_price, resrc_amount, efficiency_amount, wait_period;"""

    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(sel))

    rows = cursor.fetchall()
    cursor.close()

    df = pd.DataFrame(rows)

    st.subheader("즐겨찾기한 차량 비교")

    # 가로로 비교 카드 보여주기
    cols = st.columns(len(df))

    for idx, col in enumerate(cols):
        row = df.iloc[idx]
        with col:
            st.image(row['img_url'], use_container_width=True)
            st.markdown(f"**{row['model_name']} {row['fuel_types']}**")
            st.dataframe(row.drop('img_url'))


# # 비교표 준비
# tbl = df.copy()
# tbl["가격"] = tbl.apply(lambda r: fmt_price(r["가격_min(만원)"], r["가격_max(만원)"]), axis=1)
# tbl["출시일"] = tbl["출시일자"].apply(lambda d: d.strftime("%Y-%m-%d"))

# view = (
#     tbl[["차량명", "브랜드", "차종", "연료", "가격", "출시일"]]
#     .set_index("차량명")
#     .T
# )

# # -------------------------------
# # 세션 보장
# # -------------------------------
def ensure_session():
    if "favorites" not in st.session_state:
        st.session_state.favorites = set()


main()
conn.close()