-- 안전하게 초기화
DROP USER IF EXISTS 'dochicar'@'localhost';
DROP USER IF EXISTS 'dochicar'@'127.0.0.1';

-- 동일 비밀번호로 두 호스트 모두 생성
CREATE USER 'dochicar'@'localhost' IDENTIFIED BY 'dochicar';
CREATE USER 'dochicar'@'127.0.0.1' IDENTIFIED BY 'dochicar';

-- 스키마 권한 부여
GRANT ALL PRIVILEGES ON dochicar.* TO 'dochicar'@'localhost';
GRANT ALL PRIVILEGES ON dochicar.* TO 'dochicar'@'127.0.0.1';

FLUSH PRIVILEGES;

-- 0) 스키마
CREATE DATABASE IF NOT EXISTS dochicar DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE dochicar;

-- 1) 정비소 테이블
CREATE TABLE IF NOT EXISTS service_center (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  name_ko          VARCHAR(200) NOT NULL COMMENT '자동차정비업체명',
  type_code        INT          NULL     COMMENT '자동차정비업체종류(코드)',
  addr_road        VARCHAR(300) NULL     COMMENT '소재지도로명주소',
  addr_jibun       VARCHAR(300) NULL     COMMENT '소재지지번주소',
  lat              DECIMAL(10,7) NULL    COMMENT '위도',
  lon              DECIMAL(10,7) NULL    COMMENT '경도',
  biz_reg_date     DATE         NULL     COMMENT '사업등록일자',
  area_text        VARCHAR(100) NULL     COMMENT '면적(원문 텍스트 보존)',
  status_code      INT          NULL     COMMENT '영업상태(코드)',
  closed_date      DATE         NULL     COMMENT '폐업일자',
  pause_from       DATE         NULL     COMMENT '휴업시작일자',
  pause_to         DATE         NULL     COMMENT '휴업종료일자',
  open_time        VARCHAR(10)  NULL     COMMENT '운영시작시각(HH:MM 등 원문 보존)',
  close_time       VARCHAR(10)  NULL     COMMENT '운영종료시각',
  phone            VARCHAR(30)  NULL     COMMENT '전화번호',
  mgmt_office_name VARCHAR(100) NULL     COMMENT '관리기관명',
  mgmt_office_tel  VARCHAR(30)  NULL     COMMENT '관리기관전화번호',
  data_ref_date    DATE         NULL     COMMENT '데이터기준일자',
  provider_code    INT          NULL     COMMENT '제공기관코드',
  provider_name    VARCHAR(100) NULL     COMMENT '제공기관명',

  -- 편의 컬럼
  region_code      VARCHAR(20)  NULL     COMMENT '지역코드(추후 맵핑 시)',
  created_at       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  -- 인덱스
  INDEX idx_provider_name (provider_name),
  INDEX idx_status (status_code),
  INDEX idx_geo (lat, lon),
  INDEX idx_name_addr (name_ko, addr_road)
);

SELECT * FROM service_center;

