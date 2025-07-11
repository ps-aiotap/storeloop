from django.core.management.base import BaseCommand
from ...models import Role

class Command(BaseCommand):
    help = 'Setup default roles for StoreLoop and Artisan CRM'
    
    def handle(self, *args, **options):
        roles_data = [
            # StoreLoop roles
            {
                'name': 'Store Owner',
                'slug': 'store_owner',
                'app_context': 'storeloop',
                'permissions': ['store.create', 'store.edit', 'store.delete', 'product.create', 'product.edit', 'product.delete', 'order.view', 'order.manage']
            },
            {
                'name': 'Store Manager',
                'slug': 'store_manager',
                'app_context': 'storeloop',
                'permissions': ['product.create', 'product.edit', 'order.view', 'order.manage']
            },
            {
                'name': 'NGO Admin',
                'slug': 'ngo_admin',
                'app_context': 'storeloop',
                'permissions': ['store.view_all', 'store.manage', 'user.manage', 'analytics.view']
            },
            
            # CRM roles
            {
                'name': 'CRM Admin',
                'slug': 'crm_admin',
                'app_context': 'artisan_crm',
                'permissions': ['customer.create', 'customer.edit', 'customer.delete', 'lead.manage', 'campaign.create', 'analytics.view']
            },
            {
                'name': 'Sales Rep',
                'slug': 'sales_rep',
                'app_context': 'artisan_crm',
                'permissions': ['customer.view', 'customer.edit', 'lead.manage', 'interaction.create']
            },
            
            # Shared roles
            {
                'name': 'Admin',
                'slug': 'admin',
                'app_context': 'shared',
                'permissions': ['*']
            },
            {
                'name': 'User',
                'slug': 'user',
                'app_context': 'shared',
                'permissions': ['profile.edit']
            }
        ]
        
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(
                slug=role_data['slug'],
                app_context=role_data['app_context'],
                defaults=role_data
            )
            
            if created:
                self.stdout.write(f"Created role: {role.name} ({role.app_context})")
            else:
                self.stdout.write(f"Role exists: {role.name} ({role.app_context})")
        
        self.stdout.write(self.style.SUCCESS('Successfully setup roles'))