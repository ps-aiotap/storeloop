from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User, Organization, UserOrganization, UserProfile
from .utils.permissions import PermissionManager

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'at_identity/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_organizations'] = PermissionManager.get_user_organizations(self.request.user)
        context['user_permissions'] = PermissionManager.get_user_permissions(self.request.user)
        return context

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'at_identity/edit_profile.html'
    fields = ['first_name', 'last_name', 'email', 'phone', 'bio', 'language', 'avatar']
    success_url = reverse_lazy('at_identity:profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class OrganizationListView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = 'at_identity/organization_list.html'
    context_object_name = 'organizations'
    
    def get_queryset(self):
        # Show organizations user belongs to
        user_orgs = UserOrganization.objects.filter(
            user=self.request.user,
            is_active=True
        ).values_list('organization_id', flat=True)
        
        return Organization.objects.filter(id__in=user_orgs, is_active=True)

class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = 'at_identity/organization_detail.html'
    context_object_name = 'organization'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        org = self.get_object()
        
        # Check if user is member
        try:
            membership = UserOrganization.objects.get(
                user=self.request.user,
                organization=org,
                is_active=True
            )
            context['user_membership'] = membership
            context['is_member'] = True
        except UserOrganization.DoesNotExist:
            context['is_member'] = False
        
        # Get all members if user has permission
        if context.get('is_member'):
            context['members'] = org.members.filter(is_active=True).select_related('user', 'role')
        
        return context

class CreateOrganizationView(LoginRequiredMixin, CreateView):
    model = Organization
    template_name = 'at_identity/create_organization.html'
    fields = ['name', 'description', 'business_type', 'email', 'phone', 'website', 'address', 'city', 'state', 'country']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Make user the owner
        from .models import Role
        owner_role = Role.objects.filter(slug='admin', app_context='shared').first()
        if owner_role:
            UserOrganization.objects.create(
                user=self.request.user,
                organization=self.object,
                role=owner_role,
                is_owner=True
            )
        
        messages.success(self.request, f'Organization "{self.object.name}" created successfully!')
        return response
    
    def get_success_url(self):
        return reverse_lazy('at_identity:organization_detail', kwargs={'slug': self.object.slug})