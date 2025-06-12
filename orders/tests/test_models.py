import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from products.models import Product
from orders.models import Order
from stores.models import Store

@pytest.mark.django_db
class TestOrderModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
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
        self.order = Order.objects.create(
            product=self.product,
            user=self.user,
            amount=9999,  # Amount in paise (99.99 INR)
            payment_id='test_payment_123',
            razorpay_order_id='order_123456',
            status='pending'
        )

    def test_order_creation(self):
        """Test that an order can be created with required fields"""
        self.assertEqual(self.order.product, self.product)
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.amount, 9999)
        self.assertEqual(self.order.payment_id, 'test_payment_123')
        self.assertEqual(self.order.razorpay_order_id, 'order_123456')
        self.assertEqual(self.order.status, 'pending')

    def test_order_string_representation(self):
        """Test the string representation of an order"""
        expected_str = f'Order {self.order.id} - {self.user.username} - {self.product.title}'
        self.assertEqual(str(self.order), expected_str)

    def test_order_status_update(self):
        """Test updating order status"""
        self.order.status = 'completed'
        self.order.save()
        updated_order = Order.objects.get(id=self.order.id)
        self.assertEqual(updated_order.status, 'completed')