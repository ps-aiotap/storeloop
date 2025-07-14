from django.urls import path
from .views import (
    ProductListView, 
    ProductDetailView, 
    BundleDetailView,
    TagCollectionView,
    StaticPageView,
    AnalyticsDashboardView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('bundles/<int:pk>/', BundleDetailView.as_view(), name='bundle_detail'),
    path('collections/<slug:tag_type>/<slug:tag>/', TagCollectionView.as_view(), name='tag_collection'),
    path('stores/<slug:store_slug>/pages/<slug:page_slug>/', StaticPageView.as_view(), name='static_page'),
    path('dashboard/analytics/', AnalyticsDashboardView.as_view(), name='analytics_dashboard'),
]