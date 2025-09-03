import pandas as pd
from sqlalchemy import create_engine

# 엑셀 로드
df = pd.read_excel('danawa_car_data1.xlsx')

# MySQL 연결
engine = create_engine("mysql+pymysql://ohgiraffers:ohgiraffers@localhost:3306/dochidb")

# INSERT 실행
df.to_sql(name='car', con=engine, if_exists='append', index=False)


df = pd.read_excel('DANAWA_car_fuel_data1.xlsx')

# MySQL 연결
engine = create_engine("mysql+pymysql://ohgiraffers:ohgiraffers@localhost:3306/dochidb")

# INSERT 실행
df.to_sql(name='fuel', con=engine, if_exists='append', index=False)