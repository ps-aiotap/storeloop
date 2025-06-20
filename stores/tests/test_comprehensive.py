import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from stores.models import Store, StoreHomepageBlock
from products.models import Product, Tag, TagType
import json


@pytest.mark.django_db
class TestStoreCreation(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testowner',
            email='owner@test.com',
            password='testpass123'
        )

    def test_store_creation_with_required_fields(self):
        """Test store creation with minimal required fields"""
        store = Store.objects.create(
            name='Test Store',
            owner=self.user
        )
        self.assertEqual(store.name, 'Test Store')
        self.assertEqual(store.owner, self.user)
        self.assertEqual(store.slug, 'test-store')
        self.assertEqual(store.theme_name, 'minimal')

    def test_store_slug_auto_generation(self):
        """Test automatic slug generation from store name"""
        store = Store.objects.create(
            name='My Amazing Store!',
            owner=self.user
        )
        self.assertEqual(store.slug, 'my-amazing-store')

    def test_store_custom_slug(self):
        """Test custom slug assignment"""
        store = Store.objects.create(
            name='Test Store',
            slug='custom-store-slug',
            owner=self.user
        )
        self.assertEqual(store.slug, 'custom-store-slug')

    def test_store_theme_settings(self):
        """Test store theme configuration"""
        store = Store.objects.create(
            name='Themed Store',
            owner=self.user,
            theme_name='dark',
            primary_color='#ff0000',
            secondary_color='#00ff00',
            font_choice='serif'
        )
        settings = store.get_theme_settings()
        self.assertEqual(settings['theme_name'], 'dark')
        self.assertEqual(settings['primary_color'], '#ff0000')
        self.assertEqual(settings['font_choice'], 'serif')

    def test_homepage_layout_json_handling(self):
        """Test homepage layout JSON serialization/deserialization"""
        store = Store.objects.create(
            name='Layout Store',
            owner=self.user
        )
        
        # Test setting layout
        layout = [
            {'type': 'hero_banner', 'order': 0},
            {'type': 'product_grid', 'order': 1}
        ]
        store.set_homepage_layout(layout)
        
        # Test getting layout
        retrieved_layout = store.get_homepage_layout()
        self.assertEqual(len(retrieved_layout), 2)
        self.assertEqual(retrieved_layout[0]['type'], 'hero_banner')


@pytest.mark.django_db
class TestProductCreation(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='storeowner',
            email='owner@store.com',
            password='testpass123'
        )
        self.store = Store.objects.create(
            name='Product Store',
            owner=self.user
        )
        self.tag_type = TagType.objects.create(
            name='Occasion',
            slug='occasion'
        )
        self.tag = Tag.objects.create(
            name='Wedding',
            tag_type=self.tag_type
        )

    def test_product_creation_basic(self):
        """Test basic product creation"""
        product = Product.objects.create(
            title='Test Product',
            description='A test product description',
            price=99.99,
            store=self.store,
            stock_quantity=10
        )
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(float(product.price), 99.99)
        self.assertEqual(product.store, self.store)
        self.assertEqual(product.slug, 'test-product')
        self.assertEqual(product.stock_quantity, 10)
        self.assertEqual(product.views, 0)

    def test_product_slug_generation(self):
        """Test product slug auto-generation"""
        product = Product.objects.create(
            title='Amazing Product With Special Characters!',
            description='Test description',
            price=50.00,
            store=self.store
        )
        self.assertEqual(product.slug, 'amazing-product-with-special-characters')

    def test_product_with_tags(self):
        """Test product creation with tags"""
        product = Product.objects.create(
            title='Tagged Product',
            description='Product with tags',
            price=75.00,
            store=self.store
        )
        product.tags.add(self.tag)
        
        self.assertEqual(product.tags.count(), 1)
        self.assertEqual(product.tags.first(), self.tag)
        self.assertIn(product, self.tag.products.all())

    def test_product_stock_management(self):
        """Test product stock quantity handling"""
        product = Product.objects.create(
            title='Stock Product',
            description='Product for stock testing',
            price=25.00,
            store=self.store,
            stock_quantity=5
        )
        
        # Test initial stock
        self.assertEqual(product.stock_quantity, 5)
        
        # Test stock update
        product.stock_quantity = 3
        product.save()
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.stock_quantity, 3)

    def test_product_view_tracking(self):
        """Test product view counter"""
        product = Product.objects.create(
            title='Viewed Product',
            description='Product for view testing',
            price=30.00,
            store=self.store
        )
        
        # Simulate view increment
        product.views = 1
        product.save()
        
        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.views, 1)


