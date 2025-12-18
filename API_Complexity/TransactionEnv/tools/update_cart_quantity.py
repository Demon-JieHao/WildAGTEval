# Copyright TransactionEnv

import json
from typing import Any, Dict
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import get_user_cart, update_cart_total, find_product_by_id


class UpdateCartQuantity(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], product_id: str, quantity: int) -> str:
        """
        Update the quantity of a product in the user's shopping cart.
        
        Args:
            data: The data dictionary containing carts and products
            product_id: ID of the product to update
            quantity: New quantity to set (must be at least 1)
            
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
        
        if quantity < 1:
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
        
        # Find the product to verify stock
        product = find_product_by_id(data, product_id)
        if not product:
            return json.dumps({
                "success": False,
                "message": f"Product with ID '{product_id}' not found in database"
            })
            
        # Check stock availability
        available_stock = product.get("stock", 0)
        if quantity > available_stock:
            return json.dumps({
                "success": False,
                "message": f"Not enough stock. Requested: {quantity}, Available: {available_stock}"
            })
        
        # Check if the product is in the cart
        cart_items = cart.get("items", [])
        for item in cart_items:
            if item.get("product_id") == product_id:
                old_quantity = item.get("quantity", 0)
                item["quantity"] = quantity
                
                # Update the cart total
                update_cart_total(data, current_user)
                
                return json.dumps({
                    "success": True,
                    "product": {
                        "product_id": product_id,
                        "name": item.get("name", "Product"),
                        "quantity": quantity,
                        "old_quantity": old_quantity
                    },
                    "cart_total": cart.get("total", 0),
                    "message": f"Updated quantity of '{item.get('name')}' from {old_quantity} to {quantity}"
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
                "name": "update_cart_quantity",
                "description": "Update the quantity of a product in the user's shopping cart. Checks for stock availability before updating.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The unique ID of the product in the cart to update."
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "The new quantity to set for the product (minimum 1)."
                        }
                    },
                    "required": ["product_id", "quantity"]
                },
                "error_cases": [
                    "No current user: Cart operations require a logged-in user",
                    "Missing product ID: The product ID parameter is not provided",
                    "Invalid quantity: Quantity must be at least 1",
                    "Product not found: The specified product does not exist in the database",
                    "Product not in cart: The specified product is not in the user's cart",
                    "Insufficient stock: The requested quantity exceeds available stock"
                ]
            }
        }
