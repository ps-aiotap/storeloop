from django.urls import path
from . import views

urlpatterns = [
    # Seller onboarding and dashboard
    path('onboarding/', views.seller_onboarding, name='seller_onboarding'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('partner-dashboard/', views.partner_admin_dashboard, name='partner_admin_dashboard'),
    
    # Product management
    path('products/upload/', views.product_upload, name='product_upload'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    
    # AI features
    path('api/generate-description/', views.generate_product_description, name='generate_product_description'),
    path('api/ai-task/<str:task_id>/', views.check_ai_task, name='check_ai_task'),
    
    # Order management
    path('orders/<str:order_id>/', views.order_detail, name='order_detail'),
    path('orders/<str:order_id>/invoice/', views.download_gst_invoice, name='download_gst_invoice'),
    
    # Analytics
    path('api/analytics/', views.analytics_api, name='analytics_api'),
    
    # Language
    path('set-language/', views.set_language, name='set_language'),
]