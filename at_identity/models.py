from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Extended user model for shared identity"""
    
    # Profile fields
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    
    # Preferences
    language = models.CharField(max_length=10, choices=[
        ('en', 'English'),
        ('hi', 'हिंदी')
    ], default='en')
    
    timezone = models.CharField(max_length=50, default='UTC')
    
    # Metadata
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    onboarding_completed = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'at_identity_user'
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

class Organization(models.Model):
    """Organization/Company model"""
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # Contact info
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    
    # Address
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Business info
    business_type = models.CharField(max_length=50, choices=[
        ('ngo', 'NGO'),
        ('artisan', 'Artisan'),
        ('consulting', 'Consulting'),
        ('startup', 'Startup'),
        ('enterprise', 'Enterprise'),
        ('other', 'Other')
    ], default='other')
    
    # Settings
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='org_logos/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'at_identity_organization'
    
    def __str__(self):
        return self.name

class Role(models.Model):
    """Role definition for permissions"""
    
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    
    # App-specific roles
    app_context = models.CharField(max_length=50, choices=[
        ('storeloop', 'StoreLoop'),
        ('artisan_crm', 'Artisan CRM'),
        ('shared', 'Shared')
    ], default='shared')
    
    # Permissions
    permissions = models.JSONField(default=list, help_text="List of permission strings")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'at_identity_role'
        unique_together = ('slug', 'app_context')
    
    def __str__(self):
        return f"{self.name} ({self.app_context})"

class UserOrganization(models.Model):
    """User membership in organizations with roles"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    # Membership details
    is_owner = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Metadata
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='invitations_sent')
    
    class Meta:
        db_table = 'at_identity_user_organization'
        unique_together = ('user', 'organization')
    
    def __str__(self):
        return f"{self.user.username} @ {self.organization.name} ({self.role.name})"

class UserProfile(models.Model):
    """Extended profile information"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Professional info
    job_title = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    
    # Social links
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # Preferences
    notification_email = models.BooleanField(default=True)
    notification_sms = models.BooleanField(default=False)
    marketing_emails = models.BooleanField(default=False)
    
    # App-specific data
    storeloop_data = models.JSONField(default=dict, blank=True)
    crm_data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'at_identity_user_profile'
    
    def __str__(self):
        return f"{self.user.username} Profile"