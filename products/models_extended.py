from django.db import models
from django.utils.text import slugify
from .models import Product
from .qr_utils import QRCodeGenerator


class ProductVariant(models.Model):
    """Model for product variants (size, color, etc.)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)  # e.g., "Large Red", "Size M"
    sku = models.CharField(max_length=50, unique=True, blank=True)
    
    # Variant attributes
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=30, blank=True)
    material = models.CharField(max_length=50, blank=True)
    
    # Pricing and inventory
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.PositiveIntegerField(default=0)
    
    # Images
    image = models.ImageField(upload_to='product_variants/', blank=True, null=True)
    
    # QR codes for different sizes
    qr_code_small = models.CharField(max_length=200, blank=True)
    qr_code_medium = models.CharField(max_length=200, blank=True)
    qr_code_large = models.CharField(max_length=200, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('product', 'name')
    
    def __str__(self):
        return f"{self.product.title} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"{self.product.slug}-{slugify(self.name)}"
        super().save(*args, **kwargs)
        
        # Generate QR codes after saving
        self.generate_qr_codes()
    
    def generate_qr_codes(self):
        """Generate QR codes for this variant in different sizes"""
        self.qr_code_small = QRCodeGenerator.generate_product_qr(self.product, self, 'small')
        self.qr_code_medium = QRCodeGenerator.generate_product_qr(self.product, self, 'medium')
        self.qr_code_large = QRCodeGenerator.generate_product_qr(self.product, self, 'large')
        
        # Update without triggering save recursion
        ProductVariant.objects.filter(id=self.id).update(
            qr_code_small=self.qr_code_small,
            qr_code_medium=self.qr_code_medium,
            qr_code_large=self.qr_code_large
        )
    
    @property
    def final_price(self):
        """Calculate final price including adjustment"""
        return self.product.price + self.price_adjustment
    
    def get_qr_code(self, size='medium'):
        """Get QR code for specified size"""
        qr_codes = {
            'small': self.qr_code_small,
            'medium': self.qr_code_medium,
            'large': self.qr_code_large
        }
        return qr_codes.get(size, self.qr_code_medium)


# Extend the existing Product model
class ProductExtended(Product):
    """Extended Product model with QR code functionality"""
    
    # QR codes for different sizes
    qr_code_small = models.CharField(max_length=200, blank=True)
    qr_code_medium = models.CharField(max_length=200, blank=True)
    qr_code_large = models.CharField(max_length=200, blank=True)
    
    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_qr_codes()
    
    def generate_qr_codes(self):
        """Generate QR codes for this product in different sizes"""
        self.qr_code_small = QRCodeGenerator.generate_product_qr(self, size='small')
        self.qr_code_medium = QRCodeGenerator.generate_product_qr(self, size='medium')
        self.qr_code_large = QRCodeGenerator.generate_product_qr(self, size='large')
        
        # Update without triggering save recursion
        Product.objects.filter(id=self.id).update(
            qr_code_small=self.qr_code_small,
            qr_code_medium=self.qr_code_medium,
            qr_code_large=self.qr_code_large
        )
    
    def get_qr_code(self, size='medium'):
        """Get QR code for specified size"""
        qr_codes = {
            'small': self.qr_code_small,
            'medium': self.qr_code_medium,
            'large': self.qr_code_large
        }
        return qr_codes.get(size, self.qr_code_medium)
    
    @property
    def has_variants(self):
        """Check if product has variants"""
        return hasattr(self, 'variants') and self.variants.exists()
    
    def get_variant_by_attributes(self, **attributes):
        """Get variant by attributes like size, color"""
        if not self.has_variants:
            return None
        
        queryset = self.variants.all()
        for attr, value in attributes.items():
            if hasattr(ProductVariant, attr):
                queryset = queryset.filter(**{attr: value})
        
        return queryset.first()


class VariantAttribute(models.Model):
    """Model for defining variant attribute types"""
    name = models.CharField(max_length=50, unique=True)  # e.g., "Size", "Color"
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class VariantAttributeValue(models.Model):
    """Model for variant attribute values"""
    attribute = models.ForeignKey(VariantAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=100)  # e.g., "Large", "Red"
    slug = models.SlugField()
    
    class Meta:
        unique_together = ('attribute', 'value')
    
    def __str__(self):
        return f"{self.attribute.name}: {self.value}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.value)
        super().save(*args, **kwargs)