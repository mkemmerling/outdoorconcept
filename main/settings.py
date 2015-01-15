"""Django settings for oc project."""
import os
import socket

from django.utils.translation import ugettext_lazy as _

# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ON_PAAS = 'OPENSHIFT_REPO_DIR' in os.environ


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+*^#b1@rvl_t!3xrb2tz!vuaho9t+ieou)fmm1*i3!9$=nc6#g'

if ON_PAAS:
    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']
else:
    SECRET_KEY = '+*^#b1@rvl_t!3xrb2tz!vuaho9t+ieou)fmm1*i3!9$=nc6#g'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

if ON_PAAS:
    ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS'], socket.gethostname()]
else:
    ALLOWED_HOSTS = []


# ----- App configuration ----- #
INSTALLED_APPS = (
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    # Required by Django Admin
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'ordered_model',
    'compressor',
    'main',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # Required by Django Admin
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'main.urls'

WSGI_APPLICATION = 'wsgi.application'

# Angular's $resource provider removes trailing slashes
APPEND_SLASH = False


# ----- REST framework ----- #
REST_FRAMEWORK = {
    'DATE_FORMAT': None,
    'DATETIME_FORMAT': None,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        # 'rest_framework.parsers.FormParser',
        # 'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
}


# ----- Database configuration ----- #
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# ----- Internationalization ----- #
LANGUAGE_CODE = 'de'

LANGUAGES = (
    ('en', _('English')),
    ('de', _('German')),
)

# LOCALE_PATHS = (
#     os.path.join(PROJECT_DIR, 'ropeelements', 'locale'),
# )

MODELTRANSLATION_AUTO_POPULATE = True

TIME_ZONE = 'Europe/Vienna'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# ----- END Internationalization ----- #


# ----- Static files ----- #
# Absolute path to the directory static files will be collected to
STATIC_ROOT = os.path.join(BASE_DIR, 'wsgi', 'static')

# URL prefix for static files
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'bower_components'),
)

# List classes that know how to find static files in various locations
STATICFILES_FINDERS = (
    'main.staticfiles.FileSystemFinder',
    'main.staticfiles.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# (Recursive) glob patterns for files to be collected into STATIC_ROOT
# by the ``collectstatic`` command.
# Since js and css files are precompressed they need not be included.
COLLECT_STATIC_FILES = [
    'bootstrap/fonts/?*.*',
]

COLLECT_STATIC_APP_FILES = [
    'main/images/?*.*',
    'ropeelements/images/?*.*',
    'modeltranslation/**/?*.*',
    'ordered_model/?*.*',
    'admin/**/?*.*',
]
# ----- END Static files ----- #
