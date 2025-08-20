#!/bin/bash
# SSL 인증서 발급 또는 갱신 스크립트

# 환경 변수 설정
DOMAIN="www.greenfesco.com"
EMAIL="hudius@hudius.com"

# 인증서 발급 또는 갱신
certbot certonly \
  --webroot \
  --webroot-path=/var/www/certbot \
  --email=$EMAIL \
  --agree-tos \
  --non-interactive \
  --domains=$DOMAIN

# nginx 재시작 (필요시)
# docker-compose restart nginx