from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Store
from products.models import Product

class StoreContextTest(TestCase):
    def setUp(self):
        # Create users
        self.owner = User.objects.create_user(username='storeowner', password='password')
        self.customer = User.objects.create_user(username='customer', password='password')
        
        # Create stores
        self.store1 = Store.objects.create(
            name='Store 1', 
            slug='store-1',
            owner=self.owner,
            theme_name='dark'
        )
        self.store2 = Store.objects.create(
            name='Store 2', 
            slug='store-2',
            owner=self.owner,
            theme_name='warm'
        )
        
        # Create products for each store
        self.product1 = Product.objects.create(
            title='Product 1',
            description='Product from Store 1',
            price=10.00,
            store=self.store1
        )
        self.product2 = Product.objects.create(
            title='Product 2',
            description='Product from Store 2',
            price=20.00,
            store=self.store2
        )
        
        self.client = Client()

    def test_store_owner_switching(self):
        # Login as store owner
        self.client.login(username='storeowner', password='password')
        
        # Test default store selection (first store)
        response = self.client.get('/')
        self.assertEqual(response.context['store_theme']['name'], 'Store 1')
        self.assertEqual(response.context['store_theme']['theme_name'], 'dark')
        
        # Test switching to second store via query param
        response = self.client.get(f'/?store_id={self.store2.id}')
        self.assertEqual(response.context['store_theme']['name'], 'Store 2')
        self.assertEqual(response.context['store_theme']['theme_name'], 'warm')
    
    def test_non_owner_store_context(self):
        # Login as customer (non-owner)
        self.client.login(username='customer', password='password')
        
        # Test accessing store 1 via path
        response = self.client.get('/stores/store-1/')
        self.assertEqual(response.context['store_theme']['name'], 'Store 1')
        self.assertEqual(response.context['store_theme']['theme_name'], 'dark')
        
        # Test accessing store 2 via query param
        response = self.client.get('/?store=store-2')
        self.assertEqual(response.context['store_theme']['name'], 'Store 2')
        self.assertEqual(response.context['store_theme']['theme_name'], 'warm')
    
    def test_anonymous_user_store_context(self):
        # Test as anonymous user
        response = self.client.get('/stores/store-1/')
        self.assertEqual(response.context['store_theme']['name'], 'Store 1')
        self.assertEqual(response.context['store_theme']['theme_name'], 'dark')
    
    def test_product_filtering(self):
        # Test that products are filtered by store
        response = self.client.get('/stores/store-1/')
        products = list(response.context['products'])
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].title, 'Product 1')
        
        response = self.client.get('/stores/store-2/')
        products = list(response.context['products'])
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].title, 'Product 2')
    
    def test_no_store_context(self):
        # Test accessing root without store context
        response = self.client.get('/')
        self.assertEqual(response.context['store_theme']['name'], 'StoreLoop')  # Default theme
        self.assertTrue(response.context.get('no_store_selected', False))  # Flag for store selection page