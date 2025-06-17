from django.db import models
from django.utils.text import slugify
import json

class BaseTheme(models.Model):
    """Base theme model that can be extended by child themes"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # Theme components
    layout_template = models.CharField(max_length=100, default='base.html')
    header_template = models.CharField(max_length=100, default='components/header.html')
    footer_template = models.CharField(max_length=100, default='components/footer.html')
    
    # Default colors
    primary_color = models.CharField(max_length=20, default='#3b82f6')
    secondary_color = models.CharField(max_length=20, default='#1f2937')
    background_color = models.CharField(max_length=20, default='#f3f4f6')
    text_color = models.CharField(max_length=20, default='#1f2937')
    
    # Default fonts
    font_choice = models.CharField(max_length=20, default='sans', choices=[
        ('sans', 'Sans-serif'),
        ('serif', 'Serif'),
        ('mono', 'Monospace'),
    ])
    
    # Default CSS/JS
    base_css = models.TextField(blank=True)
    base_js = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Store(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='stores')
    description = models.TextField(blank=True)
    
    # Theme settings
    base_theme = models.ForeignKey(BaseTheme, on_delete=models.SET_NULL, null=True, blank=True)
    theme_name = models.CharField(max_length=50, default='minimal', choices=[
        ('minimal', 'Minimal'),
        ('dark', 'Dark'),
        ('warm', 'Warm'),
    ])
    theme_version = models.CharField(max_length=10, default='v1')
    primary_color = models.CharField(max_length=20, default='#3b82f6')
    secondary_color = models.CharField(max_length=20, default='#1f2937')
    font_choice = models.CharField(max_length=20, default='sans', choices=[
        ('sans', 'Sans-serif'),
        ('serif', 'Serif'),
        ('mono', 'Monospace'),
    ])
    logo_url = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    custom_css = models.TextField(blank=True, default='')
    custom_js = models.TextField(blank=True, default='')
    
    # Theme overrides
    override_header = models.BooleanField(default=False)
    override_footer = models.BooleanField(default=False)
    header_template = models.CharField(max_length=100, blank=True)
    footer_template = models.CharField(max_length=100, blank=True)
    
    # Homepage layout configuration
    homepage_layout = models.TextField(blank=True, default='[]')
    
    # Analytics settings
    google_analytics_id = models.CharField(max_length=20, blank=True)
    facebook_pixel_id = models.CharField(max_length=20, blank=True)
    
    # Contact information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    # Social media links
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    
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
    
    def get_theme_settings(self):
        """Get effective theme settings, inheriting from base theme if needed"""
        settings = {
            'name': self.name,
            'theme_name': self.theme_name,
            'theme_version': self.theme_version,
            'primary_color': self.primary_color,
            'secondary_color': self.secondary_color,
            'font_choice': self.font_choice,
            'logo_url': self.logo_url.url if self.logo_url else None,
            'custom_css': self.custom_css,
            'custom_js': self.custom_js,
        }
        
        # Inherit from base theme if available
        if self.base_theme:
            # Layout templates
            if not self.override_header:
                settings['header_template'] = self.base_theme.header_template
            else:
                settings['header_template'] = self.header_template or self.base_theme.header_template
                
            if not self.override_footer:
                settings['footer_template'] = self.base_theme.footer_template
            else:
                settings['footer_template'] = self.footer_template or self.base_theme.footer_template
            
            # Add base CSS/JS
            settings['base_css'] = self.base_theme.base_css
            settings['base_js'] = self.base_theme.base_js
        
        return settings


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
        ('trust_badges', 'Trust Badges'),
        ('contact_form', 'Contact Form'),
        ('tag_collection', 'Tag Collection'),
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
        ('trust_badges', 'Trust Badges'),
        ('contact_form', 'Contact Form'),
        ('tag_collection', 'Tag Collection'),
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