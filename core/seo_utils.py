from django.conf import settings
from django.utils.html import format_html
from django.urls import reverse
from typing import Dict, List, Optional
import json


class SEOHelper:
    """Helper class for SEO optimization across the platform"""
    
    @staticmethod
    def generate_meta_tags(
        title: str,
        description: str,
        url: str,
        image: Optional[str] = None,
        article_author: Optional[str] = None,
        article_published_time: Optional[str] = None,
        article_modified_time: Optional[str] = None,
        product_price: Optional[str] = None,
        product_currency: Optional[str] = None,
        product_availability: Optional[str] = None
    ) -> str:
        """Generate comprehensive meta tags for SEO"""
        
        site_name = getattr(settings, 'SITE_NAME', 'StoreLoop')
        site_url = getattr(settings, 'SITE_URL', 'https://storeloop.com')
        
        # Ensure absolute URL
        if url and not url.startswith('http'):
            url = f"{site_url.rstrip('/')}{url}"
        
        # Ensure absolute image URL
        if image and not image.startswith('http'):
            image = f"{site_url.rstrip('/')}{image}"
        
        meta_tags = []
        
        # Basic meta tags
        meta_tags.extend([
            f'<title>{title}</title>',
            f'<meta name="description" content="{description}">',
            f'<meta name="robots" content="index, follow">',
            f'<link rel="canonical" href="{url}">',
        ])
        
        # Open Graph tags
        meta_tags.extend([
            f'<meta property="og:title" content="{title}">',
            f'<meta property="og:description" content="{description}">',
            f'<meta property="og:url" content="{url}">',
            f'<meta property="og:site_name" content="{site_name}">',
            f'<meta property="og:type" content="website">',
        ])
        
        if image:
            meta_tags.extend([
                f'<meta property="og:image" content="{image}">',
                f'<meta property="og:image:alt" content="{title}">',
            ])
        
        # Twitter Card tags
        meta_tags.extend([
            f'<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{title}">',
            f'<meta name="twitter:description" content="{description}">',
        ])
        
        if image:
            meta_tags.append(f'<meta name="twitter:image" content="{image}">')
        
        # Article-specific tags
        if article_author:
            meta_tags.extend([
                f'<meta property="article:author" content="{article_author}">',
                f'<meta name="author" content="{article_author}">',
            ])
        
        if article_published_time:
            meta_tags.append(f'<meta property="article:published_time" content="{article_published_time}">')
        
        if article_modified_time:
            meta_tags.append(f'<meta property="article:modified_time" content="{article_modified_time}">')
        
        # Product-specific tags
        if product_price and product_currency:
            meta_tags.extend([
                f'<meta property="product:price:amount" content="{product_price}">',
                f'<meta property="product:price:currency" content="{product_currency}">',
            ])
        
        if product_availability:
            meta_tags.append(f'<meta property="product:availability" content="{product_availability}">')
        
        return '\n'.join(meta_tags)
    
    @staticmethod
    def generate_structured_data(data_type: str, data: Dict) -> str:
        """Generate JSON-LD structured data"""
        
        base_data = {
            "@context": "https://schema.org",
            "@type": data_type
        }
        
        structured_data = {**base_data, **data}
        
        return format_html(
            '<script type="application/ld+json">{}</script>',
            json.dumps(structured_data, indent=2)
        )
    
    @staticmethod
    def generate_product_structured_data(product, store) -> str:
        """Generate structured data for products"""
        
        site_url = getattr(settings, 'SITE_URL', 'https://storeloop.com')
        
        data = {
            "name": product.title,
            "description": product.description,
            "image": f"{site_url}{product.image.url}" if product.image else None,
            "url": f"{site_url}/stores/{store.slug}/products/{product.slug}/",
            "sku": str(product.id),
            "brand": {
                "@type": "Brand",
                "name": store.name
            },
            "offers": {
                "@type": "Offer",
                "price": str(product.price),
                "priceCurrency": "INR",
                "availability": "https://schema.org/InStock" if product.stock_quantity > 0 else "https://schema.org/OutOfStock",
                "seller": {
                    "@type": "Organization",
                    "name": store.name
                }
            }
        }
        
        # Add aggregate rating if available
        if hasattr(product, 'reviews') and product.reviews.exists():
            avg_rating = product.reviews.aggregate(avg=models.Avg('rating'))['avg']
            review_count = product.reviews.count()
            
            if avg_rating:
                data["aggregateRating"] = {
                    "@type": "AggregateRating",
                    "ratingValue": str(round(avg_rating, 1)),
                    "reviewCount": str(review_count)
                }
        
        return SEOHelper.generate_structured_data("Product", data)
    
    @staticmethod
    def generate_store_structured_data(store) -> str:
        """Generate structured data for stores"""
        
        site_url = getattr(settings, 'SITE_URL', 'https://storeloop.com')
        
        data = {
            "name": store.name,
            "description": store.description,
            "url": f"{site_url}/stores/{store.slug}/",
            "logo": f"{site_url}{store.logo_url.url}" if store.logo_url else None,
            "sameAs": []
        }
        
        # Add social media links
        if store.facebook_url:
            data["sameAs"].append(store.facebook_url)
        if store.instagram_url:
            data["sameAs"].append(store.instagram_url)
        if store.twitter_url:
            data["sameAs"].append(store.twitter_url)
        
        # Add contact information
        if store.contact_email or store.contact_phone:
            data["contactPoint"] = {
                "@type": "ContactPoint",
                "contactType": "customer service"
            }
            
            if store.contact_email:
                data["contactPoint"]["email"] = store.contact_email
            if store.contact_phone:
                data["contactPoint"]["telephone"] = store.contact_phone
        
        return SEOHelper.generate_structured_data("Organization", data)
    
    @staticmethod
    def generate_breadcrumb_structured_data(breadcrumbs: List[Dict[str, str]]) -> str:
        """Generate breadcrumb structured data"""
        
        site_url = getattr(settings, 'SITE_URL', 'https://storeloop.com')
        
        items = []
        for i, crumb in enumerate(breadcrumbs, 1):
            url = crumb['url']
            if not url.startswith('http'):
                url = f"{site_url.rstrip('/')}{url}"
            
            items.append({
                "@type": "ListItem",
                "position": i,
                "name": crumb['name'],
                "item": url
            })
        
        data = {
            "itemListElement": items
        }
        
        return SEOHelper.generate_structured_data("BreadcrumbList", data)
    
    @staticmethod
    def generate_website_structured_data() -> str:
        """Generate website structured data"""
        
        site_name = getattr(settings, 'SITE_NAME', 'StoreLoop')
        site_url = getattr(settings, 'SITE_URL', 'https://storeloop.com')
        
        data = {
            "name": site_name,
            "url": site_url,
            "description": "Multi-store e-commerce platform for artisans and small businesses",
            "potentialAction": {
                "@type": "SearchAction",
                "target": f"{site_url}/search?q={{search_term_string}}",
                "query-input": "required name=search_term_string"
            }
        }
        
        return SEOHelper.generate_structured_data("WebSite", data)


def get_seo_context(request, page_type: str, **kwargs) -> Dict:
    """Get SEO context for templates"""
    
    context = {
        'seo_helper': SEOHelper,
        'page_type': page_type,
        'canonical_url': request.build_absolute_uri(),
    }
    
    # Add page-specific context
    if page_type == 'product' and 'product' in kwargs:
        product = kwargs['product']
        store = kwargs.get('store', product.store)
        
        context.update({
            'meta_title': f"{product.title} - {store.name}",
            'meta_description': product.description[:160],
            'meta_image': product.image.url if product.image else None,
            'structured_data': SEOHelper.generate_product_structured_data(product, store),
        })
    
    elif page_type == 'store' and 'store' in kwargs:
        store = kwargs['store']
        
        context.update({
            'meta_title': f"{store.name} - Handcrafted Products",
            'meta_description': store.description[:160] if store.description else f"Shop unique handcrafted products from {store.name}",
            'meta_image': store.logo_url.url if store.logo_url else None,
            'structured_data': SEOHelper.generate_store_structured_data(store),
        })
    
    return context