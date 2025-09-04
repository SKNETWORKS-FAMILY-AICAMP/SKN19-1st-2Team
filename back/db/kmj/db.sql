
# 1. dochicar 테이블 생성
create database dochicar;
# 2. 권한 부여
grant all privileges on dochicar.* to ohgiraffers@'%';

# 3. 테이블 스키마 정의
use dochicar;
CREATE TABLE IF NOT EXISTS vehicle_reg (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  gender      VARCHAR(10)  NOT NULL COMMENT '남성/여성',
  age_group   VARCHAR(20)  NOT NULL COMMENT '10대이하/20대/30대',
  region      VARCHAR(20)  NOT NULL COMMENT '시도명',
  reg_year    VARCHAR(10)  NOT NULL COMMENT '집계 기준월(년 첫날 저장)',
  reg_month   VARCHAR(10)  NOT NULL COMMENT '집계 기준월(월 첫날 저장)',
  reg_count   INT          NOT NULL COMMENT '계',
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_vehicle_reg (reg_month, region, gender, age_group),
  KEY idx_vehicle_reg_region_month (region, reg_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;