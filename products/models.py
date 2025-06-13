from django.db import models
from django.urls import reverse
import segno
from stores.models import Store
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
    stock = models.PositiveIntegerField(default=100)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})
    
    def is_new(self):
        """Return True if product was created within the last 7 days"""
        return self.created_at >= (timezone.now() - timedelta(days=7))
    
    def is_limited(self):
        """Return True if product stock is 5 or less"""
        return self.stock <= 5
    
    def is_bestseller(self):
        """Return True if product is in top 3 most ordered this month"""
        # This would typically query the Order model to check
        # For now, we'll use a placeholder implementation
        from orders.models import Order
        
        # Get the first day of the current month
        first_day = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Get top 3 products by order count this month
        top_products = Order.objects.filter(
            created_at__gte=first_day,
            status='completed'
        ).values('product').annotate(
            order_count=Count('id')
        ).order_by('-order_count')[:3]
        
        # Check if this product is in the top 3
        return any(item['product'] == self.id for item in top_products)

    def save(self, *args, **kwargs):
        # First save to get an ID if it's a new product
        super().save(*args, **kwargs)

        # Generate QR code if it doesn't exist
        if not self.qr_code:
            import os
            from django.conf import settings

            product_url = f"/products/{self.id}/"
            qr = segno.make(product_url)
            qr_path = f"qrcodes/product_{self.id}.png"

            # Create directory if it doesn't exist
            media_dir = os.path.join(settings.BASE_DIR, "media", "qrcodes")
            os.makedirs(media_dir, exist_ok=True)

            # Use absolute path
            file_path = os.path.join(settings.BASE_DIR, "media", qr_path)
            qr.save(file_path, scale=5)
            self.qr_code = qr_path
            super().save(update_fields=["qr_code"])