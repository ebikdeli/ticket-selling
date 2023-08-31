"""
*** We have secured our settings file by hiding the secret informations by 'python-decouple' library***
"""
import os
from collections import OrderedDict
from decouple import config


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

SECRET_KEY = config('SECRET_KEY')

SITE_ID = 3

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_extensions',

    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    'django_quill',
    'sorl.thumbnail',
    'constance',
    # To be able to use database for 'constance'
    'constance.backends.database',
    'watchman',
    
    # APPs in django
    'users',
    'login',
    'vitrin',
    'cart',
    'order',
    'payment',
    'ticket',
    'support',
    'dashboard',
    
    # allauth apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',                # To activate 'cors-headers'
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',    
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cart.custom_middleware.InitialSessionMiddleware',      # Customized middleware to check sessions
]


ROOT_URLCONF = 'config.urls'


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 
                os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processor.get_cart',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('MYSQL_DB'),
        'USER': config('MYSQL_USER'),
        'PASSWORD': config('MYSQL_PASSWORD'),
        'HOST': config('MYSQL_HOST'),
        'PORT': config('MYSQL_PORT'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL = 'users.User'


LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = ','

STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
# To deploy on Host (Sub folders do not accepted by host!):
STATIC_ROOT = '/home/dornikas/public_html/static'

STATICFILES_DIRS = [
    BASE_DIR,
    os.path.join(BASE_DIR, 'statics')
]

MEDIA_URL = '/media/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# To deploy on Host:
MEDIA_ROOT = '/home/dornikas/public_html/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = 'dashboard:profile'
LOGIN_URL = 'login:login-signup'

LOGOUT_REDIRECT_URL = 'vitrin:index'


# Cors headers settings (NOTE: Without 'cors', process on diffrent domains and ports could not speak to each other! 'same-origin' only enabled when two process work on same domain and port)
# In ajax request using 'fetch' or any front techs like 'reqct', 'angular' or even an script with 'requests' library, we must enable 'CORS' for the server.
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
    'http://127.0.0.1:5500',
    'https://127.0.0.1:5500',
]
# * If we don't set 'CORS_ALLOW_CREDENTIALS = True', We will get this error on client side:
# Access to fetch at 'http://127.0.0.1:8000/add_product_cart' from origin 'http://127.0.0.1:5500' has been blocked by CORS policy: The value of the 'Access-Control-Allow-Credentials' header in the response is '' which must be 'true' when the request's credentials mode is 'include'.
# NOTE: Remember that without this field, any cookie sent by client, does not checked by server!
CORS_ALLOW_CREDENTIALS = True

# * To be able to let 'X-CSRFToken' header checked by server (this header sent by any client) we must 
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:5500",
    'http://*:*'
]


# CKEditor settings
# each one of three below is acceptable
CKEDITOR_BASEPATH = f"{STATIC_URL}ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = "uploads/"

# CKEditor optional settings
# CKEDITOR_CONFIGS = {
    # 'default': {
        # 'toolbar': 'full',
        # 'toolbar': 'basic',
        # 'height': 300,
        # 'width': 300,
    # },
# }


# django-constance settings
# https://django-constance.readthedocs.io/en/latest/
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = OrderedDict([
    # Email
    ('email', ('admin@dornikas.shop', 'Main email of the server')),
    # Contact Number
    ('contact', ('09124455666', 'Main contact for contact us page')),
    # About us field
    # ('about_us', ('', 'About Us field shown to users in "about us page"')),
    # Address of the links used in website
    ('instagram', ('', 'Instagram link')),
    ('linkedin', ('', 'Linkedin')),
    ('twitter', ('', 'Twitter')),
    ('whatsapp', ('', 'Whatsapp')),
    ('facebook', ('', 'Facebook')),
])

CONSTANCE_CONFIG_FIELDSETS = {
    'Email': ('email',),
    'Contact Number': ('contact',),
    # 'About Us': ('about_us',),
    'Links': {'fields': ['instagram', 'linkedin', 'twitter', 'whatsapp', 'facebook'], 'collapse': True},
}

CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True


# By default django uses 'redis' to store 'constance' variables. to use database we should follow this document:
# https://django-constance.readthedocs.io/en/latest/backends.html#database
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


# ! To authenticate email server, we either have to use ('EMAIL_PORT=587', 'EMAIL_USE_TLS=True') or ('EMAIL_PORT=465', 'EMAIL_USE_SSL=True'). We cannot use both
# ? Both of SSL and TSL works, but it looks ('EMAIL_PORT=587', 'EMAIL_USE_TLS=True') is faster

# SMTP server connection
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')




# AUTHENTICATION_BACKENDS

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]


# Social login settings

SOCIALACCOUNT_LOGIN_ON_GET = True
# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account',
        }
    }
}


# ? Payment Gateway data

ZARIN_MERCHANT_ID = config('ZARIN_MERCHANT_ID')
