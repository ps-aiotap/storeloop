from abc import ABC, abstractmethod
from typing import Dict, Any, List

class StoreLoopPlugin(ABC):
    """Base class for all StoreLoop plugins"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the plugin"""
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Return the version of the plugin"""
        pass
    
    @property
    def description(self) -> str:
        """Return the description of the plugin"""
        return ""
    
    def initialize(self) -> None:
        """Initialize the plugin"""
        pass
    
    def cleanup(self) -> None:
        """Clean up resources when plugin is disabled"""
        pass

class PaymentProvider(StoreLoopPlugin):
    """Base class for payment provider plugins"""
    
    @abstractmethod
    def create_payment(self, amount: int, currency: str, description: str) -> Dict[str, Any]:
        """Create a payment and return payment details"""
        pass
    
    @abstractmethod
    def verify_payment(self, payment_id: str, payment_data: Dict[str, Any]) -> bool:
        """Verify a payment is valid"""
        pass
    
    @abstractmethod
    def get_payment_status(self, payment_id: str) -> str:
        """Get the status of a payment"""
        pass

class ShippingProvider(StoreLoopPlugin):
    """Base class for shipping provider plugins"""
    
    @abstractmethod
    def calculate_shipping_cost(self, products: List[Dict[str, Any]], address: Dict[str, Any]) -> float:
        """Calculate shipping cost for products to an address"""
        pass
    
    @abstractmethod
    def create_shipping_label(self, order_id: str, address: Dict[str, Any]) -> Dict[str, Any]:
        """Create a shipping label for an order"""
        pass
    
    @abstractmethod
    def track_shipment(self, tracking_id: str) -> Dict[str, Any]:
        """Track a shipment by tracking ID"""
        pass