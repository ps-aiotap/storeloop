from django.urls import path
from . import views

urlpatterns = [
    # Store theme settings
    path('store/<int:store_id>/theme/', views.store_theme_settings, name='store_theme_settings'),
    
    # Store homepage
    path('<slug:store_slug>/', views.store_homepage, name='store_homepage'),
    path('<slug:store_slug>/products/', views.StoreProductListView.as_view(), name='store_products'),
    
    # Homepage editor
    path('<slug:store_slug>/homepage/editor/', views.store_homepage_editor, name='store_homepage_editor'),
    path('<slug:store_slug>/homepage/blocks/create/', views.store_homepage_block_create, name='store_homepage_block_create'),
    path('<slug:store_slug>/homepage/blocks/<int:block_id>/update/', views.store_homepage_block_update, name='store_homepage_block_update'),
    path('<slug:store_slug>/homepage/blocks/<int:block_id>/delete/', views.store_homepage_block_delete, name='store_homepage_block_delete'),
    path('<slug:store_slug>/homepage/blocks/reorder/', views.store_homepage_blocks_reorder, name='store_homepage_blocks_reorder'),
]