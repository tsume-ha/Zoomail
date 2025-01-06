"""
Django settings for zoomail project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path

import environ


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Take environment variables from .env file
environ.Env.read_env(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "formtools",
    "social_django",
    "private_storage",
    "top",
    "members",
    "mail",
]

# CustomUserModel
AUTH_USER_MODEL = "members.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if os.getenv("DATABASE") == "mariadb":
    # docker compose で起動しているなら compose.yaml の設定から
    # DATABASE環境変数にmariadbを指定している
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "HOST": env("DATABASE_HOST", "database"),  # docker networkの解決先
            "PORT": env("DATABASE_PORT", "3306"),
            "NAME": env("DATABASE_NAME", "zoomail"),
            "USER": env("DATABASE_USER", "zoomail"),
            "PASSWORD": env("DATABASE_PASSWORD"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Social Auth
# https://python-social-auth.readthedocs.io/en/latest/configuration/django.html

# SOCIAL_AUTH_JSONFIELD_ENABLED = True # for postgresql
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "config.social_auth.auth0backend.Auth0",
)
SOCIAL_AUTH_LOGIN_URL = "/"
LOGIN_URL = "/"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/logged_out/"

SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_URL_NAMESPACE = "social"
SOCIAL_AUTH_LIVELOG_KEY = os.getenv("SOCIAL_AUTH_LIVELOG_KEY", "")
SOCIAL_AUTH_LIVELOG_SECRET = os.getenv("SOCIAL_AUTH_LIVELOG_SECRET", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", "")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", "")
SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
TRAILING_SLASH = False
# Google 認証のurlもスラッシュを外したモノに変更する必要
SOCIAL_AUTH_LIVELOG_DOMAIN = "patient-bar-7812.auth0.com"
SOCIAL_AUTH_LIVELOG_SCOPE = [
    "aud",
    "openid",
    "email",
    "email_verified",
]
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
    "config.social_auth.override_create_user.create_user",
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


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ja"

TIME_ZONE = "Asia/Tokyo"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Private Storage
PRIVATE_STORAGE_ROOT = BASE_DIR / "private_media"
PRIVATE_STORAGE_AUTH_FUNCTION = "private_storage.permissions.allow_authenticated"
