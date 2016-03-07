"""
Django settings for the Calendar Journal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


ENVIRONMENT = os.getenv('APP_ENVIRONMENT', 'dev')
if ENVIRONMENT == 'prod':
    PRODUCTION= True  # Defined for convenience
else:
    PRODUCTION = False  # Defined for convenience

# Configured prod/non-prod settings

if PRODUCTION:
    BASE_URL = 'panalytics.elasticbeanstalk.com'
    DEBUG = False
    TEMPLATE_DEBUG = False
else:
    BASE_URL = os.getenv('BASE_URL', 'http://localhost:8000')
    DEBUG = True
    TEMPLATE_DEBUG = True

# Environment variables
SECRET_KEY = os.environ.get('CJ_DJANGO_SECRET_KEY', "fake_key")
if ENVIRONMENT == 'prod':
    assert SECRET_KEY != "fake_key", "SECRET_KEY environment variable must be set"

GOOGLE_CALENDAR_API_CLIENT_ID = os.getenv('CJ_GOOGLE_CALENDAR_API_CLIENT_ID', None)
GOOGLE_CALENDAR_API_CLIENT_SECRET = os.getenv('CJ_GOOGLE_CALENDAR_API_CLIENT_SECRET', None)
assert GOOGLE_CALENDAR_API_CLIENT_ID, "GOOGLE_CALENDAR_API_CLIENT_ID environment variable must be set"
assert GOOGLE_CALENDAR_API_CLIENT_SECRET, "GOOGLE_CALENDAR_API_CLIENT_SECRET environment variable must be set"

ALLOWED_HOSTS = ['panalytics.elasticbeanstalk.com', 'localhost', '127.0.0.1', 'ngrok.io']

AUTHENTICATION_BACKENDS = (
    'cal.auth_backend.PasswordlessAuthBackend',
    'django.contrib.auth.backends.ModelBackend',

    # Python social auth
    'social.backends.google.GoogleOAuth2',
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # CalendarJournal App(s)
    'cal',
    'api',

    # Vendor App(s)
    'rest_framework',
    'social.apps.django_app.default',
)

# TODO make an actual login page for redirection
LOGIN_URL = "/"

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middleware
    'cal.middleware.UserBasedExceptionMiddleware',
)
# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    'PAGE_SIZE': 10,
}


ROOT_URLCONF = 'cal.urls'

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.template.context_processors.debug',
    'django.template.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

    # Custom processors
    'cal.context_processors.google_client_id_processor',

    # Vendor processors
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',  # TODO ensure this is used
    
]

WSGI_APPLICATION = 'cal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    # These environment variables are automagically set in prod
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

if ENVIRONMENT == 'prod':
    STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
    STATIC_URL = '/static/'
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
    STATIC_URL = '/static/'
