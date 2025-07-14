from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:product_id>/', views.create_order, name='create_order'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]