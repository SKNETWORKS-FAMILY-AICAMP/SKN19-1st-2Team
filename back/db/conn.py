from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os

try:
    import streamlit as st  # 선택적 의존성: st.secrets 사용
except Exception:
    st = None

"""
공용 DB 연결 유틸리티
- .env 의 DB_URL을 사용해 SQLAlchemy Engine 제공
- 팀원별 다른 DB를 연결할 수 있도록, 선택적으로 별칭 키를 받아 환경변수에서 조회
  예) DB_URL__TEAM1, DB_URL__TEAM2 ... 없으면 기본(DB_URL) 사용
"""


# .env 로드 전략(견고성 강화)
# 1) 실행 CWD 기준 자동 탐색(find_dotenv)
# 2) 파일 기준(project root 추정) 보조 탐색
ROOT = Path(__file__).resolve().parents[2]
dotenv_path = find_dotenv(usecwd=True) or str(ROOT / ".env")
load_dotenv(dotenv_path)


def _env_key_for(alias: str | None) -> str:
    if alias:
        return f"DB_URL__{alias.upper()}"
    return "DB_URL"


@lru_cache(maxsize=8)
def get_engine(alias: str | None = None) -> Engine:
    """팀별 별칭(alias) 또는 기본 환경변수/Streamlit secrets에서 Engine 생성"""
    env_key = _env_key_for(alias)

    # 1) Streamlit secrets 우선
    db_url = None
    if st is not None:
        try:
            # secrets에 alias별/기본 키 둘 다 지원
            if alias and f"DB_URL__{alias.upper()}" in st.secrets:
                db_url = st.secrets[f"DB_URL__{alias.upper()}"]
            elif "DB_URL" in st.secrets:
                db_url = st.secrets["DB_URL"]
        except Exception:
            pass

    # 2) 환경변수(.env 포함)
    if not db_url:
        db_url = os.getenv(env_key)
    if not db_url and alias:
        db_url = os.getenv("DB_URL")
    if not db_url:
        raise RuntimeError(
            "환경변수 DB_URL이 없습니다. .env 또는 .streamlit/secrets.toml에 DB_URL=mysql+pymysql://user:pass@host:port/db 형식으로 설정하세요."
        )
    return create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_size=5,
        max_overflow=10,
    )
