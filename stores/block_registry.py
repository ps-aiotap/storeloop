from abc import ABC, abstractmethod
from typing import Dict, Any, List
import importlib
import os
from django.conf import settings


class BaseBlock(ABC):
    """Base class for all homepage blocks"""
    
    # Block metadata
    name: str = ""
    icon: str = "📦"
    category: str = "General"
    description: str = ""
    
    # Configuration schema
    config_schema: Dict[str, Any] = {}
    
    @abstractmethod
    def render(self, context: Dict[str, Any], configuration: Dict[str, Any]) -> str:
        """Render the block with given context and configuration"""
        pass
    
    @abstractmethod
    def get_template_name(self) -> str:
        """Return the template name for this block"""
        pass
    
    def validate_configuration(self, configuration: Dict[str, Any]) -> List[str]:
        """Validate block configuration and return list of errors"""
        errors = []
        
        for field, schema in self.config_schema.items():
            if schema.get('required', False) and field not in configuration:
                errors.append(f"Required field '{field}' is missing")
            
            if field in configuration:
                value = configuration[field]
                field_type = schema.get('type', 'string')
                
                if field_type == 'integer' and not isinstance(value, int):
                    try:
                        int(value)
                    except (ValueError, TypeError):
                        errors.append(f"Field '{field}' must be an integer")
                
                elif field_type == 'boolean' and not isinstance(value, bool):
                    errors.append(f"Field '{field}' must be a boolean")
                
                elif field_type == 'url' and value:
                    if not (value.startswith('http://') or value.startswith('https://') or value.startswith('/')):
                        errors.append(f"Field '{field}' must be a valid URL")
        
        return errors
    
    def get_default_configuration(self) -> Dict[str, Any]:
        """Get default configuration for this block"""
        defaults = {}
        for field, schema in self.config_schema.items():
            if 'default' in schema:
                defaults[field] = schema['default']
        return defaults


class HeroBannerBlock(BaseBlock):
    """Hero banner block with image and call-to-action"""
    
    name = "Hero Banner"
    icon = "🖼️"
    category = "Layout"
    description = "Large banner with image and call-to-action button"
    
    config_schema = {
        'image_url': {
            'type': 'url',
            'required': False,
            'label': 'Background Image URL',
            'help': 'URL of the background image'
        },
        'title': {
            'type': 'string',
            'required': False,
            'label': 'Banner Title',
            'default': 'Welcome to Our Store'
        },
        'subtitle': {
            'type': 'string',
            'required': False,
            'label': 'Banner Subtitle'
        },
        'button_text': {
            'type': 'string',
            'required': False,
            'label': 'Button Text',
            'default': 'Shop Now'
        },
        'button_url': {
            'type': 'url',
            'required': False,
            'label': 'Button URL',
            'default': '/products/'
        },
        'text_color': {
            'type': 'color',
            'required': False,
            'label': 'Text Color',
            'default': 'white'
        },
        'height': {
            'type': 'select',
            'required': False,
            'label': 'Banner Height',
            'options': [
                {'value': 'sm', 'label': 'Small'},
                {'value': 'md', 'label': 'Medium'},
                {'value': 'lg', 'label': 'Large'},
                {'value': 'xl', 'label': 'Extra Large'}
            ],
            'default': 'lg'
        }
    }
    
    def render(self, context: Dict[str, Any], configuration: Dict[str, Any]) -> str:
        from django.template.loader import render_to_string
        
        block_context = {
            **context,
            'config': configuration,
            'title': configuration.get('title', 'Welcome to Our Store'),
            'subtitle': configuration.get('subtitle', ''),
            'button_text': configuration.get('button_text', 'Shop Now'),
            'button_url': configuration.get('button_url', '/products/'),
            'image_url': configuration.get('image_url', ''),
            'text_color': configuration.get('text_color', 'white'),
            'height': configuration.get('height', 'lg')
        }
        
        return render_to_string(self.get_template_name(), block_context)
    
    def get_template_name(self) -> str:
        return 'stores/blocks/hero_banner.html'


