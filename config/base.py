"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", False)

ALLOWED_HOSTS = ["zoomail.ku-unplugged.net", "ku-unplugged.net", "127.0.0.1", "localhost"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "private_storage",
    "social_django",
    "imagekit",
    "django_extensions",
    "webpack_loader",
    "home",
    "members",
    "board",
    "sound",
    "kansou",
    "pictures",
    "movie",
    "otherdocs",
    "mail",
    "meeting_room",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "config.message.ajax_middleware.AjaxMessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
    "config.social_auth.newliveloguser.NewUserRedirectMiddleware",
]

ROOT_URLCONF = "home.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.getenv("DATABASE_HOST", "database"),  # docker networkの解決先
        "PORT": os.getenv("DATABASE_PORT", "3306"),
        "NAME": os.getenv("DATABASE_NAME", "zoomail"),
        "USER": os.getenv("DATABASE_USER", "zoomail"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD"),
    }
}


# CustomUserModel
AUTH_USER_MODEL = "members.User"

# auto primary key
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Private uploaded files
PRIVATE_STORAGE_ROOT = os.path.join(BASE_DIR, "private_media/")
PRIVATE_STORAGE_AUTH_FUNCTION = "private_storage.permissions.allow_authenticated"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static/")


DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024
# 20 KB


# Google OAuth 2
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "config.social_auth.auth0backend.Auth0",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_LOGIN_URL = "/login/"
LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/logged_out/"
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
# Google 認証のurlもスラッシュを外したモノに変更する必要
SOCIAL_AUTH_AUTH0_DOMAIN = "patient-bar-7812.auth0.com"
SOCIAL_AUTH_AUTH0_KEY = os.getenv("SOCIAL_AUTH_AUTH0_KEY")
SOCIAL_AUTH_AUTH0_SECRET = os.getenv("SOCIAL_AUTH_AUTH0_SECRET")

SOCIAL_AUTH_AUTH0_SCOPE = [
    "aud",
    "openid",
    "email",
    "email_verified",
]

# allow CORS origin
CORS_ORIGIN_WHITELIST = [
    "http://localhost:3333",
    "http://localhost:8080",
    "https://ku-unplugged.net",
    "https://message.ku-unplugged.net",
    "https://awase-no-awase.web.app",
]
# レスポンスを公開する
CORS_ALLOW_CREDENTIALS = True

# other settings
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_CLEAN_USERNAMES = True

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    "config.social_auth.social_auth_pipelines.social_details",
    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    "config.social_auth.social_auth_pipelines.social_uid",
    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    "config.social_auth.social_auth_pipelines.auth_allowed",
    # Checks if the current social-account is already associated in the site.
    "config.social_auth.social_auth_pipelines.social_user",
    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    "social_core.pipeline.user.get_username",
    # Create a user account if we haven't found one yet.
    "config.social_auth.create_user_override.create_user",
    # Create the record that associates the social account with the user.
    "config.social_auth.social_auth_pipelines.associate_user",
    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    "config.social_auth.social_auth_pipelines.load_extra_data",
    # Update the user record with any changed info from the auth service.
    "social_core.pipeline.user.user_details",
    # Livelogのメールアドレスを保存
    "config.social_auth.social_auth_pipelines.save_livelog_email",
    # LiveLog, Googleでのログイン情報を保存
    "config.social_auth.social_auth_pipelines.update_login_status",
)

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "dist/",  # must end with slash
        "STATS_FILE": os.path.join(BASE_DIR, "static/dist/webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
    }
}


SEND_MAIL = False
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
AWS_SES_SEND_NUM = 10
AWS_SES_SEND_RATE = 20
SENDGRID_SEND_NUM = 100
EMAIL_USE_SENDGRID = True
EMAIL_USE_SES = True
AWS_SES_REGION_NAME = "us-east-1"
AWS_SES_ACCESS_KEY = os.getenv("AWS_SES_ACCESS_KEY", "")
AWS_SES_SECRET_KEY = os.getenv("AWS_SES_SECRET_KEY", "")


SEND_MAIL_API_ENDPOINT = os.getenv("SEND_MAIL_API_ENDPOINT", "")
SEND_MAIL_API_ID = os.getenv("SEND_MAIL_API_ID", "")
SEND_MAIL_API_KEY = os.getenv("SEND_MAIL_API_KEY", "")
MAIL_STATUS_API_KEY = os.getenv("MAIL_STATUS_API_KEY", "")

# Send Grid Mail Settings
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# # log file create
# if not os.path.isdir(os.path.join(BASE_DIR, 'log')):
#     os.mkdir(os.path.join(BASE_DIR, 'log'))
# if not os.path.isfile(os.path.join(BASE_DIR, 'log', 'debug.log')):
#     f = open(os.path.join(BASE_DIR, 'log', 'debug.log'), 'w')
#     f.close()


# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'production': {
#             'format': '%(asctime)s [%(levelname)s] %(process)d %(thread)d '
#                       '%(pathname)s:%(lineno)d %(message)s'
#         },
#     },
#     'handlers': {
#         # 'file': {
#         #     'level': 'INFO',
#         #     'class': 'logging.handlers.TimedRotatingFileHandler',
#         #     'filename': os.path.join(BASE_DIR, 'log', 'debug.log'),
#         #     'when':'D',
#         #     'interval':1,
#         #     'backupCount':100,
#         #     'delay':False
#         # },
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': './log/debug.log',
#             'maxBytes': 10*1000,
#             'backupCount': 100,
#             'delay':False
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }
