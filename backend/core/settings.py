from pathlib import Path
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# ⚠️ NO expongas esta clave en producción. Usá variables de entorno.
SECRET_KEY = 'django-insecure-lw4kzeg-7oi%0l@9_x=@dsj%35&l%pch)pctzga2@rjqf#v)b%'

# 🔴 Producción
#DEBUG = False
#ALLOWED_HOSTS = ['miapp-eb.elasticbeanstalk.com', 'ligavlc.cl', 'www.ligavlc.cl']

# ✅ Para desarrollo local (activar solo en local)
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',
    'talleres',
    'cursos',
    'clientes',
    'coordinacion',
    'asistencia',
    "widget_tweaks",
]

# Usuario personalizado
AUTH_USER_MODEL = 'usuarios.Usuario'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent / 'frontend' / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# 🔴 Producción con PostgreSQL (activa)
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'ligavlc_db',
#        'USER': 'root',
#        'PASSWORD': 'admin1234',
#        'HOST': 'tu-endpoint-rds.amazonaws.com',
#        'PORT': '5432',
#    }
#}

# ✅ Desarrollo local con SQLite (activar solo localmente)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
#    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.parent / 'frontend' / 'static']
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = reverse_lazy('usuarios:login')
LOGIN_REDIRECT_URL = reverse_lazy('usuarios:home')
LOGOUT_REDIRECT_URL = reverse_lazy('usuarios:login')
