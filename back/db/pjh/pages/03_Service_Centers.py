"""
정비소 현황 페이지
MySQL의 dochicar.service_center 실데이터 연동
"""

import streamlit as st
import pandas as pd
from sqlalchemy import text
from pathlib import Path
import sys
import os


# 프로젝트 루트를 경로에 추가하여 내부 모듈 import 가능하게 설정
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from back.db.conn import get_engine  # noqa: E402


st.set_page_config(
    page_title="정비소 현황 - DOCHICAR",
    page_icon="🔧"
)


def _fetch_service_types() -> list:
    """DB에서 사용 중인 정비소 유형 목록(type_code)을 조회"""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT DISTINCT COALESCE(NULLIF(TRIM(type_code), ''), '미분류') AS type_code
            FROM service_center
            ORDER BY type_code
        """))
        return [row[0] for row in result]


def _search_service_centers(keyword: str, service_type: str, limit: int = 500) -> pd.DataFrame:
    """서비스센터 검색. 이름/주소에 키워드 LIKE, 유형 필터 적용"""
    engine = get_engine()

    conditions = [
        "(name_ko LIKE :kw OR addr_road LIKE :kw OR addr_jibun LIKE :kw)"
    ]
    params = {"kw": f"%{keyword.strip()}%" if keyword else "%"}

    if service_type and service_type != "전체":
        conditions.append("COALESCE(NULLIF(TRIM(type_code), ''), '미분류') = :tp")
        params["tp"] = service_type

    where_sql = " AND ".join(conditions)

    sql = text(f"""
        SELECT
            name_ko AS 정비소명,
            addr_road AS 도로명주소,
            addr_jibun AS 지번주소,
            phone AS 전화번호,
            COALESCE(NULLIF(TRIM(type_code), ''), '미분류') AS 정비유형,
            lat, lon,
            open_time AS 운영시작,
            close_time AS 운영종료,
            status_code AS 영업상태
        FROM service_center
        WHERE {where_sql}
        ORDER BY name_ko
        LIMIT :limit
    """)

    params["limit"] = int(limit)
    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params=params)
    return df


def main():
    st.title("🔧 정비소 현황")
    st.markdown("도치카 DB에 적재된 실데이터를 검색하고 지도에서 확인하세요.")

    # 필터 영역
    st.subheader("🔍 정비소 검색")

    type_options = ["전체"] + _fetch_service_types()

    col1, col2, col3 = st.columns(3)

    with col1:
        keyword = st.text_input("검색어", placeholder="정비소명, 도로명주소, 지번주소")

    with col2:
        service_type = st.selectbox("정비 유형", options=type_options)

    with col3:
        limit = st.slider("표시 개수", min_value=50, max_value=2000, value=500, step=50)

    # 검색 실행
    if st.button("🔎 검색", type="primary"):
        df = _search_service_centers(keyword=keyword, service_type=service_type, limit=limit)

        st.caption(f"총 {len(df):,}건 표시")
        st.dataframe(df.drop(columns=["lat", "lon"]), use_container_width=True)

        # 지도 표시 (lat/lon이 있는 행만)
        st.subheader("🗺️ 지도")
        map_df = df.dropna(subset=["lat", "lon"]).rename(columns={"lat": "latitude", "lon": "longitude"})
        if not map_df.empty:
            st.map(map_df[["latitude", "longitude"]])
        else:
            st.info("표시할 좌표가 없습니다.")

        # 상세 정보 영역
        st.subheader("📋 정비소 상세 정보")
        if not df.empty:
            selected = st.selectbox("정비소 선택", df["정비소명"].unique())
            row = df[df["정비소명"] == selected].iloc[0]
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"**정비소명**: {row['정비소명']}")
                st.markdown(f"**도로명주소**: {row['도로명주소']}")
                st.markdown(f"**지번주소**: {row['지번주소']}")
                st.markdown(f"**전화번호**: {row.get('전화번호') or '-'}")
            with c2:
                st.markdown(f"**정비유형**: {row['정비유형']}")
                st.markdown(f"**영업상태**: {row.get('영업상태') or '-'}")
                st.markdown(f"**운영시간**: {row.get('운영시작') or '-'} ~ {row.get('운영종료') or '-'}")


if __name__ == "__main__":
    main()
