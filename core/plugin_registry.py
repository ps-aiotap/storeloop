from typing import Dict, List, Type
from core.plugins import StoreLoopPlugin
import importlib
import logging

logger = logging.getLogger(__name__)

class PluginRegistry:
    """Registry for StoreLoop plugins"""
    
    def __init__(self):
        self._plugins = {}
        self._instances = {}
    
    def register_plugin(self, plugin_class: Type[StoreLoopPlugin]) -> None:
        """Register a plugin class"""
        plugin_name = plugin_class.__name__
        self._plugins[plugin_name] = plugin_class
        logger.info(f"Registered plugin: {plugin_name}")
    
    def get_plugin_class(self, plugin_name: str) -> Type[StoreLoopPlugin]:
        """Get a plugin class by name"""
        return self._plugins.get(plugin_name)
    
    def get_plugin_instance(self, plugin_name: str) -> StoreLoopPlugin:
        """Get or create a plugin instance by name"""
        if plugin_name not in self._instances:
            plugin_class = self.get_plugin_class(plugin_name)
            if plugin_class:
                instance = plugin_class()
                instance.initialize()
                self._instances[plugin_name] = instance
                logger.info(f"Initialized plugin: {plugin_name}")
            else:
                return None
        return self._instances.get(plugin_name)
    
    def get_all_plugins(self) -> Dict[str, Type[StoreLoopPlugin]]:
        """Get all registered plugin classes"""
        return self._plugins
    
    def get_all_instances(self) -> Dict[str, StoreLoopPlugin]:
        """Get all plugin instances"""
        return self._instances
    
    def load_plugins_from_settings(self, plugin_settings: List[Dict]) -> None:
        """Load plugins from settings configuration"""
        for plugin_config in plugin_settings:
            module_path = plugin_config.get('module')
            class_name = plugin_config.get('class')
            enabled = plugin_config.get('enabled', True)
            
            if not enabled:
                continue
                
            try:
                module = importlib.import_module(module_path)
                plugin_class = getattr(module, class_name)
                self.register_plugin(plugin_class)
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to load plugin {module_path}.{class_name}: {e}")

# Create a global registry instance
plugin_registry = PluginRegistry()

def initialize_plugins():
    """Initialize plugins from Django settings"""
    from django.conf import settings
    
    plugin_settings = getattr(settings, 'STORELOOP_PLUGINS', [])
    plugin_registry.load_plugins_from_settings(plugin_settings)
    
    return plugin_registry