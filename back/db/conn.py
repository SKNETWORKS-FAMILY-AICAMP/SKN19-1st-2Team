from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from functools import lru_cache
from dotenv import load_dotenv
from pathlib import Path
import os

"""
공용 DB 연결 유틸리티
- .env 의 DB_URL을 사용해 SQLAlchemy Engine 제공
- 팀원별 다른 DB를 연결할 수 있도록, 선택적으로 별칭 키를 받아 환경변수에서 조회
  예) DB_URL__TEAM1, DB_URL__TEAM2 ... 없으면 기본(DB_URL) 사용
"""


# 프로젝트 루트의 .env 로드
ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")


def _env_key_for(alias: str | None) -> str:
    if alias:
        return f"DB_URL__{alias.upper()}"
    return "DB_URL"


@lru_cache(maxsize=8)
def get_engine(alias: str | None = None) -> Engine:
    """팀별 별칭(alias) 또는 기본 환경변수로부터 Engine 생성/캐시"""
    env_key = _env_key_for(alias)
    db_url = os.getenv(env_key)
    if not db_url and alias:
        # 별칭이 비어있다면 기본으로 폴백
        db_url = os.getenv("DB_URL")
    if not db_url:
        raise RuntimeError(
            "환경변수 DB_URL이 없습니다. .env에 DB_URL=mysql+mysqlconnector://user:pass@host:port/db 형식으로 설정하세요."
        )
    return create_engine(db_url, pool_pre_ping=True, pool_recycle=3600, pool_size=5, max_overflow=10)
