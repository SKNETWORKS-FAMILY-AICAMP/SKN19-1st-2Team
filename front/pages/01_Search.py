# front/pages/02_Recommend.py
import streamlit as st
import pandas as pd
from datetime import date
from sqlalchemy import create_engine
from datetime import datetime, date
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

st.set_page_config(
    page_title="차량 열람 - DOCHICHA.Inc",
    page_icon="🚗",
    layout="wide",
)

if "favorites" not in st.session_state:
    st.session_state.favorites = set()

@st.cache_data
@st.cache_data
def load_cars():
    DB_URL = os.getenv("DB_URL", "").strip()
    car_df = None
    fuel_df = None

    def _parse_launch(v):
        if pd.isna(v):
            return pd.NaT
        s = str(v).strip()
        # DB는 YYYYMMDD(8자리) 기준
        if s.isdigit() and len(s) == 8:
            try:
                return datetime.strptime(s, "%Y%m%d").date()
            except Exception:
                return pd.NaT
        # 엑셀 등 다른 포맷도 유연 처리
        try:
            return pd.to_datetime(s).date()
        except Exception:
            return pd.NaT

    # 1) 우선 DB 시도
    if DB_URL:
        try:
            engine = create_engine(DB_URL)
            car_df  = pd.read_sql("SELECT * FROM car", con=engine)
            try:
                fuel_df = pd.read_sql("SELECT model_name, fuel_type FROM fuel", con=engine)
            except Exception:
                fuel_df = pd.DataFrame(columns=["model_name", "fuel_type"])
        except Exception as e:
            st.warning(f"DB 연결 실패로 엑셀로 대체합니다. ({e})")

    # 2) DB가 없거나 실패하면 엑셀 fallback
    if car_df is None:
        for p in ["data/pdy/danawa_car_data1.xlsx", "danawa_car_data1.xlsx"]:
            if os.path.exists(p):
                car_df = pd.read_excel(p)
                break
        if car_df is None:
            st.error("차량 엑셀(danawa_car_data1.xlsx)을 찾을 수 없습니다.")
            return pd.DataFrame()

    if fuel_df is None:
        for p in ["data/pdy/DANAWA_car_fuel_data1.xlsx", "DANAWA_car_fuel_data1.xlsx"]:
            if os.path.exists(p):
                fuel_df = pd.read_excel(p)
                break
        if fuel_df is None:
            fuel_df = pd.DataFrame(columns=["model_name", "fuel_type"])

    # fuel 집계: 모델별 복수 연료 → '가솔린/하이브리드' 형태로 합치기
    if not fuel_df.empty:
        fuel_agg = (fuel_df
                    .dropna(subset=["model_name", "fuel_type"])
                    .groupby("model_name")["fuel_type"]
                    .apply(lambda s: "/".join(sorted(pd.unique(s)))).reset_index())
        fuel_agg.rename(columns={"fuel_type": "연료"}, inplace=True)
        df = car_df.merge(fuel_agg, on="model_name", how="left")
    else:
        df = car_df.copy()
        df["연료"] = df.get("resrc_type", "")

    # Streamlit 카드/필터가 기대하는 컬럼으로 매핑
    out = pd.DataFrame()
    out["모델ID"]        = df.get("car_id", pd.Series(range(1, len(df)+1)))
    out["차량명"]        = df.get("model_name", "")
    out["브랜드"]        = df.get("comp_name", "")
    out["차종"]          = df.get("model_type", "")
    out["연료"]          = df.get("연료", df.get("resrc_type", ""))
    # 단가만 있을 경우 min=max 동일하게 세팅 (단위는 '만원' 기준으로 준비 권장)
    price = df.get("model_price", 0).fillna(0).astype("int64", errors="ignore")
    out["가격_min(만원)"] = price
    out["가격_max(만원)"] = price
    out["이미지"]        = df.get("img_url", "")
    out["브랜드로고"]    = ""  # 현재 UI에서 미사용. 필요 시 매핑 dict로 보강 가능.

    # 날짜 파싱
    out["출시일자"] = df.get("launch_date", "").apply(_parse_launch)
    # 필터/정렬 안정성을 위해 결측/빈 이름 제거
    out = out.dropna(subset=["차량명", "브랜드"]).reset_index(drop=True)

    # 혹시 가격 단위가 '원'이면 여기서 10000으로 나눠서 만원 단위로 변환
    # out["가격_min(만원)"] = (out["가격_min(만원)"] // 10000).astype(int)
    # out["가격_max(만원)"] = (out["가격_max(만원)"] // 10000).astype(int)

    return out


