# Django settings for windmill/leaguevine project.
import os
ROOT_PATH = os.path.dirname(__file__)

OFFLINE = True

#HOST="http://api.playwithlv.com"
HOST="https://api.leaguevine.com"

if HOST=="http://api.playwithlv.com":
    CLIENT_ID = 'a18d62e40f4d269996b01f7cf462a9'
    CLIENT_PWD = '93dbb28011a5224303074b3deebaf6'
#    CLIENT_ID = 'da9b4f5fd6770f788f8be8aff867e9'
#    CLIENT_PWD = '93cecdd6f083134879a0ca05b204ae'
    TOKEN_URL = 'http://www.playwithlv.com'
else:
    TOKEN_URL = 'https://www.leaguevine.com'    
# rehuebli-credentials:
#    CLIENT_ID = '22f92a859d27f9354480ecc92e2900'
#    CLIENT_PWD = '63d60fed612d6fcd86cfc5e47361b0'
## huebli-credentials (is admin now):    
    CLIENT_ID = '07962b73dd29bffd7301ce8e454f77'
    CLIENT_PWD = '4baa879302f7f56572db85347c8cbb'

GROUPME_TOKEN='981e5c303bfe0130acc51231380fc4c3'    

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

# open fields
# 1       array(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20),
# 2       array(20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1),
# 3       array(11,12,13,14,15,16,17,18,19,20,1,2,3,4,5,6,7,8,9,10),
# 4       array(1,2,3,10,14,15,16,11,12,13,17,18,4,5,6,7,8,9,19,20),
# 5       array(1,11,12,18,19,2,3,13,14,15,16,17,4,5,6,7,8,9,10,20),
# 6       array(12,13,14,8,9,10,5,6,7,18,19,11,15,16,17,1,2,3,4,20),
# 7       array(1,2,7,15,8,9,17,18,19,20,10,13,14,11,12,3,4,5,6,16),
# 8       array(1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20), 
# fin       array(3)                   

# mixed fields:
# 1       array(1,2,4,6,8,9,10,11,13,16,17,18,19),
# 2       array(20,19,18,17,16,15,14,13,12,11,10,3,2),
# 3       array(5,4,3,2,1,20,19,18,10,11,9,6,7),
# 4       array(7,8,9,1,2,3,16,18,4,13,5,6,19),
# 5       array(10,11,12,19,7,8,9,17,18,13,14,15,20),
# 6       array(1,2,3,4,11,12,13,14,15,16,17,18,19),
# 7       array(20,18,6,14,19,7,15,13,11,10,12,8,1),
# 8       array(1,2,4,10,11,7,14,15,16,17,18,19),
# fin       array(8)

# women fields:
# 1       array(3,5,7,12,14,15,20), 
# 2       array(4,5,6,7,8,9,1), 
# 3       array(12,13,14,15,16,17,8),
# 4       array(10,11,12,14,15,17,20), 
# 5       array(1,2,3,4,5,6,16), 
# 6       array(5,6,7,8,9,10,20),
# 7       array(3,4,5,9,16,17,2), 
# 8       array(4,5,6,8,9,20),
# fin       array(3)

