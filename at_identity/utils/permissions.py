from typing import List, Optional
from django.contrib.auth import get_user_model
from ..models import UserOrganization, Role

User = get_user_model()

class PermissionManager:
    """Centralized permission management"""
    
    @staticmethod
    def user_has_permission(user: User, permission: str, organization=None, app_context='shared') -> bool:
        """Check if user has specific permission"""
        if user.is_superuser:
            return True
        
        # Get user's roles
        memberships = UserOrganization.objects.filter(
            user=user,
            is_active=True
        )
        
        if organization:
            memberships = memberships.filter(organization=organization)
        
        for membership in memberships:
            role = membership.role
            if role.app_context in [app_context, 'shared'] and permission in role.permissions:
                return True
        
        return False
    
    @staticmethod
    def get_user_permissions(user: User, organization=None, app_context='shared') -> List[str]:
        """Get all permissions for user"""
        if user.is_superuser:
            return ['*']  # Superuser has all permissions
        
        permissions = set()
        memberships = UserOrganization.objects.filter(
            user=user,
            is_active=True
        ).select_related('role')
        
        if organization:
            memberships = memberships.filter(organization=organization)
        
        for membership in memberships:
            role = membership.role
            if role.app_context in [app_context, 'shared']:
                permissions.update(role.permissions)
        
        return list(permissions)
    
    @staticmethod
    def get_user_organizations(user: User) -> List:
        """Get organizations user belongs to"""
        return UserOrganization.objects.filter(
            user=user,
            is_active=True
        ).select_related('organization', 'role')

def has_permission(permission: str, app_context='shared'):
    """Decorator to check permissions"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            
            if not PermissionManager.user_has_permission(
                request.user, permission, app_context=app_context
            ):
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator