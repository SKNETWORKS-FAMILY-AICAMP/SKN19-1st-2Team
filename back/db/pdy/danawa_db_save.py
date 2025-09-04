"""Danawa 엑셀 데이터를 MySQL 테이블(car, fuel)에 적재하는 스크립트.

개선 사항:
1. 작업 디렉토리(CWD)에 의존하던 상대 경로 -> __file__ 기반 절대 경로 사용
2. 중복 코드 제거 (함수화)
3. 예외 처리 및 로깅 추가
4. PyMySQL 대신 requirements 에 포함된 mysql-connector-python 사용

실행 방법 (프로젝트 루트 어디서든 가능):
    python back/db/pdy/danawa_db_save.py
"""

from pathlib import Path
import logging
import sys
import os
import pandas as pd
from sqlalchemy import create_engine
<<<<<<< HEAD
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# 프로젝트 루트 ( .../back/db/pdy/ 에서 3단계 상위 )
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data" / "pdy"
=======
from dotenv import load_dotenv
load_dotenv()
import os

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("URL 불러오기에 실패했습니다.")


# 엑셀 로드
df = pd.read_excel('data/pdy/danawa_car_data1.xlsx')

# MySQL 연결
# DB 
engine = create_engine(DB_URL)
>>>>>>> origin

CAR_FILE = DATA_DIR / "danawa_car_data1.xlsx"
FUEL_FILE = DATA_DIR / "DANAWA_car_fuel_data1.xlsx"

# 환경변수로 덮어쓸 수 있게 기본값 설정
DB_USER = os.getenv("DB_USER", "ohgiraffers")
DB_PASS = os.getenv("DB_PASS", "ohgiraffers")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "dochicar")  # 기존 스크립트 기준


<<<<<<< HEAD
def load_excel(path: Path) -> pd.DataFrame:
    if not path.exists():
        logging.error(f"파일 없음: {path}")
        raise FileNotFoundError(path)
    logging.info(f"엑셀 로드: {path}")
    return pd.read_excel(path)

=======
df = pd.read_excel('data/pdy/DANAWA_car_fuel_data1.xlsx')

# MySQL 연결
engine = create_engine(DB_URL)
>>>>>>> origin

def get_engine():
    # mysql-connector-python 드라이버 사용
    url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    logging.info(f"DB 엔진 생성 시도 (host={DB_HOST}, db={DB_NAME})")
    return create_engine(url)


def insert_df(df: pd.DataFrame, table: str, engine):
    if df.empty:
        logging.warning(f"빈 데이터프레임 -> 건너뜀 ({table})")
        return
    logging.info(f"{table} 테이블에 {len(df)}행 적재...")
    df.to_sql(name=table, con=engine, if_exists="append", index=False)
    logging.info(f"{table} 적재 완료")


def main():
    try:
        engine = get_engine()
    except Exception as e:
        logging.error(f"DB 엔진 생성 실패: {e}")
        sys.exit(1)

    # car 데이터
    try:
        car_df = load_excel(CAR_FILE)
        insert_df(car_df, "car", engine)
    except FileNotFoundError:
        logging.error("car 데이터 파일을 찾을 수 없어 스크립트 중단")
        return
    except SQLAlchemyError as e:
        logging.error(f"car 적재 중 DB 오류: {e}")
    except Exception as e:
        logging.error(f"car 처리 중 일반 오류: {e}")

    # fuel 데이터 (없으면 경고만)
    try:
        fuel_df = load_excel(FUEL_FILE)
        insert_df(fuel_df, "fuel", engine)
    except FileNotFoundError:
        logging.warning("fuel 데이터 파일 없음 -> 건너뜀")
    except SQLAlchemyError as e:
        logging.error(f"fuel 적재 중 DB 오류: {e}")
    except Exception as e:
        logging.error(f"fuel 처리 중 일반 오류: {e}")


if __name__ == "__main__":
    main()
