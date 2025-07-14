from django.db import models
from django.utils.text import slugify
from stores.models import Store

class TagType(models.Model):
    """Model for different types of tags (e.g., Occasion, Lifestyle, Festival)"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    """Model for individual tags within a tag type"""
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    tag_type = models.ForeignKey(TagType, on_delete=models.CASCADE, related_name='tags')
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ('slug', 'tag_type')
    
    def __str__(self):
        return f"{self.name} ({self.tag_type.name})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/collections/{self.tag_type.slug}/{self.slug}/"

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_catalog')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Bundle(models.Model):
    """Model for product bundles"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    products = models.ManyToManyField(Product, through='BundleItem')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='bundle_images/', blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='bundles')
    tags = models.ManyToManyField(Tag, blank=True, related_name='bundles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    @property
    def available_stock(self):
        """Returns the maximum number of bundles that can be created based on product stock"""
        if not hasattr(self, '_available_stock'):
            bundle_items = self.bundleitem_set.all()
            if not bundle_items:
                self._available_stock = 0
            else:
                # Find the limiting product
                self._available_stock = min(
                    item.product.stock_quantity // item.quantity 
                    for item in bundle_items
                )
        return self._available_stock

class BundleItem(models.Model):
    """Model for items in a bundle with quantity"""
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ('bundle', 'product')
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title} in {self.bundle.name}"

class StaticPage(models.Model):
    """Model for static pages like About, FAQ, etc."""
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='static_pages')
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return f"/stores/{self.store.slug}/pages/{self.slug}/"

class TrustBadge(models.Model):
    """Model for trust badges"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to='trust_badges/')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='trust_badges')
    
    def __str__(self):
        return self.name

class ContactForm(models.Model):
    """Model for contact/inquiry forms"""
    title = models.CharField(max_length=100)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='contact_forms')
    email_to = models.EmailField()
    success_message = models.TextField(default="Thank you for your message. We'll get back to you soon.")
    show_phone = models.BooleanField(default=True)
    show_subject = models.BooleanField(default=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    newsletter_integration = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} - {self.store.name}"

class ProductView(models.Model):
    """Model for tracking product views for analytics"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='view_records')
    session_id = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['product', 'timestamp']),
            models.Index(fields=['session_id', 'product']),
        ]
    
    def __str__(self):
        return f"View of {self.product.title} at {self.timestamp}"