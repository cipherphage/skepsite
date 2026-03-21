from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='skepsite'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# In dev, allow all IPs for admin access unless explicitly set
ADMIN_ALLOWED_IPS = config(
    'ADMIN_ALLOWED_IPS',
    default='',
    cast=lambda v: [ip.strip() for ip in v.split(',') if ip.strip()]
)

# Show Django debug toolbar output in dev
INTERNAL_IPS = ['127.0.0.1']
