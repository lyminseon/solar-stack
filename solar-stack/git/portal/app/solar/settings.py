import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ── 비밀/모드 ──────────────────────────────────────────────
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "change-me-dev-only")
DEBUG = os.getenv("DJANGO_DEBUG", "false").lower() == "true"

def _split_env_list(name: str, default: str = ""):
    raw = os.getenv(name, default)
    return [x.strip() for x in raw.replace(" ", "").split(",") if x.strip()]

ALLOWED_HOSTS = _split_env_list(
    "ALLOWED_HOSTS",
    "www.greenfesco.com,greenfesco.com"
)

CSRF_TRUSTED_ORIGINS = _split_env_list(
    "CSRF_TRUSTED_ORIGINS",
    "https://www.greenfesco.com,https://greenfesco.com"
)

# ── 앱/미들웨어 ───────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "mozilla_django_oidc",
]

MIDDLEWARE = [
     # ... other middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'mozilla_django_oidc.middleware.OIDCAuthenticationBackend', # Corrected line
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ... other middleware
]

ROOT_URLCONF = "solar.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]

WSGI_APPLICATION = "solar.wsgi.application"

# ── 데이터베이스 (DATABASE_URL 우선) ───────────────────────
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=60)}
else:
    DATABASES = {"default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3"
    }}

# ── 패스워드 정책 ─────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── 국제화/시간대 ─────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Seoul")
USE_I18N = True
USE_TZ = True

# ── 정적파일 ──────────────────────────────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── OIDC(키클록) ──────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    "mozilla_django_oidc.auth.OIDCAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

OIDC_OP_AUTHORIZATION_ENDPOINT = "https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/auth"
OIDC_OP_TOKEN_ENDPOINT = "https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/token"
OIDC_OP_USER_ENDPOINT = "https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/userinfo"
OIDC_OP_JWKS_ENDPOINT = "https://www.greenfesco.com/keycloak/realms/solar/protocol/openid-connect/certs"

OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID", "portal")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET", "portal-secret-key-2024")

OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = "openid profile email"
OIDC_CREATE_USER = True

LOGIN_URL = "oidc_authentication_init"
LOGOUT_URL = "oidc_logout"

# ── 프록시/보안 (운영값) ───────────────────────────────────
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

if DEBUG:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]
    CSRF_TRUSTED_ORIGINS += ["http://localhost", "http://127.0.0.1"]

# Python 3.11 호환성을 위한 추가 설정
import sys
if sys.version_info >= (3, 11):
    # Python 3.11+ 특화 설정
    USE_TZ = True
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "solar_db"),
            "USER": os.getenv("POSTGRES_USER", "hudius"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "hudius2020!"),
            "HOST": os.getenv("POSTGRES_HOST", "postgres"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
            "OPTIONS": {
                "sslmode": "disable",
            },
        }
    }

# OIDC 설정 최적화 (Python 3.11용)
OIDC_OP_DISCOVERY_ENDPOINT = os.getenv(
    "OIDC_OP_DISCOVERY_ENDPOINT",
    "https://www.greenfesco.com/keycloak/realms/solar/.well-known/openid-configuration"
)

OIDC_RP_CLIENT_ID = os.getenv("OIDC_RP_CLIENT_ID", "portal")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_RP_CLIENT_SECRET", "portal-secret-key-2024")
OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = "openid profile email"
OIDC_CREATE_USER = True

# Python 3.11 최적화
if sys.version_info >= (3, 11):
    # 비동기 지원 개선
    ASGI_APPLICATION = "solar.asgi.application"
    
    # 캐시 최적화
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "unique-snowflake",
        }
    }