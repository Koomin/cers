from .base import *  # noqa

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),  # noqa
        'HOST': get_env_variable('DB_HOST'),  # noqa
        'USER': get_env_variable('DB_USER'),  # noqa
        'PASSWORD': get_env_variable('DB_PASSWORD'),  # noqa
        'PORT': get_env_variable('DB_PORT'),  # noqa
    }
}
