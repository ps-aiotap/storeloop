"""
StoreLoop integration with AT Identity service
"""
import requests
from typing import Dict, List, Optional
from django.conf import settings
from django.contrib.auth.models import User

class IdentityClient:
    """Client for StoreLoop to communicate with AT Identity service"""
    
    def __init__(self):
        self.base_url = getattr(settings, 'AT_IDENTITY_URL', 'http://localhost:8001/api/')
        self.api_key = getattr(settings, 'AT_IDENTITY_API_KEY', '')
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def sync_user(self, user: User) -> bool:
        """Sync StoreLoop user to AT Identity"""
        try:
            response = self.session.post(f'{self.base_url}sync/user/', json={
                'app_name': 'storeloop',
                'user_data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def get_user_permissions(self, user: User) -> List[str]:
        """Get user permissions from AT Identity"""
        try:
            response = self.session.get(
                f'{self.base_url}permissions/',
                params={
                    'app_name': 'storeloop',
                    'external_user_id': user.id
                }
            )
            if response.status_code == 200:
                return response.json().get('permissions', [])
        except requests.RequestException:
            pass
        return []
    
    def has_permission(self, user: User, permission: str) -> bool:
        """Check if user has specific permission"""
        try:
            response = self.session.post(f'{self.base_url}verify-permission/', json={
                'app_name': 'storeloop',
                'external_user_id': user.id,
                'permission': permission
            })
            if response.status_code == 200:
                return response.json().get('has_permission', False)
        except requests.RequestException:
            pass
        return False
    
    def create_organization(self, user: User, org_data: Dict) -> Optional[int]:
        """Create organization in AT Identity"""
        try:
            # First sync user
            self.sync_user(user)
            
            response = self.session.post(f'{self.base_url}organizations/', json={
                'app_name': 'storeloop',
                'creator_id': user.id,
                'organization': org_data
            })
            if response.status_code == 201:
                return response.json().get('id')
        except requests.RequestException:
            pass
        return None

# Global instance
identity_client = IdentityClient()