"""
StoreLoop settings for AT Identity integration
Add this to your main settings.py or import from here
"""

# AT Identity Configuration
USE_AT_IDENTITY = True
AT_IDENTITY_URL = 'http://localhost:8001/api/'
AT_IDENTITY_API_KEY = 'your-api-key'
APP_NAME = 'storeloop'

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'at_identity.auth.backends.ATIdentityBackend',
    'django.contrib.auth.backends.ModelBackend',  # Fallback
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'at_identity.auth.middleware.ATIdentityMiddleware',  # Add this
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Login/Logout URLs
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'