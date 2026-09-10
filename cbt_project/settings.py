import dj_database_url
"""
Django settings for cbt_project project.
"""

from pathlib import Path

# ==========================
# Base Directory
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================
# Security
# ==========================

SECRET_KEY = 'django-insecure-%$yl7vel1elk-s4d8+!4-p46#6yrn8rlf0)v+v-$w1)q3u@z+0'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Session & Security Limits
SESSION_COOKIE_AGE = 7200  # 2 jam
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# ==========================
# INSTALLED APPS
# ==========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project Apps
    'home',

    'akun',
    'bank_soal',
    'ujian',
    'importer',
]


# ==========================
# MIDDLEWARE
# ==========================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cbt_project.middleware.NetworkGatewayMiddleware',
]


# ==========================
# URL
# ==========================

ROOT_URLCONF = 'cbt_project.urls'


# ==========================
# Templates
# ==========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ==========================
# WSGI
# ==========================

WSGI_APPLICATION = 'cbt_project.wsgi.application'


# ==========================
# Database
# ==========================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==========================
# Password Validation
# ==========================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]


# ==========================
# Internationalization
# ==========================

LANGUAGE_CODE = 'id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True


# ==========================
# Static Files
# ==========================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==========================
# Default Auto Field
# ==========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================
# Login
# ==========================

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"

# Development email backend: print emails to console (password reset)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Mengizinkan POST dari tunnel (localtunnel) agar tidak error 403 CSRF
CSRF_TRUSTED_ORIGINS = ['https://*.loca.lt']

# Wajib untuk iPhone/Safari karena mendeteksi HTTPS dari Proxy (Tunneling)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
STATIC_ROOT = BASE_DIR / 'staticfiles'

import os
import dj_database_url
if os.environ.get('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
