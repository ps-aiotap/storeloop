#!/usr/bin/env python
"""Test partner dashboard URL directly"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_partner_url():
    """Test partner dashboard URL directly"""
    
    # Create test client
    client = Client()
    
    # Create or get test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@test.com'}
    )
    if created:
        user.set_password('password')
        user.save()
    
    # Login user
    login_success = client.login(username='testuser', password='password')
    print(f"Login success: {login_success}")
    
    if not login_success:
        # Force login using session
        from django.contrib.auth import login
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.get('/')
        request.user = user
        client.force_login(user)
    
    print("Testing partner dashboard URL...")
    
    try:
        # Test the URL with force login
        client.force_login(user)
        response = client.get('/stores/partner-dashboard/')
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS: Partner dashboard loaded")
            print(f"Content length: {len(response.content)} bytes")
        elif response.status_code == 302:
            print(f"REDIRECT: {response.get('Location', 'Unknown')}")
        elif response.status_code == 500:
            print("ERROR 500: Server error")
            print("Response content:")
            print(response.content.decode('utf-8')[:500])
        else:
            print(f"UNEXPECTED STATUS: {response.status_code}")
            
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_partner_url()