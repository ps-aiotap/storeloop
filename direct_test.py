#!/usr/bin/env python
"""Direct test of partner dashboard function"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from stores.views import partner_admin_dashboard

def test_direct():
    """Test partner dashboard function directly"""
    
    try:
        # Create request
        factory = RequestFactory()
        request = factory.get('/test/')
        
        # Create user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@test.com'}
        )
        request.user = user
        
        print("Testing partner dashboard function directly...")
        
        # Call function directly
        response = partner_admin_dashboard(request)
        
        print(f"Response type: {type(response)}")
        print(f"Response status: {getattr(response, 'status_code', 'No status')}")
        
        if hasattr(response, 'content'):
            content = response.content.decode('utf-8')
            print(f"Content length: {len(content)}")
            if 'error' in content.lower():
                print("ERROR FOUND IN CONTENT:")
                print(content[:500])
            else:
                print("SUCCESS: No errors in content")
        
        return True
        
    except Exception as e:
        print(f"DIRECT TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_direct()