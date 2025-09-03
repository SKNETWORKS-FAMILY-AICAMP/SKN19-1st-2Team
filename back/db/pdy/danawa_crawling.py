# 정적 웹페이지 크롤링

import requests
from bs4 import BeautifulSoup
from datetime import datetime #현재 시간 가져올 수 있는 모듈
from urllib.request import urlretrieve #url로 다운로드 할 수 있는 모듈
import pandas as pd


# 3. beautifulsoup 객체 생성

with open("danawa_cars_html_1page.html", "r", encoding="utf-8") as f:
    html1 = f.read()

# 2. 다나와 1페이지 BeautifulSoup 객체 생성
danawa_bs1 = BeautifulSoup(html1, "html.parser")


# ------------------------차 모델명, 차 이미지 url 저장

car_name_image = danawa_bs1.select('a.image')

name_image_info = []

for ni in car_name_image:
    img = ni.find('img')
    if img and img.has_attr('src') and img.has_attr('alt'):
        name_image_info.append({
            '이미지url': img['src'],
            '모델명': img['alt']
        })

# for info in name_image_info:
#     print(info)


# -------------- .detail_middle에서 뽑을 것들 저장
car_detail = danawa_bs1.select('div.detail_middle')

spec_info = []

# 2. alt와 spec 스펙 리스트 추출
for detail in car_detail:
    # 자손 <img> 태그의 alt 속성 추출
    img_tag = detail.find('img')
    alt_value = img_tag['alt'] if img_tag and img_tag.has_attr('alt') else '없음'

    # 자식 <div class="spec"> 내부 <span> 값 추출
    spec_div = detail.find('div', class_='spec')
    span_texts = [span.text.strip() for span in spec_div.find_all('span')] if spec_div else []

    # 딕셔너리로 저장
    spec_info.append({
        '제조사명': alt_value,
        'specs': span_texts
    })

# for spec in spec_info:
#     print(spec)

# ----------------------- <strong>에서 '가격' 뽑을 것
car_price = danawa_bs1.select('strong')

price_d= []

for price in car_price:
    price_d.append(price.text.strip())

price_numbers = [int(price.replace(',', '')) for price in price_d]
# print(price_numbers)

danawa_car_table1 = []
danawa_car_en_table1 = []

for i in range(len(name_image_info)):
    specs = spec_info[i]['specs']
    launch = specs[0].replace('. 출시', '').strip()
    
    fuel = [fu.strip() for fu in specs[2].split(', ')]
    
    en_dict = {
        'model_name': name_image_info[i]['모델명'].strip(),
        'model_fuel': fuel
    }

    danawa_car_en_table1.append(en_dict)

    car_dict = {
        'comp_name':spec_info[i]['제조사명'].strip(),
        'model_name': name_image_info[i]['모델명'].strip(),
        'img_url': name_image_info[i]['이미지url'],   # 예: ('기아 쏘렌토', 'https://...'),
        'launch_date':launch.replace('.','-'),
        'model_type':specs[1].strip(),
        #'연료':specs[2].strip(),
        'model_price': price_numbers[i]
    }

    for spec in specs:
        if '복합연비' in spec:
            key, value = spec.split(' ', 1)
            car_dict['efficiency_type'] = '복합연비'
            car_dict['efficiency_amount'] = value.strip()
        elif '복합전비' in spec:
            car_dict['efficiency_type'] = '복합전비'
            key, value = spec.split(' ', 1)
            car_dict['efficiency_amount'] = value.strip()
           
        if 'cc' in spec:
            car_dict['resrc_type']='배기량'
            car_dict['resrc_amount'] = spec
        elif '용량' in spec:
            car_dict['resrc_type']='배터리 용량'
            car_dict['resrc_amount'] = spec.split('용량')[-1].strip()

        if ':' in spec:
            key, value = spec.split(':', 1)
            car_dict['wait_period'] = value.strip()


    danawa_car_table1.append(car_dict)


df = pd.DataFrame(danawa_car_table1)

# car 테이블 정보 Excel 파일로 저장
df.to_excel('danawa_car_data1.xlsx', index=False, engine='openpyxl')

rows = []
for item in danawa_car_en_table1:
    model = item['model_name']
    for fuel in item['model_fuel']:
        rows.append({'model_name': model, 'fuel_type': fuel})


df = pd.DataFrame(rows)

# fuel 테이블 정보 엑셀로 저장
df.to_excel('DANAWA_car_fuel_data1.xlsx', index=False)

        
