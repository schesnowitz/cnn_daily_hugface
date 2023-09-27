import json
import os
from dotenv import load_dotenv
load_dotenv()

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8le@&x=cyme!af7e+$m_ch9a(2_hsm05)fjjn1xo5#w4@ndv=9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_seed',
    'raw_data',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dj_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dj_project.wsgi.application'




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

FIXTURE_DIRS = [
    'fixtures',
]

 
ASTRA_ARTIFACT_PATH = BASE_DIR / 'vector_db_connect'
ASTRA_DB_SECURE_BUNDLE_PATH = ASTRA_ARTIFACT_PATH / os.environ.get('ASTRA_DB_SECURE_BUNDLE')
ASTRA_DB_TOKEN_JSON_PATH = ASTRA_ARTIFACT_PATH / os.environ.get('ASTRA_DB_TOKEN_JSON')
ASTRA_DB_KEYSPACE = 'vector_db_keyspace'
ASTRA_DB_TABLE_NAME = 'vector_db'


CLOUD_CONFIG = {
  "secure_connect_bundle": ASTRA_DB_SECURE_BUNDLE_PATH
}

with open(ASTRA_DB_TOKEN_JSON_PATH) as f:
    secrets = json.load(f)

ASTRA_DB_APPLICATION_TOKEN = secrets["token"]

INSTALLED_APPS = ['django_cassandra_engine'] + INSTALLED_APPS
# Database
DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'astra': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': ASTRA_DB_KEYSPACE,
        'USER': 'token',
        'PASSWORD': ASTRA_DB_APPLICATION_TOKEN,
        'OPTIONS': {
            'connection': {
                'cloud': {
                    'secure_connect_bundle': ASTRA_DB_SECURE_BUNDLE_PATH
             }
         }
     }
    }
}
"""
from django.db import connections
conn = connections['astra']
 or check for default 
conn = connections['default']
conn
c = conn.cursor()
c

result = c.execute("SELECT body_blob text_qa_vectors LIMIT 1")
data = result.all()
data
"""
