#!/usr/bin/env python
"""Debug script to test partner dashboard functionality"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

def test_partner_dashboard():
    """Test partner dashboard components"""
    print("Testing Partner Dashboard Components...")
    
    try:
        # Test 1: Import models
        print("\n1. Testing model imports...")
        from stores.models import Store, PartnerStoreAccess
        print("[OK] Models imported successfully")
        
        # Test 2: Check database tables
        print("\n2. Testing database access...")
        store_count = Store.objects.count()
        print(f"[OK] Found {store_count} stores in database")
        
        # Test 3: Check PartnerStoreAccess table
        try:
            access_count = PartnerStoreAccess.objects.count()
            print(f"[OK] Found {access_count} partner access records")
        except Exception as e:
            print(f"[ERROR] PartnerStoreAccess table error: {str(e)}")
            return False
        
        # Test 4: List all stores
        print("\n3. Listing all stores...")
        stores = Store.objects.all()[:10]
        for store in stores:
            print(f"   - Store ID {store.id}: {store.name}")
        
        # Test 5: Check for Riwayat store
        print("\n4. Looking for Riwayat store...")
        try:
            riwayat = Store.objects.get(id=35)
            print(f"[OK] Found Riwayat: ID {riwayat.id}, Name: {riwayat.name}")
        except Store.DoesNotExist:
            print("[ERROR] Riwayat store (ID 35) not found")
        
        # Test 6: Test user access
        print("\n5. Testing user access...")
        from django.contrib.auth.models import User
        users = User.objects.all()[:3]
        for user in users:
            print(f"   - User: {user.username} (ID: {user.id})")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Critical error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_partner_view():
    """Test the partner dashboard view directly"""
    print("\nTesting Partner Dashboard View...")
    
    try:
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        from stores.views import partner_admin_dashboard
        
        # Create a test request
        factory = RequestFactory()
        request = factory.get('/stores/partner-dashboard/')
        
        # Get or create a test user
        user, created = User.objects.get_or_create(username='testuser')
        request.user = user
        
        print(f"[OK] Created test request for user: {user.username}")
        
        # Call the view
        response = partner_admin_dashboard(request)
        print(f"[OK] View executed successfully, status: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] View test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("StoreLoop Partner Dashboard Debug")
    print("=" * 50)
    
    success1 = test_partner_dashboard()
    success2 = test_partner_view()
    
    if success1 and success2:
        print("\n[SUCCESS] All tests passed! Partner dashboard should work.")
    else:
        print("\n[FAILED] Some tests failed. Check the errors above.")