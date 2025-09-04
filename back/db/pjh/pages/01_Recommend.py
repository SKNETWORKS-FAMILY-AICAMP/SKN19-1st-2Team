# front/pages/02_Recommend.py
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="차량 열람 - DOCHICHA.Inc",
    page_icon="🚗",
    layout="wide",
)

def main():
    st.title("🚗 차량 열람")
    st.markdown("브랜드, 가격, 연료, 차종으로 빠르게 필터링하고 카드에서 이미지와 스펙을 확인해봐.")

        # 담긴 개수/이동 링크 표시
    with st.container():
        cnt = len(st.session_state.favorites)
        st.markdown(f"**비교 담긴 모델:** {cnt}대")
        try:
            # Streamlit 1.32+에서 지원
            st.page_link("pages/02_Compare.py", label="↔️ 비교 페이지로 이동", disabled=(cnt < 2))
        except Exception:
            st.caption("비교는 2대 이상 담으면 더 유용해요!")

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

# ===== 예시 데이터 (실서비스에선 CSV/DB로 교체) =====
@st.cache_data
def load_cars():
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
            "브랜드로고": "https://cdn.aictimg.com/newcar/brand/147763.png",
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
            "브랜드로고": "https://cdn.aictimg.com/newcar/brand/147763.png",
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
            "브랜드로고": "https://cdn.aictimg.com/newcar/brand/147763.png",
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
            "브랜드로고": "https://cdn.aictimg.com/newcar/brand/147763.png",
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
            "브랜드로고": "https://cdn.aictimg.com/newcar/brand/147763.png",
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
            "브랜드로고": "https://cdn.aictimg.com/newcar/brand/147763.png",
        },
    ])

def format_price(min_won, max_won):
    if pd.isna(max_won) or max_won == 0 or max_won == min_won:
        return f"{int(min_won):,}만원"
    return f"{int(min_won):,}~{int(max_won):,}만원"

def render_filters(cars: pd.DataFrame):
    # 상단 한 줄 필터 바
    st.markdown("### 🔍 빠른 필터")
    c1, c2, c3, c4, c5 = st.columns([1.3, 1.3, 1.3, 2.0, 1.2])

    with c1:
        brand = st.multiselect("브랜드", options=sorted(cars["브랜드"].unique().tolist()))
    with c2:
        car_type = st.multiselect("차종", options=sorted(cars["차종"].unique().tolist()))
    with c3:
        fuel = st.multiselect("연료", options=sorted(cars["연료"].unique().tolist()))
    with c4:
        pmin = int(cars["가격_min(만원)"].min())
        pmax = int(cars["가격_max(만원)"].max())
        price = st.slider("가격(만원)", min_value=pmin, max_value=pmax, value=(pmin, pmax))
    with c5:
        sort_key = st.selectbox("정렬", ["출시일 최신순", "가격 낮은순", "가격 높은순"])

    # 최근 3년 토글 (필요하다는 요청 기억!)
    only_recent = st.checkbox("최근 3년만 보기", value=True)

    return {
        "brand": brand,
        "car_type": car_type,
        "fuel": fuel,
        "price": price,
        "sort_key": sort_key,
        "only_recent": only_recent,
    }

def apply_filters(df: pd.DataFrame, f: dict):
    out = df.copy()

    # 멀티 선택
    if f["brand"]:
        out = out[out["브랜드"].isin(f["brand"])]
    if f["car_type"]:
        out = out[out["차종"].isin(f["car_type"])]
    if f["fuel"]:
        out = out[out["연료"].isin(f["fuel"])]

    # 가격 범위 (min~max 어느 쪽이라도 범위에 걸치면 포함)
    pmin, pmax = f["price"]
    out = out[
        (out["가격_min(만원)"] <= pmax) &
        (out["가격_max(만원)"] >= pmin)
    ]

    # 최근 3년
    if f["only_recent"]:
        cutoff = date.today().replace(year=date.today().year - 3)
        out = out[out["출시일자"] >= cutoff]

    # 정렬
    if f["sort_key"] == "출시일 최신순":
        out = out.sort_values("출시일자", ascending=False)
    elif f["sort_key"] == "가격 낮은순":
        out = out.sort_values("가격_min(만원)", ascending=True)
    elif f["sort_key"] == "가격 높은순":
        out = out.sort_values("가격_max(만원)", ascending=False)

    return out

