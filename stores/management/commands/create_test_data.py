from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stores.models import Store, Product, SellerProfile

class Command(BaseCommand):
    help = 'Create test data for published stores'

    def handle(self, *args, **options):
        # Create a published store with products for buyer flow tests
        try:
            test_user = User.objects.get(username='teststore')
        except User.DoesNotExist:
            test_user = User.objects.create_user('teststore', 'test@example.com', 'password')
        
        # Delete existing test store
        Store.objects.filter(owner=test_user).delete()
        
        # Create published store
        store = Store.objects.create(
            name='Test Artisan Store',
            slug='test-artisan-store',
            description='Beautiful handcrafted items',
            owner=test_user,
            onboarding_completed=True,
            is_published=True,
            theme='warm',
            primary_color='#8B4513',
            secondary_color='#DEB887'
        )
        
        # Create sample products
        products = [
            {
                'name': 'Handwoven Silk Saree',
                'description': 'Beautiful traditional silk saree',
                'price': 5000,
                'stock': 10,
                'category': 'Clothing',
                'material': 'Silk',
                'region': 'Varanasi',
                'style': 'Traditional'
            },
            {
                'name': 'Wooden Handicraft',
                'description': 'Carved wooden decorative item',
                'price': 1500,
                'stock': 5,
                'category': 'Decor',
                'material': 'Wood',
                'region': 'Rajasthan',
                'style': 'Rajasthani'
            }
        ]
        
        for product_data in products:
            Product.objects.create(store=store, **product_data)
        
        self.stdout.write(self.style.SUCCESS(f'Created test store: {store.name} with {len(products)} products'))