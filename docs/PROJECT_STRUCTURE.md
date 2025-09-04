# 🏗️ 프로젝트 구조 상세

## 📁 전체 폴더 구조

```
project_1st/
├── front/                           # Streamlit 프런트엔드
│   ├── main.py                      # 메인 페이지 진입점
│   ├── pages/                       # 각 기능별 페이지
│   │   ├── 01_Search.py             # 신차 검색 (박진형)
│   │   ├── 02_Recommend.py          # 추천 (김민정)
│   │   ├── 03_Compare.py            # 비교 (박도연)
│   │   ├── 04_Service_Centers.py    # 정비소 현황 (오흥재)
│   │   └── 05_FAQ.py                # FAQ (박진형)
│   └── .streamlit/                  # Streamlit 설정
│       └── secrets.toml             # DB 연결 정보 (선택사항)
├── back/                            # 백엔드/공용 모듈
│   ├── db/                          # 데이터베이스 관련
│   │   ├── conn.py                  # 공용 DB 커넥션 유틸
│   │   ├── pjh/                     # 박진형 DB 스크립트
│   │   │   ├── 01_car_models_table.sql
│   │   │   ├── 02_faq_table.sql
│   │   │   ├── 03_insert_car_data.py
│   │   │   └── 04_insert_faq_data.py
│   │   ├── kmj/                     # 김민정 DB 스크립트
│   │   │   ├── 01_user_preferences_table.sql
│   │   │   ├── 02_recommendation_algorithm.py
│   │   │   └── 03_insert_preference_data.py
│   │   ├── pdy/                     # 박도연 DB 스크립트
│   │   │   ├── 01_comparison_table.sql
│   │   │   ├── 02_like_system.py
│   │   │   └── 03_insert_comparison_data.py
│   │   └── ohj/                     # 오흥재 DB 스크립트
│   │       ├── 00_setup_database.py # 자동 설정 스크립트
│   │       ├── 01_service_center_table.sql
│   │       ├── 02_load_data_sources.py
│   │       └── 03_insert_service_centers_data.py
│   └── utils/                       # 공용 유틸리티
│       └── paths.py                 # 경로 유틸리티
├── data/                            # 데이터 저장소
│   ├── raw/                         # 원본 데이터
│   ├── interim/                     # 중간 처리 데이터
│   ├── external/                    # 외부 데이터
│   ├── pjh/                         # 박진형 데이터
│   │   ├── car_models.csv
│   │   ├── faq_data.csv
│   │   └── danawa_crawling_data.csv
│   ├── kmj/                         # 김민정 데이터
│   │   ├── age_preference_data.csv
│   │   ├── region_data.csv
│   │   └── registration_stats.csv
│   ├── pdy/                         # 박도연 데이터
│   │   ├── comparison_data.csv
│   │   ├── like_data.csv
│   │   └── car_specs.csv
│   └── ohj/                         # 오흥재 데이터
│       ├── auto_repair_standard.csv
│       └── service_center_data.csv
├── docs/                            # 프로젝트 문서
│   ├── SETUP_DB.md                  # DB 설정 가이드
│   ├── TEAM_GUIDE.md                # 팀원별 개발 가이드
│   └── PROJECT_STRUCTURE.md         # 프로젝트 구조 (이 파일)
├── research/                        # 연구/참고 자료
│   ├── data/                        # 연구용 데이터
│   ├── insight/                     # 인사이트
│   └── project_reference/           # 프로젝트 참고 자료
├── notebooks/                       # Jupyter 노트북
├── requirements.txt                 # Python 의존성
├── env.example                      # 환경변수 예시
├── .env                             # 환경변수 (로컬, Git 제외)
├── .gitignore                       # Git 제외 파일
├── package.json                     # Node.js 의존성 (선택사항)
├── package-lock.json                # Node.js 잠금 파일
└── README.md                        # 프로젝트 문서
```

## 🔧 핵심 파일 설명

### 1. 프론트엔드 (front/)

#### `main.py`
- Streamlit 애플리케이션의 진입점
- 메인 페이지 (홈) 구현
- 네비게이션 및 브랜딩

#### `pages/` 폴더
- 각 기능별 페이지 구현
- 팀원별 담당 페이지 분리
- 공통 DB 연결 모듈 사용

### 2. 백엔드 (back/)

#### `db/conn.py`
- 공용 DB 커넥션 유틸리티
- SQLAlchemy Engine 제공
- 환경변수(.env) 및 Streamlit secrets 지원

#### `db/{팀원이름}/` 폴더
- 팀원별 DB 스크립트
- 테이블 생성, 데이터 삽입 스크립트
- 번호 매기기로 실행 순서 관리

#### `utils/paths.py`
- 프로젝트 경로 관리
- 팀원별 데이터 경로 제공
- 디렉토리 자동 생성