def render_card(item: pd.Series):
    # 카드 한 장 (이미지 + 기본 스펙)
    st.markdown(
         """
        <style>
        .car-card {
            border-radius:16px; padding:16px;
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
        }
        /* 차량명(타이틀) — 더 굵고 크게 */
        .car-title {
            font-weight:800; font-size:1.28rem;   /* 기존 1.05rem → 1.28rem */
            margin:10px 0 6px; letter-spacing:-0.01em;
        }
        /* 배지(브랜드/차종/연료) — 가독성 업 */
        .car-badge {
            display:inline-block; padding:4px 10px;   /* 기존 2px 8px → 4px 10px */
            border-radius:999px; font-size:0.95rem;   /* 기존 0.75rem → 0.95rem */
            border:1px solid rgba(255,255,255,0.14);
            margin-right:6px; margin-top:4px;
        }
        /* 스펙 텍스트(가격/출시일) — 더 크게/턴 */
        .car-spec {
            font-size:1.06rem;            /* 기존 0.92rem → 1.06rem */
            opacity:0.95; line-height:1.65;
            margin-top:6px;
        }
        /* 비교 담기 버튼도 약간 키움 */
        .car-card div.stButton > button {
            font-size:0.98rem; padding:0.45rem 0.85rem; border-radius:10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():
        st.markdown('<div class="car-card">', unsafe_allow_html=True)
        # 이미지
        st.image(item["이미지"], use_container_width=True)
        # 타이틀
        st.markdown(f'<div class="car-title">{item["차량명"]}</div>', unsafe_allow_html=True)
        # 배지 (브랜드/차종/연료)
        st.markdown(
            f'<span class="car-badge">{item["브랜드"]}</span>'
            f'<span class="car-badge">{item["차종"]}</span>'
            f'<span class="car-badge">{item["연료"]}</span>',
            unsafe_allow_html=True
        )

        # ▼▼▼ 여기부터 새로 추가 ▼▼▼

        # 1) 가격/출시일 표기
        #   - 예시 데이터 기준: 가격_min(만원)/가격_max(만원) 컬럼 사용
        #   - 만약 단일 컬럼 "가격(만원)"만 있다면 아래 fallback 코드가 자동으로 처리
        min_price = item["가격_min(만원)"] if "가격_min(만원)" in item else item["가격(만원)"]
        max_price = item["가격_max(만원)"] if "가격_max(만원)" in item else item["가격(만원)"]

        def _fmt_price(lo, hi):
            lo = int(lo)
            hi = int(hi)
            return f"{lo:,}만원" if lo == hi else f"{lo:,}~{hi:,}만원"

        price_txt = _fmt_price(min_price, max_price)
        release_txt = item["출시일자"].strftime("%Y-%m-%d")

        st.markdown(
            f'<div class="car-spec">가격: {price_txt}<br/>출시일: {release_txt}</div>',
            unsafe_allow_html=True
        )

        # 2) ⭐ 비교 담기 토글
        mid = item["모델ID"]
        starred = mid in st.session_state.favorites
        btn_label = "⭐ 비교 담김" if starred else "☆ 비교 담기"
        if st.button(btn_label, key=f"fav_{mid}"):
            if starred:
                st.session_state.favorites.remove(mid)
            else:
                if len(st.session_state.favorites) >= 4:
                    st.warning("비교는 최대 4대까지 담을 수 있어요.")
                else:
                    st.session_state.favorites.add(mid)
            st.rerun()

        # ▲▲▲ 여기까지 새로 추가 ▲▲▲

        # (선택) 상세/비교 버튼은 나중에 연결
        # st.button("비교에 추가", key=f"cmp_{item['모델ID']}")
        st.markdown('</div>', unsafe_allow_html=True)

def render_grid(df: pd.DataFrame, cols_per_row: int = 3):
    # 카드 그리드 배치
    if df.empty:
        st.info("조건에 맞는 차량이 없어. 필터를 조금 완화해볼래?")
        return
    rows = [df.iloc[i:i+cols_per_row] for i in range(0, len(df), cols_per_row)]
    for chunk in rows:
        cols = st.columns(len(chunk))
        for col, (_, row) in zip(cols, chunk.iterrows()):
            with col:
                render_card(row)

    cars = load_cars()
    filters = render_filters(cars)

    # 결과 헤더 + 건수
    filtered = apply_filters(cars, filters)
    st.markdown(f"### 🗂️ 검색 결과 (**{len(filtered)}대**)")
    st.caption("카드를 클릭하지 않고도 기본 스펙을 한눈에 볼 수 있어.")

    # 카드 그리드 렌더
    render_grid(filtered, cols_per_row=3)

if __name__ == "__main__":
    main()


