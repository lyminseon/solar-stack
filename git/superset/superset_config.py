import os
from cachelib.file import FileSystemCache

# ── 기본 보안 키 ─────────────────────────────
SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "change-me-please")

# ── 데이터베이스 연결 ────────────────────────
SQLALCHEMY_DATABASE_URI = os.getenv(
    "SUPERSET_DATABASE_URI",
    "postgresql+psycopg2://hudius:hudius2020!@postgres:5432/solar_db"
)

# Results backend (optional, 캐싱용)
RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

# ── 보안 옵션 ────────────────────────────────
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

# ── CSRF ─────────────────────────────────────
WTF_CSRF_ENABLED = True
WTF_CSRF_EXEMPT_LIST = []
WTF_CSRF_TIME_LIMIT = 60 * 60

# ── Flask AppBuilder 인증 ───────────────────
from flask_appbuilder.security.manager import AUTH_OAUTH

AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True              # 최초 로그인 시 사용자 자동 생성
AUTH_USER_REGISTRATION_ROLE = "Public"     # 기본 역할 (admin 수동 할당 필요)

OAUTH_PROVIDERS = [
    {
        "name": "keycloak",
        "icon": "fa-key",
        "token_key": "access_token",
        "remote_app": {
            "client_id": os.getenv("OIDC_RP_CLIENT_ID", "superset"),
            "client_secret": os.getenv("OIDC_RP_CLIENT_SECRET", "superset-secret-key-2024"),
            "api_base_url": "https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect",
            "authorize_url": "https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/auth",
            "access_token_url": "https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/token",
            "userinfo_endpoint": "https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/userinfo",
            "client_kwargs": {
                "scope": "openid email profile"
            },
        },
    }
]

# ── Role 매핑 함수 (Keycloak → Superset) ─────
def AUTH_REMOTE_USER_INFO(userinfo):
    """
    Keycloak userinfo → Superset user object 매핑
    """
    return {
        "username": userinfo.get("preferred_username"),
        "first_name": userinfo.get("given_name"),
        "last_name": userinfo.get("family_name"),
        "email": userinfo.get("email"),
    }

# ── 로깅/디버그 ─────────────────────────────
LOG_LEVEL = "INFO"