@pytest.mark.django_db
class TestHomepageBlockLogic(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='blockowner',
            email='block@test.com',
            password='testpass123'
        )
        self.store = Store.objects.create(
            name='Block Store',
            owner=self.user
        )

    def test_homepage_block_creation(self):
        """Test creating homepage blocks"""
        block = StoreHomepageBlock.objects.create(
            store=self.store,
            block_type='hero_banner',
            title='Welcome Banner',
            content='Welcome to our store!',
            order=0,
            is_active=True
        )
        
        self.assertEqual(block.store, self.store)
        self.assertEqual(block.block_type, 'hero_banner')
        self.assertEqual(block.title, 'Welcome Banner')
        self.assertEqual(block.order, 0)
        self.assertTrue(block.is_active)

    def test_homepage_block_ordering(self):
        """Test homepage block ordering"""
        block1 = StoreHomepageBlock.objects.create(
            store=self.store,
            block_type='hero_banner',
            title='First Block',
            order=0
        )
        block2 = StoreHomepageBlock.objects.create(
            store=self.store,
            block_type='product_grid',
            title='Second Block',
            order=1
        )
        block3 = StoreHomepageBlock.objects.create(
            store=self.store,
            block_type='testimonials',
            title='Third Block',
            order=2
        )
        
        blocks = list(self.store.homepage_blocks.all())
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0].title, 'First Block')
        self.assertEqual(blocks[1].title, 'Second Block')
        self.assertEqual(blocks[2].title, 'Third Block')

    def test_homepage_block_configuration(self):
        """Test homepage block JSON configuration"""
        config = {
            'image_url': 'https://example.com/banner.jpg',
            'button_text': 'Shop Now',
            'button_url': '/products/',
            'text_color': 'white'
        }
        
        block = StoreHomepageBlock.objects.create(
            store=self.store,
            block_type='hero_banner',
            title='Configured Banner',
            configuration=config
        )
        
        self.assertEqual(block.configuration['image_url'], 'https://example.com/banner.jpg')
        self.assertEqual(block.configuration['button_text'], 'Shop Now')
        self.assertEqual(block.configuration['text_color'], 'white')

    def test_homepage_block_active_filtering(self):
        """Test filtering active vs inactive blocks"""
        active_block = StoreHomepageBlock.objects.create(
            store=self.store,
            block_type='hero_banner',
            title='Active Block',
            is_active=True
        )
        inactive_block = StoreHomepageBlock.objects.create(
            store=self.store,
            block_type='product_grid',
            title='Inactive Block',
            is_active=False
        )
        
        active_blocks = self.store.homepage_blocks.filter(is_active=True)
        inactive_blocks = self.store.homepage_blocks.filter(is_active=False)
        
        self.assertEqual(active_blocks.count(), 1)
        self.assertEqual(inactive_blocks.count(), 1)
        self.assertEqual(active_blocks.first().title, 'Active Block')
        self.assertEqual(inactive_blocks.first().title, 'Inactive Block')

    def test_homepage_block_types(self):
        """Test different homepage block types"""
        block_types = [
            'hero_banner',
            'product_grid',
            'featured_products',
            'testimonials',
            'text_block',
            'contact_form'
        ]
        
        for i, block_type in enumerate(block_types):
            block = StoreHomepageBlock.objects.create(
                store=self.store,
                block_type=block_type,
                title=f'{block_type.title()} Block',
                order=i
            )
            self.assertEqual(block.block_type, block_type)
        
        self.assertEqual(self.store.homepage_blocks.count(), len(block_types))

    def test_multiple_stores_block_isolation(self):
        """Test that blocks are isolated between stores"""
        other_user = User.objects.create_user(
            username='otherowner',
            email='other@test.com',
            password='testpass123'
        )
        other_store = Store.objects.create(
            name='Other Store',
            owner=other_user
        )
        
        # Create blocks for first store
        StoreHomepageBlock.objects.create(
            store=self.store,
            block_type='hero_banner',
            title='Store 1 Block'
        )
        
        # Create blocks for second store
        StoreHomepageBlock.objects.create(
            store=other_store,
            block_type='product_grid',
            title='Store 2 Block'
        )
        
        # Verify isolation
        self.assertEqual(self.store.homepage_blocks.count(), 1)
        self.assertEqual(other_store.homepage_blocks.count(), 1)
        self.assertEqual(self.store.homepage_blocks.first().title, 'Store 1 Block')
        self.assertEqual(other_store.homepage_blocks.first().title, 'Store 2 Block')