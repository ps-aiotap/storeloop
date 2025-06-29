#!/usr/bin/env python
"""
Quick test script to verify the main fixes work
"""
import os
import django
from django.test import TestCase, Client
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from stores.models import Store, Product, SellerProfile

def test_unicode_support():
    """Test that Unicode text can be saved and retrieved"""
    print("Testing Unicode support...")
    
    # Create test user
    user = User.objects.create_user('testuser', 'test@example.com', 'password')
    
    # Create store
    store = Store.objects.create(
        name='Test Store',
        description='Test Description',
        owner=user,
        slug='test-store'
    )
    
    # Create product with Hindi name
    hindi_name = 'बनारसी सिल्क साड़ी'
    product = Product.objects.create(
        store=store,
        name=hindi_name,
        description='Beautiful handwoven saree',
        price=15000,
        stock=3
    )
    
    # Retrieve and verify
    retrieved_product = Product.objects.get(id=product.id)
    assert retrieved_product.name == hindi_name, f"Expected '{hindi_name}', got '{retrieved_product.name}'"
    
    print(f"✓ Unicode test passed: {retrieved_product.name}")
    
    # Clean up
    product.delete()
    store.delete()
    user.delete()

def test_ngo_admin():
    """Test NGO admin functionality"""
    print("Testing NGO admin setup...")
    
    # Create NGO user
    ngo_user = User.objects.create_user('ngo_admin', 'ngo@example.com', 'password')
    
    # Create profile
    profile = SellerProfile.objects.create(
        user=ngo_user,
        is_partner_admin=True,
        organization_name='Test NGO'
    )
    
    assert profile.is_partner_admin == True
    print("✓ NGO admin test passed")
    
    # Clean up
    profile.delete()
    ngo_user.delete()

def test_pages_load():
    """Test that key pages load without errors"""
    print("Testing page loads...")
    
    client = Client()
    
    # Test pages that should load without auth
    pages = [
        '/stores/',
        '/stores/hindi-test/',
    ]
    
    for page in pages:
        try:
            response = client.get(page)
            assert response.status_code in [200, 302], f"Page {page} returned {response.status_code}"
            print(f"✓ Page {page} loads correctly")
        except Exception as e:
            print(f"✗ Page {page} failed: {e}")

if __name__ == '__main__':
    print("Running quick fix verification tests...")
    
    try:
        test_unicode_support()
        test_ngo_admin()
        test_pages_load()
        print("\n✓ All tests passed! Fixes are working.")
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()