DJANGO_SETTINGS_MODULE=solar.settings
DJANGO_SECRET_KEY=change-me        # 운영에서 강한 랜덤값으로 교체
DJANGO_DEBUG=false

# 호스트/오리진 (콤마로 구분)
ALLOWED_HOSTS=www.greenfesco.com,greenfesco.com
CSRF_TRUSTED_ORIGINS=https://www.greenfesco.com,https://greenfesco.com

# DB 연결 (compose의 postgres를 사용)
DATABASE_URL=postgresql://hudius:hudius2020!@postgres:5432/solar_db

# OIDC (Keycloak) - Discovery 사용
OIDC_OP_DISCOVERY_ENDPOINT=https://www.greenfesco.com/keycloak/realms/solar/.well-known/openid-configuration
OIDC_RP_CLIENT_ID=portal
OIDC_RP_CLIENT_SECRET=portal-secret-key-2024

# OIDC (Keycloak) - 개별 엔드포인트 수동 추가
OIDC_OP_AUTHORIZATION_ENDPOINT=https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/auth
OIDC_OP_TOKEN_ENDPOINT=https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/token
OIDC_OP_USERINFO_ENDPOINT=https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/userinfo

# 시간대
TIME_ZONE=Asia/Seoul

