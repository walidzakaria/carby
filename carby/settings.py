"""
Django settings for carby project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import configparser
from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = os.path.join(Path(BASE_DIR).parent.absolute(), 'frontend')


config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.ini'))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('App', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean('App', 'DEBUG')
LOCAL = config.getboolean('App', 'LOCAL')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '64.226.64.150',
    'avriostores.xyz',
    'www.avriostores.xyz',
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8000',
    'http://localhost:9000',
    'http://localhost:8080',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:9000',
    'http://127.0.0.1:8080',
    'http://64.226.64.150:8000',
    'http://64.226.64.150',
    'http://avriostores.xyz',
    'http://www.avriostores.xyz',
    'https://avriostores.xyz',
    'https://www.avriostores.xyz',
)

CSRF_TRUSTED_ORIGINS = [
    'http://64.226.64.150',
    'http://localhost',
    'http://127.0.0.1',
    'http://avriostores.xyz',
    'http://www.avriostores.xyz',
    'https://avriostores.xyz',
    'https://www.avriostores.xyz',
]

BASE_URL = 'https://avriostores.xyz'
SECURE_CROSS_ORIGIN_OPENER_POLICY = None
# CSRF_COOKIE_SECURE = False  # Set to True if using HTTPS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'drf_yasg',
    'explorer',
    
    'users',
    'definitions',
    'operation',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'carby.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(FRONTEND_DIR, 'dist'),
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {  # Adding this section should work around the issue.
                'staticfiles': 'django.templatetags.static',
            },
        },
    },
]

WSGI_APPLICATION = 'carby.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
if LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config.get('Database', 'DB_NAME'),
            'USER': config.get('Database', 'DB_USER'),
            'PASSWORD': config.get('Database', 'DB_PASSWORD'),
            'HOST': 'localhost',
            'PORT': '',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATIC_URL = '/assets/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Vue assets directory (assetsDir)
STATICFILES_DIRS = [
    os.path.join(FRONTEND_DIR, 'dist/assets'),
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:9000",
    "http://127.0.0.1:9000",
    'http://64.226.64.150',
    'http://64.226.64.150:8000',
    'http://avriostores.xyz',
    'http://www.avriostores.xyz',
    'https://avriostores.xyz',
    'https://www.avriostores.xyz',
]

CORS_ALLOW_ALL_ORIGINS = True

DJOSER = {
    # 'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    # 'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    # 'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    # 'PASSWORD_RESET_CONFIRM_URL': 'auth/password/reset/confirm/{uid}/{token}',
    # 'USERNAME_RESET_CONFIRM_URL': 'auth/username/reset/confirm/{uid}/{token}',
    # 'ACTIVATION_URL': 'auth/activate/{uid}/{token}',
    # 'SEND_ACTIVATION_EMAIL': True,
    # 'SEND_CONFIRMATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    # 'PASSWORD_RESET_CONFIRM_RETYPE': True,
    # 'SERIALIZERS': {
    #     'user_create': 'authapp.serializers.UserCreateSerializer',
    #     'user': 'authapp.serializers.UserCreateSerializer',
    # }
}

EXPLORER_CONNECTIONS = { 'Default': 'default' }
EXPLORER_DEFAULT_CONNECTION = 'default'
EXPLORER_PERMISSION_VIEW = lambda r: r.user.is_staff
EXPLORER_PERMISSION_CHANGE = lambda r: r.user.is_staff
EXPLORER_SQL_BLACKLIST = (
     # DML
    #  'COMMIT', 'MERGE', 'REPLACE', 'ROLLBACK', 'START', 'UPSERT', # 'DELETE', 'SET', 'UPDATE', 'INSERT',
    #  # DDL
    #  'ALTER', 'CREATE', 'DROP', 'RENAME', 'TRUNCATE',
    #  # DCL
    #  'GRANT', 'REVOKE',
 )