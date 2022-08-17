from .base import *

DEBUG = True


ALLOWED_HOSTS =['3.110.117.161','0.0.0.0','http://3.110.117.161/']
CSRF_TRUSTED_ORIGINS= ['http://3.110.117.161/','3.110.117.161']
CORS_ORIGIN_ALLOW_ALL=True

CORS_ORIGIN_WHITELIST=[
    'http://127.0.0.1:9090',
    'http://127.0.0.1:8000',
    'http://3.110.117.161',
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