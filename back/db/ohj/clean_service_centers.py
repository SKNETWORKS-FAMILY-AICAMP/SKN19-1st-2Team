"""
정비소 데이터 정제 모듈
공공데이터의 정비소 정보를 정제하고 표준화
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServiceCenterCleaner:
    """정비소 데이터 정제 클래스"""
    
    def __init__(self):
        self.required_columns = [
            '업체명', '주소', '전화번호', '위도', '경도', 
            '업종', '인증여부', '평점'
        ]
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """정비소 데이터 정제"""
        logger.info(f"정제 전 데이터 shape: {df.shape}")
        
        # 1. 기본 정제
        df_cleaned = self._basic_cleaning(df)
        
        # 2. 주소 정제
        df_cleaned = self._clean_address(df_cleaned)
        
        # 3. 전화번호 정제
        df_cleaned = self._clean_phone(df_cleaned)
        
        # 4. 좌표 정제
        df_cleaned = self._clean_coordinates(df_cleaned)
        
        # 5. 중복 제거
        df_cleaned = self._remove_duplicates(df_cleaned)
        
        logger.info(f"정제 후 데이터 shape: {df_cleaned.shape}")
        return df_cleaned
    
    def _basic_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """기본 정제 작업"""
        # 컬럼명 표준화
        column_mapping = {
            '업체명': '업체명',
            '사업장명': '업체명',
            '업소명': '업체명',
            '주소': '주소',
            '도로명주소': '주소',
            '지번주소': '주소',
            '전화번호': '전화번호',
            '대표전화': '전화번호',
            '연락처': '전화번호',
            '위도': '위도',
            '경도': '경도',
            '업종': '업종',
            '업태': '업종',
            '인증여부': '인증여부',
            '평점': '평점'
        }
        
        # 컬럼명 변경
        df = df.rename(columns=column_mapping)
        
        # 필수 컬럼이 없으면 기본값으로 추가
        for col in self.required_columns:
            if col not in df.columns:
                if col in ['위도', '경도', '평점']:
                    df[col] = np.nan
                else:
                    df[col] = ''
        
        return df
    
    def _clean_address(self, df: pd.DataFrame) -> pd.DataFrame:
        """주소 정제"""
        if '주소' in df.columns:
            # 주소에서 불필요한 문자 제거
            df['주소'] = df['주소'].astype(str).str.strip()
            df['주소'] = df['주소'].str.replace(r'\s+', ' ', regex=True)
            
            # 빈 주소 처리
            df['주소'] = df['주소'].replace(['', 'nan', 'None'], np.nan)
        
        return df
    
    def _clean_phone(self, df: pd.DataFrame) -> pd.DataFrame:
        """전화번호 정제"""
        if '전화번호' in df.columns:
            # 전화번호에서 숫자와 하이픈만 남기기
            df['전화번호'] = df['전화번호'].astype(str).str.replace(r'[^\d-]', '', regex=True)
            
            # 빈 전화번호 처리
            df['전화번호'] = df['전화번호'].replace(['', 'nan', 'None'], np.nan)
        
        return df
    
    def _clean_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """좌표 정제"""
        # 위도 정제
        if '위도' in df.columns:
            df['위도'] = pd.to_numeric(df['위도'], errors='coerce')
            # 한국 위도 범위 체크 (33~43도)
            df['위도'] = df['위도'].where((df['위도'] >= 33) & (df['위도'] <= 43), np.nan)
        
        # 경도 정제
        if '경도' in df.columns:
            df['경도'] = pd.to_numeric(df['경도'], errors='coerce')
            # 한국 경도 범위 체크 (124~132도)
            df['경도'] = df['경도'].where((df['경도'] >= 124) & (df['경도'] <= 132), np.nan)
        
        return df
    
    def _remove_duplicates(self, df: pd.DataFrame) -> pd.DataFrame:
        """중복 제거"""
        # 업체명과 주소 기준으로 중복 제거
        if '업체명' in df.columns and '주소' in df.columns:
            df = df.drop_duplicates(subset=['업체명', '주소'], keep='first')
        
        return df
    
    def add_region_info(self, df: pd.DataFrame) -> pd.DataFrame:
        """지역 정보 추가"""
        if '주소' in df.columns:
            # 주소에서 시/도 추출
            df['시도'] = df['주소'].str.extract(r'([가-힣]+(?:시|도))')
            df['구군'] = df['주소'].str.extract(r'([가-힣]+(?:구|군|시))')
        
        return df

def clean_auto_repair_data(df: pd.DataFrame) -> pd.DataFrame:
    """자동차 정비소 데이터 정제 함수"""
    cleaner = ServiceCenterCleaner()
    
    # 데이터 정제
    df_cleaned = cleaner.clean_data(df)
    
    # 지역 정보 추가
    df_cleaned = cleaner.add_region_info(df_cleaned)
    
    return df_cleaned
