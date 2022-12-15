from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DB_ENGINE'),
        'NAME': get_env_variable('DB_NAME'),
        'HOST': get_env_variable('DB_HOST'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'PORT': get_env_variable('DB_PORT')
    }
}