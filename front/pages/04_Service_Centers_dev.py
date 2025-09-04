"""
정비소 현황 페이지 - 개선된 버전
MySQL의 dochicar.service_center 실데이터 연동
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import text
from pathlib import Path
import sys
import os
from datetime import datetime, time
import math
import folium
from streamlit_folium import st_folium

# 프로젝트 루트를 경로에 추가하여 내부 모듈 import 가능하게 설정
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from back.db.conn import get_engine  # noqa: E402

st.set_page_config(
    page_title="정비소 현황 - DOCHICAR",
    page_icon="🔧",
    layout="wide"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    /* DOCHICAR 브랜딩 스타일 */
    .main-header {
        background: linear-gradient(135deg, #FDB813 0%, #FFE082 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: #1F1F1F;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #FDB813 0%, #FFE082 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 12px rgba(253,184,19,0.3);
        margin-bottom: 1rem;
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .service-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border-left: 4px solid #FDB813;
        margin: 1rem 0;
    }
    
    .search-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .distance-badge {
        background: #4CAF50;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-open {
        color: #4CAF50;
        font-weight: 600;
    }
    
    .status-closed {
        color: #F44336;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

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

def _calculate_distance(lat1, lon1, lat2, lon2):
    """두 지점 간의 거리를 계산 (단위: km)"""
    if pd.isna(lat1) or pd.isna(lon1) or pd.isna(lat2) or pd.isna(lon2):
        return None
    
    # 하버사인 공식
    R = 6371  # 지구의 반지름 (km)
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    return distance

def _get_current_status(open_time, close_time):
    """현재 시간 기준으로 영업 상태 확인"""
    if not open_time or not close_time:
        return "정보없음"
    
    current_time = datetime.now().time()
    
    # 시간 파싱
    try:
        if isinstance(open_time, str):
            open_t = datetime.strptime(open_time, "%H:%M").time()
        else:
            open_t = open_time
            
        if isinstance(close_time, str):
            close_t = datetime.strptime(close_time, "%H:%M").time()
        else:
            close_t = close_time
        
        if open_t <= current_time <= close_t:
            return "영업중"
        else:
            return "영업종료"
    except:
        return "정보없음"

def _search_service_centers(keyword: str, service_type: int, brand: str, operating_only: bool, user_lat=None, user_lon=None) -> pd.DataFrame:
    """서비스센터 검색 + 거리 계산"""
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

    where_sql = " AND ".join(conditions) if conditions else "1=1"

    sql = text(f"""
        SELECT
            name_ko AS 정비소명,
            addr_road AS 도로명주소,
            phone AS 전화번호,
            type_code,
            lat, lon,
            open_time,
            close_time,
            status_code
        FROM service_center
        WHERE {where_sql}
        ORDER BY name_ko
        LIMIT 1000
    """)

    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params=params)
    
    if not df.empty:
        # 정비 유형을 실제 명칭으로 변환
        df['정비유형'] = df['type_code'].map(type_mapping).fillna('미분류')
        
        # 운영시간 처리
        df['운영시간'] = df.apply(lambda row: 
            f"{row['open_time'] or '09:00'} - {row['close_time'] or '18:00'}", axis=1)
        
        # 현재 영업상태 확인
        df['영업상태'] = df.apply(lambda row: 
            _get_current_status(row['open_time'], row['close_time']), axis=1)
        
        # 거리 계산 (사용자 위치가 있는 경우)
        if user_lat and user_lon:
            df['거리'] = df.apply(lambda row: 
                _calculate_distance(user_lat, user_lon, row['lat'], row['lon']), axis=1)
            df = df.sort_values('거리', na_last=True)
        
        # 운영중인 정비소만 필터 (옵션)
        if operating_only:
            df = df[df['영업상태'] == '영업중']
        
        # 빈 값 처리
        df['도로명주소'] = df['도로명주소'].fillna('-')
        df['전화번호'] = df['전화번호'].fillna('-')
    
    return df

def _get_statistics():
    """정비소 통계 정보"""
    engine = get_engine()
    
    with engine.connect() as conn:
        # 전체 정비소 수
        total_count = conn.execute(text("SELECT COUNT(*) FROM service_center")).scalar()
        
        # 유형별 분포
        type_stats = pd.read_sql(text("""
            SELECT type_code, COUNT(*) as count
            FROM service_center
            WHERE type_code IS NOT NULL
            GROUP BY type_code
            ORDER BY count DESC
        """), conn)
        
        # 지역별 분포 (상위 10개)
        region_stats = pd.read_sql(text("""
            SELECT 
                SUBSTRING_INDEX(SUBSTRING_INDEX(addr_road, ' ', 2), ' ', -1) as region,
                COUNT(*) as count
            FROM service_center
            WHERE addr_road IS NOT NULL
            GROUP BY region
            ORDER BY count DESC
            LIMIT 10
        """), conn)
        
    return total_count, type_stats, region_stats

def create_folium_map(df, center_lat=37.5665, center_lon=127.0780):
    """Folium을 이용한 인터랙티브 지도 생성"""
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # 정비소 마커 추가
    for idx, row in df.iterrows():
        if pd.notna(row['lat']) and pd.notna(row['lon']):
            # 영업상태에 따른 마커 색상
            color = 'green' if row['영업상태'] == '영업중' else 'red'
            
            # 거리 정보 포함 (있는 경우)
            distance_info = f"<br>거리: {row['거리']:.1f}km" if '거리' in row and pd.notna(row['거리']) else ""
            
            popup_text = f"""
            <b>{row['정비소명']}</b><br>
            주소: {row['도로명주소']}<br>
            전화: {row['전화번호']}<br>
            유형: {row['정비유형']}<br>
            운영: {row['운영시간']}<br>
            상태: {row['영업상태']}{distance_info}
            """
            
            folium.Marker(
                [row['lat'], row['lon']],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=row['정비소명'],
                icon=folium.Icon(color=color, icon='wrench', prefix='fa')
            ).add_to(m)
    
    return m

def main():
    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1>🔧 DOCHICAR 정비소 현황</h1>
        <p>전국 자동차 정비소 정보를 검색하고 지도에서 확인하세요</p>
    </div>
    """, unsafe_allow_html=True)

    # 세션 상태 초기화
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'user_location' not in st.session_state:
        st.session_state.user_location = {"lat": 37.5665, "lon": 127.0780}  # 서울 기본값

    # 통계 정보 표시
    st.subheader("📊 정비소 현황 통계")
    
    try:
        total_count, type_stats, region_stats = _get_statistics()
        
        # 통계 카드
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{total_count:,}</div>
                <div class="stat-label">전체 정비소</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            operating_count = int(total_count * 0.85)  # 임시 추정값
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{operating_count:,}</div>
                <div class="stat-label">운영중 정비소</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            avg_per_region = total_count // 17 if total_count > 0 else 0
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{avg_per_region:,}</div>
                <div class="stat-label">시도당 평균</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{len(type_stats)}</div>
                <div class="stat-label">정비 유형</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 차트 섹션
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            if not type_stats.empty:
                # 유형별 분포 차트
                type_mapping = _get_service_type_mapping()
                type_stats['유형명'] = type_stats['type_code'].map(type_mapping)
                
                fig_type = px.pie(
                    type_stats, 
                    values='count', 
                    names='유형명',
                    title="정비소 유형별 분포"
                )
                st.plotly_chart(fig_type, use_container_width=True)
        
        with col_chart2:
            if not region_stats.empty:
                # 지역별 분포 차트
                fig_region = px.bar(
                    region_stats.head(8), 
                    x='region', 
                    y='count',
                    title="지역별 정비소 수 (TOP 8)",
                    color='count',
                    color_continuous_scale='Blues'
                )
                st.plotly_chart(fig_region, use_container_width=True)
    
    except Exception as e:
        st.warning(f"통계 로딩 중 오류: {e}")

    # 검색 섹션
    st.markdown("""
    <div class="search-container">
    """, unsafe_allow_html=True)
    
    st.subheader("🔍 정비소 검색")

    # 사용자 위치 입력
    st.markdown("**📍 내 위치 (선택사항 - 거리 계산용)**")
    col_loc1, col_loc2 = st.columns(2)
    
    with col_loc1:
        user_lat = st.number_input("위도", value=37.5665, format="%.6f", key="user_lat")
    with col_loc2:
        user_lon = st.number_input("경도", value=127.0780, format="%.6f", key="user_lon")
    
    # 검색 조건
    service_types = _fetch_service_types()
    type_options = [("전체", "전체")] + service_types
    type_labels = [f"{name}" for code, name in type_options]
    type_values = [code for code, name in type_options]
    brand_options = ["전체"] + _get_brand_keywords()

    col1, col2, col3 = st.columns(3)

    with col1:
        keyword = st.text_input("🏪 정비소명 또는 주소", placeholder="예: 현대, 강남구")
        selected_type_idx = st.selectbox("🔧 정비 유형", range(len(type_labels)), format_func=lambda x: type_labels[x])

    with col2:
        brand = st.selectbox("🚗 전문 브랜드", brand_options)
        operating_only = st.checkbox("✅ 현재 영업중인 정비소만", value=False)

    with col3:
        max_distance = st.slider("📏 최대 거리 (km)", 1, 50, 10)
        search_clicked = st.button("🔎 검색하기", type="primary", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 검색 실행
    if search_clicked or st.session_state.search_results is None:
        with st.spinner("🔍 정비소를 검색하고 있습니다..."):
            service_type = type_values[selected_type_idx] if type_values[selected_type_idx] != "전체" else None
            df = _search_service_centers(
                keyword=keyword,
                service_type=service_type,
                brand=brand,
                operating_only=operating_only,
                user_lat=user_lat,
                user_lon=user_lon
            )
            
            # 거리 필터링
            if '거리' in df.columns:
                df = df[df['거리'] <= max_distance]
            
        st.session_state.search_results = df
        st.session_state.user_location = {"lat": user_lat, "lon": user_lon}

    # 검색 결과 표시
    if st.session_state.search_results is not None:
        df = st.session_state.search_results
        
        if df.empty:
            st.warning("🔍 검색 조건에 맞는 정비소가 없습니다. 다른 조건으로 검색해보세요.")
        else:
            st.success(f"✅ 총 **{len(df):,}개**의 정비소를 찾았습니다!")
            
            # 탭으로 구분
            tab1, tab2, tab3 = st.tabs(["📋 목록보기", "🗺️ 지도보기", "📊 분석"])
            
            with tab1:
                # 정비소 카드 형태로 표시
                for idx, row in df.head(20).iterrows():  # 상위 20개만 표시
                    with st.container():
                        col_info, col_status = st.columns([3, 1])
                        
                        with col_info:
                            # 거리 배지
                            distance_badge = ""
                            if '거리' in row and pd.notna(row['거리']):
                                distance_badge = f'<span class="distance-badge">{row["거리"]:.1f}km</span>'
                            
                            st.markdown(f"""
                            <div class="service-card">
                                <h4>🔧 {row['정비소명']} {distance_badge}</h4>
                                <p><strong>📍 주소:</strong> {row['도로명주소']}</p>
                                <p><strong>📞 전화:</strong> {row['전화번호']}</p>
                                <p><strong>🏷️ 유형:</strong> {row['정비유형']}</p>
                                <p><strong>🕒 운영시간:</strong> {row['운영시간']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_status:
                            status_class = "status-open" if row['영업상태'] == '영업중' else "status-closed"
                            st.markdown(f'<p class="{status_class}">● {row["영업상태"]}</p>', unsafe_allow_html=True)
                            
                            if st.button(f"📍 위치보기", key=f"loc_{idx}"):
                                st.info(f"지도 탭에서 {row['정비소명']}의 위치를 확인하세요!")
                
                # 더보기 기능
                if len(df) > 20:
                    st.info(f"상위 20개 정비소를 표시했습니다. 총 {len(df)}개 중에서 더 보려면 검색 조건을 조정해주세요.")
            
            with tab2:
                st.subheader("🗺️ 정비소 위치")
                
                # 지도에 표시할 데이터 준비
                map_df = df.dropna(subset=["lat", "lon"]).head(100)  # 성능상 100개로 제한
                
                if not map_df.empty:
                    # 지도 중심점 계산
                    center_lat = map_df['lat'].mean()
                    center_lon = map_df['lon'].mean()
                    
                    # Folium 지도 생성
                    folium_map = create_folium_map(map_df, center_lat, center_lon)
                    
                    # 지도 표시
                    st_folium(folium_map, width=700, height=500)
                    
                    st.caption(f"🟢 영업중 | 🔴 영업종료 | 총 {len(map_df)}개 정비소 표시")
                else:
                    st.warning("지도에 표시할 좌표 정보가 없습니다.")
            
            with tab3:
                st.subheader("📊 검색 결과 분석")
                
                if len(df) > 0:
                    col_a1, col_a2 = st.columns(2)
                    
                    with col_a1:
                        # 영업상태 분포
                        status_counts = df['영업상태'].value_counts()
                        fig_status = px.pie(
                            values=status_counts.values,
                            names=status_counts.index,
                            title="영업상태 분포"
                        )
                        st.plotly_chart(fig_status, use_container_width=True)
                    
                    with col_a2:
                        # 유형별 분포
                        type_counts = df['정비유형'].value_counts()
                        fig_types = px.bar(
                            x=type_counts.index,
                            y=type_counts.values,
                            title="정비유형별 분포"
                        )
                        st.plotly_chart(fig_types, use_container_width=True)
                    
                    # 거리별 분포 (거리 정보가 있는 경우)
                    if '거리' in df.columns and df['거리'].notna().any():
                        st.subheader("📏 거리별 분포")
                        fig_distance = px.histogram(
                            df,
                            x='거리',
                            nbins=20,
                            title="거리별 정비소 수"
                        )
                        st.plotly_chart(fig_distance, use_container_width=True)

if __name__ == "__main__":
    main()