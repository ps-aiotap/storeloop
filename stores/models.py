from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Store(models.Model):
    THEME_CHOICES = [
        ('minimal', 'Minimal'),
        ('warm', 'Warm'),
        ('dark', 'Dark'),
    ]
    
    FONT_CHOICES = [
        ('sans', 'Sans-serif'),
        ('serif', 'Serif'),
        ('mono', 'Monospace'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    description = models.TextField(blank=True, null=True)
    
    # Theme settings
    theme_name = models.CharField(max_length=20, choices=THEME_CHOICES, default='minimal')
    primary_color = models.CharField(max_length=20, default='blue')
    font_choice = models.CharField(max_length=20, choices=FONT_CHOICES, default='sans')
    logo = models.ImageField(upload_to='store_logos/', blank=True, null=True)
    
    # Custom code injection
    custom_css = models.TextField(blank=True, null=True, help_text="Custom CSS to be injected into store pages")
    custom_js = models.TextField(blank=True, null=True, help_text="Custom JavaScript to be injected into store pages")
    
    # Theme version tracking
    theme_version = models.CharField(max_length=10, default='v1', help_text="Theme version to use for this store")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)