"""
00_setup_database.py
DOCHICAR 프로젝트 - 데이터베이스 자동 설정 스크립트
팀원들이 git pull 후 한 번에 실행할 수 있는 통합 스크립트
"""

import subprocess
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

def run_sql_script(sql_file: Path):
    """SQL 스크립트 실행"""
    print(f"🔧 SQL 스크립트 실행: {sql_file.name}")
    
    # MySQL 명령어 구성
    cmd = [
        "mysql",
        "-u", "root",  # 또는 적절한 사용자명
        "-p",  # 비밀번호 입력 요청
        "-e", f"source {sql_file.absolute()}"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, input="\n")
        if result.returncode == 0:
            print(f"✅ {sql_file.name} 실행 완료")
            return True
        else:
            print(f"❌ {sql_file.name} 실행 실패:")
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ MySQL 클라이언트를 찾을 수 없습니다. MySQL이 설치되어 있는지 확인하세요.")
        return False
    except Exception as e:
        print(f"❌ SQL 실행 중 오류: {e}")
        return False

def run_python_script(script_file: Path):
    """Python 스크립트 실행"""
    print(f"🐍 Python 스크립트 실행: {script_file.name}")
    
    try:
        result = subprocess.run([sys.executable, str(script_file)], 
                              capture_output=True, text=True, cwd=script_file.parent)
        if result.returncode == 0:
            print(f"✅ {script_file.name} 실행 완료")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {script_file.name} 실행 실패:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Python 스크립트 실행 중 오류: {e}")
        return False

def check_requirements():
    """필수 요구사항 확인"""
    print("🔍 필수 요구사항 확인 중...")
    
    # 1) .env 파일 확인
    ROOT = Path(__file__).resolve().parents[3]  # project_1st/ 까지 올라가기
    env_file = ROOT / ".env"
    
    if not env_file.exists():
        print("❌ .env 파일이 없습니다.")
        print("   env.example을 복사하여 .env를 생성하고 DB_URL을 설정하세요.")
        return False
    
    # 2) .env에서 DB_URL 확인
    load_dotenv(env_file)
    db_url = os.getenv("DB_URL")
    if not db_url:
        print("❌ .env 파일에 DB_URL이 설정되지 않았습니다.")
        return False
    
    print(f"✅ .env 파일 확인 완료: {db_url[:20]}...")
    
    # 3) CSV 파일 확인
    csv_file = ROOT / "data" / "ohj" / "auto_repair_standard.csv"
    if not csv_file.exists():
        print(f"❌ CSV 파일을 찾을 수 없습니다: {csv_file}")
        return False
    
    print(f"✅ CSV 파일 확인 완료: {csv_file.name}")
    
    return True

def main():
    """메인 실행 함수"""
    print("🚀 DOCHICAR 데이터베이스 자동 설정 시작")
    print("=" * 50)
    
    # 0) 요구사항 확인
    if not check_requirements():
        print("❌ 필수 요구사항을 만족하지 않습니다. 위의 오류를 해결한 후 다시 실행하세요.")
        return False
    
    # 스크립트 파일 경로
    script_dir = Path(__file__).parent
    scripts = [
        ("01_service_center_table.sql", "SQL"),
        ("02_load_data_sources.py", "Python"),
        ("03_insert_service_centers_data.py", "Python"),
    ]
    
    # MySQL 클라이언트 확인
    mysql_available = True
    try:
        subprocess.run(["mysql", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        mysql_available = False
        print("⚠️ MySQL 클라이언트를 찾을 수 없습니다. Python 스크립트만 실행합니다.")
    
    success_count = 0
    
    # 각 스크립트 순차 실행
    for script_name, script_type in scripts:
        script_path = script_dir / script_name
        
        if not script_path.exists():
            print(f"⚠️ 스크립트 파일을 찾을 수 없습니다: {script_name}")
            continue
        
        print(f"\n📋 {script_name} 실행 중...")
        
        if script_type == "SQL":
            if mysql_available:
                success = run_sql_script(script_path)
            else:
                print(f"⚠️ {script_name} 건너뜀 (MySQL 클라이언트 없음)")
                success = True  # 건너뛰기로 처리
        else:  # Python
            success = run_python_script(script_path)
        
        if success:
            success_count += 1
        else:
            print(f"❌ {script_name} 실행 실패로 중단됩니다.")
            break
    
    # 결과 요약
    print("\n" + "=" * 50)
    print("📊 실행 결과 요약")
    print(f"   성공: {success_count}/{len(scripts)}")
    
    if success_count == len(scripts):
        print("🎉 모든 스크립트가 성공적으로 실행되었습니다!")
        print("   이제 streamlit run front/main.py로 애플리케이션을 실행할 수 있습니다.")
        return True
    else:
        print("❌ 일부 스크립트 실행에 실패했습니다.")
        print("   오류 메시지를 확인하고 문제를 해결한 후 다시 실행하세요.")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류가 발생했습니다: {e}")
        sys.exit(1)
