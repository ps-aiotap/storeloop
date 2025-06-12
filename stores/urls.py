from django.urls import path
from . import views

urlpatterns = [
    path('store/<int:store_id>/theme/', views.store_theme_settings, name='store_theme_settings'),
]