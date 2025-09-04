"""
차량 비교 페이지
최대 3개 차량 비교
"""
import mysql.connector
import streamlit as st
import pandas as pd
from sqlalchemy import text
from pathlib import Path
import sys

from dotenv import load_dotenv
load_dotenv()
import os
# ------import


#DB 커넥트 객체 생성
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

#DB 커넥트 커서 생성
cursor = conn.cursor()

#SQL문
sql = 'SELECT comp_name FROM car GROUP BY comp_name'
cursor.execute(sql)

rows = cursor.fetchall()
car_brand_list = [row[0] for row in rows]

cursor.execute('select model_name from car')

rows = cursor.fetchall()
car_name_list = [row[0] for row in rows]

print(car_brand_list)
print(car_name_list)

cursor.close()
conn.close()



#STREAMLIT 페이지
st.set_page_config(
    page_title="차량 비교 - DOCHICHA.Inc",
    page_icon="⚖️"
)



def main():
    st.title("⚖️ 차량 비교")
    st.markdown("최대 3개 차량을 비교하여 최적의 선택을 하세요.")
    
    # 차량 선택
    st.subheader("🚗 비교할 차량 선택")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**차량 1**")
        car1_brand = st.selectbox("브랜드", car_brand_list, key="car1_brand")
        car1_model = st.selectbox("차량명", [row[0] for row in rows], key="car1_model")
    
    with col2:
        st.markdown("**차량 2**")
        car2_brand = st.selectbox("브랜드", ["현대", "기아", "쉐보레", "르노삼성", "쌍용"], key="car2_brand")
        car2_model = st.text_input("차량명", key="car2_model", placeholder="예: 소나타")
    
    with col3:
        st.markdown("**차량 3**")
        car3_brand = st.selectbox("브랜드", ["현대", "기아", "쉐보레", "르노삼성", "쌍용"], key="car3_brand")
        car3_model = st.text_input("차량명", key="car3_model", placeholder="예: 투싼")
    
    # 비교 버튼
    if st.button("⚖️ 비교하기", type="primary"):
        # TODO: 실제 비교 로직 구현
        st.success("비교 기능이 곧 구현될 예정입니다!")
        
        # 임시 비교 결과
        st.subheader("📊 비교 결과")
        
        comparison_data = pd.DataFrame({
            "항목": ["가격(만원)", "연비(km/L)", "안전등급", "배기량(cc)", "연료", "출시년도"],
            "차량 1": [2000, 15.2, 1600, 2023],
            "차량 2": [3000, 12.8, 2000, 2023],
            "차량 3": [2500, 13.5,, 1800, 2022]
        })
        
        st.dataframe(comparison_data, use_container_width=True)
        
        fig = comparison_data.plot.pie(
            y='차량 1',
            labels=comparison_data['항목'],
            # autopct='%1.1f%%',
            figsize=(10,10),
            legend = False
        ).get_figure()      #호출해야 만들어진 pie 차트가 반환이 됨

        st.pyplot(fig)





        # 좋아요 기능
        # st.subheader("👍 선호도")
        
        # col1, col2, col3 = st.columns(3)
        
        # with col1:
        #     if st.button("👍 차량 1 좋아요", key="like1"):
        #         st.success("차량 1에 좋아요를 눌렀습니다!")
        
        # with col2:
        #     if st.button("👍 차량 2 좋아요", key="like2"):
        #         st.success("차량 2에 좋아요를 눌렀습니다!")
        
        # with col3:
        #     if st.button("👍 차량 3 좋아요", key="like3"):
        #         st.success("차량 3에 좋아요를 눌렀습니다!")

if __name__ == "__main__":
    main()
