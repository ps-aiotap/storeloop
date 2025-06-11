from django.test import TestCase
from django.urls import reverse
from products.models import Product
from .models import Order, OrderItem

class OrderModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Test Product",
            description="This is a test product",
            price=99.99
        )
        
        self.order = Order.objects.create(
            customer_name="Test Customer",
            customer_email="test@example.com",
            customer_phone="1234567890",
            shipping_address="123 Test Street",
            status="pending",
            total_amount=99.99
        )
        
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=99.99
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.customer_name, "Test Customer")
        self.assertEqual(self.order.customer_email, "test@example.com")
        self.assertEqual(self.order.status, "pending")
        self.assertEqual(self.order.total_amount, 99.99)
    
    def test_order_str(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} - Test Customer")
    
    def test_order_item_creation(self):
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 1)
        self.assertEqual(self.order_item.price, 99.99)
    
    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), "1 x Test Product")
    
    def test_get_total_price(self):
        self.assertEqual(self.order_item.get_total_price(), 99.99)