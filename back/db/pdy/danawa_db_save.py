import pandas as pd
from sqlalchemy import create_engine
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

# INSERT 실행
df.to_sql(name='car', con=engine, if_exists='append', index=False)


df = pd.read_excel('data/pdy/DANAWA_car_fuel_data1.xlsx')

# MySQL 연결
engine = create_engine(DB_URL)

# INSERT 실행
df.to_sql(name='fuel', con=engine, if_exists='append', index=False)