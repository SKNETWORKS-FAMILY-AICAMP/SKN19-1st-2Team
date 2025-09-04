# 🚗 DOCHICAR.Inc

자동차 등록 데이터 기반 신차 비교·추천 플랫폼

## 📋 프로젝트 개요

**DOCHICAR.Inc**는 최근 3년간 자동차등록 데이터를 통한 트렌드 동향 분석을 기반으로 사용자가 신차를 비교·구매할 수 있도록 지원하는 데이터 기반 서비스입니다.

### 🎯 주요 목표
- 공공데이터와 크롤링 데이터를 통합해 데이터 기반 차량 비교·추천 플랫폼 구현
- 지역별 정비소 현황을 지도 기반으로 제공하여 구매 후 유지보수까지 고려 가능
- 소비자의 차량 구매 의사결정을 돕는 원스톱 플랫폼 구축

## 👥 팀 구성 및 역할 분담

**따봉도치 팀 (2팀)** - SK네트웍스 Family AI 캠프 19기

| 팀원 | 역할 | 담당 페이지 | 데이터 | DB 스크립트 |
|------|------|-------------|--------|-------------|
| **박진형 (PJH)** | 신차 검색, FAQ | `01_Search.py`, `05_FAQ.py` | `data/pjh/` | `back/db/pjh/` |
| **김민정 (KMJ)** | 맞춤 추천 | `02_Recommend.py` | `data/kmj/` | `back/db/kmj/` |
| **박도연 (PDY)** | 차량 비교 | `03_Compare.py` | `data/pdy/` | `back/db/pdy/` |
| **오흥재 (OHJ)** | 정비소 현황 | `04_Service_Centers.py` | `data/ohj/` | `back/db/ohj/` |

### 📧 연락처
- **박진형**: kyj01138@gmail.com
- **김민정**: focso5@gmail.com  
- **박도연**: pdyoen999@gmail.com
- **오흥재**: vfxpedia1987@kakao.com

## 🏗️ 프로젝트 구조

```
project_1st/
├── front/                       # Streamlit 프런트엔드
│   ├── main.py                  # 메인 페이지 진입점
│   └── pages/                   # 각 기능별 페이지
│       ├── 01_Search.py         # 신차 검색
│       ├── 02_Recommend.py      # 추천
│       ├── 03_Compare.py        # 비교
│       ├── 04_Service_Centers.py# 정비소 현황
│       └── 05_FAQ.py            # FAQ
├── back/                        # 백엔드/공용 모듈
│   ├── db/
│   │   ├── conn.py              # 공용 DB 커넥션 유틸
│   │   ├── pjh/                 # 박진형 DB 스크립트
│   │   ├── kmj/                 # 김민정 DB 스크립트
│   │   ├── pdy/                 # 박도연 DB 스크립트
│   │   └── ohj/                 # 오흥재 DB 스크립트
│   └── utils/
│       └── paths.py             # 경로 유틸리티
├── data/                        # 데이터 저장소
│   ├── pjh/                     # 박진형 데이터
│   ├── kmj/                     # 김민정 데이터
│   ├── pdy/                     # 박도연 데이터
│   └── ohj/                     # 오흥재 데이터
├── docs/                        # 프로젝트 문서
│   ├── SETUP_DB.md              # DB 설정 가이드
│   ├── TEAM_GUIDE.md            # 팀원별 개발 가이드
│   └── PROJECT_STRUCTURE.md     # 프로젝트 구조 상세
├── requirements.txt             # Python 의존성
├── env.example                  # 환경변수 예시
└── README.md                    # 프로젝트 문서
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# Python 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp env.example .env
# .env 파일을 열어 DB_URL을 본인 환경에 맞게 수정
```

### 2. 데이터베이스 설정

#### 자동 설정 (권장)
```bash
# 프로젝트 루트에서 실행
python back/db/ohj/00_setup_database.py
```

#### 수동 설정
```bash
# 1. 테이블 생성 (MySQL 클라이언트 필요)
mysql -u root -p < back/db/ohj/01_service_center_table.sql

# 2. 데이터 삽입
python back/db/ohj/02_load_data_sources.py
python back/db/ohj/03_insert_service_centers_data.py
```

### 3. 애플리케이션 실행

```bash
# Streamlit으로 실행
streamlit run front/main.py
```

## 📊 주요 기능

### 1. 🔍 신차 검색 (박진형)
- 차량명, 가격, 차종, 출시일 기준 검색
- 다나와 신차 크롤링 데이터 기반
- FAQ 페이지 연동

### 2. 💡 맞춤 추천 (김민정)
- 사용자 입력(연령대, 지역, 차종, 예산) 기반 맞춤형 추천
- 최근 3년간 등록 현황 데이터와 연계
- 데이터 시각화

### 3. ⚖️ 차량 비교 (박도연)
- 최대 3개 차량 비교 (제원·가격·안전등급 등)
- 좋아요 기능 → MySQL COUNT 기반 선호도 집계

### 4. 🔧 정비소 현황 (오흥재)
- 지역별 정비소 검색 및 필터링
- 지도 시각화 (위도·경도 활용)
- 전화번호, 평점, 인증 여부 등 상세 제공

### 5. ❓ FAQ (박진형)
- 신차 구매 시 자주 묻는 질문(계약·납기·보증 등) 제공
- 제조사별 FAQ 크롤링/연동

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **Backend**: Python 3.11+
- **Database**: MySQL
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib, Folium
- **Web Scraping**: BeautifulSoup, Requests
- **Configuration**: TOML, Python-dotenv

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

## 📚 추가 문서

- [데이터베이스 설정 가이드](docs/SETUP_DB.md)
- [팀원별 개발 가이드](docs/TEAM_GUIDE.md)
- [프로젝트 구조 상세](docs/PROJECT_STRUCTURE.md)
- [프로젝트 기획서](project_plan.md)

## 📈 기대효과

### 소비자
- 최근 3년간 등록 트렌드 기반 신차 비교 제공
- 차량 구매 시 정비소/리콜/FAQ까지 고려한 합리적 의사결정 지원

### 학습/팀 성과
- 공공데이터+크롤링+DB+시각화 엔드투엔드 프로젝트 경험
- Python, MySQL, Streamlit, Web Crawling 등 학습 내용을 종합 적용
- GitHub 협업과 데이터 정규화 실습을 통한 실무 능력 강화

## 📝 라이선스

MIT License

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request