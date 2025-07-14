import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order
from stores.models import Store
from unittest.mock import patch, MagicMock

@pytest.mark.django_db
class TestRazorpayIntegration(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.store = Store.objects.create(
            name='Test Store',
            slug='test-store',
            owner=self.user
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=99.99,
            store=self.store
        )

    @patch('orders.views.razorpay.Client')
    def test_create_order(self, mock_razorpay_client):
        """Test creating an order with Razorpay"""
        # Mock Razorpay client
        mock_client_instance = MagicMock()
        mock_razorpay_client.return_value = mock_client_instance
        
        # Mock order creation response
        mock_client_instance.order.create.return_value = {
            'id': 'order_123456',
            'amount': 9999,
            'currency': 'INR'
        }
        
        # Make request to create order
        url = reverse('create_order', args=[self.product.id])
        response = self.client.post(url)
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertIn('razorpay_order_id', response.json())
        self.assertEqual(response.json()['razorpay_order_id'], 'order_123456')
        
        # Check order was created in database
        order = Order.objects.filter(product=self.product, user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.amount, 9999)
        self.assertEqual(order.status, 'pending')

    @patch('orders.views.razorpay.Client')
    def test_payment_success_callback(self, mock_razorpay_client):
        """Test successful payment callback from Razorpay"""
        # Create order first
        order = Order.objects.create(
            product=self.product,
            user=self.user,
            amount=9999,
            razorpay_order_id='order_123456',
            status='pending'
        )
        
        # Mock Razorpay client
        mock_client_instance = MagicMock()
        mock_razorpay_client.return_value = mock_client_instance
        
        # Mock signature verification
        mock_client_instance.utility.verify_payment_signature.return_value = True
        
        # Make request to payment success endpoint
        url = reverse('payment_success')
        data = {
            'razorpay_payment_id': 'pay_123456',
            'razorpay_order_id': 'order_123456',
            'razorpay_signature': 'valid_signature'
        }
        response = self.client.post(url, data)
        
        # Check response
        self.assertEqual(response.status_code, 302)  # Redirect to confirmation page
        
        # Check order was updated
        order.refresh_from_db()
        self.assertEqual(order.status, 'completed')
        self.assertEqual(order.payment_id, 'pay_123456')