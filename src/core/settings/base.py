import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv
from dotenv.main import find_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(override=True)
load_dotenv(find_dotenv())

SECRET_KEY = 't2@aserx(4iqmb-@z1&br%8s0%iklkk9f46o9h+ti#r)*nl5(t'



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'drf_spectacular',
    'django_filters',
    'drf_yasg',
    'authentication',
    'zipchoAdmin',
    'core'

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

ROOT_URLCONF = 'core.urls'
AUTH_USER_MODEL = 'authentication.User'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR,'templates')], #[],
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

WSGI_APPLICATION = 'core.wsgi.application'



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_root')]
VENV_PATH = os.path.dirname(BASE_DIR)
STATIC_ROOT = os.path.join(VENV_PATH, 'static_root')
MEDIAL_URL ='/media/'
MEDIA_ROOT = os.path.join(VENV_PATH, 'media')



# Configure the JWT settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=172800),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=35),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS' : {
        'Bearer' : {
            'type' : 'apiKey',
            'name' : 'Authorization',
            'in'   : 'header'
        }
    }
}


# REST framework settings
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER' : 'core.utils.custom_exception_handler',
    'DEFAULT_SCHEMA_CLASS' : 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny'

    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
}

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME='ap-south-1'
AWS_STORAGE_BUCKET_NAME='zipchodev'
AWS_S3_ADDRESSING_STYPE='path'

AWS_QUERYSTRING_AUTH=False
AWS_DEFAULT_ACL=None


SPECTACULAR_SETTINGS = {
    'TITLE' : 'ZIPCHO ADMIN PORTAL APIS',
    'DESCRIPTION': 'Zipcho Chat',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# Email Setup
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
SUPPORT_EMAIL_USER = os.environ.get('SUPPORT_EMAIL_USER')

# Celery 
#CELERY_TIMEZONE = "America/New_York"

# MongoDB Settings 
mongodb_databaseName = os.environ.get('MONGODB_DATABASENAME')
mongo_port = os.environ.get('MONGO_PORT')
username=None
password=None
mongo_host='localhost'
mongo_srv = os.environ.get('MONGO_SRV')
mongo_proddbname = os.environ.get('MONGO_PRODDBNAME')

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": "AAAAWq9CWAs:APA91bGvHVYFaawyEi0e87X2DUnECe_zlZBPgVotJ7FkiU2clGH03Zbfx5ZTv_fWGFkDyuDEKzgGYPoQ2Apjtq182OjsqwwknbXbjdJV9RthRibHP1Oaezq7RZ34zgWHAzvahmKMNzCk",
}