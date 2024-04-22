from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('db_engine'),
        'NAME': config('db_name'),
        'USER': config('db_user'),
        'PASSWORD': config('db_password'),
        'HOST': config('db_host'),
        'PORT': config('db_port'),
    }
}
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
