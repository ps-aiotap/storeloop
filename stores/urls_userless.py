from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponse
from . import views_userless

def home_redirect(request):
    return redirect('/login/')

def test_view(request):
    return HttpResponse("<h1>Test View Works!</h1><p><a href='/login/'>Go to Login</a></p>")

urlpatterns = [
    path('', home_redirect, name='home'),
    path('test/', test_view, name='test'),
    path('login/', views_userless.login_view, name='login'),
    path('logout/', views_userless.logout_view, name='logout'),
    path('dashboard/', views_userless.dashboard, name='dashboard'),
    path('create-store/', views_userless.create_store, name='create_store'),
]