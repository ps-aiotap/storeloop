from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Store, Product

class StoreTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        
    def test_currency_symbol_rupees(self):
        """Test that currency symbol shows ₹ instead of $"""
        store = Store.objects.create(
            name='Test Store',
            owner=self.user,
            is_published=True
        )
        product = Product.objects.create(
            store=store,
            name='Test Product',
            price=100.00
        )
        
        response = self.client.get(f'/stores/{store.slug}/')
        self.assertContains(response, '₹100')
        self.assertNotContains(response, '$100')
        
    def test_unpublished_store_access_control(self):
        """Test access control for unpublished stores"""
        store = Store.objects.create(
            name='Unpublished Store',
            owner=self.user,
            is_published=False
        )
        
        # Anonymous user cannot access
        response = self.client.get(f'/stores/{store.slug}/')
        self.assertContains(response, 'Store not available')
        
        # Owner can access
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(f'/stores/{store.slug}/')
        self.assertEqual(response.status_code, 200)
        
        # Admin can access
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(f'/stores/{store.slug}/')
        self.assertEqual(response.status_code, 200)
        
    def test_store_listing_visibility(self):
        """Test store listing shows only published stores to regular users"""
        published_store = Store.objects.create(
            name='Published Store',
            owner=self.user,
            is_published=True
        )
        unpublished_store = Store.objects.create(
            name='Unpublished Store', 
            owner=self.user,
            is_published=False
        )
        
        # Anonymous user sees only published
        response = self.client.get('/stores/')
        self.assertContains(response, 'Published Store')
        self.assertNotContains(response, 'Unpublished Store')
        
        # Admin sees all stores
        self.client.login(username='admin', password='adminpass')
        response = self.client.get('/stores/')
        self.assertContains(response, 'Published Store')
        self.assertContains(response, 'Unpublished Store')
        
    def test_unique_slug_generation(self):
        """Test that stores get unique slugs"""
        store1 = Store.objects.create(name='Test Store', owner=self.user)
        store2 = Store.objects.create(name='Test Store', owner=self.user)
        
        self.assertNotEqual(store1.slug, store2.slug)
        self.assertTrue(store2.slug.startswith('test-store'))
        
    def test_onboarding_flow(self):
        """Test 5-step onboarding creates store properly"""
        self.client.login(username='testuser', password='testpass')
        
        # Step 1: Basic info
        response = self.client.post('/stores/onboarding/', {
            'name': 'कलाकार शिल्प',
            'description': 'Handmade crafts'
        })
        self.assertEqual(response.status_code, 302)
        
        store = Store.objects.get(owner=self.user)
        self.assertEqual(store.name, 'कलाकार शिल्प')
        self.assertTrue(store.slug)  # Slug should be generated
        
    def test_hindi_ui_support(self):
        """Test Hindi store names generate proper slugs"""
        store = Store.objects.create(
            name='कलाकार शिल्प',
            owner=self.user
        )
        # Should generate a valid slug even for Hindi names
        self.assertTrue(store.slug)
        self.assertNotEqual(store.slug, '')