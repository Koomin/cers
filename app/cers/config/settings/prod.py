from .base import *  # noqa

DEBUG = get_env_variable('DEBUG')  # noqa

DATABASES = {
    'default': {
        'ENGINE': get_env_variable('DB_ENGINE'),  # noqa
        'NAME': get_env_variable('DB_NAME'),  # noqa
        'HOST': get_env_variable('DB_HOST'),  # noqa
        'USER': get_env_variable('DB_USER'),  # noqa
        'PASSWORD': get_env_variable('DB_PASSWORD'),  # noqa
        'PORT': get_env_variable('DB_PORT'),  # noqa
    }
}