### 3. 데이터 (data/)

#### `{팀원이름}/` 폴더
- 팀원별 데이터 저장소
- CSV, JSON, Excel 파일
- 크롤링 데이터, 공공데이터

### 4. 문서 (docs/)

#### `SETUP_DB.md`
- 데이터베이스 설정 가이드
- 자동 설정 스크립트 사용법
- 문제 해결 방법

#### `TEAM_GUIDE.md`
- 팀원별 개발 가이드
- 역할 분담 및 개발 규칙
- 코드 예시 및 템플릿

## 🗄️ 데이터베이스 구조

### 테이블 설계

#### 1. 정비소 테이블 (service_center) - 오흥재
```sql
CREATE TABLE service_center (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_ko VARCHAR(200) NOT NULL,
    type_code INT,
    addr_road VARCHAR(300),
    addr_jibun VARCHAR(300),
    lat DECIMAL(10,7),
    lon DECIMAL(10,7),
    phone VARCHAR(30),
    open_time VARCHAR(10),
    close_time VARCHAR(10),
    status_code INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 2. 차량 모델 테이블 (car_models) - 박진형
```sql
CREATE TABLE car_models (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INT,
    price DECIMAL(10, 2),
    fuel_type VARCHAR(50),
    car_type VARCHAR(50),
    engine_size DECIMAL(3, 1),
    fuel_efficiency DECIMAL(4, 1),
    safety_rating INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. 사용자 선호도 테이블 (user_preferences) - 김민정
```sql
CREATE TABLE user_preferences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_model_id INT,
    user_ip VARCHAR(45),
    age_group VARCHAR(20),
    region VARCHAR(50),
    preference_type ENUM('like', 'dislike', 'view') DEFAULT 'view',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (car_model_id) REFERENCES car_models(id)
);
```

#### 4. FAQ 테이블 (faq) - 박진형
```sql
CREATE TABLE faq (
    id INT AUTO_INCREMENT PRIMARY KEY,
    manufacturer VARCHAR(100),
    category VARCHAR(100),
    question TEXT,
    answer TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 데이터 흐름

### 1. 데이터 수집
```
공공데이터/크롤링 → data/{팀원이름}/ → CSV/JSON 파일
```

### 2. 데이터 처리
```
CSV/JSON → back/db/{팀원이름}/02_load_data_sources.py → DataFrame
```

### 3. 데이터베이스 적재
```
DataFrame → back/db/{팀원이름}/03_insert_data.py → MySQL 테이블
```

### 4. 웹 애플리케이션
```
MySQL → back/db/conn.py → front/pages/{페이지}.py → Streamlit UI
```

## 🚀 배포 및 실행

### 1. 로컬 개발 환경
```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경변수 설정
cp env.example .env
# .env 파일 수정

# 3. 데이터베이스 설정
python back/db/ohj/00_setup_database.py

# 4. 애플리케이션 실행
streamlit run front/main.py
```

### 2. 팀원별 개발
```bash
# 1. Git pull
git pull origin main

# 2. 환경 설정
pip install -r requirements.txt
cp env.example .env

# 3. 자동 설정
python back/db/ohj/00_setup_database.py

# 4. 개발 시작
streamlit run front/main.py
```

## 🔧 설정 파일

### 1. 환경변수 (.env)
```bash
# 데이터베이스 연결
DB_URL=mysql+pymysql://user:password@127.0.0.1:3306/dochicar

# API 키 (필요시)
API_KEY=your_api_key_here
```

### 2. Streamlit 설정 (front/.streamlit/secrets.toml)
```toml
DB_URL = "mysql+pymysql://user:password@127.0.0.1:3306/dochicar"
```

### 3. Python 의존성 (requirements.txt)
```
streamlit>=1.28.0
pandas>=2.0.0
sqlalchemy>=2.0.0
pymysql>=1.1.0
python-dotenv>=1.0.0
plotly>=5.15.0
```

## 📊 모니터링 및 로깅

### 1. 로깅 설정
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 2. 에러 처리
```python
try:
    # DB 작업
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
except Exception as e:
    st.error(f"데이터베이스 오류: {e}")
    logging.error(f"DB Error: {e}")
```

## 🔒 보안 고려사항

### 1. 환경변수 보안
- `.env` 파일은 Git에 커밋하지 않음
- 민감한 정보는 환경변수로 관리
- Streamlit secrets 사용 권장

### 2. 데이터베이스 보안
- 로컬 개발용 사용자 계정 사용
- 프로덕션 환경에서는 강력한 비밀번호 사용
- 방화벽 설정으로 외부 접근 제한

### 3. 코드 보안
- 하드코딩된 비밀번호 금지
- SQL 인젝션 방지 (파라미터화된 쿼리 사용)
- 입력 데이터 검증
