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
├── app/                          # Streamlit 애플리케이션
│   ├── streamlit_app.py         # 메인(Home) 페이지
│   ├── pages/                   # 각 기능별 페이지
│   │   ├── 01_Search.py         # 신차 검색
│   │   ├── 02_Recommend.py      # 추천
│   │   ├── 03_Compare.py        # 비교
│   │   ├── 04_Service_Centers.py # 정비소 현황
│   │   └── 05_FAQ.py            # FAQ
│   └── components/              # 공통 UI 위젯 모음
├── config/                      # 설정 파일
│   └── settings.example.toml    # 설정 예시
├── data/                        # 데이터 저장소
│   ├── raw/                     # 원본 JSON/CSV/XML
│   ├── interim/                 # 정제 후 캐시본
│   └── external/                # 외부 참조 데이터
├── src/                         # 소스 코드
│   ├── ingest/                  # 데이터 로더
│   ├── cleaning/                # 데이터 정제
│   └── utils/                   # 경로/공통 함수
├── notebooks/                   # 데이터 분석/EDA 노트북
├── requirements.txt             # Python 의존성
├── package.json                 # Node.js 설정
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

```bash
# 환경 변수 파일 복사
cp env.example .env

# .env 파일 편집하여 데이터베이스 정보 입력
```

### 3. 애플리케이션 실행

#### Streamlit으로 실행
```bash
# 개발 모드로 실행
npm run dev

# 또는 직접 실행
streamlit run app/streamlit_app.py
```

#### Node.js 스크립트로 실행
```bash
# package.json의 스크립트 사용
npm run start
```

## 🗄️ 데이터베이스 설정

### MySQL 설정
1. MySQL 서버 설치 및 실행
2. 데이터베이스 생성:
   ```sql
   CREATE DATABASE dochicha_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. `.env` 파일에 데이터베이스 연결 정보 입력

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
