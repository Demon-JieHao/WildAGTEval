# Copyright TransactionEnv

import json
from typing import Any, Dict
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import get_user_cart


class ClearCart(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        """
        Clear all items from the user's shopping cart.
        
        Args:
            data: The data dictionary containing carts
            
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
        
        # Check if the cart is already empty
        if not cart.get("items"):
            return json.dumps({
                "success": True,
                "message": "Cart is already empty."
            })
        
        # Store item count for message
        item_count = len(cart.get("items", []))
        total_quantity = sum(item.get("quantity", 0) for item in cart.get("items", []))
        
        # Clear the cart
        cart["items"] = []
        cart["total"] = 0.0
        
        return json.dumps({
            "success": True,
            "message": f"Removed all items from your cart ({item_count} product types, {total_quantity} total items)."
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "clear_cart",
                "description": "Remove all items from the user's shopping cart, resetting it to an empty state with zero total.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
                "error_cases": [
                    "No current user: Cart operations require a logged-in user"
                ]
            }
        }
