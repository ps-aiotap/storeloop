from django.urls import path
from . import views

urlpatterns = [
    path('store/<int:store_id>/theme/', views.store_theme_settings, name='store_theme_settings'),
    path('store/<slug:slug>/', views.StoreProductListView.as_view(), name='store_products'),
]