class ProductGridBlock(BaseBlock):
    """Product grid display block"""
    
    name = "Product Grid"
    icon = "🛍️"
    category = "Products"
    description = "Grid layout displaying products"
    
    config_schema = {
        'columns': {
            'type': 'integer',
            'required': False,
            'label': 'Columns per Row',
            'default': 3,
            'min': 1,
            'max': 6
        },
        'limit': {
            'type': 'integer',
            'required': False,
            'label': 'Maximum Products',
            'default': 12,
            'min': 1,
            'max': 50
        },
        'show_price': {
            'type': 'boolean',
            'required': False,
            'label': 'Show Prices',
            'default': True
        },
        'filter_by_tag': {
            'type': 'string',
            'required': False,
            'label': 'Filter by Tag Slug'
        }
    }
    
    def render(self, context: Dict[str, Any], configuration: Dict[str, Any]) -> str:
        from django.template.loader import render_to_string
        from products.models import Product, Tag
        
        # Get products
        products = Product.objects.filter(store=context['store'])
        
        # Apply tag filter if specified
        tag_slug = configuration.get('filter_by_tag')
        if tag_slug:
            try:
                tag = Tag.objects.get(slug=tag_slug)
                products = products.filter(tags=tag)
            except Tag.DoesNotExist:
                pass
        
        # Apply limit
        limit = configuration.get('limit', 12)
        products = products[:limit]
        
        block_context = {
            **context,
            'config': configuration,
            'products': products,
            'columns': configuration.get('columns', 3),
            'show_price': configuration.get('show_price', True)
        }
        
        return render_to_string(self.get_template_name(), block_context)
    
    def get_template_name(self) -> str:
        return 'stores/blocks/product_grid.html'


class TestimonialsBlock(BaseBlock):
    """Customer testimonials block"""
    
    name = "Testimonials"
    icon = "💬"
    category = "Social Proof"
    description = "Display customer testimonials and reviews"
    
    config_schema = {
        'testimonials': {
            'type': 'json',
            'required': False,
            'label': 'Testimonials Data',
            'default': []
        },
        'layout': {
            'type': 'select',
            'required': False,
            'label': 'Layout Style',
            'options': [
                {'value': 'grid', 'label': 'Grid Layout'},
                {'value': 'carousel', 'label': 'Carousel'},
                {'value': 'single', 'label': 'Single Testimonial'}
            ],
            'default': 'grid'
        },
        'show_ratings': {
            'type': 'boolean',
            'required': False,
            'label': 'Show Star Ratings',
            'default': True
        }
    }
    
    def render(self, context: Dict[str, Any], configuration: Dict[str, Any]) -> str:
        from django.template.loader import render_to_string
        
        testimonials = configuration.get('testimonials', [])
        
        block_context = {
            **context,
            'config': configuration,
            'testimonials': testimonials,
            'layout': configuration.get('layout', 'grid'),
            'show_ratings': configuration.get('show_ratings', True)
        }
        
        return render_to_string(self.get_template_name(), block_context)
    
    def get_template_name(self) -> str:
        return 'stores/blocks/testimonials.html'


