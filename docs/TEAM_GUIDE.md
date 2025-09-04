# 👥 팀원별 개발 가이드

## 📋 개요
DOCHICAR 프로젝트의 팀원별 역할과 개발 가이드입니다.

## 🏗️ 폴더 구조 규칙

### 1. 데이터 저장 규칙
```
data/
├── pjh/          # 박진형 데이터 (신차 검색, FAQ)
├── kmj/          # 김민정 데이터 (추천 알고리즘)
├── pdy/          # 박도연 데이터 (차량 비교)
└── ohj/          # 오흥재 데이터 (정비소 현황)
```

### 2. DB 스크립트 규칙
```
back/db/
├── pjh/          # 박진형 DB 스크립트
├── kmj/          # 김민정 DB 스크립트
├── pdy/          # 박도연 DB 스크립트
└── ohj/          # 오흥재 DB 스크립트
```

### 3. 페이지 파일 규칙
```
front/pages/
├── 01_Search.py         # 박진형
├── 02_Recommend.py      # 김민정
├── 03_Compare.py        # 박도연
├── 04_Service_Centers.py# 오흥재
└── 05_FAQ.py            # 박진형
```

## 👤 팀원별 상세 가이드

### 🔍 박진형 (PJH) - 신차 검색 & FAQ

#### 담당 페이지
- `front/pages/01_Search.py` - 신차 검색
- `front/pages/05_FAQ.py` - FAQ

#### 데이터 소스
- `data/pjh/` - 신차 데이터, FAQ 데이터
- 다나와 자동차 크롤링 데이터

#### DB 스크립트
- `back/db/pjh/` - 신차 테이블, FAQ 테이블 생성/삽입

#### 주요 기능
- 신차 검색 (차량명, 가격, 차종, 출시일)
- FAQ 시스템 (제조사별 Q&A)
- 다나와 크롤링 연동

#### 개발 예시
```python
# 01_Search.py
from back.db.conn import get_engine
import pandas as pd

def search_cars(keyword, price_range, car_type):
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql("""
            SELECT * FROM car_models 
            WHERE model LIKE :keyword 
            AND price BETWEEN :min_price AND :max_price
        """, conn, params={
            'keyword': f'%{keyword}%',
            'min_price': price_range[0],
            'max_price': price_range[1]
        })
    return df
```

### 💡 김민정 (KMJ) - 맞춤 추천

#### 담당 페이지
- `front/pages/02_Recommend.py` - 맞춤 추천

#### 데이터 소스
- `data/kmj/` - 연령대별 선호도, 지역별 데이터
- 자동차 등록 현황 데이터

#### DB 스크립트
- `back/db/kmj/` - 추천 알고리즘 관련 테이블

#### 주요 기능
- 사용자 입력 기반 맞춤형 추천
- 연령대별 차종 선호도 분석
- 데이터 시각화 (차트, 그래프)

#### 개발 예시
```python
# 02_Recommend.py
from back.db.conn import get_engine
import plotly.express as px

def get_recommendations(age, region, budget, car_type):
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql("""
            SELECT * FROM car_models cm
            JOIN user_preferences up ON cm.id = up.car_model_id
            WHERE up.age_group = :age 
            AND up.region = :region
            AND cm.price <= :budget
        """, conn, params={
            'age': age,
            'region': region,
            'budget': budget
        })
    
    # 추천 결과 시각화
    fig = px.bar(df, x='model', y='preference_score')
    return df, fig
```

### ⚖️ 박도연 (PDY) - 차량 비교

#### 담당 페이지
- `front/pages/03_Compare.py` - 차량 비교

#### 데이터 소스
- `data/pdy/` - 차량 제원, 비교 데이터
- 좋아요/선호도 데이터

#### DB 스크립트
- `back/db/pdy/` - 비교 테이블, 선호도 테이블

#### 주요 기능
- 최대 3개 차량 비교
- 좋아요 기능 (MySQL COUNT 기반)
- 제원·가격·안전등급 비교

