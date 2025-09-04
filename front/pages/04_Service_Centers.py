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
from datetime import datetime, time


# 프로젝트 루트를 경로에 추가하여 내부 모듈 import 가능하게 설정
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from back.db.conn import get_engine  # noqa: E402


st.set_page_config(
    page_title="정비소 현황 - DOCHICAR",
    page_icon="🔧"
)


def _get_service_type_mapping() -> dict:
    """정비소 유형 코드를 실제 명칭으로 매핑"""
    return {
        1: "자동차종합정비업(1급)",
        2: "소형자동차정비업(2급)", 
        3: "자동차전문정비업(3급)",
        4: "기타",
        99: "미분류"
    }


def _fetch_service_types() -> list:
    """DB에서 사용 중인 정비소 유형 목록을 실제 명칭으로 조회"""
    engine = get_engine()
    type_mapping = _get_service_type_mapping()
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT DISTINCT type_code
            FROM service_center
            WHERE type_code IS NOT NULL
            ORDER BY type_code
        """))
        
        types = []
        for row in result:
            type_code = row[0]
            type_name = type_mapping.get(type_code, f"기타({type_code})")
            types.append((type_code, type_name))
        
        return types


def _get_brand_keywords() -> list:
    """브랜드별 검색 키워드 목록"""
    return [
        "현대", "기아", "르노", "쌍용", "제네시스",
        "벤츠", "BMW", "아우디", "폭스바겐", "볼보",
        "토요타", "혼다", "닛산", "마쓰다", "스바루",
        "포드", "쉐보레", "캐딜락", "링컨", "지프",
        "테슬라", "포르쉐", "재규어", "랜드로버", "미니"
    ]


def _calculate_zoom_level(map_df: pd.DataFrame) -> int:
    """검색 결과의 좌표 분포에 따라 적절한 줌 레벨 계산"""
    if map_df.empty:
        return 6  # 기본 줌 레벨 (전국)
    
    # 위도와 경도의 범위 계산
    lat_min, lat_max = map_df['latitude'].min(), map_df['latitude'].max()
    lon_min, lon_max = map_df['longitude'].min(), map_df['longitude'].max()
    
    # 위도와 경도의 차이 계산
    lat_diff = lat_max - lat_min
    lon_diff = lon_max - lon_min
    
    # 더 큰 차이를 기준으로 줌 레벨 결정
    max_diff = max(lat_diff, lon_diff)
    
    # 줌 레벨 결정 로직
    if max_diff > 2.0:  # 전국 단위
        return 6
    elif max_diff > 1.0:  # 시/도 단위
        return 8
    elif max_diff > 0.5:  # 시/군/구 단위
        return 10
    elif max_diff > 0.1:  # 동/면 단위
        return 12
    elif max_diff > 0.05:  # 상세 지역
        return 14
    else:  # 매우 좁은 지역
        return 16


def _search_service_centers(keyword: str, service_type: int, brand: str, operating_only: bool) -> pd.DataFrame:
    """서비스센터 검색. 이름/주소에 키워드 LIKE, 유형/브랜드/운영상태 필터 적용"""
    engine = get_engine()
    type_mapping = _get_service_type_mapping()

    conditions = []
    params = {}

    # 키워드 검색
    if keyword:
        conditions.append("(name_ko LIKE :kw OR addr_road LIKE :kw)")
        params["kw"] = f"%{keyword.strip()}%"

    # 정비 유형 필터
    if service_type:
        conditions.append("type_code = :type_code")
        params["type_code"] = service_type

    # 브랜드 필터
    if brand and brand != "전체":
        conditions.append("(name_ko LIKE :brand OR addr_road LIKE :brand)")
        params["brand"] = f"%{brand}%"

    # 운영중인 정비소만 필터
    if operating_only:
        current_time = datetime.now().time()
        current_hour = current_time.hour
        conditions.append("""
            (status_code = 1 OR status_code IS NULL) AND
            (
                (open_time IS NULL AND close_time IS NULL) OR
                (
                    open_time IS NOT NULL AND close_time IS NOT NULL AND
                    TIME(open_time) <= :current_time AND TIME(close_time) >= :current_time
                )
            )
        """)
        params["current_time"] = current_time.strftime("%H:%M")

    where_sql = " AND ".join(conditions) if conditions else "1=1"

    sql = text(f"""
        SELECT
            name_ko AS 정비소명,
            addr_road AS 도로명주소,
            phone AS 전화번호,
            type_code,
            lat, lon,
            open_time,
            close_time
        FROM service_center
        WHERE {where_sql}
        ORDER BY name_ko
        LIMIT 1000
    """)

    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params=params)
    
    # 정비 유형을 실제 명칭으로 변환
    if not df.empty:
        df['정비유형'] = df['type_code'].map(type_mapping).fillna('미분류')
        
        # 운영시간 처리 (기본값: 09:00-18:00)
        df['운영시간'] = df.apply(lambda row: 
            f"{row['open_time'] or '09:00'} - {row['close_time'] or '18:00'}", axis=1)
        
        # 빈 값 처리
        df['도로명주소'] = df['도로명주소'].fillna('-')
        df['전화번호'] = df['전화번호'].fillna('-')
    
    return df


def main():
    st.title("🔧 정비소 현황")
    st.markdown("도치카 DB에 적재된 실데이터를 검색하고 지도에서 확인하세요.")

    # 세션 상태 초기화
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'selected_center' not in st.session_state:
        st.session_state.selected_center = None

    # 필터 영역
    st.subheader("🔍 정비소 검색")

    # 서비스 유형 옵션 준비
    service_types = _fetch_service_types()
    type_options = [("전체", "전체")] + service_types
    type_labels = [f"{name} ({code})" if code != "전체" else name for code, name in type_options]
    type_values = [code for code, name in type_options]

    # 브랜드 옵션 준비
    brand_options = ["전체"] + _get_brand_keywords()

    # 검색 필터와 버튼을 같은 라인에 배치
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 1, 1])

    with col1:
        keyword = st.text_input("검색어", placeholder="정비소명, 주소")

    with col2:
        selected_type_idx = st.selectbox("정비 유형", range(len(type_labels)), format_func=lambda x: type_labels[x])
        service_type = type_values[selected_type_idx] if type_values[selected_type_idx] != "전체" else None

    with col3:
        brand = st.selectbox("브랜드", brand_options)

    with col4:
        operating_only = st.checkbox("영업중", value=False)

    with col5:
        search_clicked = st.button("🔎 검색", type="primary", use_container_width=True)

    # 검색 실행
    if search_clicked:
        with st.spinner("검색 중..."):
            df = _search_service_centers(
                keyword=keyword, 
                service_type=service_type, 
                brand=brand,
                operating_only=operating_only
            )
        
        # 검색 결과를 세션 상태에 저장
        st.session_state.search_results = df
        st.session_state.selected_center = None  # 검색 시 선택 초기화

    # 검색 결과가 있으면 표시
    if st.session_state.search_results is not None:
        df = st.session_state.search_results
        
        if df.empty:
            st.warning("검색 결과가 없습니다. 검색 조건을 변경해보세요.")
        else:
            st.caption(f"총 {len(df):,}건 검색됨")
            
            # 데이터 테이블 표시 (영업상태 컬럼 제외)
            display_df = df.drop(columns=["lat", "lon", "type_code", "open_time", "close_time"])
            st.dataframe(display_df, use_container_width=True)

            # 지도 표시
            st.subheader("🗺️ 지도")
            map_df = df.dropna(subset=["lat", "lon"]).copy()
            
            if not map_df.empty:
                # 좌표 컬럼명 변경
                map_df = map_df.rename(columns={"lat": "latitude", "lon": "longitude"})
                
                # 검색 결과에 따른 지도 줌 레벨 결정
                zoom_level = _calculate_zoom_level(map_df)
                
                # 지도 표시 (검색 결과에 맞게 fit)
                st.map(map_df[["latitude", "longitude"]], zoom=zoom_level)
                
                # 정비소 선택을 위한 selectbox
                st.subheader("📋 정비소 선택")
                
                # 선택 옵션 준비
                center_options = ["정비소를 선택하세요"] + list(map_df["정비소명"].unique())
                
                # 현재 선택된 정비소가 있으면 해당 인덱스 사용, 없으면 0 (첫 번째 옵션)
                current_index = 0
                if st.session_state.selected_center and st.session_state.selected_center in center_options:
                    current_index = center_options.index(st.session_state.selected_center)
                
                selected = st.selectbox(
                    "정비소를 선택하세요", 
                    center_options,
                    index=current_index,
                    key="center_selector"
                )
                
                # 선택이 변경되었을 때만 세션 상태 업데이트
                if selected != "정비소를 선택하세요":
                    st.session_state.selected_center = selected
                    
                    # 선택된 정비소 정보 표시
                    row = map_df[map_df["정비소명"] == selected].iloc[0]
                    
                    st.markdown("**선택된 정비소 정보**")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"**정비소명**: {row['정비소명']}")
                        st.markdown(f"**도로명주소**: {row['도로명주소']}")
                        st.markdown(f"**전화번호**: {row['전화번호']}")
                    with c2:
                        st.markdown(f"**정비유형**: {row['정비유형']}")
                        st.markdown(f"**운영시간**: {row['운영시간']}")
                else:
                    st.session_state.selected_center = None
            else:
                st.info("표시할 좌표가 없습니다.")


if __name__ == "__main__":
    main()