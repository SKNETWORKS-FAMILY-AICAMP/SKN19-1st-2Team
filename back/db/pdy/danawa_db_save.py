import pandas as pd
from sqlalchemy import create_engine

from dotenv import load_dotenv

load_dotenv()
import os

DB_URL = os.getenv("DB_URL")

if not DB_URL:
    raise ValueError("URL 불러오기에 실패했습니다.")


# 엑셀 로드
df_car = pd.read_excel("data/pdy/danawa_car_data1.xlsx")
df_fuel = pd.read_excel("data/pdy/DANAWA_car_fuel_data1.xlsx")


# MySQL 연결
engine = create_engine(DB_URL)

# car 테이블 INSERT 실행
df_car.to_sql(name="car", con=engine, if_exists="append", index=False)

# fuel 테이블 INSERT 실행
df_fuel.to_sql(name="fuel", con=engine, if_exists="append", index=False)
