import os
from pathlib import Path
from decouple import config
import datetime
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY", default="django-insecure-super-secret-key-for-dev-change-me")
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS_STR = config("ALLOWED_HOSTS", default="127.0.0.1,localhost")
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_STR.split(',') if host.strip()]
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    'rest_framework',
    'decouple',
    'rest_framework.authtoken',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = config("LANGUAGE_CODE", default="uz-Latn")
TIME_ZONE = config("TIME_ZONE", default="Asia/Tashkent")
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

JAZZMIN_SETTINGS = {
    "site_title": config("JAZZMIN_SITE_TITLE", default="Admin Panel"),
    "site_header": config("JAZZMIN_SITE_HEADER", default="Boshqaruv Paneli"),
    "site_brand": config("JAZZMIN_SITE_BRAND", default="Loyiha Nomi"),
    "welcome_sign": config("JAZZMIN_WELCOME_SIGN", default="Xush kelibsiz!"),
    "copyright": config("JAZZMIN_COPYRIGHT", default=f"Loyiha Nomi © {datetime.date.today().year}"),
    "search_model": ["auth.User", "models.UserModel"],
    "topmenu_links": [
        {"name": "Bosh Sahifa", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "core"},
    ],
    "order_with_respect_to": ["auth", "core"],
    "show_sidebar": True,
    "navigation_expanded": True,
    "language_chooser": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "admin.LogEntry": "fas fa-file-alt",
        "core.usermodel": "fas fa-id-card",
        "core.comegonetimemodel": "fas fa-stopwatch",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,
    "show_ui_builder": config("JAZZMIN_SHOW_UI_BUILDER", default=DEBUG, cast=bool),
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_flat_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_accordion": True,
    "actions_sticky_top": True
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'core.throttling.UserFieldRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': config("THROTTLE_RATE_ANON", default='100/day'),
        'user': config("THROTTLE_RATE_USER", default='1000/day'),
        'user_field_post': config("THROTTLE_RATE_USER_FIELD_POST", default='60/minute'),
    }
}

CSRF_TRUSTED_ORIGINS_STR = config("CSRF_TRUSTED_ORIGINS", default="http://localhost:8000,http://127.0.0.1:8000")
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in CSRF_TRUSTED_ORIGINS_STR.split(',') if origin.strip()]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}