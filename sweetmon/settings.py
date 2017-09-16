import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
# - Please Change this key before install on server.
SECRET_KEY = 'y3r$r7#g(g_6xt!q35ct=6sqt0kiihqe2vc#k%bktayz@vok2v'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

HASHSALT = "th1s1ss0rt"

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'monitor',
    'track',
    'testcase',
    'fuzz'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'sweetmon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sweetmon.wsgi.application'


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

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_URL = '/files/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'files')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/assets/'  # change later DEBUG

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, '/')
LOGIN_URL="/account/login/"
LOGIN_REDIRECT_URL="/"


USE_EMAIL_ALERT=True
USE_TELEGRAM_ALERT=True


CRASH_STORAGE_ROOT = os.path.join(BASE_DIR, 'files/crashes/')
TESTCASE_STORAGE_ROOT = os.path.join(BASE_DIR, 'files/testcase/')
FUZZER_STORAGE_ROOT = os.path.join(BASE_DIR, 'files/fuzzer/')
USERIMAGE_STORAGE_ROOT = os.path.join(BASE_DIR, 'files/userimage/')

if DEBUG == False:
    SESSION_COOKIE_AGE = 60 * 30

# AUTH_USER_MODEL = 'auth.User'
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
