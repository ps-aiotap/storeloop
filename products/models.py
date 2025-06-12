from django.db import models
from django.urls import reverse
import segno
from stores.models import Store


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

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


# Removed Seller model as it's replaced by Store model in stores app