def render_filters(cars: pd.DataFrame):
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
    only_recent = st.checkbox("최근 3년만 보기", value=True)
    return {"brand": brand, "car_type": car_type, "fuel": fuel, "price": price, "sort_key": sort_key, "only_recent": only_recent}

def apply_filters(df: pd.DataFrame, f: dict):
    out = df.copy()
    if f["brand"]:
        out = out[out["브랜드"].isin(f["brand"])]
    if f["car_type"]:
        out = out[out["차종"].isin(f["car_type"])]
    if f["fuel"]:
        out = out[out["연료"].isin(f["fuel"])]
    pmin, pmax = f["price"]
    out = out[(out["가격_min(만원)"] <= pmax) & (out["가격_max(만원)"] >= pmin)]
    if f["only_recent"]:
        cutoff = date.today().replace(year=date.today().year - 3)
        out = out[out["출시일자"] >= cutoff]
    if f["sort_key"] == "출시일 최신순":
        out = out.sort_values("출시일자", ascending=False)
    elif f["sort_key"] == "가격 낮은순":
        out = out.sort_values("가격_min(만원)", ascending=True)
    elif f["sort_key"] == "가격 높은순":
        out = out.sort_values("가격_max(만원)", ascending=False)
    return out

def render_card(item: pd.Series):
    st.markdown(
        """
        <style>
        .car-card {
            border-radius:16px; padding:16px;
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
        }
        .car-title {
            font-weight:800; font-size:1.28rem;
            margin:10px 0 6px; letter-spacing:-0.01em;
        }
        .car-badge {
            display:inline-block; padding:4px 10px;
            border-radius:999px; font-size:0.95rem;
            border:1px solid rgba(255,255,255,0.14);
            margin-right:6px; margin-top:4px;
        }
        .car-spec {
            font-size:1.06rem;
            opacity:0.95; line-height:1.65;
            margin-top:6px;
        }
        .car-card div.stButton > button {
            font-size:0.98rem; padding:0.45rem 0.85rem; border-radius:10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.container():
        st.markdown('<div class="car-card">', unsafe_allow_html=True)
        st.image(item["이미지"], use_container_width=True)
        st.markdown(f'<div class="car-title">{item["차량명"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<span class="car-badge">{item["브랜드"]}</span>'
            f'<span class="car-badge">{item["차종"]}</span>'
            f'<span class="car-badge">{item["연료"]}</span>',
            unsafe_allow_html=True
        )
        min_price = item["가격_min(만원)"] if "가격_min(만원)" in item else item["가격(만원)"]
        max_price = item["가격_max(만원)"] if "가격_max(만원)" in item else item["가격(만원)"]
        lo, hi = int(min_price), int(max_price)
        price_txt = f"{lo:,}만원" if lo == hi else f"{lo:,}~{hi:,}만원"
        release_txt = item["출시일자"].strftime("%Y-%m-%d")
        st.markdown(f'<div class="car-spec">가격: {price_txt}<br/>출시일: {release_txt}</div>', unsafe_allow_html=True)

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

        st.markdown('</div>', unsafe_allow_html=True)

def render_grid(df: pd.DataFrame, cols_per_row: int = 3):
    if df.empty:
        st.info("조건에 맞는 차량이 없어. 필터를 조금 완화해볼래?")
        return
    rows = [df.iloc[i:i+cols_per_row] for i in range(0, len(df), cols_per_row)]
    for chunk in rows:
        cols = st.columns(len(chunk))
        for col, (_, row) in zip(cols, chunk.iterrows()):
            with col:
                render_card(row)

def main():
    st.title("🚗 차량 열람")
    st.markdown("브랜드, 가격, 연료, 차종으로 빠르게 필터링하고 카드에서 이미지와 스펙을 확인해봐.")
    with st.container():
        cnt = len(st.session_state.favorites)
        st.markdown(f"**비교 담긴 모델:** {cnt}대")
        try:
            st.page_link("pages/02_Compare.py", label="↔️ 비교 페이지로 이동", disabled=(cnt < 2))
        except Exception:
            st.caption("비교는 2대 이상 담으면 더 유용해요!")
    cars = load_cars()
    filters = render_filters(cars)
    filtered = apply_filters(cars, filters)
    st.markdown(f"### 🗂️ 검색 결과 (**{len(filtered)}대**)")
    st.caption("카드를 클릭하지 않고도 기본 스펙을 한눈에 볼 수 있어.")
    render_grid(filtered, cols_per_row=3)

if __name__ == "__main__":
    main()