class ContactFormBlock(BaseBlock):
    """Contact form block"""
    
    name = "Contact Form"
    icon = "📧"
    category = "Interaction"
    description = "Customer contact and inquiry form"
    
    config_schema = {
        'form_title': {
            'type': 'string',
            'required': False,
            'label': 'Form Title',
            'default': 'Get in Touch'
        },
        'background_color': {
            'type': 'color',
            'required': False,
            'label': 'Background Color',
            'default': '#f9fafb'
        },
        'show_phone': {
            'type': 'boolean',
            'required': False,
            'label': 'Show Phone Field',
            'default': True
        },
        'show_subject': {
            'type': 'boolean',
            'required': False,
            'label': 'Show Subject Field',
            'default': True
        },
        'contact_form_id': {
            'type': 'integer',
            'required': False,
            'label': 'Contact Form ID'
        }
    }
    
    def render(self, context: Dict[str, Any], configuration: Dict[str, Any]) -> str:
        from django.template.loader import render_to_string
        from products.models import ContactForm
        
        # Get contact form if specified
        contact_form = None
        form_id = configuration.get('contact_form_id')
        if form_id:
            try:
                contact_form = ContactForm.objects.get(id=form_id, store=context['store'])
            except ContactForm.DoesNotExist:
                pass
        
        block_context = {
            **context,
            'config': configuration,
            'contact_form': contact_form,
            'form_title': configuration.get('form_title', 'Get in Touch'),
            'background_color': configuration.get('background_color', '#f9fafb'),
            'show_phone': configuration.get('show_phone', True),
            'show_subject': configuration.get('show_subject', True)
        }
        
        return render_to_string(self.get_template_name(), block_context)
    
    def get_template_name(self) -> str:
        return 'stores/blocks/contact_form.html'


class BlockRegistry:
    """Registry for managing homepage blocks"""
    
    def __init__(self):
        self._blocks: Dict[str, BaseBlock] = {}
        self._load_default_blocks()
        self._load_plugin_blocks()
    
    def _load_default_blocks(self):
        """Load default built-in blocks"""
        default_blocks = [
            HeroBannerBlock(),
            ProductGridBlock(),
            TestimonialsBlock(),
            ContactFormBlock(),
        ]
        
        for block in default_blocks:
            self.register_block(block.__class__.__name__.lower().replace('block', ''), block)
    
    def _load_plugin_blocks(self):
        """Load blocks from plugins"""
        # Look for blocks in the plugins directory
        plugins_dir = os.path.join(settings.BASE_DIR, 'plugins')
        if not os.path.exists(plugins_dir):
            return
        
        for plugin_name in os.listdir(plugins_dir):
            plugin_path = os.path.join(plugins_dir, plugin_name)
            if os.path.isdir(plugin_path):
                try:
                    # Try to import blocks module from plugin
                    module = importlib.import_module(f'plugins.{plugin_name}.blocks')
                    
                    # Look for block classes
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, BaseBlock) and 
                            attr != BaseBlock):
                            
                            block_instance = attr()
                            block_key = attr_name.lower().replace('block', '')
                            self.register_block(block_key, block_instance)
                            
                except ImportError:
                    # Plugin doesn't have blocks module
                    continue
                except Exception as e:
                    # Log error but continue loading other plugins
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.warning(f"Error loading blocks from plugin {plugin_name}: {e}")
    
    def register_block(self, block_type: str, block: BaseBlock):
        """Register a new block type"""
        self._blocks[block_type] = block
    
    def get_block(self, block_type: str) -> BaseBlock:
        """Get a block by type"""
        return self._blocks.get(block_type)
    
    def get_all_blocks(self) -> Dict[str, BaseBlock]:
        """Get all registered blocks"""
        return self._blocks.copy()
    
    def get_blocks_by_category(self) -> Dict[str, List[tuple]]:
        """Get blocks grouped by category"""
        categories = {}
        
        for block_type, block in self._blocks.items():
            category = block.category
            if category not in categories:
                categories[category] = []
            
            categories[category].append((block_type, block))
        
        return categories
    
    def render_block(self, block_type: str, context: Dict[str, Any], configuration: Dict[str, Any]) -> str:
        """Render a block with given context and configuration"""
        block = self.get_block(block_type)
        if not block:
            return f"<!-- Block type '{block_type}' not found -->"
        
        # Validate configuration
        errors = block.validate_configuration(configuration)
        if errors:
            return f"<!-- Block configuration errors: {', '.join(errors)} -->"
        
        try:
            return block.render(context, configuration)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error rendering block {block_type}: {e}")
            return f"<!-- Error rendering block: {e} -->"


# Global registry instance
block_registry = BlockRegistry()