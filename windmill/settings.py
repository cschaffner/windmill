# Django settings for windmill/leaguevine project.
import os
ROOT_PATH = os.path.dirname(__file__)

HOST="playwithlv.com"
CLIENT_ID = 'a18d62e40f4d269996b01f7cf462a9'
CLIENT_PWD = '93dbb28011a5224303074b3deebaf6'

# Windmill fixtures

#//  open division:
#//        Swiss 1:     Fr 15.06.2012    11:15 (game length: 75min)
#//        Swiss 2:     Fr 15.06.2012    14:00 (game length: 90min)
#//        Swiss 3:     Fr 15.06.2012    17:00
#//        Swiss 4:     Sa 16.06.2012    09:00
#//        Swiss 5:     Sa 16.06.2012    12:00
#//        QF:          Sa 16.06.2012    15:00
#//        Semis:       Sa 16.06.2012    18:00
#//        Finals:      So 17.06.2012    10:30
#//        BigFinal:    So 17.06.2012    15:00

#//  women/mixed division:
#//        Swiss 1:     Fr 15.06.2012    10:00 (game length: 75min)
#//        Swiss 2:     Fr 15.06.2012    12:30 (game length: 90min)
#//        Swiss 3:     Fr 15.06.2012    15:30
#//        Swiss 4:     Sa 16.06.2012    10:30
#//        Swiss 5:     Sa 16.06.2012    13:30
#//        QF:          Sa 16.06.2012    16:30
#//        Semis:       So 17.06.2012    09:00
#//        Finals:      So 17.06.2012    12:00
#
#//        mixed Fin:   So 17.06.2012    14:00
#//        women Fin:   So 17.06.2012    13:00

ROUNDS={"open": [
                 {"round_nr" : 1,
                  "time": "2012-06-15T11:15:00+02:00",
                  "mode": "fold"},
                 {"round_nr" : 2,
                  "time": "2012-06-15T14:00:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 3,
                  "time": "2012-06-15T17:00:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 4,
                  "time": "2012-06-16T09:00:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 5,
                  "time": "2012-06-16T12:00:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 6,
                  "time": "2012-06-16T15:00:00+02:00",
                  "mode": "QF"},
                 {"round_nr" : 7,
                  "time": "2012-06-16T18:00:00+02:00",
                  "mode": "SF"},
                 {"round_nr" : 8,
                  "time": "2012-06-17T10:30:00+02:00",
                  "mode": "Final"},
                 {"round_nr" : 9,
                  "time": "2012-06-17T15:00:00+02:00",
                  "mode": "BigFinal"},
                 ],
        "mixed": [
                 {"round_nr" : 1,
                  "time": "2012-06-15T10:00:00+02:00",
                  "mode": "fold"},
                 {"round_nr" : 2,
                  "time": "2012-06-15T12:30:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 3,
                  "time": "2012-06-15T15:30:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 4,
                  "time": "2012-06-16T10:30:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 5,
                  "time": "2012-06-16T13:30:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 6,
                  "time": "2012-06-16T16:30:00+02:00",
                  "mode": "QF"},
                 {"round_nr" : 7,
                  "time": "2012-06-17T09:00:00+02:00",
                  "mode": "SF"},
                 {"round_nr" : 8,
                  "time": "2012-06-17T12:00:00+02:00",
                  "mode": "Final"},
                 {"round_nr" : 9,
                  "time": "2012-06-17T14:00:00+02:00",
                  "mode": "BigFinal"},
                 ],
        "women": [
                 {"round_nr" : 1,
                  "time": "2012-06-15T10:00:00+02:00",
                  "mode": "fold"},
                 {"round_nr" : 2,
                  "time": "2012-06-15T12:30:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 3,
                  "time": "2012-06-15T15:30:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 4,
                  "time": "2012-06-16T10:30:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 5,
                  "time": "2012-06-16T13:30:00+02:00",
                  "mode": "adjacent"},
                 {"round_nr" : 6,
                  "time": "2012-06-16T16:30:00+02:00",
                  "mode": "QF"},
                 {"round_nr" : 7,
                  "time": "2012-06-17T09:00:00+02:00",
                  "mode": "SF"},
                 {"round_nr" : 8,
                  "time": "2012-06-17T12:00:00+02:00",
                  "mode": "Final"},
                 {"round_nr" : 9,
                  "time": "2012-06-17T13:00:00+02:00",
                  "mode": "BigFinal"},
                 ]
        }


SEASON_ID = {'open': '6980',
             'mixed': '7513',
             'women': '7515'}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'postgres',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Amsterdam'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# use time-zone support
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/Users/chris/Sites/windmill/static',
    '/app/windmill/static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9#$yz-mc(zkm9dfjk@4-)%g66knsxg+2_h)e2j36pd6)$$v7&3'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'windmill.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),

    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'windmill.tools'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# logging configuration from the Django doc
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'windmill.tools': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        }
    }
}
