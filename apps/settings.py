# Django settings for ark project.

DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
	('admin', 'bubastix0@gmail.com'),
	# ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

PROJECT_NAME = 'Arenasmedia'

# no se por que los tags no tienen la url absoluta :S
SITE_URL = 'http://arenasmedia.arkad1a.com.ar/'
DJSUBSCRIBE_TO_EMAIL = ['bubastix0@gmail.com']
#DJSUBSCRIBE_TO_EMAIL=(('Nitzer','bubastix0@gmail.com'))
DISQUS_USER = 'arkad1adevel'

SOCIALFEED_FACEBOOK_ID = 101582293251986
SOCIALFEED_FACEBOOK_COUNT = 10 

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
		'NAME': '/home/nitzer/www/arenasmedia/arenasmedia.db',					  # Or path to database file if using sqlite3.
		'USER': '',					  # Not used with sqlite3.
		'PASSWORD': '',				  # Not used with sqlite3.
		'HOST': '',					  # Set to empty string for localhost. Not used with sqlite3.
		'PORT': '',					  # Set to empty string for default. Not used with sqlite3.
	}
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ar'

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/nitzer/www/arenasmedia/statics/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://arenasmedia.arkad1a.com.ar/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '$-u#vh(8aqnf7aiun@*-yd#9^fys0(31(&xfx!5a0wu+xm-(*9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
#	 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.core.context_processors.request',
   'django.contrib.auth.context_processors.auth',
   'context_processor_admin.getapplist',
   'context_processor_admin.getconfig',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'apps.debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'apps.urls'

TEMPLATE_DIRS = (
	# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
	# Always use forward slashes, even on Windows.
	# Don't forget to use absolute paths, not relative paths.
	'/home/nitzer/www/arenasmedia/statics/templates'
)

INSTALLED_APPS = (
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	# Uncomment the next line to enable the admin:
	'django.contrib.admin',
	# Uncomment the next line to enable admin documentation:
	#'django.contrib.admindocs',
	'apps.blocks',
	'apps.captcha',
	'apps.content_media',
	'apps.debug_toolbar',
	'apps.djblog',
	'apps.djcontact',
	'apps.registration',
	'apps.user_profile',
	'apps.socialfeed',
	'apps.djsubscribe',
)

# Debug toolbar
INTERNAL_IPS = ('127.0.0.1','192.168.1.100',)

DEBUG_TOOLBAR_PANELS = (
	'debug_toolbar.panels.version.VersionDebugPanel',
	'debug_toolbar.panels.timer.TimerDebugPanel',
	'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
	'debug_toolbar.panels.headers.HeaderDebugPanel',
	'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
	'debug_toolbar.panels.template.TemplateDebugPanel',
	'debug_toolbar.panels.sql.SQLDebugPanel',
	'debug_toolbar.panels.signals.SignalDebugPanel',
	'debug_toolbar.panels.logger.LoggingPanel',
)


DEBUG_TOOLBAR_CONFIG = {
	'INTERCEPT_REDIRECTS': False,
	'HIDE_DJANGO_SQL': False,
	'TAG': 'div',
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'bubastix0@gmail.com'
EMAIL_HOST_PASSWORD = 'g001109WAWA2'
EMAIL_PORT = 587
