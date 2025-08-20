#!/bin/bash

# Grafana 사용자 초기화 스크립트
# 기본 계정을 hudius/hudius2020!로 변경

echo "Grafana 사용자 초기화 시작..."

# Grafana 서버가 준비될 때까지 대기
until curl -s http://localhost:3000/api/health | grep -q "ok"; do
    echo "Grafana 서버 연결 대기 중..."
    sleep 5
done

echo "Grafana 서버 연결 성공"

# 기본 admin 사용자 비밀번호 변경
echo "admin 사용자 비밀번호 변경 중..."
curl -X PUT -H "Content-Type: application/json" \
  -d '{"oldPassword":"admin","newPassword":"hudius2020!"}' \
  http://admin:admin@localhost:3000/api/user/password

# 새로운 hudius 사용자 생성
echo "hudius 사용자 생성 중..."
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"hudius","email":"hudius@greenfesco.com","login":"hudius","password":"hudius2020!"}' \
  http://admin:hudius2020!@localhost:3000/api/admin/users

# Admin 권한 부여
echo "Admin 권한 부여 중..."
curl -X PUT -H "Content-Type: application/json" \
  -d '{"role":"Admin"}' \
  http://admin:hudius2020!@localhost:3000/api/admin/users/2/permissions

echo "Grafana 사용자 초기화 완료!"
echo "로그인 정보:"
echo "  사용자명: hudius"
echo "  비밀번호: hudius2020!"
