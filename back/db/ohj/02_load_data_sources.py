"""
02_load_data_sources.py
DOCHICAR 프로젝트 - 데이터 소스 로더
실행 순서: 2번 (01_service_center_table.sql 실행 후)
"""

import pandas as pd
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """데이터 로더 클래스"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
    
    def load_csv(self, filename: str, **kwargs) -> pd.DataFrame:
        """CSV 파일 로드 (인코딩 폴백 지원)"""
        try:
            file_path = self.data_dir / filename
            # UTF-8로 먼저 시도
            try:
                df = pd.read_csv(file_path, encoding="utf-8-sig", **kwargs)
            except UnicodeDecodeError:
                # CP949로 폴백
                df = pd.read_csv(file_path, encoding="cp949", **kwargs)
            logger.info(f"CSV 파일 로드 완료: {filename}, shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"CSV 파일 로드 실패: {filename}, error: {e}")
            raise
    
    def load_json(self, filename: str) -> Dict[Any, Any]:
        """JSON 파일 로드"""
        try:
            file_path = self.data_dir / filename
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"JSON 파일 로드 완료: {filename}")
            return data
        except Exception as e:
            logger.error(f"JSON 파일 로드 실패: {filename}, error: {e}")
            raise
    
    def load_xml(self, filename: str) -> ET.Element:
        """XML 파일 로드"""
        try:
            file_path = self.data_dir / filename
            tree = ET.parse(file_path)
            root = tree.getroot()
            logger.info(f"XML 파일 로드 완료: {filename}")
            return root
        except Exception as e:
            logger.error(f"XML 파일 로드 실패: {filename}, error: {e}")
            raise
    
    def load_excel(self, filename: str, sheet_name: Optional[str] = None, **kwargs) -> pd.DataFrame:
        """Excel 파일 로드"""
        try:
            file_path = self.data_dir / filename
            df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            logger.info(f"Excel 파일 로드 완료: {filename}, shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Excel 파일 로드 실패: {filename}, error: {e}")
            raise

def load_auto_repair_data(data_dir: Path) -> pd.DataFrame:
    """자동차 정비소 데이터 로드 - 현재 폴더 구조에 맞게 수정"""
    loader = DataLoader(data_dir)
    
    # 현재 폴더 구조: data/ohj/auto_repair_standard.csv
    csv_file = "auto_repair_standard.csv"
    json_file = "auto_repair_standard.json"
    
    if (data_dir / csv_file).exists():
        return loader.load_csv(csv_file)
    elif (data_dir / json_file).exists():
        data = loader.load_json(json_file)
        return pd.DataFrame(data)
    else:
        raise FileNotFoundError(f"정비소 데이터 파일을 찾을 수 없습니다: {csv_file} 또는 {json_file}")

def load_car_registration_data(data_dir: Path) -> pd.DataFrame:
    """자동차 등록 현황 데이터 로드"""
    loader = DataLoader(data_dir)
    
    # 자동차 등록 현황 파일 찾기
    registration_files = list(data_dir.glob("*자동차등록현황*"))
    
    if not registration_files:
        raise FileNotFoundError("자동차 등록 현황 데이터 파일을 찾을 수 없습니다.")
    
    # CSV 파일 우선 로드
    csv_files = [f for f in registration_files if f.suffix == '.csv']
    if csv_files:
        return loader.load_csv(csv_files[0].name)
    
    # Excel 파일 로드
    excel_files = [f for f in registration_files if f.suffix in ['.xlsx', '.xls']]
    if excel_files:
        return loader.load_excel(excel_files[0].name)
    
    raise FileNotFoundError("지원하는 형식의 자동차 등록 현황 데이터 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    # 테스트 실행
    ROOT = Path(__file__).resolve().parents[3]  # project_1st/
    DATA_DIR = ROOT / "data" / "ohj"
    
    try:
        df = load_auto_repair_data(DATA_DIR)
        print(f"[SUCCESS] 정비소 데이터 로드 성공: {df.shape}")
        print(f"컬럼: {list(df.columns)}")
    except Exception as e:
        print(f"[ERROR] 데이터 로드 실패: {e}")
