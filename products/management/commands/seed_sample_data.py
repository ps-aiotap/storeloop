from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from stores.models import Store, StoreHomepageBlock
from products.models import Product, Tag, TagType, TrustBadge
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seed database with sample data for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=3,
            help='Number of users to create'
        )
        parser.add_argument(
            '--stores',
            type=int,
            default=2,
            help='Number of stores per user'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=10,
            help='Number of products per store'
        )

    def handle(self, *args, **options):
        self.stdout.write('Seeding sample data...')
        
        # Create tag types and tags
        self.create_tags()
        
        # Create users and stores
        users = self.create_users(options['users'])
        stores = self.create_stores(users, options['stores'])
        
        # Create products
        self.create_products(stores, options['products'])
        
        # Create homepage blocks
        self.create_homepage_blocks(stores)
        
        # Create trust badges
        self.create_trust_badges(stores)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {len(users)} users, '
                f'{len(stores)} stores, and sample data'
            )
        )

    def create_tags(self):
        """Create sample tag types and tags"""
        tag_data = {
            'Occasion': ['Wedding', 'Birthday', 'Anniversary', 'Festival', 'Corporate'],
            'Lifestyle': ['Minimalist', 'Bohemian', 'Modern', 'Traditional', 'Eco-friendly'],
            'Material': ['Cotton', 'Silk', 'Jute', 'Wood', 'Metal', 'Ceramic'],
            'Color': ['Red', 'Blue', 'Green', 'Yellow', 'Black', 'White', 'Multi-color']
        }
        
        for tag_type_name, tag_names in tag_data.items():
            tag_type, created = TagType.objects.get_or_create(
                name=tag_type_name,
                defaults={'description': f'Tags related to {tag_type_name.lower()}'}
            )
            
            for tag_name in tag_names:
                Tag.objects.get_or_create(
                    name=tag_name,
                    tag_type=tag_type,
                    defaults={
                        'description': f'{tag_name} related products',
                        'meta_title': f'{tag_name} Products',
                        'meta_description': f'Browse our collection of {tag_name.lower()} products'
                    }
                )

    def create_users(self, count):
        """Create sample users"""
        users = []
        for i in range(count):
            username = f'storeowner{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': f'Store',
                    'last_name': f'Owner {i+1}'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        return users

    def create_stores(self, users, stores_per_user):
        """Create sample stores"""
        stores = []
        themes = ['minimal', 'dark', 'warm']
        colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6']
        fonts = ['sans', 'serif', 'mono']
        
        store_names = [
            'Artisan Crafts', 'Modern Living', 'Eco Store', 'Vintage Collection',
            'Creative Corner', 'Style Hub', 'Craft Central', 'Design Studio'
        ]
        
        for user in users:
            for i in range(stores_per_user):
                store_name = f"{random.choice(store_names)} {user.username}"
                store, created = Store.objects.get_or_create(
                    name=store_name,
                    owner=user,
                    defaults={
                        'description': f'Welcome to {store_name}! We offer unique, handcrafted items.',
                        'theme_name': random.choice(themes),
                        'primary_color': random.choice(colors),
                        'secondary_color': random.choice(colors),
                        'font_choice': random.choice(fonts),
                        'contact_email': user.email,
                        'contact_phone': f'+91 9876543{random.randint(100, 999)}',
                        'whatsapp_number': f'+91 9876543{random.randint(100, 999)}'
                    }
                )
                stores.append(store)
        return stores

    def create_products(self, stores, products_per_store):
        """Create sample products"""
        product_templates = [
            {
                'title': 'Handcrafted Patchwork Art',
                'description': 'Beautiful handmade patchwork art piece perfect for home decoration.',
                'price_range': (500, 2000)
            },
            {
                'title': 'Eco-friendly Tote Bag',
                'description': 'Sustainable and stylish tote bag made from organic materials.',
                'price_range': (300, 800)
            },
            {
                'title': 'Ceramic Home Decor',
                'description': 'Elegant ceramic pieces to enhance your living space.',
                'price_range': (400, 1500)
            },
            {
                'title': 'Wooden Wall Art',
                'description': 'Rustic wooden wall art handcrafted by local artisans.',
                'price_range': (800, 3000)
            },
            {
                'title': 'Fabric Lampshade',
                'description': 'Unique fabric lampshade with intricate patterns.',
                'price_range': (600, 1200)
            },
            {
                'title': 'Jute Bottle Art',
                'description': 'Upcycled bottle transformed into beautiful decorative piece.',
                'price_range': (200, 600)
            }
        ]
        
        all_tags = list(Tag.objects.all())
        
        for store in stores:
            for i in range(products_per_store):
                template = random.choice(product_templates)
                
                product = Product.objects.create(
                    title=f"{template['title']} #{i+1}",
                    description=template['description'],
                    price=Decimal(random.randint(*template['price_range'])),
                    store=store,
                    stock_quantity=random.randint(1, 20),
                    views=random.randint(0, 100)
                )
                
                # Add random tags
                product_tags = random.sample(all_tags, random.randint(2, 5))
                product.tags.set(product_tags)

    def create_homepage_blocks(self, stores):
        """Create sample homepage blocks"""
        block_templates = [
            {
                'block_type': 'hero_banner',
                'title': 'Welcome to Our Store',
                'content': 'Discover unique handcrafted items made with love and care.',
                'configuration': {
                    'button_text': 'Shop Now',
                    'button_url': '/products/',
                    'text_color': 'white',
                    'height': 'lg'
                }
            },
            {
                'block_type': 'featured_products',
                'title': 'Featured Products',
                'content': 'Check out our most popular items.',
                'configuration': {
                    'product_count': 6,
                    'show_price': True
                }
            },
            {
                'block_type': 'text_block',
                'title': 'About Our Craft',
                'content': 'We are passionate artisans dedicated to creating beautiful, sustainable products that bring joy to your everyday life.',
                'configuration': {
                    'text_align': 'center',
                    'background_color': '#f9fafb'
                }
            },
            {
                'block_type': 'testimonials',
                'title': 'What Our Customers Say',
                'content': '',
                'configuration': {
                    'testimonials': [
                        {
                            'text': 'Amazing quality and beautiful designs!',
                            'author': 'Sarah M.',
                            'rating': 5
                        },
                        {
                            'text': 'Love the eco-friendly approach.',
                            'author': 'John D.',
                            'rating': 5
                        }
                    ]
                }
            },
            {
                'block_type': 'contact_form',
                'title': 'Get in Touch',
                'content': 'Have questions? We\'d love to hear from you!',
                'configuration': {
                    'background_color': '#f3f4f6',
                    'show_phone': True,
                    'show_subject': True
                }
            }
        ]
        
        for store in stores:
            for i, template in enumerate(block_templates):
                StoreHomepageBlock.objects.get_or_create(
                    store=store,
                    block_type=template['block_type'],
                    defaults={
                        'title': template['title'],
                        'content': template['content'],
                        'configuration': template['configuration'],
                        'order': i,
                        'is_active': True
                    }
                )

    def create_trust_badges(self, stores):
        """Create sample trust badges"""
        badge_data = [
            {
                'name': 'Handmade Quality',
                'description': 'All products are carefully handcrafted'
            },
            {
                'name': 'Eco-Friendly',
                'description': 'Sustainable materials and processes'
            },
            {
                'name': 'Fast Shipping',
                'description': 'Quick and reliable delivery'
            },
            {
                'name': 'Secure Payment',
                'description': 'Safe and secure payment processing'
            }
        ]
        
        for store in stores:
            for badge in badge_data:
                TrustBadge.objects.get_or_create(
                    name=badge['name'],
                    store=store,
                    defaults={
                        'description': badge['description']
                    }
                )