"""
경로 및 공통 함수 모음 - 현재 폴더 구조에 맞게 수정
"""

from pathlib import Path
import os

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 데이터 경로 - 현재 구조에 맞게 수정
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

# 팀원별 데이터 경로
OHJ_DATA_DIR = DATA_DIR / "ohj"  # 오흥재 데이터
PDY_DATA_DIR = DATA_DIR / "pdy"  # 박도연 데이터
KMJ_DATA_DIR = DATA_DIR / "kmj"  # 김민정 데이터
PJH_DATA_DIR = DATA_DIR / "pjh"  # 박진형 데이터

# 설정 파일 경로
CONFIG_DIR = PROJECT_ROOT / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.toml"

# 앱 경로 - 현재 구조에 맞게 수정
FRONT_DIR = PROJECT_ROOT / "front"
PAGES_DIR = FRONT_DIR / "pages"
COMPONENTS_DIR = FRONT_DIR / "components"

# 백엔드 경로
BACK_DIR = PROJECT_ROOT / "back"
DB_DIR = BACK_DIR / "db"

def ensure_directories():
    """필요한 디렉토리들이 존재하는지 확인하고 생성"""
    directories = [
        DATA_DIR,
        RAW_DATA_DIR,
        INTERIM_DATA_DIR,
        EXTERNAL_DATA_DIR,
        OHJ_DATA_DIR,
        PDY_DATA_DIR,
        KMJ_DATA_DIR,
        PJH_DATA_DIR,
        CONFIG_DIR,
        FRONT_DIR,
        PAGES_DIR,
        COMPONENTS_DIR,
        BACK_DIR,
        DB_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def get_data_path(filename: str, data_type: str = "raw", team: str = "ohj") -> Path:
    """데이터 파일의 전체 경로를 반환"""
    if data_type == "raw":
        base_dir = RAW_DATA_DIR
    elif data_type == "interim":
        base_dir = INTERIM_DATA_DIR
    elif data_type == "external":
        base_dir = EXTERNAL_DATA_DIR
    elif data_type == "team":
        # 팀원별 데이터 디렉토리
        team_dirs = {
            "ohj": OHJ_DATA_DIR,
            "pdy": PDY_DATA_DIR,
            "kmj": KMJ_DATA_DIR,
            "pjh": PJH_DATA_DIR
        }
        base_dir = team_dirs.get(team, OHJ_DATA_DIR)
    else:
        raise ValueError(f"Unknown data_type: {data_type}")
    
    return base_dir / filename

def get_config_path(filename: str) -> Path:
    """설정 파일의 전체 경로를 반환"""
    return CONFIG_DIR / filename

def get_db_script_path(filename: str, team: str = "ohj") -> Path:
    """DB 스크립트 파일의 전체 경로를 반환"""
    team_dirs = {
        "ohj": DB_DIR / "ohj",
        "pdy": DB_DIR / "pdy", 
        "kmj": DB_DIR / "kmj",
        "pjh": DB_DIR / "pjh"
    }
    return team_dirs.get(team, DB_DIR / "ohj") / filename

def get_front_path(filename: str) -> Path:
    """프론트엔드 파일의 전체 경로를 반환"""
    return FRONT_DIR / filename

def get_page_path(filename: str) -> Path:
    """페이지 파일의 전체 경로를 반환"""
    return PAGES_DIR / filename

# 자주 사용되는 경로들을 미리 정의
AUTO_REPAIR_CSV = get_data_path("auto_repair_standard.csv", "team", "ohj")
ENV_FILE = PROJECT_ROOT / ".env"
REQUIREMENTS_FILE = PROJECT_ROOT / "requirements.txt"
README_FILE = PROJECT_ROOT / "README.md"

if __name__ == "__main__":
    # 테스트 실행
    print("📁 프로젝트 경로 구조:")
    print(f"   ROOT: {PROJECT_ROOT}")
    print(f"   DATA: {DATA_DIR}")
    print(f"   FRONT: {FRONT_DIR}")
    print(f"   BACK: {BACK_DIR}")
    print(f"   OHJ_DATA: {OHJ_DATA_DIR}")
    print(f"   AUTO_REPAIR_CSV: {AUTO_REPAIR_CSV}")
    print(f"   ENV_FILE: {ENV_FILE}")
    
    # 디렉토리 생성 테스트
    ensure_directories()
    print("✅ 디렉토리 구조 확인 완료")