ROUNDS={"open": [
                 {"round_nr" : 1,
                  "time": "2012-06-15T11:15:00+02:00",
                  "mode": "slide pairing",
                  "fields": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]},
                 {"round_nr" : 2,
                  "time": "2012-06-15T14:00:00+02:00",
                  "mode": "adjacent pairing",
                  "fields": [20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]},
                 {"round_nr" : 3,
                  "time": "2012-06-15T17:00:00+02:00",
                  "mode": "adjacent pairing",
                  "fields": [11,12,13,14,15,16,17,18,19,20,1,2,3,4,5,6,7,8,9,10]},
                 {"round_nr" : 4,
                  "time": "2012-06-16T09:00:00+02:00",
                  "mode": "adjacent pairing",
                  "fields": [1,2,3,10,14,15,16,11,12,13,17,18,4,5,6,7,8,9,19,20]},
                 {"round_nr" : 5,
                  "time": "2012-06-16T12:00:00+02:00",
                  "mode": "adjacent pairing",
                  "fields": [1,11,12,18,19,2,3,13,14,15,16,17,4,5,6,7,8,9,10,20]},
                 {"round_nr" : 6,
                  "time": "2012-06-16T15:00:00+02:00",
                  "name": "QF",
                  "mode": "adjacent pairing",
                  "fields": [12,13,14,8,9,10,5,6,7,18,19,11,15,16,17,1,2,3,4,20]},
                 {"round_nr" : 7,
                  "time": "2012-06-16T18:00:00+02:00",
                  "name": "SF",
                  "mode": "adjacent pairing",
                  "fields": [1,2,7,15,8,9,17,18,19,20,10,13,14,11,12,3,4,5,6,16]},
                 {"round_nr" : 8,
                  "time": "2012-06-17T10:30:00+02:00",
                  "name": "Final",
                  "mode": "adjacent pairing",
                  "fields": [1,2,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]},
                 {"round_nr" : 9,
                  "time": "2012-06-17T15:00:00+02:00",
                  "name": "BigFinal",
                  "fields": [6]},
                 ],
        "mixed": [
                 {"round_nr" : 1,
                  "time": "2012-06-15T10:00:00+02:00",
                  "mode": "slide pairing",
                  "fields":[1,2,4,6,8,9,10,11,13,16,17,18,19]},
                 {"round_nr" : 2,
                  "time": "2012-06-15T12:30:00+02:00",
                  "mode": "adjacent pairing",
                  "fields":[20,19,18,17,16,15,14,13,12,11,10,3,2]},
                 {"round_nr" : 3,
                  "time": "2012-06-15T15:30:00+02:00",
                  "mode": "adjacent pairing",
                  "fields":[5,4,3,2,1,20,19,18,10,11,9,6,7]},
                 {"round_nr" : 4,
                  "time": "2012-06-16T10:30:00+02:00",
                  "mode": "adjacent pairing",
                  "fields":[7,8,9,1,2,3,16,18,4,13,5,6,19]},
                 {"round_nr" : 5,
                  "time": "2012-06-16T13:30:00+02:00",
                  "mode": "adjacent pairing",
                  "fields":[10,11,12,19,7,8,9,17,18,13,14,15,20]},
                 {"round_nr" : 6,
                  "time": "2012-06-16T16:30:00+02:00",
                  "name": "QF",
                  "mode": "adjacent pairing",
                  "fields":[1,2,3,4,11,12,13,14,15,16,17,18,19]},
                 {"round_nr" : 7,
                  "time": "2012-06-17T09:00:00+02:00",
                  "name": "SF",
                  "mode": "adjacent pairing",
                  "fields":[20,18,6,14,19,7,15,13,11,10,12,8,1]},
                 {"round_nr" : 8,
                  "time": "2012-06-17T12:00:00+02:00",
                  "name": "Final",
                  "mode": "adjacent pairing",
                  "fields":[1,2,4,10,11,3,14,15,16,17,18,19]},
                 {"round_nr" : 9,
                  "time": "2012-06-17T13:00:00+02:00",
                  "name": "BigFinal",
                  "fields":[6]},
                 ],
        "women": [
                 {"round_nr" : 1,
                  "time": "2012-06-15T10:00:00+02:00",
                  "mode": "slide pairing",
                  "fields":[3,5,7,12,14,15,20]},
                 {"round_nr" : 2,
                  "time": "2012-06-15T12:30:00+02:00",
                  "mode": "adjacent pairing",
                  "fields":[4,5,6,7,8,9,1]},
                 {"round_nr" : 3,
                  "time": "2012-06-15T15:30:00+02:00",
                  "mode": "adjacent pairing",
                  "fields":[12,13,14,15,16,17,8]},
                 {"round_nr" : 4,
                  "time": "2012-06-16T10:30:00+02:00",
                  "mode": "adjacent pairing",
                  "fields":[10,11,12,14,15,17,20]},
                 {"round_nr" : 5,
                  "time": "2012-06-16T13:30:00+02:00",
                  "mode": "adjacent pairing",
                  "fields":[1,2,3,4,5,6,16]},
                 {"round_nr" : 6,
                  "time": "2012-06-16T16:30:00+02:00",
                  "name": "QF",
                  "mode": "adjacent pairing",
                  "fields":[5,6,7,8,9,10,20]},
                 {"round_nr" : 7,
                  "time": "2012-06-17T09:00:00+02:00",
                  "name": "SF",
                  "mode": "adjacent pairing",
                  "fields":[3,4,5,9,16,17,2]},
                 {"round_nr" : 8,
                  "time": "2012-06-17T12:00:00+02:00",
                  "name": "Final",
                  "mode": "adjacent pairing",
                  "fields":[12,5,13,8,9,20]},
                 {"round_nr" : 9,
                  "time": "2012-06-17T14:00:00+02:00",
                  "name": "BigFinal",
                  "fields":[7]},
                 ]
        }

# sanity checks for fields:
# open:
for r in ROUNDS["open"]:
    if r['round_nr']<8 and sorted(r['fields'])!=range(1,21):
#        logger.error('field fixtures in open division incorrect')
        raise
# mixed & women
for r in ROUNDS['mixed']:
    fields=r['fields']+ROUNDS['women'][r['round_nr']-1]['fields']
    if r['round_nr']<8 and sorted(fields)!=range(1,21):
#        logger.error('field fixtures in mixed/women incorrect')
        raise
    

SEASON_ID = {'open': '20068',
             'mixed': '20067',
             'women': '20069'}

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Christian Schaffner', 'huebli@gmail.com'),
)

MANAGERS = ADMINS
# 
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#         'NAME': 'windmill',                      # Or path to database file if using sqlite3.
#         'USER': '',                      # Not used with sqlite3.
#         'PASSWORD': '',                  # Not used with sqlite3.
#         'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#         'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#     }
# }


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost:5432/windmill')}

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
    '/Users/chris/Sites/windmill/windmill/static',
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
    'windmill.tools',
    'windmill.spirit',
 #   'windmill.sms',
 #   'windmill.powerrank',
    'windmill.groupme',
    'gunicorn',
    'south'
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
        },
        'windmill.spirit': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'windmill.sms': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'windmill.powerrank': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        }
    }
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
