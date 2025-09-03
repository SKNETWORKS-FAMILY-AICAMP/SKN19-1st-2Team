"""
MySQL 데이터베이스 연결 및 관리 모듈
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path
import toml

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    """MySQL 데이터베이스 관리 클래스"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.connection = None
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """설정 파일 로드"""
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent / "config" / "settings.toml"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return toml.load(f)
        else:
            # 기본 설정 반환
            return {
                'database': {
                    'host': 'localhost',
                    'port': 3306,
                    'name': 'dochicha_db',
                    'user': 'root',
                    'password': '',
                    'charset': 'utf8mb4'
                }
            }
    
    def connect(self) -> bool:
        """데이터베이스 연결"""
        try:
            self.connection = mysql.connector.connect(
                host=self.config['database']['host'],
                port=self.config['database']['port'],
                database=self.config['database']['name'],
                user=self.config['database']['user'],
                password=self.config['database']['password'],
                charset=self.config['database']['charset']
            )
            
            if self.connection.is_connected():
                logger.info("MySQL 데이터베이스에 성공적으로 연결되었습니다.")
                return True
                
        except Error as e:
            logger.error(f"데이터베이스 연결 실패: {e}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 해제"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("MySQL 데이터베이스 연결이 해제되었습니다.")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[pd.DataFrame]:
        """쿼리 실행 및 결과 반환"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # SELECT 쿼리인 경우 결과를 DataFrame으로 반환
            if query.strip().upper().startswith('SELECT'):
                columns = [desc[0] for desc in cursor.description]
                data = cursor.fetchall()
                return pd.DataFrame(data, columns=columns)
            else:
                # INSERT, UPDATE, DELETE 쿼리인 경우 커밋
                self.connection.commit()
                return pd.DataFrame()
                
        except Error as e:
            logger.error(f"쿼리 실행 실패: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def create_tables(self):
        """필요한 테이블들 생성"""
        tables = {
            'service_centers': """
                CREATE TABLE IF NOT EXISTS service_centers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    address TEXT,
                    phone VARCHAR(50),
                    latitude DECIMAL(10, 8),
                    longitude DECIMAL(11, 8),
                    service_type VARCHAR(100),
                    certification_status VARCHAR(50),
                    rating DECIMAL(3, 2),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            'car_models': """
                CREATE TABLE IF NOT EXISTS car_models (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    brand VARCHAR(100) NOT NULL,
                    model VARCHAR(100) NOT NULL,
                    year INT,
                    price DECIMAL(10, 2),
                    fuel_type VARCHAR(50),
                    car_type VARCHAR(50),
                    engine_size DECIMAL(3, 1),
                    fuel_efficiency DECIMAL(4, 1),
                    safety_rating INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            'car_registrations': """
                CREATE TABLE IF NOT EXISTS car_registrations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    region VARCHAR(100),
                    year INT,
                    month INT,
                    total_count INT,
                    gasoline_count INT,
                    diesel_count INT,
                    hybrid_count INT,
                    electric_count INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """,
            'user_preferences': """
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    car_model_id INT,
                    user_ip VARCHAR(45),
                    preference_type ENUM('like', 'dislike', 'view') DEFAULT 'view',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (car_model_id) REFERENCES car_models(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
        }
        
        for table_name, create_sql in tables.items():
            try:
                self.execute_query(create_sql)
                logger.info(f"테이블 '{table_name}' 생성 완료")
            except Error as e:
                logger.error(f"테이블 '{table_name}' 생성 실패: {e}")
    
    def insert_dataframe(self, df: pd.DataFrame, table_name: str) -> bool:
        """DataFrame을 테이블에 삽입"""
        try:
            if df.empty:
                logger.warning("삽입할 데이터가 없습니다.")
                return False
            
            # DataFrame을 SQL INSERT 쿼리로 변환
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            # 데이터를 튜플 리스트로 변환
            data = [tuple(row) for row in df.values]
            
            cursor = self.connection.cursor()
            cursor.executemany(query, data)
            self.connection.commit()
            
            logger.info(f"{len(data)}개 행이 '{table_name}' 테이블에 삽입되었습니다.")
            return True
            
        except Error as e:
            logger.error(f"데이터 삽입 실패: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

# 싱글톤 인스턴스
db_manager = DatabaseManager()

def get_database_manager() -> DatabaseManager:
    """데이터베이스 매니저 인스턴스 반환"""
    return db_manager
