import mysql.connector


def get_conn():
    return mysql.connector.connect(
        host="localhost",  #
        user="ohgiraffers",  #
        password="ohgiraffers",  #
        database="dochicar",
    )


# 연결 확인
# if conn.is_connected():
#     print("MySQL 데이터베이스에 연결되었습니다.")
# else:
#     print("MySQL 데이터베이스에 연결할 수 없습니다.")
