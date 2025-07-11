# AT Identity - Shared Identity Management

A reusable Django app for user, organization, and role management across StoreLoop and Artisan CRM.

## Features

### 🔐 Extended User Model
- Custom User model extending AbstractUser
- Profile fields (phone, avatar, bio, language)
- Email/phone verification
- Onboarding tracking

### 🏢 Organization Management
- Multi-tenant organization support
- Business type categorization
- Contact information and branding
- Address management

### 👥 Role-Based Access Control
- App-specific roles (StoreLoop, Artisan CRM, Shared)
- JSON-based permissions
- User-Organization-Role relationships
- Permission checking utilities

### 🔧 Django Allauth Integration
- Social authentication ready
- Email verification
- Account management
- Customizable signup/login flows

## Models

### User
Extended Django user with additional fields:
- `phone`, `avatar`, `bio`
- `language` (en/hi support)
- `email_verified`, `phone_verified`
- `onboarding_completed`

### Organization
Multi-tenant organization model:
- Basic info (name, description, logo)
- Contact details (email, phone, website)
- Address information
- Business type classification

### Role
App-specific role definitions:
- `app_context` (storeloop/artisan_crm/shared)
- JSON permissions array
- Active/inactive status

### UserOrganization
User membership in organizations:
- User-Organization-Role relationship
- Owner/member status
- Invitation tracking

### UserProfile
Extended profile information:
- Professional details
- Social links
- Notification preferences
- App-specific data storage

## Setup

### 1. Add to INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ... other apps
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'at_identity',
]
```

### 2. Configure Settings
```python
AUTH_USER_MODEL = 'at_identity.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE = [
    # ... other middleware
    'allauth.account.middleware.AccountMiddleware',
]

# Allauth settings
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
```

### 3. Run Migrations
```bash
python manage.py makemigrations at_identity
python manage.py migrate
```

### 4. Setup Default Roles
```bash
python manage.py setup_roles
```

## Usage

### Permission Checking
```python
from at_identity.utils.permissions import PermissionManager

# Check permission
has_perm = PermissionManager.user_has_permission(
    user, 'store.create', app_context='storeloop'
)

# Get all permissions
permissions = PermissionManager.get_user_permissions(
    user, app_context='artisan_crm'
)

# Decorator usage
from at_identity.utils.permissions import has_permission

@has_permission('customer.edit', app_context='artisan_crm')
def edit_customer(request):
    # View logic
    pass
```

### Organization Management
```python
from at_identity.models import Organization, UserOrganization, Role

# Create organization
org = Organization.objects.create(
    name="My Company",
    business_type="startup"
)

# Add user to organization
admin_role = Role.objects.get(slug='admin', app_context='shared')
UserOrganization.objects.create(
    user=user,
    organization=org,
    role=admin_role,
    is_owner=True
)
```

## Default Roles

### StoreLoop Roles
- **Store Owner**: Full store management
- **Store Manager**: Product and order management
- **NGO Admin**: Multi-store oversight

### Artisan CRM Roles
- **CRM Admin**: Full CRM access
- **Sales Rep**: Customer and lead management

### Shared Roles
- **Admin**: Full system access
- **User**: Basic profile access

## Integration with Apps

### StoreLoop Integration
```python
# In StoreLoop views
from at_identity.utils.permissions import has_permission

@has_permission('store.create', app_context='storeloop')
def create_store(request):
    # Store creation logic
    pass
```

### Artisan CRM Integration
```python
# In CRM views
from at_identity.utils.permissions import PermissionManager

def customer_list(request):
    if not PermissionManager.user_has_permission(
        request.user, 'customer.view', app_context='artisan_crm'
    ):
        return HttpResponseForbidden()
    # View logic
```

## Templates

The app provides basic templates for:
- User profile management
- Organization listing and details
- Account settings

Extend these templates in your main apps as needed.

## Migration from Existing User Model

When migrating from Django's default User model:

1. Update all ForeignKey references to use `settings.AUTH_USER_MODEL`
2. Create data migration to transfer existing users
3. Update admin configurations
4. Test authentication flows

## Future Enhancements

- Social authentication providers
- Advanced permission management UI
- Organization invitation system
- Audit logging
- Multi-factor authentication