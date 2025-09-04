import mysql.connector
import os


def get_conn():
    return mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
    )


# 연결 확인
# if conn.is_connected():
#     print("MySQL 데이터베이스에 연결되었습니다.")
# else:
#     print("MySQL 데이터베이스에 연결할 수 없습니다.")
