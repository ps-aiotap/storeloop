import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from stores.models import Store
import os
from django.conf import settings

@pytest.mark.django_db
class TestProductModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.store = Store.objects.create(
            name='Test Store',
            slug='test-store',
            owner=self.user,
            theme_name='minimal',
            primary_color='#3b82f6',
            font_choice='sans'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=99.99,
            store=self.store
        )

    def test_product_creation(self):
        """Test that a product can be created with required fields"""
        self.assertEqual(self.product.title, 'Test Product')
        self.assertEqual(self.product.description, 'Test description')
        self.assertEqual(float(self.product.price), 99.99)
        self.assertEqual(self.product.store, self.store)

    def test_product_string_representation(self):
        """Test the string representation of a product"""
        self.assertEqual(str(self.product), 'Test Product')

    def test_product_absolute_url(self):
        """Test the absolute URL of a product"""
        expected_url = f'/products/{self.product.id}/'
        self.assertEqual(self.product.get_absolute_url(), expected_url)

    def test_qr_code_generation(self):
        """Test that QR code is generated when product is saved"""
        self.assertIsNotNone(self.product.qr_code)
        qr_path = f'qrcodes/product_{self.product.id}.png'
        self.assertEqual(self.product.qr_code, qr_path)

    def tearDown(self):
        # Clean up created files
        if self.product.qr_code and os.path.exists(os.path.join(settings.MEDIA_ROOT, self.product.qr_code)):
            os.remove(os.path.join(settings.MEDIA_ROOT, self.product.qr_code))