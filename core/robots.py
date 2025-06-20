from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from stores.models import Store


def robots_txt(request):
    """Generate robots.txt for multi-store deployment"""
    
    # Base robots.txt content
    lines = [
        "User-agent: *",
        "",
        "# Allow crawling of main content",
        "Allow: /",
        "Allow: /stores/",
        "Allow: /products/",
        "Allow: /collections/",
        "",
        "# Disallow admin and private areas",
        "Disallow: /admin/",
        "Disallow: /api/",
        "Disallow: /accounts/",
        "Disallow: /checkout/",
        "Disallow: /payment/",
        "",
        "# Disallow search and filter parameters",
        "Disallow: /*?search=",
        "Disallow: /*?filter=",
        "Disallow: /*?sort=",
        "Disallow: /*?page=",
        "",
        "# Disallow theme editor and admin tools",
        "Disallow: /stores/*/theme/",
        "Disallow: /stores/*/homepage/editor/",
        "Disallow: /stores/*/analytics/",
        "",
        "# Allow specific file types",
        "Allow: /*.css$",
        "Allow: /*.js$",
        "Allow: /*.png$",
        "Allow: /*.jpg$",
        "Allow: /*.jpeg$",
        "Allow: /*.gif$",
        "Allow: /*.webp$",
        "Allow: /*.svg$",
        "",
        "# Crawl delay for respectful crawling",
        "Crawl-delay: 1",
        "",
    ]
    
    # Add sitemap URLs
    if hasattr(settings, 'SITE_URL') and settings.SITE_URL:
        site_url = settings.SITE_URL.rstrip('/')
        lines.extend([
            "# Sitemaps",
            f"Sitemap: {site_url}/sitemap.xml",
            f"Sitemap: {site_url}/sitemap-stores.xml",
            f"Sitemap: {site_url}/sitemap-products.xml",
            f"Sitemap: {site_url}/sitemap-collections.xml",
            ""
        ])
    
    # Add store-specific instructions if needed
    stores = Store.objects.all()
    if stores.exists():
        lines.extend([
            "# Store-specific crawling instructions",
            "# All stores are publicly accessible",
        ])
        
        for store in stores:
            lines.append(f"Allow: /stores/{store.slug}/")
    
    # Add special instructions for different user agents
    lines.extend([
        "",
        "# Google-specific instructions",
        "User-agent: Googlebot",
        "Allow: /",
        "Crawl-delay: 1",
        "",
        "# Bing-specific instructions", 
        "User-agent: Bingbot",
        "Allow: /",
        "Crawl-delay: 2",
        "",
        "# Social media crawlers",
        "User-agent: facebookexternalhit",
        "Allow: /",
        "",
        "User-agent: Twitterbot",
        "Allow: /",
        "",
        "User-agent: LinkedInBot",
        "Allow: /",
        "",
        "# Block aggressive crawlers",
        "User-agent: AhrefsBot",
        "Disallow: /",
        "",
        "User-agent: MJ12bot",
        "Disallow: /",
        "",
        "User-agent: DotBot",
        "Disallow: /",
    ])
    
    # Join all lines
    content = "\n".join(lines)
    
    return HttpResponse(content, content_type="text/plain")


def security_txt(request):
    """Generate security.txt for responsible disclosure"""
    
    lines = [
        "# Security Policy for StoreLoop",
        "",
        "Contact: security@storeloop.com",
        "Expires: 2025-12-31T23:59:59.000Z",
        "Preferred-Languages: en",
        "",
        "# Reporting Guidelines",
        "# Please report security vulnerabilities responsibly",
        "# Include detailed steps to reproduce the issue",
        "# Allow reasonable time for fixes before public disclosure",
        "",
        "# Scope",
        "# In scope: Authentication, payment processing, data handling",
        "# Out of scope: Social engineering, physical attacks, DoS",
        "",
        "# Acknowledgments",
        "# We appreciate responsible security researchers",
        "# Acknowledgments will be provided for valid reports",
    ]
    
    content = "\n".join(lines)
    return HttpResponse(content, content_type="text/plain")