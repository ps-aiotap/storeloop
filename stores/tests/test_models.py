import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from stores.models import Store

@pytest.mark.django_db
class TestStoreModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.store = Store.objects.create(
            name='Test Store',
            owner=self.user,
            theme_name='minimal',
            primary_color='#3b82f6',
            font_choice='sans'
        )

    def test_store_creation(self):
        """Test that a store can be created with required fields"""
        self.assertEqual(self.store.name, 'Test Store')
        self.assertEqual(self.store.owner, self.user)
        self.assertEqual(self.store.theme_name, 'minimal')
        self.assertEqual(self.store.primary_color, '#3b82f6')
        self.assertEqual(self.store.font_choice, 'sans')

    def test_store_string_representation(self):
        """Test the string representation of a store"""
        self.assertEqual(str(self.store), 'Test Store')

    def test_slug_generation(self):
        """Test that slug is automatically generated from name"""
        self.assertEqual(self.store.slug, 'test-store')

    def test_custom_slug(self):
        """Test that a custom slug can be provided"""
        store = Store.objects.create(
            name='Another Store',
            slug='custom-slug',
            owner=self.user
        )
        self.assertEqual(store.slug, 'custom-slug')