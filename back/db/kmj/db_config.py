import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def get_conn():
    return mysql.connector.connect(
        host=os.getenv("HOST", "127.0.0.1"),  # 기본값 명시
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        port=os.getenv("PORT", 3306),  # 필요시 포트도 명시
    )


# 연결 확인
# if conn.is_connected():
#     print("MySQL 데이터베이스에 연결되었습니다.")
# else:
#     print("MySQL 데이터베이스에 연결할 수 없습니다.")
