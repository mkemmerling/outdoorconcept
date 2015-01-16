"""Django settings for oc project."""
import os
import socket

from django.utils.translation import ugettext_lazy as _

# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ON_OPENSHIFT = 'OPENSHIFT_REPO_DIR' in os.environ


# ----- Base configuration ----- #
if ON_OPENSHIFT:
    DEBUG = False
    TEMPLATE_DEBUG = False
    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']
    ALLOWED_HOSTS = [os.environ['OPENSHIFT_APP_DNS'], socket.gethostname()]
else:
    DEBUG = True
    TEMPLATE_DEBUG = True
    SECRET_KEY = '+*^#b1@rvl_t!3xrb2tz!vuaho9t+ieou)fmm1*i3!9$=nc6#g'
    ALLOWED_HOSTS = []
# ----- END Base configuration ----- #


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
    'ropeelements',
    'siebert',
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
# ----- END App configuration ----- #


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

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'ropeelements', 'locale'),
)

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


# ----- django-compresor ----- #
if ON_OPENSHIFT:
    COMPRESS_OFFLINE = True
else:
    # JS and CSS files are compressed only if DEBUG is False, whereas the less
    # precompiler is always applied.
    _lessc_cmd = os.path.join(BASE_DIR, 'node_modules', 'less', 'bin', 'lessc')

    _less_paths = (
        os.path.join(BASE_DIR, 'ropeelements', 'static', 'ropeelements',
                               'less'),
        os.path.join(BASE_DIR, 'siebert', 'static', 'siebert', 'less'),
        # If DEBUG is True
        os.path.join(BASE_DIR, 'bower_components', 'bootstrap', 'less'),
        # If DEBUG is False
        os.path.join(STATIC_ROOT, 'bootstrap', 'less'),
    )
    _lessc_options = '--include-path=' + os.pathsep.join(_less_paths)
    COMPRESS_PRECOMPILERS = (
        ('text/less',
         '{0} {1} {{infile}} {{outfile}}'.format(_lessc_cmd, _lessc_options)),
    )
    COMPRESS_CSS_FILTERS = (
        # Normalize URLs in url() statements
        'compressor.filters.css_default.CssAbsoluteFilter',
        'compressor.filters.cssmin.CSSMinFilter',
    )
# ----- END django-compresor ----- #


# ----- Media files ----- #
MEDIA_ROOT = os.path.join(BASE_DIR, 'wsgi', 'media')
MEDIA_URL = '/media/'
if not ON_OPENSHIFT:
    SERVE_MEDIA = True


# ----- Logging ----- #
if not ON_OPENSHIFT:
    LOGGING = {
        'version': 1,
        # The default is True, which would disable gunicorn loggers
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] "
                          "%(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'django.utils.log.NullHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
            'logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 500000,
                'backupCount': 9,
                'formatter': 'standard',
            },
            'db_logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'maxBytes': 500000,
            },
        }
    }

    LOG_DIR = os.path.join(os.path.join(BASE_DIR, 'logs'))
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    LOGGING['handlers']['logfile']['filename'] = os.path.join(
        LOG_DIR, 'django.log')

    LOGGING['handlers']['db_logfile']['filename'] = os.path.join(
        LOG_DIR, 'db.log')

    LOGGING['loggers'] = {
        'django': {
            'handlers': ['logfile', 'console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'django.db': {
            'handlers': ['db_logfile'],
            'propagate': False,
            'level': 'DEBUG',
        },
    }
# ----- END Logging ----- #
