import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def _carregar_env():
    arquivo = BASE_DIR / '.env'
    if not arquivo.is_file():
        return
    for linha in arquivo.read_text(encoding='utf-8').splitlines():
        linha = linha.strip()
        if not linha or linha.startswith('#') or '=' not in linha:
            continue
        chave, valor = linha.split('=', 1)
        os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


def _lista_env(nome):
    return [item.strip() for item in os.environ.get(nome, '').split(',') if item.strip()]


_carregar_env()


DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'chave-insegura-apenas-para-desenvolvimento-local'
    else:
        raise ImproperlyConfigured(
            'Defina DJANGO_SECRET_KEY (no ambiente ou no arquivo .env). '
            'O README explica como gerar uma.'
        )



ALLOWED_HOSTS = _lista_env('DJANGO_ALLOWED_HOSTS')

CSRF_TRUSTED_ORIGINS = _lista_env('DJANGO_CSRF_TRUSTED_ORIGINS')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eduardo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eduardo.wsgi.application'




if os.environ.get('POSTGRES_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ['POSTGRES_DB'],
            'USER': os.environ.get('POSTGRES_USER', ''),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True



STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



if os.environ.get('DJANGO_BEHIND_PROXY') == '1':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



if not DEBUG and os.environ.get('DJANGO_HTTPS', '1') == '1':
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'alunos'
LOGOUT_REDIRECT_URL = 'login'
