"""
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
"""

from pathlib import Path
import os
#from dotenv import load_dotenv
#import django_heroku #for heroku--------------
import dj_database_url#for heroku------and---railway-----
#from decouple import config#for heroku--------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

#load our environmental variables
#load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-mzuo-tt457h9occf(rk@cn+k4wi9-v&s+2fuk21naxpm(l^x0z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['https://ctndrd.com','ctndrd.com','web-production-5e1e7.up.railway.app','https://web-production-5e1e7.up.railway.app']
CSRF_TRUSTED_ORIGINS = ['https://ctndrd.com','https://web-production-5e1e7.up.railway.app']

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
    'cloudinary_storage',#cloudinary_cloud_storage
    'cloudinary',#cloudinary_cloud_storage
    'whitenoise.runserver_nostatic',
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'railway',
#        'USER': 'postgres',
#        'PASSWORD': os.environ.get('DB_PASSWORD'),
#        'HOST': 'postgres.railway.internal',
#        'PORT': '5432',
#    }
#}

DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))#os.getenv('DATABASE_URL'))#
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

#whitenoise storage stuff-----
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = BASE_DIR / 'staticfiles'
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = '/media/' #we are using cloudinary instead

#Cloudinary_cloud_storage_media _root:
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

#cloudinary_cloud_storage_configuration:
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUD_NAME'),#os.getenv('CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUD_API_KEY'),#os.getenv('CLOUD_API_KEY'),
    'API_SECRET': os.environ.get('CLOUD_API_SECRET'),#os.getenv('CLOUD_API_SECRET')
    'SECURE': True,
    'MEDIA_TAG': 'media',
    'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
}

#django_heroku.settings(locals())#for heroku--------------
#-------------------------------------------------------------------------
#---------------------code by Dr.James Atwiine----------------------------
#-------------------------------------------------------------------------