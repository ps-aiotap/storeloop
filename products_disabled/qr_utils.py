import qrcode
import os
from django.conf import settings
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image


class QRCodeGenerator:
    """Optimized QR code generator for products and variants"""
    
    @staticmethod
    def generate_product_qr(product, variant=None, size='medium'):
        """Generate QR code for product or variant with caching"""
        # Determine URL and filename
        if variant:
            url = f"{settings.SITE_URL}/products/{product.slug}/?variant={variant.id}"
            filename = f"product_{product.id}_variant_{variant.id}_{size}.png"
        else:
            url = f"{settings.SITE_URL}/products/{product.slug}/"
            filename = f"product_{product.id}_{size}.png"
        
        # Check if QR code already exists
        qr_path = os.path.join('qrcodes', filename)
        full_path = os.path.join(settings.MEDIA_ROOT, qr_path)
        
        if os.path.exists(full_path):
            return qr_path
        
        # Generate QR code
        qr_sizes = {
            'small': (150, 150),
            'medium': (300, 300),
            'large': (600, 600)
        }
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize(qr_sizes.get(size, qr_sizes['medium']), Image.Resampling.LANCZOS)
        
        # Save to media directory
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        img.save(full_path, 'PNG')
        
        return qr_path
    
    @staticmethod
    def generate_batch_qr_codes(products, sizes=['medium']):
        """Generate QR codes for multiple products in batch"""
        results = {}
        
        for product in products:
            product_qrs = {}
            
            # Generate for main product
            for size in sizes:
                qr_path = QRCodeGenerator.generate_product_qr(product, size=size)
                product_qrs[f'main_{size}'] = qr_path
            
            # Generate for variants if they exist
            if hasattr(product, 'variants') and product.variants.exists():
                for variant in product.variants.all():
                    for size in sizes:
                        qr_path = QRCodeGenerator.generate_product_qr(product, variant, size)
                        product_qrs[f'variant_{variant.id}_{size}'] = qr_path
            
            results[product.id] = product_qrs
        
        return results
    
    @staticmethod
    def cleanup_old_qr_codes(product):
        """Remove old QR codes when product is updated"""
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        if not os.path.exists(qr_dir):
            return
        
        # Find all QR codes for this product
        for filename in os.listdir(qr_dir):
            if filename.startswith(f'product_{product.id}_'):
                file_path = os.path.join(qr_dir, filename)
                try:
                    os.remove(file_path)
                except OSError:
                    pass