from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Organization, Role, UserOrganization, UserProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'email_verified', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'email_verified', 'language', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {
            'fields': ('phone', 'avatar', 'bio', 'language', 'timezone')
        }),
        ('Verification', {
            'fields': ('email_verified', 'phone_verified', 'onboarding_completed')
        }),
    )

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'business_type', 'city', 'country', 'is_active', 'created_at']
    list_filter = ['business_type', 'is_active', 'country', 'created_at']
    search_fields = ['name', 'email', 'city']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'app_context', 'is_active', 'created_at']
    list_filter = ['app_context', 'is_active', 'created_at']
    search_fields = ['name', 'description']

@admin.register(UserOrganization)
class UserOrganizationAdmin(admin.ModelAdmin):
    list_display = ['user', 'organization', 'role', 'is_owner', 'is_active', 'joined_at']
    list_filter = ['role', 'is_owner', 'is_active', 'joined_at']
    search_fields = ['user__username', 'organization__name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'job_title', 'company', 'notification_email', 'created_at']
    list_filter = ['notification_email', 'notification_sms', 'marketing_emails', 'created_at']
    search_fields = ['user__username', 'job_title', 'company']