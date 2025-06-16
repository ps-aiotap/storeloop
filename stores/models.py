from django.db import models
from django.utils.text import slugify
import json

class Store(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='stores')
    description = models.TextField(blank=True)
    
    # Theme settings
    theme_name = models.CharField(max_length=50, default='minimal', choices=[
        ('minimal', 'Minimal'),
        ('dark', 'Dark'),
        ('warm', 'Warm'),
    ])
    theme_version = models.CharField(max_length=10, default='v1')
    primary_color = models.CharField(max_length=20, default='#3b82f6')
    font_choice = models.CharField(max_length=20, default='sans', choices=[
        ('sans', 'Sans-serif'),
        ('serif', 'Serif'),
        ('mono', 'Monospace'),
    ])
    logo_url = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    custom_css = models.TextField(blank=True)
    custom_js = models.TextField(blank=True)
    
    # Homepage layout configuration
    homepage_layout = models.TextField(blank=True, default='[]')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    def get_homepage_layout(self):
        """Returns the homepage layout as a Python list"""
        try:
            return json.loads(self.homepage_layout)
        except (json.JSONDecodeError, TypeError):
            return []
    
    def set_homepage_layout(self, layout):
        """Sets the homepage layout from a Python list"""
        self.homepage_layout = json.dumps(layout)
        self.save()


class HomepageBlock(models.Model):
    """Model to store predefined homepage blocks"""
    name = models.CharField(max_length=100)
    block_type = models.CharField(max_length=50, choices=[
        ('hero_banner', 'Hero Banner'),
        ('product_grid', 'Product Grid'),
        ('featured_products', 'Featured Products'),
        ('testimonials', 'Testimonials'),
        ('text_block', 'Text Block'),
        ('image_gallery', 'Image Gallery'),
        ('newsletter_signup', 'Newsletter Signup'),
        ('video_embed', 'Video Embed'),
    ])
    template_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.name} ({self.block_type})"


class StoreHomepageBlock(models.Model):
    """Model to store store-specific homepage block instances"""
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='homepage_blocks')
    block_type = models.CharField(max_length=50, choices=[
        ('hero_banner', 'Hero Banner'),
        ('product_grid', 'Product Grid'),
        ('featured_products', 'Featured Products'),
        ('testimonials', 'Testimonials'),
        ('text_block', 'Text Block'),
        ('image_gallery', 'Image Gallery'),
        ('newsletter_signup', 'Newsletter Signup'),
        ('video_embed', 'Video Embed'),
    ])
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    configuration = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.store.name} - {self.get_block_type_display()} ({self.order})"