#### 개발 예시
```python
# 03_Compare.py
from back.db.conn import get_engine

def compare_cars(car_ids):
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql("""
            SELECT 
                cm.*,
                COUNT(up.id) as like_count
            FROM car_models cm
            LEFT JOIN user_preferences up ON cm.id = up.car_model_id
            WHERE cm.id IN :car_ids
            GROUP BY cm.id
        """, conn, params={'car_ids': tuple(car_ids)})
    
    return df

def add_like(car_id, user_ip):
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute("""
            INSERT INTO user_preferences (car_model_id, user_ip, preference_type)
            VALUES (:car_id, :user_ip, 'like')
        """, params={'car_id': car_id, 'user_ip': user_ip})
        conn.commit()
```

### 🔧 오흥재 (OHJ) - 정비소 현황

#### 담당 페이지
- `front/pages/04_Service_Centers.py` - 정비소 현황

#### 데이터 소스
- `data/ohj/` - 정비소 데이터 (auto_repair_standard.csv)
- 공공데이터 (자동차정비업체 현황)

#### DB 스크립트
- `back/db/ohj/` - 정비소 테이블 생성/삽입
- `00_setup_database.py` - 자동 설정 스크립트

#### 주요 기능
- 지역별 정비소 검색 및 필터링
- 지도 시각화 (위도·경도)
- 정비소 상세 정보 제공

#### 개발 예시
```python
# 04_Service_Centers.py
from back.db.conn import get_engine

def search_service_centers(keyword, service_type, limit=500):
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql("""
            SELECT 
                name_ko, addr_road, phone, lat, lon,
                open_time, close_time, status_code
            FROM service_center
            WHERE (name_ko LIKE :keyword OR addr_road LIKE :keyword)
            AND type_code = :service_type
            LIMIT :limit
        """, conn, params={
            'keyword': f'%{keyword}%',
            'service_type': service_type,
            'limit': limit
        })
    
    return df
```

## 🔧 공통 개발 규칙

### 1. DB 연결 방법
```python
# 모든 페이지에서 공통 사용
from back.db.conn import get_engine

engine = get_engine()
with engine.connect() as conn:
    # 쿼리 실행
    df = pd.read_sql("SELECT * FROM your_table", conn)
```

### 2. 환경변수 설정
```bash
# .env 파일에 DB_URL 설정
DB_URL=mysql+pymysql://user:password@127.0.0.1:3306/dochicar
```

### 3. 페이지 구조 템플릿
```python
import streamlit as st
from back.db.conn import get_engine
import pandas as pd

st.set_page_config(
    page_title="페이지명 - DOCHICAR",
    page_icon="🔧"
)

def main():
    st.title("🔧 페이지명")
    st.markdown("페이지 설명")
    
    # 필터 영역
    st.subheader("🔍 검색/필터")
    
    # 검색 실행
    if st.button("🔎 검색", type="primary"):
        # DB 쿼리 실행
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM your_table", conn)
        
        # 결과 표시
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
```

### 4. Git 협업 규칙
```bash
# 작업 시작 전
git pull origin main

# 작업 완료 후
git add .
git commit -m "feat: 기능명 추가"
git push origin main
```

## 🐛 문제 해결

### 1. DB 연결 오류
- `.env` 파일의 `DB_URL` 확인
- MySQL 서버 실행 상태 확인
- 사용자 권한 확인

### 2. 모듈 import 오류
- `sys.path.append(str(ROOT))` 추가
- 상대 경로 확인

### 3. 데이터 로드 오류
- 파일 경로 확인 (`data/{팀원이름}/`)
- 파일 존재 여부 확인
- 인코딩 문제 확인

## 📞 지원

문제가 발생하면 팀 채널에서 문의하세요:
- **박진형**: kyj01138@gmail.com
- **김민정**: focso5@gmail.com
- **박도연**: pdyoen999@gmail.com
- **오흥재**: vfxpedia1987@kakao.com
