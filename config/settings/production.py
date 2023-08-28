from .base import *

DEBUG = False

# https://docs.djangoproject.com/en/4.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost', '.localhost', '127.0.0.1', 'dornika.shop', 'dornikas.shop', 'https://dornikash.shop']   # WILL CHANGE
# In production if server returns error '400 BAD REQUEST' it means 'ALLOWED_HOSTS' is not
# set correctly

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Security srttings (These are should be True in production)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True


# try:
#     from .local import *
# except ImportError:
#     pass
