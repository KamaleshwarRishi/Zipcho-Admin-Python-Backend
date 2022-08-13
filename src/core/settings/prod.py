from .base import *

DEBUG = True

ALLOWED_HOSTS =['http://zipchodev.com/', 'zipchodev.com'  ,'65.0.89.205','0.0.0.0','http://65.0.89.205/']
CSRF_TRUSTED_ORIGINS= ['http://zipchodev.com/','zipchodev.com','http://65.0.89.205/','65.0.89.205']
CORS_ORIGIN_ALLOW_ALL=True

CORS_ORIGIN_WHITELIST=[
    'http://127.0.0.1:9090',
    'http://127.0.0.1:8000',
    'http://65.0.89.205',
    'http://zipchodev.com'
]


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'zipchoAdminDB',
        'OPTIONS' : {
            'read_default_file': '/etc/mysql/my.cnf',
        },
    }
}


INTERNAL_IPS = [
    '127.0.0.1',
]