"""
경로 및 공통 함수 모음
"""

from pathlib import Path
import os

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 데이터 경로
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# 설정 파일 경로
CONFIG_DIR = PROJECT_ROOT / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.toml"

# 앱 경로
APP_DIR = PROJECT_ROOT / "app"
PAGES_DIR = APP_DIR / "pages"
COMPONENTS_DIR = APP_DIR / "components"

def ensure_directories():
    """필요한 디렉토리들이 존재하는지 확인하고 생성"""
    directories = [
        DATA_DIR,
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        EXTERNAL_DATA_DIR,
        CONFIG_DIR,
        APP_DIR,
        PAGES_DIR,
        COMPONENTS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_data_path(filename: str, data_type: str = "raw") -> Path:
    """데이터 파일의 전체 경로를 반환"""
    if data_type == "raw":
        return RAW_DATA_DIR / filename
    elif data_type == "interim":
        return INTERIM_DATA_DIR / filename
    elif data_type == "external":
        return EXTERNAL_DATA_DIR / filename
    else:
        raise ValueError(f"Unknown data_type: {data_type}")

def get_config_path(filename: str) -> Path:
    """설정 파일의 전체 경로를 반환"""
    return CONFIG_DIR / filename
