from django.urls import path, include
from . import views

app_name = 'at_identity'

urlpatterns = [
    # Profile management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    
    # Organization management
    path('organizations/', views.OrganizationListView.as_view(), name='organization_list'),
    path('organizations/create/', views.CreateOrganizationView.as_view(), name='create_organization'),
    path('organizations/<slug:slug>/', views.OrganizationDetailView.as_view(), name='organization_detail'),
    
    # Include allauth URLs
    path('', include('allauth.urls')),
]