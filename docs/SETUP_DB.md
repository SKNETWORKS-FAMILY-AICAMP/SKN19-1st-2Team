# 🗄️ 데이터베이스 설정 가이드

## 📋 개요
DOCHICAR 프로젝트의 데이터베이스 설정을 위한 단계별 가이드입니다.

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
back/db/ohj/
├── 00_setup_database.py          # 🚀 자동 설정 스크립트 (팀원용)
├── 01_service_center_table.sql   # 📊 테이블 생성
├── 02_load_data_sources.py       # 📂 데이터 로더
└── 03_insert_service_centers_data.py # 💾 데이터 삽입
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

## 📞 지원

문제가 지속되면 팀 채널에서 문의하세요:
- 오흥재: vfxpedia1987@kakao.com
- 박진형: kyj01138@gmail.com
- 김민정: focso5@gmail.com
- 박도연: pdyoen999@gmail.com
