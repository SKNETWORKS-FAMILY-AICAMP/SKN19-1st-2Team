# 🗄️ 데이터베이스 설정 가이드

## 📋 개요
DOCHICAR 프로젝트의 데이터베이스 설정을 위한 단계별 가이드입니다.

## 👥 팀원별 DB 설정

### 팀원별 담당 테이블
- **박진형 (PJH)**: `car_models`, `faq` 테이블
- **김민정 (KMJ)**: `user_preferences` 테이블  
- **박도연 (PDY)**: `comparison_data`, `like_system` 테이블
- **오흥재 (OHJ)**: `service_center` 테이블 (기본 설정 완료)

## 🚀 빠른 시작 (팀원용)

### 1. 환경 설정
```bash
# 1) 의존성 설치
pip install -r requirements.txt

# 2) 환경변수 설정
cp env.example .env
# .env 파일을 열어 DB_URL을 본인 환경에 맞게 수정
```

### 2. 자동 설정 (권장)
```bash
# 프로젝트 루트에서 실행
python back/db/ohj/00_setup_database.py
```

이 스크립트가 자동으로 다음을 수행합니다:
- ✅ 필수 요구사항 확인 (.env, CSV 파일)
- ✅ 01_service_center_table.sql 실행 (테이블 생성)
- ✅ 02_load_data_sources.py 실행 (데이터 로드)
- ✅ 03_insert_service_centers_data.py 실행 (데이터 삽입)

### 3. 수동 설정 (문제 발생 시)

#### 3-1. MySQL 테이블 생성
```bash
# MySQL에 로그인 후
mysql -u root -p < back/db/ohj/01_service_center_table.sql
```

#### 3-2. 데이터 삽입
```bash
python back/db/ohj/02_load_data_sources.py
python back/db/ohj/03_insert_service_centers_data.py
```

## 📁 파일 구조

```
back/db/
├── ohj/                          # 오흥재 (정비소 현황)
│   ├── 00_setup_database.py      # 🚀 자동 설정 스크립트 (팀원용)
│   ├── 01_service_center_table.sql
│   ├── 02_load_data_sources.py
│   └── 03_insert_service_centers_data.py
├── pjh/                          # 박진형 (신차 검색, FAQ)
│   ├── 01_car_models_table.sql
│   ├── 02_faq_table.sql
│   ├── 03_insert_car_data.py
│   └── 04_insert_faq_data.py
├── kmj/                          # 김민정 (추천)
│   ├── 01_user_preferences_table.sql
│   ├── 02_recommendation_algorithm.py
│   └── 03_insert_preference_data.py
└── pdy/                          # 박도연 (비교)
    ├── 01_comparison_table.sql
    ├── 02_like_system.py
    └── 03_insert_comparison_data.py
```

## 🔧 환경변수 설정

### .env 파일 예시
```bash
# 데이터베이스 URL
DB_URL=mysql+pymysql://user:password@127.0.0.1:3306/dochicar

# 또는 mysqlconnector 사용
DB_URL=mysql+mysqlconnector://user:password@127.0.0.1:3306/dochicar
```

### Streamlit secrets 사용 (대안)
`front/.streamlit/secrets.toml` 파일 생성:
```toml
DB_URL = "mysql+pymysql://user:password@127.0.0.1:3306/dochicar"
```

## 🐛 문제 해결

### 1. "Access denied" 오류
- MySQL 사용자 계정/비밀번호 확인
- .env의 DB_URL이 올바른지 확인
- MySQL 서버가 실행 중인지 확인

### 2. "Table doesn't exist" 오류
- 01_service_center_table.sql이 먼저 실행되었는지 확인
- MySQL에서 `SHOW TABLES;`로 테이블 존재 확인

### 3. "CSV 파일을 찾을 수 없습니다" 오류
- `data/ohj/auto_repair_standard.csv` 파일이 존재하는지 확인
- 파일 경로가 올바른지 확인

### 4. 드라이버 오류
```bash
# PyMySQL 설치
pip install pymysql

# 또는 mysql-connector-python 설치
pip install mysql-connector-python
```

## 📊 데이터 확인

### MySQL에서 확인
```sql
USE dochicar;
SELECT COUNT(*) FROM service_center;
SELECT * FROM service_center LIMIT 5;
```

### Python에서 확인
```python
from back.db.conn import get_engine
import pandas as pd

engine = get_engine()
df = pd.read_sql("SELECT COUNT(*) as total FROM service_center", engine)
print(f"총 {df['total'].iloc[0]}건의 정비소 데이터가 있습니다.")
```

## 🔄 데이터 재설정

기존 데이터를 삭제하고 새로 설정하려면:

```sql
-- MySQL에서 실행
USE dochicar;
TRUNCATE TABLE service_center;
```

그 후 다시 `00_setup_database.py` 실행

## 👥 팀원별 추가 설정

### 박진형 (PJH) - 신차 검색 & FAQ
```bash
# 차량 모델 테이블 생성
mysql -u root -p < back/db/pjh/01_car_models_table.sql

# FAQ 테이블 생성  
mysql -u root -p < back/db/pjh/02_faq_table.sql

# 데이터 삽입
python back/db/pjh/03_insert_car_data.py
python back/db/pjh/04_insert_faq_data.py
```

### 김민정 (KMJ) - 추천 시스템
```bash
# 사용자 선호도 테이블 생성
mysql -u root -p < back/db/kmj/01_user_preferences_table.sql

# 데이터 삽입
python back/db/kmj/03_insert_preference_data.py
```

### 박도연 (PDY) - 차량 비교
```bash
# 비교 테이블 생성
mysql -u root -p < back/db/pdy/01_comparison_table.sql

# 데이터 삽입
python back/db/pdy/03_insert_comparison_data.py
```

### 오흥재 (OHJ) - 정비소 현황 (기본 설정 완료)
```bash
# 이미 00_setup_database.py로 설정 완료
# 추가 설정이 필요한 경우 개별 스크립트 실행
```

## 📞 지원

문제가 지속되면 팀 채널에서 문의하세요:
- **박진형**: kyj01138@gmail.com
- **김민정**: focso5@gmail.com
- **박도연**: pdyoen999@gmail.com
- **오흥재**: vfxpedia1987@kakao.com
