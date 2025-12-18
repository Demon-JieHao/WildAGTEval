# Copyright TransactionEnv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base_env import BaseEnvironment
from common.shared_memory_service import SharedMemoryService
from TransactionEnv.tools import ALL_TOOLS
from TransactionEnv.rules import RULES
from TransactionEnv.wiki import WIKI
from TransactionEnv.helpers import (
    find_product_by_id, search_products, get_user_cart, 
    get_user_orders, find_order_by_id
)
from typing import Optional, Dict, Any, List


class TransactionEnv(BaseEnvironment):
    """
    Transaction Environment for e-commerce product search, shopping cart management,
    checkout, and order tracking.
    """
    
    def __init__(self):
        """
        Initialize the Transaction Environment.
        """
        self.rules = RULES
        self.wiki = WIKI
        super().__init__()  # This will call _initialize_environment_data and _load_tools
        
    def _initialize_environment_data(self) -> None:
        """Initialize TransactionEnv-specific data structures"""
        # Initialize product data if it doesn't exist
        if "products" not in self.data:
            self.data["products"] = []
        
        # Initialize shopping cart data if it doesn't exist
        if "shopping_carts" not in self.data:
            self.data["shopping_carts"] = {}
        
        # Initialize order data if it doesn't exist
        if "orders" not in self.data:
            self.data["orders"] = []
            
        # Ensure user transaction info structure exists
        for user in self.data.get("users", []):
            if "transaction_info" not in user:
                user["transaction_info"] = {
                    "payment_methods": [],
                    "addresses": []
                }
    
    def _load_tools(self) -> Dict[str, Any]:
        """Load TransactionEnv-specific tools"""
        # Convert from list to dict format expected by base class
        tools_dict = {}
        for tool in ALL_TOOLS:
            tool_info = tool.get_info()
            if 'function' in tool_info and 'name' in tool_info['function']:
                tool_name = tool_info['function']['name']
                tools_dict[tool_name] = tool
        return tools_dict
    
    def _save_data(self) -> None:
        """
        Legacy method required by base class.
        In the new design, data is only stored in memory and never saved to disk.
        """
        # Don't save to disk, just update memory service
        self.memory_service.update_data(self.data)
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all available tools.
        
        Returns:
            List of tool information dictionaries
        """
        return [tool.get_info() for tool in self.tools.values()]
    
    def get_rules(self) -> List[str]:
        """
        Get all rules for the environment.
        
        Returns:
            List of rule strings
        """
        return self.rules
    
    def get_wiki(self) -> str:
        """
        Get the wiki documentation for the environment.
        
        Returns:
            Wiki documentation string
        """
        return self.wiki
    
    def search_products(self, query: Optional[str] = None, 
                        category: Optional[str] = None,
                        min_price: Optional[float] = None, 
                        max_price: Optional[float] = None, 
                        sort_by: Optional[str] = None, 
                        limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for products based on various criteria.
        
        Args:
            query: Search term for product name or description
            category: Filter by product category
            min_price: Minimum price filter
            max_price: Maximum price filter
            sort_by: Field to sort by ('price', 'rating', 'name')
            limit: Maximum number of results to return
            
        Returns:
            List of matching product dictionaries
        """
        return search_products(
            self.data, 
            query=query, 
            category=category, 
            min_price=min_price, 
            max_price=max_price, 
            sort_by=sort_by, 
            limit=limit
        )
    
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific product.
        
        Args:
            product_id: The ID of the product to retrieve
            
        Returns:
            The product dictionary if found, None otherwise
        """
        return find_product_by_id(self.data, product_id)
    
    def get_user_cart(self, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get the shopping cart for a user.
        
        Args:
            user_id: The user ID (if None, uses current user)
            
        Returns:
            The user's shopping cart dictionary if found, None otherwise
        """
        return get_user_cart(self.data, user_id)
    
    def get_user_orders(self, user_id: Optional[str] = None, 
                       limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get all orders for a user.
        
        Args:
            user_id: The user ID (if None, uses current user)
            limit: Maximum number of orders to return
            
        Returns:
            List of order dictionaries for the user
        """
        return get_user_orders(self.data, user_id, limit)
    
    def get_order_details(self, order_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific order.
        
        Args:
            order_id: The ID of the order to retrieve
            user_id: If provided, ensures the order belongs to this user
            
        Returns:
            The order dictionary if found, None otherwise
        """
        return find_order_by_id(self.data, order_id, user_id)
