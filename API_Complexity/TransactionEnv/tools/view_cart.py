# Copyright TransactionEnv

import json
from typing import Any, Dict, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import get_user_cart


class ViewCart(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        """
        View the contents of the current user's shopping cart.
        
        Args:
            data: The data dictionary containing shopping carts
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No current user. Please log in first."
            })
        
        # Get the user's cart
        cart = get_user_cart(data, current_user)
        
        if not cart:
            return json.dumps({
                "success": False,
                "message": "Failed to retrieve cart."
            })
        
        # Count total items
        item_count = sum(item.get("quantity", 0) for item in cart.get("items", []))
        
        return json.dumps({
            "success": True,
            "cart": cart,
            "item_count": item_count,
            "message": f"Cart has {item_count} items with a total of ${cart.get('total', 0):.2f}" if item_count > 0 else "Your cart is empty."
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "view_cart",
                "description": "View the current contents of the user's shopping cart. Shows all items, quantities, prices, and the total cart value.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
                "error_cases": [
                    "No current user: Cart operations require a logged-in user"
                ]
            }
        }
