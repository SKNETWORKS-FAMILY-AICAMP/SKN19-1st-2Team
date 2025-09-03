# front/pages/03_Compare.py
"""
⭐ 열람 페이지에서 담은 모델만 비교하는 페이지
- 썸네일 행 + 스펙 비교표(세로=항목, 가로=모델)
- '차이만 보기' 토글, 개별 제거/전체 비우기, CSV 다운로드
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime

st.set_page_config(
    page_title="차량 비교 - DOCHICHA.Inc",
    page_icon="⚖️",
    layout="wide",
)

# -------------------------------
# 세션 보장
# -------------------------------
def ensure_session():
    if "favorites" not in st.session_state:
        st.session_state.favorites = set()

# -------------------------------
# 데이터 로더 (공용 모듈 있으면 사용, 없으면 폴백)
# -------------------------------
def _fallback_load_cars():
    # 02_Recommend.py에서 사용한 예시 스키마와 동일
    return pd.DataFrame([
        {
            "모델ID": 132067,
            "차량명": "더 뉴 캐스퍼",
            "브랜드": "현대",
            "차종": "경형 SUV",
            "연료": "가솔린",
            "가격_min(만원)": 1450,
            "가격_max(만원)": 2107,
            "출시일자": date(2026, 7, 15),
            "이미지": "https://cdn.aictimg.com/newcar/model/202410/132067.png",
        },
        {
            "모델ID": 999001,
            "차량명": "아반떼",
            "브랜드": "현대",
            "차종": "승용차",
            "연료": "가솔린",
            "가격_min(만원)": 2000,
            "가격_max(만원)": 2500,
            "출시일자": date(2023, 3, 1),
            "이미지": "https://cdn.aictimg.com/newcar/model/202410/132067.png",
        },
        {
            "모델ID": 999002,
            "차량명": "소나타",
            "브랜드": "현대",
            "차종": "승용차",
            "연료": "하이브리드",
            "가격_min(만원)": 3000,
            "가격_max(만원)": 3800,
            "출시일자": date(2024, 2, 20),
            "이미지": "https://cdn.aictimg.com/newcar/model/202410/132067.png",
        },
        {
            "모델ID": 999003,
            "차량명": "투싼",
            "브랜드": "현대",
            "차종": "SUV",
            "연료": "가솔린",
            "가격_min(만원)": 2500,
            "가격_max(만원)": 3200,
            "출시일자": date(2023, 8, 1),
            "이미지": "https://cdn.aictimg.com/newcar/model/202410/132067.png",
        },
        {
            "모델ID": 999004,
            "차량명": "스포티지",
            "브랜드": "기아",
            "차종": "SUV",
            "연료": "하이브리드",
            "가격_min(만원)": 3100,
            "가격_max(만원)": 3600,
            "출시일자": date(2024, 4, 15),
            "이미지": "https://cdn.aictimg.com/newcar/model/202410/132067.png",
        },
        {
            "모델ID": 999005,
            "차량명": "EV6",
            "브랜드": "기아",
            "차종": "SUV",
            "연료": "전기",
            "가격_min(만원)": 4800,
            "가격_max(만원)": 6300,
            "출시일자": date(2022, 11, 11),
            "이미지": "https://cdn.aictimg.com/newcar/model/202410/132067.png",
        },
    ])

@st.cache_data(show_spinner=False)
def load_cars():
    # 프로젝트에 공용 모듈이 있다면 사용 (없으면 폴백)
    try:
        from front.components.data import load_cars as _load  # 필요 시 경로 조정
        return _load()
    except Exception:
        return _fallback_load_cars()

# -------------------------------
# 유틸
# -------------------------------
def fmt_price(min_won, max_won):
    try:
        lo, hi = int(min_won), int(max_won)
    except Exception:
        lo = hi = int(min_won)
    return f"{lo:,}만원" if lo == hi else f"{lo:,}~{hi:,}만원"

# -------------------------------
# 렌더링
# -------------------------------
ensure_session()
sel = list(st.session_state.favorites)

st.title("⚖️ 차량 비교")
st.caption("열람 페이지에서 ⭐로 담은 모델만 불러와 나란히 비교해요.")

top_l, top_r = st.columns([1, 1])
with top_l:
    st.markdown(f"**담긴 모델:** {len(sel)}대")
    try:
        # 당신의 구조에서 Recommend는 pages/02_Recommend.py 입니다.
        st.page_link("pages/02_Recommend.py", label="← 열람 페이지로 돌아가기")
    except Exception:
        pass
with top_r:
    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("🧹 전체 비우기", use_container_width=True):
            st.session_state.favorites.clear()
            st.rerun()
    with c2:
        # CSV 다운로드 버튼은 표 생성 후 렌더
        pass

if len(sel) == 0:
    st.info("열람 페이지에서 '☆ 비교 담기'를 눌러 모델을 먼저 담아주세요.")
    st.stop()

cars = load_cars()
cols_need = ["모델ID", "차량명", "브랜드", "차종", "연료",
             "가격_min(만원)", "가격_max(만원)", "출시일자", "이미지"]
missing_cols = [c for c in cols_need if c not in cars.columns]
if missing_cols:
    st.error(f"데이터에 필요한 컬럼이 없습니다: {missing_cols}")
    st.stop()

df = cars[cars["모델ID"].isin(sel)][cols_need].copy()
if df.empty:
    st.warning("선택한 모델을 찾지 못했습니다. (모델ID/데이터 확인)")
    st.stop()

# 선택 칩(개별 제거)
st.markdown("#### 선택된 모델")
chips = st.columns(len(df))
for col, (_, row) in zip(chips, df.iterrows()):
    with col:
        if st.button(f"❌ {row['차량명']}", key=f"rm_{row['모델ID']}", use_container_width=True):
            st.session_state.favorites.remove(row["모델ID"])
            st.rerun()

# 썸네일 행
st.markdown("---")
thumb_cols = st.columns(len(df))
for col, (_, row) in zip(thumb_cols, df.iterrows()):
    with col:
        st.image(row["이미지"], use_container_width=True)
        st.markdown(f"**{row['차량명']}**")
        st.caption(f"{row['브랜드']} · {row['차종']} · {row['연료']}")

# 비교표 준비
tbl = df.copy()
tbl["가격"] = tbl.apply(lambda r: fmt_price(r["가격_min(만원)"], r["가격_max(만원)"]), axis=1)
tbl["출시일"] = tbl["출시일자"].apply(lambda d: d.strftime("%Y-%m-%d"))

view = (
    tbl[["차량명", "브랜드", "차종", "연료", "가격", "출시일"]]
    .set_index("차량명")
    .T
)

# 차이만 보기
st.markdown("### 스펙 비교")
diff_only = st.toggle("차이만 보기", value=False, help="모든 모델이 동일한 항목은 숨깁니다.")
if diff_only:
    mask = view.nunique(axis=1) > 1
    view_to_show = view[mask]
    if view_to_show.empty:
        st.info("서로 다른 항목이 없습니다. 모든 값이 동일합니다.")
        view_to_show = view
else:
    view_to_show = view

# 표 & 다운로드
st.dataframe(view_to_show, use_container_width=True)

csv = view_to_show.to_csv(encoding="utf-8-sig")
st.download_button(
    "CSV 다운로드",
    data=csv,
    file_name=f"DOCHICAR_compare_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv",
    use_container_width=True,
)
