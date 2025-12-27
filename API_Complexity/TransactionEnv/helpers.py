# Copyright TransactionEnv

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import uuid

def find_product_by_id(data: Dict[str, Any], product_id: str) -> Optional[Dict[str, Any]]:
    """
    Find a product by its ID.
    
    Args:
        data: The data dictionary containing products
        product_id: The ID of the product to find
        
    Returns:
        The product dictionary if found, None otherwise
    """
    for product in data.get("products", []):
        if product.get("product_id") == product_id:
            return product
    return None

def search_products(data: Dict[str, Any], query: str = None, category: str = None, 
                    min_price: float = None, max_price: float = None, 
                    sort_by: str = None, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search products based on various criteria.
    
    Args:
        data: The data dictionary containing products
        query: Search term for product name or description
        category: Filter by product category
        min_price: Minimum price filter
        max_price: Maximum price filter
        sort_by: Field to sort by ('price', 'rating', 'name')
        limit: Maximum number of results to return
        
    Returns:
        List of matching product dictionaries
    """
    products = data.get("products", [])
    results = []
    
    # Filter products
    for product in products:
        # Filter by query (name or description)
        if query and query.lower() not in product.get("name", "").lower() and \
           query.lower() not in product.get("description", "").lower():
            continue
            
        # Filter by category
        if category and product.get("category") != category:
            continue
            
        # Filter by price range
        if min_price is not None and product.get("price", 0) < min_price:
            continue
        if max_price is not None and product.get("price", 0) > max_price:
            continue
            
        results.append(product)
    
    # Sort results if requested
    if sort_by:
        if sort_by == "price":
            results.sort(key=lambda p: p.get("price", 0))
        elif sort_by == "price_desc":
            results.sort(key=lambda p: p.get("price", 0), reverse=True)
        elif sort_by == "rating":
            results.sort(key=lambda p: p.get("rating", 0), reverse=True)
        elif sort_by == "name":
            results.sort(key=lambda p: p.get("name", ""))
    
    # Limit results
    if limit and limit > 0:
        results = results[:limit]
        
    return results

def get_user_cart(data: Dict[str, Any], user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Get the shopping cart for a user.
    
    Args:
        data: The data dictionary containing shopping carts
        user_id: The user ID (if None, uses current user)
        
    Returns:
        The user's shopping cart dictionary if found, None otherwise
    """
    if not user_id:
        user_id = data.get("current_user")
    if not user_id:
        return None
        
    shopping_carts = data.get("shopping_carts", {})
    
    # Create a new cart if it doesn't exist
    if user_id not in shopping_carts:
        shopping_carts[user_id] = {
            "items": [],
            "total": 0.0
        }
        
    return shopping_carts[user_id]

def calculate_cart_total(cart: Dict[str, Any]) -> float:
    """
    Calculate the total price of all items in a cart.
    
    Args:
        cart: The shopping cart dictionary
        
    Returns:
        The total price of all items
    """
    total = 0.0
    for item in cart.get("items", []):
        total += item.get("price", 0) * item.get("quantity", 0)
    return round(total, 2)

def update_cart_total(data: Dict[str, Any], user_id: Optional[str] = None) -> None:
    """
    Update the total price of a user's shopping cart.
    
    Args:
        data: The data dictionary containing shopping carts
        user_id: The user ID (if None, uses current user)
    """
    cart = get_user_cart(data, user_id)
    if cart:
        cart["total"] = calculate_cart_total(cart)

def find_order_by_id(data: Dict[str, Any], order_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find an order by its ID.
    
    Args:
        data: The data dictionary containing orders
        order_id: The ID of the order to find (can be original ID or carrier-prefixed ID)
        user_id: If provided, ensures the order belongs to this user
        
    Returns:
        The order dictionary if found, None otherwise
    """
    if not user_id:
        user_id = data.get("current_user")
    
    # Handle carrier-prefixed IDs (e.g., "UPS-der1")
    original_order_id = None
    if "-" in order_id:
        # Extract the part after carrier prefix
        parts = order_id.split("-", 1)
        if len(parts) == 2:
            suffix = parts[1]
            # Try to find an order with this suffix
            for order in data.get("orders", []):
                order_id_value = order.get("order_id", "")
                # Check if the order ID ends with this suffix
                if len(order_id_value) > len(suffix) and order_id_value[-len(suffix):] == suffix:
                    original_order_id = order_id_value
                    break
    
    # Search by original ID first
    if original_order_id:
        for order in data.get("orders", []):
            if order.get("order_id") == original_order_id:
                # If user_id is provided, check that the order belongs to this user
                if user_id and order.get("user_id") != user_id:
                    continue
                return order
                
    # Then fall back to direct ID match
    for order in data.get("orders", []):
        if order.get("order_id") == order_id:
            # If user_id is provided, check that the order belongs to this user
            if user_id and order.get("user_id") != user_id:
                continue
            return order
            
    return None

def get_user_orders(data: Dict[str, Any], user_id: Optional[str] = None, limit: int = None) -> List[Dict[str, Any]]:
    """
    Get all orders for a user.
    
    Args:
        data: The data dictionary containing orders
        user_id: The user ID (if None, uses current user)
        limit: Maximum number of orders to return
        
    Returns:
        List of order dictionaries for the user
    """
    if not user_id:
        user_id = data.get("current_user")
    if not user_id:
        return []
        
    orders = [order for order in data.get("orders", []) if order.get("user_id") == user_id]
    
    # Sort by creation date (newest first)
    orders.sort(key=lambda o: o.get("created_at", ""), reverse=True)
    
    if limit and limit > 0:
        return orders[:limit]
    return orders

def get_user_payment_methods(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all payment methods for a user.
    
    Args:
        data: The data dictionary containing users
        user_id: The user ID (if None, uses current user)
        
    Returns:
        List of payment method dictionaries for the user
    """
    if not user_id:
        user_id = data.get("current_user")
    if not user_id:
        return []
        
    for user in data.get("users", []):
        if user.get("user_id") == user_id:
            # Check if transaction_info exists with payment_methods
            if "transaction_info" in user and "payment_methods" in user["transaction_info"]:
                return user["transaction_info"]["payment_methods"]
            return []
    return []

def get_user_addresses(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all addresses for a user.
    
    Args:
        data: The data dictionary containing users
        user_id: The user ID (if None, uses current user)
        
    Returns:
        List of address dictionaries for the user
    """
    if not user_id:
        user_id = data.get("current_user")
    if not user_id:
        return []
        
    for user in data.get("users", []):
        if user.get("user_id") == user_id:
            # Check if transaction_info exists with addresses
            if "transaction_info" in user and "addresses" in user["transaction_info"]:
                return user["transaction_info"]["addresses"]
            return []
    return []

def generate_order_id(data: Dict[str, Any]) -> str:
    """Generate a sequential order ID"""
    import re
    
    if "orders" not in data:
        data["orders"] = []
    
    existing_ids = []
    for order in data["orders"]:
        if "order_id" in order and order["order_id"].startswith("order"):
            try:
                match = re.search(r'^order(\d+)$', order["order_id"])
                if match:
                    num = int(match.group(1))
                    existing_ids.append(num)
            except (ValueError, AttributeError):
                continue
    
    next_num = 1
    if existing_ids:
        next_num = max(existing_ids) + 1
    
    return f"order{next_num}"

def get_current_timestamp() -> str:
    """Get the current timestamp in ISO format"""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
