from django.test import TestCase
from django.urls import reverse
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Test Product",
            description="This is a test product",
            price=99.99
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.title, "Test Product")
        self.assertEqual(self.product.description, "This is a test product")
        self.assertEqual(self.product.price, 99.99)
    
    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")
    
    def test_get_absolute_url(self):
        url = self.product.get_absolute_url()
        self.assertEqual(url, f'/products/{self.product.id}/')

class ProductViewTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Test Product",
            description="This is a test product",
            price=99.99
        )
    
    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertTemplateUsed(response, 'products/product_list.html')
    
    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Product")
        self.assertContains(response, "This is a test product")
        self.assertTemplateUsed(response, 'products/product_detail.html')