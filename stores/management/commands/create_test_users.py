from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stores.models import SellerProfile, Store, Product, Order

class Command(BaseCommand):
    help = 'Create test users for Playwright tests'

    def handle(self, *args, **options):
        # Delete all test data
        User.objects.filter(username__in=['admin', 'ngo_admin']).delete()
        
        # Create fresh admin user with no store
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        self.stdout.write('Created fresh admin user')
        
        # Create NGO admin user
        ngo_user = User.objects.create_user('ngo_admin', 'ngo@example.com', 'password')
        SellerProfile.objects.create(user=ngo_user, is_partner_admin=True, language_preference='hi')
        self.stdout.write('Created ngo_admin user')
        
        self.stdout.write(self.style.SUCCESS('Test users ready with clean state'))