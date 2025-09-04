# 🚗 DOCHICHA.Inc

자동차 등록 데이터 기반 신차 비교·추천 플랫폼

## 📋 프로젝트 개요

**DOCHICHA.Inc**는 최근 3년간 자동차등록 데이터를 통한 트렌드 동향 분석을 기반으로 사용자가 신차를 비교·구매할 수 있도록 지원하는 데이터 기반 서비스입니다.

### 🎯 주요 목표
- 공공데이터와 크롤링 데이터를 통합해 데이터 기반 차량 비교·추천 플랫폼 구현
- 지역별 정비소 현황을 지도 기반으로 제공하여 구매 후 유지보수까지 고려 가능
- 소비자의 차량 구매 의사결정을 돕는 원스톱 플랫폼 구축

## 🏗️ 프로젝트 구조

```
project_1st/
├── front/                       # Streamlit 프런트엔드
│   ├── main.py                  # 메인(Home) 페이지 진입점
│   └── pages/                   # 각 기능별 페이지
│       ├── 01_Search.py         # 신차 검색
│       ├── 02_Recommend.py      # 추천
│       ├── 03_Compare.py        # 비교
│       └── 04_Service_Centers.py# 정비소 현황
├── back/                        # 백엔드/공용 모듈
│   └── db/
│       └── conn.py              # 공용 DB 커넥션 유틸 (DB_URL 읽음)
├── data/                        # 데이터 저장소
│   ├── raw/
│   ├── interim/
│   └── external/
├── requirements.txt             # Python 의존성
├── env.example                  # 환경변수 예시(.env 템플릿)
└── README.md                    # 프로젝트 문서
```

## 🚀 시작하기

### 1. 환경 설정

#### Python 환경
```bash
# Python 의존성 설치
pip install -r requirements.txt
```

#### Node.js 환경 (선택사항)
```bash
# npm 의존성 설치 (필요시)
npm install
```

### 2. 환경 변수 설정

옵션 A) 루트 .env 사용(권장)
```bash
cp env.example .env
# .env 를 열어 DB_URL 값을 채웁니다 (예시)
# DB_URL=mysql+pymysql://user:password@127.0.0.1:3306/dbname
```

옵션 B) Streamlit secrets 사용(동일 효과)
```
front/.streamlit/secrets.toml

DB_URL = "mysql+pymysql://user:password@127.0.0.1:3306/dbname"
```

참고: 보안상 .env/.toml 파일은 Git에 커밋하지 않습니다. 각 개발자 로컬에서 개별 구성합니다.

### 3. 애플리케이션 실행

#### Streamlit으로 실행
```bash
# 프로젝트 루트에서 실행
pip install -r requirements.txt

streamlit run front/main.py
```

#### Node.js 스크립트로 실행
```bash
# package.json의 스크립트 사용
npm run start
```

## 🗄️ 데이터베이스 설정

### MySQL 설정
1. MySQL 서버 설치 및 실행
2. 데이터베이스 생성(예시):
   ```sql
   CREATE DATABASE dochicar CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 연결 정보는 `.env` 또는 `front/.streamlit/secrets.toml`의 `DB_URL`에 설정
   - 예: `DB_URL=mysql+pymysql://dochicar:dochicar@127.0.0.1:3306/dochicar`
   - mysqlconnector를 선호하면: `mysql+mysqlconnector://user:pass@host:3306/dbname`

## 📊 주요 기능

### 1. 🔍 신차 검색
- 차량명, 가격, 차종, 출시일 기준 검색
- 다나와 신차 크롤링 데이터 기반

### 2. 💡 맞춤 추천
- 사용자 입력(연령대, 지역, 차종, 예산) 기반 맞춤형 추천
- 최근 3년간 등록 현황 데이터와 연계

### 3. ⚖️ 차량 비교
- 최대 3개 차량 비교 (제원·가격·안전등급 등)
- 좋아요 기능 → MySQL COUNT 기반 선호도 집계

### 4. 🔧 정비소 현황
- 지역별 정비소 검색 및 필터링
- 지도 시각화 (위도·경도 활용)
- 전화번호, 평점, 인증 여부 등 상세 제공

### 5. ❓ FAQ
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

## 👥 팀 구성

**따봉도치 팀 (2팀)** - SK네트웍스 Family AI 캠프 19기

- **JAY**: 정비소 현황 페이지(REPAIR), FAQ, 메인 페이지(Home) 뼈대
- **팀원 A**: 신차 데이터 수집/검색 (SEARCH)
- **팀원 B**: 추천 알고리즘 및 데이터 시각화 (RECOMMEND)
- **팀원 C**: 차량 비교 및 좋아요 통계 (COMPARE)

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
