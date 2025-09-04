from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from functools import lru_cache
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# 프로젝트 루트 경로
ROOT = Path(__file__).resolve().parents[2]

def _load_env_files():
    """환경변수 파일들을 순차적으로 로드"""
    env_files = [
        ROOT / ".env",
        ROOT / ".streamlit" / "secrets.toml",
    ]
    
    # find_dotenv 결과 추가
    found_dotenv = find_dotenv(usecwd=True)
    if found_dotenv:
        env_files.append(Path(found_dotenv))
    
    loaded_files = []
    for env_file in env_files:
        if env_file and env_file.exists():
            try:
                if env_file.suffix == '.toml':
                    # TOML 파일은 직접 파싱하지 않고 Streamlit이 처리하도록 함
                    logger.info(f"TOML 파일 발견: {env_file}")
                else:
                    load_dotenv(env_file, override=True)
                    logger.info(f"환경변수 파일 로드됨: {env_file}")
                loaded_files.append(str(env_file))
            except Exception as e:
                logger.warning(f"환경변수 파일 로드 실패 {env_file}: {e}")
    
    return loaded_files

def _get_db_url_from_streamlit_secrets(alias: str | None = None) -> str | None:
    """Streamlit secrets에서 DB_URL 가져오기"""
    if st is None:
        return None
    
    try:
        # Streamlit 컨텍스트 확인
        if hasattr(st, 'secrets') and st.secrets is not None:
            # secrets에 alias별/기본 키 둘 다 지원
            if alias and f"DB_URL__{alias.upper()}" in st.secrets:
                return st.secrets[f"DB_URL__{alias.upper()}"]
            elif "DB_URL" in st.secrets:
                return st.secrets["DB_URL"]
    except Exception as e:
        logger.warning(f"Streamlit secrets에서 DB_URL 가져오기 실패: {e}")
    
    return None

def _get_db_url_from_env(alias: str | None = None) -> str | None:
    """환경변수에서 DB_URL 가져오기"""
    env_key = f"DB_URL__{alias.upper()}" if alias else "DB_URL"
    
    # 1) alias별 환경변수 시도
    db_url = os.getenv(env_key)
    if db_url:
        return db_url
    
    # 2) 기본 DB_URL 시도
    if alias:
        db_url = os.getenv("DB_URL")
        if db_url:
            return db_url
    
    return None

def _get_default_db_url() -> str:
    """기본 DB_URL 반환"""
    return "mysql+mysqlconnector://dochicar:dochicar@127.0.0.1:3306/dochicar"

def _env_key_for(alias: str | None) -> str:
    if alias:
        return f"DB_URL__{alias.upper()}"
    return "DB_URL"

def get_engine(alias: str | None = None) -> Engine:
    """팀별 별칭(alias) 또는 기본 환경변수/Streamlit secrets에서 Engine 생성"""
    
    # 환경변수 파일들 로드 (매번 새로 로드)
    loaded_files = _load_env_files()
    logger.info(f"로드된 환경변수 파일들: {loaded_files}")
    
    env_key = _env_key_for(alias)
    db_url = None
    
    # 1) Streamlit secrets 우선 시도
    db_url = _get_db_url_from_streamlit_secrets(alias)
    if db_url:
        logger.info(f"Streamlit secrets에서 DB_URL 로드됨 (alias: {alias})")
    
    # 2) 환경변수에서 시도
    if not db_url:
        db_url = _get_db_url_from_env(alias)
        if db_url:
            logger.info(f"환경변수에서 DB_URL 로드됨 (alias: {alias})")
    
    # 3) 기본값 사용
    if not db_url:
        db_url = _get_default_db_url()
        logger.info(f"기본 DB_URL 사용: {db_url[:30]}...")
    
    if not db_url:
        raise RuntimeError(
            f"환경변수 {env_key}이 없습니다. "
            "다음 중 하나를 설정하세요:\n"
            "1. .env 파일에 DB_URL=mysql+mysqlconnector://user:pass@host:port/db\n"
            "2. .streamlit/secrets.toml에 DB_URL = \"mysql+mysqlconnector://user:pass@host:port/db\"\n"
            "3. 환경변수로 DB_URL 설정"
        )

    try:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=5,
            max_overflow=10,
        )
        logger.info("데이터베이스 엔진 생성 성공")
        return engine
    except Exception as e:
        logger.error(f"데이터베이스 엔진 생성 실패: {e}")
        raise RuntimeError(f"데이터베이스 연결 실패: {e}")

# 모듈 로드 시 환경변수 파일들 로드
_load_env_files()