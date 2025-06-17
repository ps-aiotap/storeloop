from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.http import Http404
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Product, Tag, TagType, Bundle, StaticPage, TrustBadge, ProductView
from stores.models import Store

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_template_names(self):
        # If no store is selected, show the store list template
        if not hasattr(self.request, 'current_store') or not self.request.current_store:
            return ['products/store_list.html']
        
        # Otherwise use the unified theme template
        return ['stores/theme_view.html']
    
    def get_queryset(self):
        # Filter products by current store
        if hasattr(self.request, 'current_store') and self.request.current_store:
            return Product.objects.filter(store=self.request.current_store)
        
        # If no store context, return empty queryset
        return Product.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # If no current store, provide a list of available stores
        if not hasattr(self.request, 'current_store') or not self.request.current_store:
            context['page_title'] = 'Browse Stores'
            context['stores'] = Store.objects.all()
            context['no_store_selected'] = True
        else:
            context['page_title'] = f'Products from {self.request.current_store.name}'
            context['stores'] = Store.objects.all()
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_template_names(self):
        # Use the product detail template
        return ['stores/product_detail.html', 'products/product_detail.html']
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Set the current store based on the product's store
        self.request.current_store = obj.store
        
        # Record product view for analytics
        self.record_product_view(obj)
        
        return obj
    
    def record_product_view(self, product):
        # Get or create session ID
        if not self.request.session.session_key:
            self.request.session.save()
        
        session_id = self.request.session.session_key
        
        # Check if this session has viewed this product recently
        recent_view = ProductView.objects.filter(
            product=product,
            session_id=session_id,
            timestamp__gte=timezone.now() - timedelta(hours=1)
        ).exists()
        
        if not recent_view:
            # Record new view
            ProductView.objects.create(
                product=product,
                session_id=session_id,
                ip_address=self.request.META.get('REMOTE_ADDR'),
                user_agent=self.request.META.get('HTTP_USER_AGENT', '')
            )
            
            # Increment product view counter
            product.views += 1
            product.save(update_fields=['views'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add related products from the same store
        store = self.object.store
        context['related_products'] = Product.objects.filter(store=store).exclude(id=self.object.id)[:3]
        
        # Add trust badges
        context['trust_badges'] = TrustBadge.objects.filter(store=store)
        
        return context

class BundleDetailView(DetailView):
    model = Bundle
    template_name = 'products/bundle_detail.html'
    context_object_name = 'bundle'
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        
        # Set the current store based on the bundle's store
        self.request.current_store = obj.store
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add bundle items with their quantities
        context['bundle_items'] = self.object.bundleitem_set.all()
        
        # Add trust badges
        context['trust_badges'] = TrustBadge.objects.filter(store=self.object.store)
        
        return context

class TagCollectionView(ListView):
    model = Product
    template_name = 'products/tag_collection.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        tag_type_slug = self.kwargs.get('tag_type')
        tag_slug = self.kwargs.get('tag')
        
        # Get the tag
        self.tag = get_object_or_404(Tag, slug=tag_slug, tag_type__slug=tag_type_slug)
        
        # Filter products by tag and current store if available
        queryset = self.tag.products.all()
        
        if hasattr(self.request, 'current_store') and self.request.current_store:
            queryset = queryset.filter(store=self.request.current_store)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        context['page_title'] = f"{self.tag.name} Collection"
        
        # Add meta information for SEO
        context['meta_title'] = self.tag.meta_title or f"{self.tag.name} Products"
        context['meta_description'] = self.tag.meta_description
        
        # Add related tags from the same tag type
        context['related_tags'] = Tag.objects.filter(tag_type=self.tag.tag_type).exclude(id=self.tag.id)
        
        return context

class StaticPageView(DetailView):
    model = StaticPage
    template_name = 'products/static_page.html'
    context_object_name = 'page'
    
    def get_object(self, queryset=None):
        store_slug = self.kwargs.get('store_slug')
        page_slug = self.kwargs.get('page_slug')
        
        # Get the store and page
        store = get_object_or_404(Store, slug=store_slug)
        page = get_object_or_404(StaticPage, slug=page_slug, store=store, is_published=True)
        
        # Set the current store
        self.request.current_store = store
        
        return page
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add meta information for SEO
        context['meta_title'] = self.object.meta_title or self.object.title
        context['meta_description'] = self.object.meta_description
        
        return context

class AnalyticsDashboardView(TemplateView):
    template_name = 'products/analytics_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Ensure user is authenticated and has a current store
        if not self.request.user.is_authenticated:
            raise Http404("Dashboard not available")
        
        store = getattr(self.request, 'current_store', None)
        if not store or store.owner != self.request.user:
            raise Http404("Dashboard not available for this store")
        
        # Get time range from query params (default to last 30 days)
        days = int(self.request.GET.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        # Get products for this store
        products = Product.objects.filter(store=store)
        
        # Product views over time
        product_views = ProductView.objects.filter(
            product__in=products,
            timestamp__gte=start_date
        )
        
        # Group by day
        views_by_day = {}
        for view in product_views:
            day = view.timestamp.date()
            views_by_day[day] = views_by_day.get(day, 0) + 1
        
        # Convert to list for chart
        view_data = [
            {'date': day.strftime('%Y-%m-%d'), 'views': count}
            for day, count in sorted(views_by_day.items())
        ]
        
        # Top products by views
        top_products = products.order_by('-views')[:10]
        
        # Tag performance
        tag_performance = []
        for tag_type in TagType.objects.all():
            for tag in tag_type.tags.all():
                tag_products = tag.products.filter(store=store)
                if tag_products.exists():
                    tag_performance.append({
                        'tag': tag.name,
                        'tag_type': tag_type.name,
                        'product_count': tag_products.count(),
                        'total_views': sum(p.views for p in tag_products),
                    })
        
        # Sort by total views
        tag_performance.sort(key=lambda x: x['total_views'], reverse=True)
        
        context.update({
            'store': store,
            'days': days,
            'view_data': view_data,
            'top_products': top_products,
            'tag_performance': tag_performance[:10],  # Top 10 tags
            'total_views': sum(p.views for p in products),
            'total_products': products.count(),
        })
        
        return context