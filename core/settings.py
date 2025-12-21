"""
Django settings for core project.
"""

import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
# 1. Définition du dossier racine
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Chargement du fichier .env
# On cherche le fichier .env à la racine du projet
load_dotenv(BASE_DIR / '.env')


# --- SÉCURITÉ ---

# Clé secrète (Indispensable !)
# Si elle n'est pas dans le .env, on utilise une clé par défaut pour le dev
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-dev-key')

# Mode Debug
# Lit la valeur dans le .env (True ou False). Par défaut False pour sécurité.
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']


# --- APPLICATIONS ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Tiers (Libraries externes)
    'rest_framework',
    'corsheaders',

    # Vos applications
    'subscriptions',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Doit être tout en haut
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
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
        'DIRS': [],
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


# --- BASE DE DONNÉES ---

# Configuration automatique via DATABASE_URL du .env
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True
    )
}


# --- VALIDATION MOT DE PASSE ---

AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# --- INTERNATIONALISATION ---

LANGUAGE_CODE = 'fr-fr'

# Très important pour ton projet (Dates de paiement correctes)
TIME_ZONE = 'Africa/Tunis'

USE_I18N = True
USE_TZ = True


# --- FICHIERS STATIQUES ---

STATIC_URL = 'static/'


# --- CONFIGURATION API (DRF) ---

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Le token d'accès dure 1h
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Le token de refresh dure 24h
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'AUTH_HEADER_TYPES': ('Bearer',),                # Important pour le frontend : "Bearer <token>"
}




# --- CONFIGURATION CORS ---

CORS_ALLOW_ALL_ORIGINS = True