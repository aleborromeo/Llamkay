"""
Configuración base de Django para el proyecto Llamkay.
Configuración común para todos los entornos.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
# En producción, esto debe venir de variables de entorno
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure--7dbecl@v_#5lvw5xd+ww*61l4x^r)g$+50&w@)x@0$fsy!13k'
)


# Application definition
INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps del proyecto
    'apps.users',
    'apps.chats',
    'apps.jobs',
    'apps.llamkay',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.csrf',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


# Media files (uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'llamkay:home'
LOGOUT_REDIRECT_URL = 'llamkay:home'


# Custom User Model (si lo usas)
# AUTH_USER_MODEL = 'users.Usuario'


# Messages framework
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# ==================== API EXTERNA - APIS.NET.PE ====================
# Token JWT para consultas de DNI (RENIEC) y RUC (SUNAT)
APIPERU_TOKEN = 'apis-token-15994.QTKH6OudufG0IiLw5plIH9ucJ6MqNQSd'
# URLs de las APIs
APIPERU_BASE_URL = 'https://api.apis.net.pe/v1'
APIPERU_TIMEOUT = 10  # segundos

# ✅ DEBUG: Verificar que el token se cargó
print("\n" + "="*60)
print("⚙️  BASE.PY - Token configurado")
print("="*60)
print(f"🔑 APIPERU_TOKEN definido: {bool(APIPERU_TOKEN)}")
if APIPERU_TOKEN:
    print(f"🔑 APIPERU_TOKEN valor: {APIPERU_TOKEN[:30]}...")
print("="*60 + "\n")