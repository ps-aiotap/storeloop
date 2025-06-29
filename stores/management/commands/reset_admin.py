from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stores.models import Store, SellerProfile, Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Reset admin user for testing'

    def handle(self, *args, **options):
        # Create or update admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        admin_user.set_password('admin123')
        admin_user.save()
        
        # Create complete store for admin
        store, created = Store.objects.get_or_create(
            owner=admin_user,
            defaults={
                'name': 'Test Store',
                'description': 'Test Description',
                'slug': 'test-store',
                'is_published': True,
                'onboarding_completed': True,
            }
        )
        
        # Create NGO admin user
        ngo_user, created = User.objects.get_or_create(
            username='ngo_admin',
            defaults={
                'email': 'ngo@example.com',
            }
        )
        ngo_user.set_password('password')
        ngo_user.save()
        
        # Create NGO profile
        ngo_profile, created = SellerProfile.objects.get_or_create(
            user=ngo_user,
            defaults={
                'is_partner_admin': True,
                'organization_name': 'Test NGO',
            }
        )
        
        # Add store to NGO management
        ngo_profile.managed_stores.add(store)
        
        self.stdout.write(self.style.SUCCESS('Admin users and store created successfully'))