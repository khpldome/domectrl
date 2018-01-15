"""
Django settings for domectrl project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""


import os.path



import os
import domectrl.config_fds as conf


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('BASE_DIR=', BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e=%ca7=6mhc^z@&l1=p+mv$k!-@y8mi#h%d17d@vie@(hv*93_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', conf.ALLOWED_IP, '3191925d.ngrok.io']
# ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dome.apps.DomeConfig',
    # 'mod_wsgi.server',    # for daemon mode

    # 'djrill',
    # 'mailchimp',
    # 'dome',
    'domeuser',
    'domeplaylist',
    # 'grappelli',
    # 'filebrowser',

    # 'easy_thumbnails',
    # 'filer',
    # 'mptt',

    'filemanager',
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

ROOT_URLCONF = 'domectrl.urls'


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
print('STATIC_ROOT=', STATIC_ROOT)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]
STATIC_URL = '/static/'


MEDIA_ROOT = os.path.join('C:\\', '')
print('MEDIA_ROOT=', MEDIA_ROOT)

MEDIA_URL = '/media/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'domectrl.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


AUTH_USER_MODEL = 'domeuser.User'
LOGIN_URL = '/account/sign-in/'



# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True




# //////////////////////////////////////////////////////////////////////////////
# ///////////////////////// local_settings /////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////

# STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


DATETIME_FORMAT = 'Y-m-d H:i'
DATETIME_INPUT_FORMATS ='%Y-%m-%d %H:%M:%S'     # '2006-10-25 14:30:59'

try:
    from .local_settings import *
except ImportError:
    pass

