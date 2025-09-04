"""
03_insert_service_centers_data.py
DOCHICAR 프로젝트 - 정비소 데이터 삽입 스크립트
실행 순서: 3번 (01, 02 실행 후)
"""

import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from dotenv import load_dotenv
import os

# 0) 경로/환경 설정 - 현재 폴더 구조에 맞게 수정
ROOT = Path(__file__).resolve().parents[2]        # project_1st/
DATA_DIR = ROOT / "data" / "ohj"                  # data/ohj/
CSV_PATH = DATA_DIR / "auto_repair_standard.csv"

# .env 로드
load_dotenv(ROOT / ".env")
DB_URL = os.getenv("DB_URL")
assert DB_URL, "환경변수 DB_URL이 없습니다 (.env 확인)."

def main():
    print("🚀 정비소 데이터 삽입 시작...")
    
    # 1) CSV 파일 존재 확인
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV 파일을 찾을 수 없습니다: {CSV_PATH}")
    
    print(f"📁 CSV 파일 경로: {CSV_PATH}")
    
    # 2) CSV 로드 (인코딩 폴백)
    try:
        df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
        print(f"✅ CSV 로드 성공 (UTF-8): {df.shape}")
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, encoding="cp949")
        print(f"✅ CSV 로드 성공 (CP949): {df.shape}")
    
    # 3) 컬럼 이름 -> DB 스키마 컬럼으로 매핑
    rename_map = {
        "자동차정비업체명": "name_ko",
        "자동차정비업체종류": "type_code",
        "소재지도로명주소": "addr_road",
        "소재지지번주소": "addr_jibun",
        "위도": "lat",
        "경도": "lon",
        "사업등록일자": "biz_reg_date",
        "면적": "area_text",
        "영업상태": "status_code",
        "폐업일자": "closed_date",
        "휴업시작일자": "pause_from",
        "휴업종료일자": "pause_to",
        "운영시작시각": "open_time",
        "운영종료시각": "close_time",
        "전화번호": "phone",
        "관리기관명": "mgmt_office_name",
        "관리기관전화번호": "mgmt_office_tel",
        "데이터기준일자": "data_ref_date",
        "제공기관코드": "provider_code",
        "제공기관명": "provider_name",
    }
    df = df.rename(columns=rename_map)
    print(f"🔄 컬럼 매핑 완료: {len(rename_map)}개 컬럼")
    
    # 4) 타입 보정/정리
    for c in ["lat", "lon"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    
    for c in ["biz_reg_date", "closed_date", "pause_from", "pause_to", "data_ref_date"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce").dt.date
    
    # 5) 좌표 유효 범위(대한민국) 필터
    if {"lat","lon"}.issubset(df.columns):
        before_count = len(df)
        df = df[df["lat"].between(33, 39, inclusive="both") & df["lon"].between(124, 132, inclusive="both")]
        after_count = len(df)
        print(f"🗺️ 좌표 필터링: {before_count} → {after_count} ({before_count - after_count}개 제거)")
    
    # 6) 핵심 결측/중복 제거
    before_count = len(df)
    df = df.dropna(subset=["name_ko"])
    dup_key = df[["name_ko","addr_road","addr_jibun"]].astype(str).agg("|".join, axis=1)
    df = df.loc[~dup_key.duplicated()].copy()
    after_count = len(df)
    print(f"🧹 데이터 정제: {before_count} → {after_count} ({before_count - after_count}개 제거)")
    
    # 7) DB 연결 및 적재
    print("🔌 데이터베이스 연결 중...")
    engine = create_engine(DB_URL)
    
    with engine.begin() as conn:
        # 기존 데이터 확인
        existing_count = conn.execute(text("SELECT COUNT(*) FROM service_center")).scalar()
        print(f"📊 기존 데이터: {existing_count}건")
        
        # 데이터 삽입
        print("💾 데이터 삽입 중...")
        df.to_sql("service_center", con=conn, if_exists="append", index=False, chunksize=2000, method="multi")
        
        # 최종 확인
        total = conn.execute(text("SELECT COUNT(*) FROM service_center")).scalar()
        inserted = total - existing_count
        print(f"✅ 삽입 완료!")
        print(f"   - 새로 삽입: {inserted}건")
        print(f"   - 전체 데이터: {total}건")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        raise
