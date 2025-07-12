from django.urls import path
from . import views_userless

urlpatterns = [
    path('login/', views_userless.login_view, name='login'),
    path('logout/', views_userless.logout_view, name='logout'),
    path('dashboard/', views_userless.dashboard, name='dashboard'),
    path('create-store/', views_userless.create_store, name='create_store'),
]