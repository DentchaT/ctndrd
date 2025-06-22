"""
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
"""

from pathlib import Path
import os
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mzuo-tt457h9occf(rk@cn+k4wi9-v&s+2fuk21naxpm(l^x0z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
INSTALLED_APPS = [
    'appl',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
ROOT_URLCONF = 'registration.urls'
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
WSGI_APPLICATION = 'registration.wsgi.application'
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

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
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------