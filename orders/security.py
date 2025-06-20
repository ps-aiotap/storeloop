import hmac
import hashlib
import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import razorpay
from decimal import Decimal

logger = logging.getLogger(__name__)


class RazorpaySecurityValidator:
    """Security validation for Razorpay payments"""
    
    def __init__(self):
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
    
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        """Verify Razorpay payment signature for authenticity"""
        try:
            # Create the signature verification string
            message = f"{razorpay_order_id}|{razorpay_payment_id}"
            
            # Generate expected signature
            expected_signature = hmac.new(
                settings.RAZORPAY_KEY_SECRET.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            # Compare signatures
            if not hmac.compare_digest(expected_signature, razorpay_signature):
                logger.warning(f"Invalid payment signature for order {razorpay_order_id}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error verifying payment signature: {str(e)}")
            return False
    
    def verify_webhook_signature(self, payload, signature):
        """Verify Razorpay webhook signature"""
        try:
            webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', '')
            if not webhook_secret:
                logger.error("Razorpay webhook secret not configured")
                return False
            
            expected_signature = hmac.new(
                webhook_secret.encode('utf-8'),
                payload.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, signature)
            
        except Exception as e:
            logger.error(f"Error verifying webhook signature: {str(e)}")
            return False
    
    def validate_payment_amount(self, order_amount, razorpay_amount):
        """Validate payment amount matches order amount"""
        try:
            # Convert to same units (paise)
            order_amount_paise = int(order_amount * 100)
            
            if order_amount_paise != razorpay_amount:
                logger.warning(f"Amount mismatch: Order {order_amount_paise}, Payment {razorpay_amount}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating payment amount: {str(e)}")
            return False
    
    def fetch_and_verify_payment(self, payment_id):
        """Fetch payment details from Razorpay and verify"""
        try:
            payment = self.client.payment.fetch(payment_id)
            
            # Check payment status
            if payment['status'] != 'captured':
                logger.warning(f"Payment {payment_id} not captured: {payment['status']}")
                return None
            
            # Check payment method is allowed
            allowed_methods = getattr(settings, 'RAZORPAY_ALLOWED_METHODS', [
                'card', 'netbanking', 'wallet', 'upi'
            ])
            
            if payment['method'] not in allowed_methods:
                logger.warning(f"Payment method {payment['method']} not allowed")
                return None
            
            return payment
            
        except Exception as e:
            logger.error(f"Error fetching payment {payment_id}: {str(e)}")
            return None
    
    def validate_order_creation_data(self, order_data):
        """Validate order creation data before sending to Razorpay"""
        errors = []
        
        # Validate amount
        if 'amount' not in order_data or order_data['amount'] <= 0:
            errors.append("Invalid amount")
        
        # Validate currency
        if order_data.get('currency') != 'INR':
            errors.append("Only INR currency supported")
        
        # Validate customer details
        if not order_data.get('notes', {}).get('customer_email'):
            errors.append("Customer email required")
        
        # Validate amount limits
        min_amount = getattr(settings, 'RAZORPAY_MIN_AMOUNT', 100)  # 1 INR
        max_amount = getattr(settings, 'RAZORPAY_MAX_AMOUNT', 10000000)  # 100,000 INR
        
        if order_data['amount'] < min_amount:
            errors.append(f"Amount below minimum limit of ₹{min_amount/100}")
        
        if order_data['amount'] > max_amount:
            errors.append(f"Amount exceeds maximum limit of ₹{max_amount/100}")
        
        if errors:
            raise ValidationError(errors)
        
        return True


class CheckoutSecurityValidator:
    """Security validation for checkout process"""
    
    @staticmethod
    def validate_customer_data(customer_data):
        """Validate customer data for security"""
        errors = []
        
        # Email validation
        email = customer_data.get('email', '').strip()
        if not email or '@' not in email:
            errors.append("Valid email required")
        
        # Phone validation
        phone = customer_data.get('phone', '').strip()
        if phone and not phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            errors.append("Invalid phone number format")
        
        # Name validation
        name = customer_data.get('name', '').strip()
        if not name or len(name) < 2:
            errors.append("Valid name required")
        
        # Address validation
        address = customer_data.get('address', '').strip()
        if not address or len(address) < 10:
            errors.append("Complete address required")
        
        if errors:
            raise ValidationError(errors)
        
        return True
    
    @staticmethod
    def validate_cart_integrity(cart_items, products):
        """Validate cart items against actual product data"""
        errors = []
        
        for item in cart_items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            price = item.get('price', 0)
            
            # Find corresponding product
            product = next((p for p in products if p.id == product_id), None)
            if not product:
                errors.append(f"Product {product_id} not found")
                continue
            
            # Validate price
            if abs(float(product.price) - float(price)) > 0.01:
                errors.append(f"Price mismatch for product {product.title}")
            
            # Validate stock
            if quantity > product.stock_quantity:
                errors.append(f"Insufficient stock for {product.title}")
            
            # Validate quantity
            if quantity <= 0:
                errors.append(f"Invalid quantity for {product.title}")
        
        if errors:
            raise ValidationError(errors)
        
        return True
    
    @staticmethod
    def check_rate_limiting(request, max_attempts=5, window_minutes=15):
        """Check for rate limiting on checkout attempts"""
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        
        cache_key = f"checkout_attempts_{session_key}"
        
        from django.core.cache import cache
        attempts = cache.get(cache_key, [])
        
        # Remove old attempts outside the window
        cutoff_time = timezone.now() - timedelta(minutes=window_minutes)
        attempts = [attempt for attempt in attempts if attempt > cutoff_time]
        
        if len(attempts) >= max_attempts:
            logger.warning(f"Rate limit exceeded for session {session_key}")
            raise ValidationError("Too many checkout attempts. Please try again later.")
        
        # Add current attempt
        attempts.append(timezone.now())
        cache.set(cache_key, attempts, timeout=window_minutes * 60)
        
        return True
    
    @staticmethod
    def validate_session_integrity(request):
        """Validate session integrity"""
        # Check session age
        session_age = timezone.now() - request.session.get('created_at', timezone.now())
        max_session_age = timedelta(hours=24)
        
        if session_age > max_session_age:
            logger.warning("Session too old, clearing cart")
            request.session.flush()
            raise ValidationError("Session expired. Please refresh and try again.")
        
        return True


class PaymentSecurityMiddleware:
    """Middleware for payment security checks"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add security headers for payment pages
        if '/checkout/' in request.path or '/payment/' in request.path:
            response = self.get_response(request)
            
            # Add security headers
            response['X-Frame-Options'] = 'DENY'
            response['X-Content-Type-Options'] = 'nosniff'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            response['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' checkout.razorpay.com; "
                "style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data: https:; "
                "connect-src 'self' api.razorpay.com;"
            )
            
            return response
        
        return self.get_response(request)


# Utility functions for secure payment processing
def create_secure_order(order_data):
    """Create Razorpay order with security validations"""
    validator = RazorpaySecurityValidator()
    
    # Validate order data
    validator.validate_order_creation_data(order_data)
    
    try:
        # Create order with Razorpay
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        razorpay_order = client.order.create(order_data)
        
        # Log order creation
        logger.info(f"Razorpay order created: {razorpay_order['id']}")
        
        return razorpay_order
        
    except Exception as e:
        logger.error(f"Error creating Razorpay order: {str(e)}")
        raise ValidationError("Failed to create payment order")


def verify_payment_completion(payment_data):
    """Verify payment completion with all security checks"""
    validator = RazorpaySecurityValidator()
    
    # Extract payment details
    razorpay_order_id = payment_data.get('razorpay_order_id')
    razorpay_payment_id = payment_data.get('razorpay_payment_id')
    razorpay_signature = payment_data.get('razorpay_signature')
    
    if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
        raise ValidationError("Missing payment verification data")
    
    # Verify signature
    if not validator.verify_payment_signature(
        razorpay_order_id, razorpay_payment_id, razorpay_signature
    ):
        raise ValidationError("Invalid payment signature")
    
    # Fetch and verify payment from Razorpay
    payment = validator.fetch_and_verify_payment(razorpay_payment_id)
    if not payment:
        raise ValidationError("Payment verification failed")
    
    return payment