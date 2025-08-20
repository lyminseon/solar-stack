#!/bin/bash

# Airflow 사용자 초기화 스크립트 (Airflow 3.0.3용)
# 기본 계정을 hudius/hudius2020!로 변경

echo "Airflow 사용자 초기화 시작..."

# Airflow 데이터베이스가 준비될 때까지 대기
until airflow db check; do
    echo "데이터베이스 연결 대기 중..."
    sleep 5
done

echo "데이터베이스 연결 성공"

# Airflow 3.0.3에서는 users 명령어가 db 그룹으로 이동
echo "기존 airflow 사용자 삭제 중..."
airflow db delete-user airflow 2>/dev/null || echo "기존 사용자가 없습니다"

# 새로운 hudius 사용자 생성
echo "hudius 사용자 생성 중..."
airflow db create-user \
    --username hudius \
    --firstname Hudius \
    --lastname Admin \
    --role Admin \
    --email hudius@greenfesco.com \
    --password hudius2020!

# 사용자 목록 확인
echo "생성된 사용자 목록:"
airflow db list-users

echo "Airflow 사용자 초기화 완료!"
echo "로그인 정보:"
echo "  사용자명: hudius"
echo "  비밀번호: hudius2020!"
