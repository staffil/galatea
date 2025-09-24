

from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_NAME = os.getenv("DB_NAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
IAMPORT_API_KEY = os.getenv("IAMPORT_API_KEY")
IAMPORT_API_SECRET = os.getenv("IAMPORT_API_SECRET")
print("GOOGLE_CLIENT_ID", GOOGLE_CLIENT_ID)
print("GOOGLE_CLIENT_SECRET", GOOGLE_CLIENT_SECRET)
PORTONE_STORE_ID=os.getenv("PORTONE_STORE_ID")

# 보안 설정
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = True

ALLOWED_HOSTS = [
    '54.173.112.53',
    'ec2-54-173-112-53.compute-1.amazonaws.com',    
    'galatea.website',
    'www.galatea.website',
    '127.0.0.1',
    'localhost',
]

# 언어 / 로케일
LANGUAGE_CODE = 'ko'
LANGUAGES = [
    ('ko', '한국어'),
    ('en', 'English'),
    ('ja', '日本語'),
    ('zh', '中文'),
    # ('fr', 'Français'),
    ('es', 'Español'),
    ('pt', 'Português'),    
    ('ru', 'Русский'),      
    ('de', 'Deutsch'), 
    ('ar', 'العربية'),
    ('hi', 'हिन्दी'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
LANGUAGE_COOKIE_NAME = 'django_language'
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# 사이트 설정 (allauth 필요)
SITE_ID = 2

# 애플리케이션
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.admin",
    "django.contrib.sites",
        'django.contrib.sitemaps',
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",

    # allauth
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",

    # 커스텀 앱
    "customer_ai",
    "celebrity",
    "makeImage",
    "payment",
    "home",
    "cloning",
    "makeVoice",
    "register",
    "mypage",
    "user_auth",
    "modeltranslation",
    "distribute",
    "helpdesk",
    "invest",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "galatea.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
                        "builtins": ["django.templatetags.i18n"], 
        },
    },
]

WSGI_APPLICATION = "galatea.wsgi.application"

# DB
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": "172.31.37.216",   # 인스턴스 바꾸면 수정 필요
        "PORT": "3306",
        "CONN_MAX_AGE": 600,
    }
}

# 사용자 모델
AUTH_USER_MODEL = "home.Users"

# 인증 관련
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
LOGIN_URL = "/register/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# allauth 설정
SOCIALACCOUNT_ADAPTER = 'register.adapter.MySocialAccountAdapter'
SOCIALACCOUNT_SIGNUP_FORM_CLASS = None

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'  # 이메일 인증 스킵
SOCIALACCOUNT_LOGIN_ON_GET = True 

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    },
    "github": {
        'APP': {
            'client_id': os.getenv("SOCIAL_AUTH_GITHUB_KEY"),
            'secret': os.getenv("SOCIAL_AUTH_GITHUB_SECRET"),
            'key': ''
        }
        
    },
}
# 세션 / 캐시
SESSION_COOKIE_AGE = 3600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# 브라우저 닫아도 세션 유지 (선택사항)
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# 세션 보안 강화
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# 이메일 (개발용: 콘솔 출력)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# 정적/미디어 파일
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# 기본 키
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 로깅
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "/home/ubuntu/galatea/logs/django.log",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
SOCIALACCOUNT_AUTO_SIGNUP = True



