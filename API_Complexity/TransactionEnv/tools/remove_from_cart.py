# Copyright TransactionEnv

import json
from typing import Any, Dict, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import get_user_cart, update_cart_total


class RemoveFromCart(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], product_id: str, quantity: Optional[int] = None) -> str:
        """
        Remove a product from the user's shopping cart.
        
        Args:
            data: The data dictionary containing carts
            product_id: ID of the product to remove
            quantity: Quantity to remove (if None, removes all of the product)
            
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
        
        if not product_id:
            return json.dumps({
                "success": False,
                "message": "Product ID is required"
            })
        
        if quantity is not None and quantity < 1:
            return json.dumps({
                "success": False,
                "message": "Quantity must be at least 1"
            })
        
        # Get the user's cart
        cart = get_user_cart(data, current_user)
        if not cart:
            return json.dumps({
                "success": False,
                "message": "Failed to retrieve cart."
            })
        
        # Check if the product is in the cart
        cart_items = cart.get("items", [])
        for i, item in enumerate(cart_items):
            if item.get("product_id") == product_id:
                item_quantity = item.get("quantity", 0)
                item_name = item.get("name", "Product")
                
                # If quantity is None or greater than current quantity, remove item entirely
                if quantity is None or quantity >= item_quantity:
                    # Remove the entire item
                    removed_item = cart_items.pop(i)
                    update_cart_total(data, current_user)
                    return json.dumps({
                        "success": True,
                        "removed": removed_item,
                        "cart_total": cart.get("total", 0),
                        "message": f"Removed all '{item_name}' from your cart"
                    })
                else:
                    # Reduce quantity
                    new_quantity = item_quantity - quantity
                    item["quantity"] = new_quantity
                    update_cart_total(data, current_user)
                    return json.dumps({
                        "success": True,
                        "product": {
                            "product_id": product_id,
                            "name": item_name,
                            "quantity": new_quantity
                        },
                        "cart_total": cart.get("total", 0),
                        "message": f"Reduced quantity of '{item_name}' to {new_quantity}"
                    })
        
        # Product not found in cart
        return json.dumps({
            "success": False,
            "message": f"Product with ID '{product_id}' not found in your cart"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "remove_from_cart",
                "description": "Remove a product from the user's shopping cart. Can remove a specific quantity or all instances of the product.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The unique ID of the product to remove from the cart."
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "(Optional) Quantity to remove. If not provided or if greater than the quantity in the cart, all instances of the product will be removed."
                        }
                    },
                    "required": ["product_id"]
                },
                "error_cases": [
                    "No current user: Cart operations require a logged-in user",
                    "Missing product ID: The product ID parameter is not provided",
                    "Invalid quantity: Quantity must be at least 1",
                    "Product not found in cart: The specified product is not in the user's cart"
                ]
            }
        }
