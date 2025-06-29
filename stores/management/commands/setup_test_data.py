from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stores.models import Store, Product, SellerProfile

class Command(BaseCommand):
    help = 'Setup test data for Playwright tests'

    def handle(self, *args, **options):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(f'Created admin user')
        
        # Create NGO admin user
        ngo_user, created = User.objects.get_or_create(
            username='ngo_admin',
            defaults={
                'email': 'ngo@example.com',
                'first_name': 'NGO',
                'last_name': 'Admin'
            }
        )
        if created:
            ngo_user.set_password('password')
            ngo_user.save()
            self.stdout.write(f'Created NGO admin user')
        
        # Create NGO profile
        ngo_profile, created = SellerProfile.objects.get_or_create(
            user=ngo_user,
            defaults={
                'is_partner_admin': True,
                'language_preference': 'hi'
            }
        )
        if created:
            self.stdout.write(f'Created NGO profile')
        
        # Create admin store
        admin_store, created = Store.objects.get_or_create(
            owner=admin_user,
            defaults={
                'name': 'Test Store',
                'description': 'Test store for admin',
                'onboarding_completed': True,
                'is_published': True,
                'theme': 'minimal',
                'primary_color': '#3B82F6',
                'secondary_color': '#10B981'
            }
        )
        if created:
            self.stdout.write(f'Created admin store: {admin_store.name}')
        
        # Add admin store to NGO managed stores
        if admin_store not in ngo_profile.managed_stores.all():
            ngo_profile.managed_stores.add(admin_store)
            self.stdout.write(f'Added store to NGO managed stores')
        
        # Create sample products with Hindi names
        hindi_products = [
            {
                'name': 'बनारसी सिल्क साड़ी',
                'description': 'Beautiful handwoven Banarasi silk saree from Varanasi',
                'price': 15000,
                'stock': 5,
                'material': 'Silk',
                'region': 'Varanasi',
                'category': 'Clothing'
            },
            {
                'name': 'कशीदाकारी शाल',
                'description': 'Exquisite embroidered shawl with traditional patterns',
                'price': 8000,
                'stock': 3,
                'material': 'Wool',
                'region': 'Kashmir',
                'category': 'Clothing'
            },
            {
                'name': 'मिट्टी का दीया',
                'description': 'Traditional clay lamp for festivals',
                'price': 299,
                'stock': 50,
                'material': 'Clay',
                'region': 'Khurja',
                'category': 'Home Decor'
            }
        ]
        
        for product_data in hindi_products:
            product, created = Product.objects.get_or_create(
                store=admin_store,
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully setup test data')
        )