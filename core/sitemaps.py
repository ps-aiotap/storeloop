from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from stores.models import Store
from products.models import Product, Tag, StaticPage


class StoreSitemap(Sitemap):
    """Sitemap for store pages"""
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Store.objects.all()
    
    def location(self, obj):
        return f'/stores/{obj.slug}/'
    
    def lastmod(self, obj):
        # Use the most recent product update as lastmod
        latest_product = obj.products.order_by('-updated_at').first()
        if latest_product:
            return latest_product.updated_at
        return timezone.now()


class ProductSitemap(Sitemap):
    """Sitemap for product pages"""
    changefreq = 'daily'
    priority = 0.9
    
    def items(self):
        return Product.objects.select_related('store').all()
    
    def location(self, obj):
        return f'/stores/{obj.store.slug}/products/{obj.slug}/'
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def priority(self, obj):
        # Higher priority for recently updated or popular products
        if obj.updated_at > timezone.now() - timedelta(days=7):
            return 1.0
        elif obj.views > 100:
            return 0.9
        return 0.7


class TagCollectionSitemap(Sitemap):
    """Sitemap for tag collection pages"""
    changefreq = 'weekly'
    priority = 0.6
    
    def items(self):
        return Tag.objects.select_related('tag_type').all()
    
    def location(self, obj):
        return f'/collections/{obj.tag_type.slug}/{obj.slug}/'
    
    def lastmod(self, obj):
        # Use the most recent product with this tag
        latest_product = obj.products.order_by('-updated_at').first()
        if latest_product:
            return latest_product.updated_at
        return timezone.now()


class StaticPageSitemap(Sitemap):
    """Sitemap for static pages"""
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self):
        return StaticPage.objects.filter(is_published=True).select_related('store')
    
    def location(self, obj):
        return f'/stores/{obj.store.slug}/pages/{obj.slug}/'
    
    def lastmod(self, obj):
        return obj.updated_at


class HomepageSitemap(Sitemap):
    """Sitemap for store homepages"""
    changefreq = 'daily'
    priority = 1.0
    
    def items(self):
        return Store.objects.all()
    
    def location(self, obj):
        return f'/stores/{obj.slug}/'
    
    def lastmod(self, obj):
        # Use the most recent homepage block update or product update
        latest_product = obj.products.order_by('-updated_at').first()
        latest_block = obj.homepage_blocks.order_by('-id').first()
        
        dates = []
        if latest_product:
            dates.append(latest_product.updated_at)
        if latest_block:
            dates.append(latest_block.id)  # Use ID as proxy for creation time
        
        return max(dates) if dates else timezone.now()


# Sitemap index
sitemaps = {
    'stores': StoreSitemap,
    'products': ProductSitemap,
    'collections': TagCollectionSitemap,
    'pages': StaticPageSitemap,
    'homepages': HomepageSitemap,
}