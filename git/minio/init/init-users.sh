#!/bin/bash

# MinIO 사용자 초기화 스크립트
# 기본 계정을 hudius/hudius2020!로 변경

echo "MinIO 사용자 초기화 시작..."

# MinIO 서버가 준비될 때까지 대기
until mc alias list | grep -q "myminio"; do
    echo "MinIO 서버 연결 대기 중..."
    sleep 5
done

echo "MinIO 서버 연결 성공"

# 기존 minioadmin 사용자 비밀번호 변경
echo "hudius 사용자 비밀번호 변경 중..."
mc admin user add myminio hudius hudius2020!

# Admin 권한 부여
echo "Admin 권한 부여 중..."
mc admin policy set myminio readwrite hudius

# 사용자 목록 확인
echo "생성된 사용자 목록:"
mc admin user list myminio

echo "MinIO 사용자 초기화 완료!"
echo "로그인 정보:"
echo "  사용자명: hudius"
echo "  비밀번호: hudius2020!"
