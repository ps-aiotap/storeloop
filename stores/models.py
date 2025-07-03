from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
import re
import unicodedata

class Store(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stores')
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    theme = models.CharField(max_length=50, default='minimal')
    primary_color = models.CharField(max_length=7, default='#3B82F6')
    secondary_color = models.CharField(max_length=7, default='#10B981')
    font_family = models.CharField(max_length=50, default='sans-serif')
    custom_domain = models.CharField(max_length=200, blank=True, null=True)
    subdomain = models.CharField(max_length=100, unique=True, blank=True)
    razorpay_key_id = models.CharField(max_length=100, blank=True)
    razorpay_key_secret = models.CharField(max_length=100, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    business_address = models.TextField(blank=True)
    onboarding_completed = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Handle Hindi and other non-ASCII characters
            if self.name:
                # First try standard slugify
                base_slug = slugify(self.name)
                
                # If empty (happens with non-ASCII), create transliterated version
                if not base_slug:
                    # Remove diacritics and convert to ASCII
                    normalized = unicodedata.normalize('NFD', self.name)
                    ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
                    
                    # If still no ASCII, use a generic approach
                    if not ascii_name or not ascii_name.strip():
                        # Create slug from first few characters or use store + timestamp
                        import time
                        base_slug = f'store-{int(time.time())}'[-10:]
                    else:
                        base_slug = slugify(ascii_name)
                        
                # Final fallback
                if not base_slug:
                    import time
                    base_slug = f'store-{int(time.time())}'[-10:]
            else:
                base_slug = 'store'
            
            slug = base_slug
            counter = 1
            
            # Ensure unique slug
            while Store.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
            
        if not self.subdomain:
            self.subdomain = self.slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    language_preference = models.CharField(max_length=10, choices=[('en', 'English'), ('hi', 'Hindi')], default='en')
    whatsapp_number = models.CharField(max_length=15, blank=True)
    is_partner_admin = models.BooleanField(default=False)
    managed_stores = models.ManyToManyField(Store, blank=True, related_name='partner_admins')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user.get_full_name()}"

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_products')
    name = models.CharField(max_length=200)  # Supports Unicode/Hindi text
    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)  # Supports Unicode/Hindi text
    short_description = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True)
    material = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    style = models.CharField(max_length=100, blank=True)
    ai_generated_description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        # Ensure proper Unicode handling
        db_table = 'stores_product'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['store', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            # Handle Hindi and other non-ASCII characters
            if self.name:
                # First try standard slugify
                base_slug = slugify(self.name)
                
                # If empty (happens with non-ASCII), create transliterated version
                if not base_slug:
                    # Try to transliterate Hindi/Devanagari to Latin
                    try:
                        # Simple transliteration for common Hindi characters
                        transliteration_map = {
                            'बनारसी': 'banarasi',
                            'सिल्क': 'silk', 
                            'साड़ी': 'saree',
                            'कशीदाकारी': 'kashidakari',
                            'शाल': 'shawl',
                            'दीया': 'diya',
                            'मिट्टी': 'mitti'
                        }
                        
                        transliterated = self.name
                        for hindi, english in transliteration_map.items():
                            transliterated = transliterated.replace(hindi, english)
                        
                        base_slug = slugify(transliterated)
                        
                        # If still empty, use generic approach
                        if not base_slug:
                            # Remove diacritics and convert to ASCII
                            normalized = unicodedata.normalize('NFD', self.name)
                            ascii_name = ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')
                            
                            if ascii_name and ascii_name.strip():
                                base_slug = slugify(ascii_name)
                    except:
                        pass
                        
                # Final fallback
                if not base_slug:
                    import time
                    base_slug = f'product-{int(time.time())}'[-10:]
                
                # Ensure unique slug
                slug = base_slug
                counter = 1
                while Product.objects.filter(slug=slug, store=self.store).exclude(pk=self.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        # Ensure proper Unicode display
        return f"{self.name} - {self.store.name}"
    
    def get_display_name(self):
        """Get display name with proper Unicode handling"""
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    delivery_address = models.ForeignKey('UserAddress', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gst_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    whatsapp_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - {self.store.name}"

class ProductUploadBatch(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    total_rows = models.PositiveIntegerField(default=0)
    successful_imports = models.PositiveIntegerField(default=0)
    failed_imports = models.PositiveIntegerField(default=0)
    errors = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=[
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], default='processing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload {self.id} - {self.store.name}"

class Customer(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.phone}"

class UserAddress(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    landmark = models.CharField(max_length=200, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.street}, {self.city}"

class PartnerStoreAccess(models.Model):
    """Partner-Store relationship with access levels"""
    ACCESS_LEVELS = [
        ('view', 'View Only'),
        ('manage', 'Full Management'),
    ]
    
    partner = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=10, choices=ACCESS_LEVELS, default='manage')
    granted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('partner', 'store')
    
    def __str__(self):
        return f"{self.partner.username} -> {self.store.name} ({self.access_level})"

class StoreHomepageBlock(models.Model):
    BLOCK_TYPES = [
        ('hero_banner', 'Hero Banner'),
        ('featured_products', 'Featured Products'),
        ('text_block', 'Text Block'),
        ('testimonials', 'Testimonials'),
        ('contact_form', 'Contact Form'),
        ('image_gallery', 'Image Gallery'),
    ]
    
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='homepage_blocks')
    block_type = models.CharField(max_length=20, choices=BLOCK_TYPES)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    configuration = models.JSONField(default=dict)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['store', 'block_type', 'order']
    
    def __str__(self):
        return f"{self.store.name} - {self.get_block_type_display()}"