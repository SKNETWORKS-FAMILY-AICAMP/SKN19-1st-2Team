import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from dotenv import load_dotenv
import os

# 0) 경로/환경
ROOT = Path(__file__).resolve().parents[2]        # project_1st/
DATA_RAW = ROOT / "data" / "raw"
CSV_PATH = DATA_RAW / "auto_repair_standard.csv"

load_dotenv(ROOT / ".env")
DB_URL = os.getenv("DB_URL")
assert DB_URL, "환경변수 DB_URL이 없습니다 (.env 확인)."

# 1) CSV 로드 (인코딩 폴백)
try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
except UnicodeDecodeError:
    df = pd.read_csv(CSV_PATH, encoding="cp949")

# 2) 컬럼 이름 -> DB 스키마 컬럼으로 매핑
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

# 3) 타입 보정/정리
for c in ["lat", "lon"]:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

for c in ["biz_reg_date", "closed_date", "pause_from", "pause_to", "data_ref_date"]:
    if c in df.columns:
        df[c] = pd.to_datetime(df[c], errors="coerce").dt.date

# 좌표 유효 범위(대한민국) 필터
if {"lat","lon"}.issubset(df.columns):
    df = df[df["lat"].between(33, 39, inclusive="both") & df["lon"].between(124, 132, inclusive="both")]

# 핵심 결측/중복 제거
df = df.dropna(subset=["name_ko"])
dup_key = df[["name_ko","addr_road","addr_jibun"]].astype(str).agg("|".join, axis=1)
df = df.loc[~dup_key.duplicated()].copy()

# 4) DB 적재
engine = create_engine(DB_URL)
with engine.begin() as conn:
    # (선택) 기존 데이터 삭제하고 새로 넣고 싶다면 다음 주석 해제
    # conn.execute(text("TRUNCATE TABLE service_center"))

    df.to_sql("service_center", con=conn, if_exists="append", index=False, chunksize=2000, method="multi")

    total = conn.execute(text("SELECT COUNT(*) FROM service_center")).scalar()
    print("✅ 적재 완료. 현재 service_center 총 행수:", total)
