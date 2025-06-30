from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stores.models import Store, Product

class Command(BaseCommand):
    help = 'Add sample products with Hindi names for testing'

    def handle(self, *args, **options):
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created test user'))

        # Get or create a test store
        store, created = Store.objects.get_or_create(
            name='कलाकार शिल्प',
            owner=user,
            defaults={
                'description': 'हस्तशिल्प कलाकृतियों का संग्रह',
                'is_published': True,
                'onboarding_completed': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created store with Hindi name'))

        # Sample products with Hindi names
        sample_products = [
            {
                'name': 'बनारसी सिल्क साड़ी',
                'description': 'वाराणसी की पारंपरिक हस्तकला से बनी सुंदर सिल्क साड़ी। यह साड़ी शादी-विवाह और त्योहारों के लिए आदर्श है।',
                'price': 15000,
                'stock': 3,
                'category': 'Clothing',
                'material': 'Silk',
                'region': 'Varanasi',
                'style': 'Traditional',
                'image_url': 'https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400'
            },
            {
                'name': 'कशीदाकारी शाल',
                'description': 'कश्मीर की प्रसिद्ध कशीदाकारी से सजी ऊनी शाल। हाथ से बुनी गई यह शाल सर्दियों के लिए बेहतरीन है।',
                'price': 2500,
                'stock': 8,
                'category': 'Accessories',
                'material': 'Wool',
                'region': 'Kashmir',
                'style': 'Embroidered',
                'image_url': 'https://images.unsplash.com/photo-1544966503-7cc5ac882d5f?w=400'
            },
            {
                'name': 'मिट्टी का दीया',
                'description': 'हाथ से बना मिट्टी का पारंपरिक दीया। दिवाली और अन्य त्योहारों के लिए उपयुक्त।',
                'price': 299,
                'stock': 25,
                'category': 'Home Decor',
                'material': 'Clay',
                'region': 'Khurja',
                'style': 'Traditional',
                'image_url': 'https://images.unsplash.com/photo-1604608672516-f1b1f2d4b8c1?w=400'
            },
            {
                'name': 'हस्तनिर्मित गहने',
                'description': 'पारंपरिक डिजाइन के साथ हाथ से बने चांदी के गहने। शादी-विवाह के अवसरों के लिए आदर्श।',
                'price': 5500,
                'stock': 5,
                'category': 'Jewelry',
                'material': 'Silver',
                'region': 'Rajasthan',
                'style': 'Traditional',
                'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400'
            },
            {
                'name': 'बांस की टोकरी',
                'description': 'प्राकृतिक बांस से बनी हस्तनिर्मित टोकरी। घर की सजावट और उपयोग दोनों के लिए उपयुक्त।',
                'price': 850,
                'stock': 12,
                'category': 'Home Decor',
                'material': 'Bamboo',
                'region': 'Assam',
                'style': 'Handwoven',
                'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400'
            }
        ]

        for product_data in sample_products:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                store=store,
                defaults=product_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS('Created Hindi product'))
            else:
                self.stdout.write('Product already exists')

        self.stdout.write(self.style.SUCCESS('Sample products setup completed!'))
        self.stdout.write(f'Store URL: /stores/{store.slug}/')