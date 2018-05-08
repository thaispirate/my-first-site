"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f*ab=)yx@!ck_7_18k@5r4u4ywe%=_pm7j*!o(98iw$oa3)wrb'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['thaispirate.pythonanywhere.com', '127.0.0.1']


# Application definition
CRISPY_TEMPLATE_PACK = 'bootstrap3'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'formtools',
    'password_reset',
    'jquery',
    'highcharts',
    'smart_selects',
    'projetofinal',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'projetofinal/templates')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL= '/login'

#Password-reset send email configuration


# Para servidor local - Início
# EMAIL_USE_TLS = False
# EMAIL_HOST = 'localhost'
# EMAIL_PORT = 1025
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# DEFAULT_FROM_EMAIL = 'webmaster@localhost.com'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#
# EMAIL_USE_TLS = False
# EMAIL_HOST = 'mail.familiacomvida.com.br'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'meetyourself@familiacomvida.com.br'
# EMAIL_HOST_PASSWORD = 'Mtys2017!'
# DEFAULT_FROM_EMAIL = 'meetyourself@familiacomvida.com.br'
# SERVER_EMAIL = 'mail.familiacomvida.com.br'
# Para servidor local - Fim

# Quando subir pro pythonanywhere tem que estar descomentado - Início
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'meetyourself.familiacomvida@gmail.com'
EMAIL_HOST_PASSWORD = 'Mtys2017!'
DEFAULT_FROM_EMAIL = 'meetyourself.familiacomvida@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SESSION_EXPIRE_AT_BROWSER_CLOSE=True
SMART_SELECTS_JQUERY_URL = True
# Quando subir pro pythonanywhere tem que estar descomentado - Fim
