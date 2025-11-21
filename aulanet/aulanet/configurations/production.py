from .base import *

# TODO: Cambiar ALLOWED_HOSTS, dejar solo el de producción
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'mi-dominio-ejemplo.com']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


# TODO: Cambiar config de la base de datos para producción
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',

        # 'ENGINE': 'django.db.backends.postgresql',
        # 'ENGINE': 'django.db.backends.mysql',

        # 'NAME': os.getenv('DB_NAME'),
        # 'USER': os.getenv('DB_USER'),
        # 'PASSWORD': os.getenv('DB_PASSWORD'),
        # 'HOST': os.getenv('DB_HOST'),
        # 'PORT': os.getenv('DB_PORT'),
    }
}


os.environ['DJANGO_PORT'] = '8080'  # Puerto por defecto para producción