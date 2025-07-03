#!/usr/bin/env python
"""Check if DEBUG mode is actually enabled"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.conf import settings

print("Django Settings Check:")
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"DATABASE ENGINE: {settings.DATABASES['default']['ENGINE']}")
print(f"DATABASE NAME: {settings.DATABASES['default']['NAME']}")

# Check if logging is enabled
if hasattr(settings, 'LOGGING'):
    print("LOGGING: Configured")
else:
    print("LOGGING: Not configured")

# Check environment variables
print(f"\nEnvironment Variables:")
print(f"DEBUG env: {os.environ.get('DEBUG', 'Not set')}")
print(f"USE_SQLITE env: {os.environ.get('USE_SQLITE', 'Not set')}")
print(f"ENABLE_FILE_LOGGING env: {os.environ.get('ENABLE_FILE_LOGGING', 'Not set')}")

# Test database connection
try:
    from stores.models import Store
    store_count = Store.objects.count()
    print(f"\nDatabase connection: OK ({store_count} stores)")
except Exception as e:
    print(f"\nDatabase connection: FAILED - {str(e)}")

print(f"\nServer should be accessible at: http://localhost:8000/stores/partner-dashboard/")