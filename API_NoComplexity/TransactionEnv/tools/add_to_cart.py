# Copyright TransactionEnv

import json
from datetime import datetime
from typing import Any, Dict, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import find_product_by_id, get_user_cart, get_current_timestamp, update_cart_total


class AddToCart(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], product_id: str, quantity: int = 1) -> str:
        """
        Add a product to the user's shopping cart.
        
        Args:
            data: The data dictionary containing products and carts
            product_id: ID of the product to add
            quantity: Quantity to add (default: 1)
            
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
        
        # Find the product
        product = find_product_by_id(data, product_id)
        if not product:
            return json.dumps({
                "success": False,
                "message": f"Product with ID '{product_id}' not found"
            })
        
        # Check stock availability
        available_stock = product.get("stock", 0)
        if available_stock < quantity:
            return json.dumps({
                "success": False,
                "message": f"Not enough stock. Requested: {quantity}, Available: {available_stock}"
            })
        
        # Get the user's cart
        cart = get_user_cart(data, current_user)
        if not cart:
            return json.dumps({
                "success": False,
                "message": "Failed to retrieve cart."
            })
        
        # Check if the product is already in the cart
        cart_items = cart.get("items", [])
        for item in cart_items:
            if item.get("product_id") == product_id:
                # Calculate the new quantity
                new_quantity = item["quantity"] + quantity
                
                # Check if the new quantity exceeds available stock
                if new_quantity > available_stock:
                    return json.dumps({
                        "success": False,
                        "message": f"Not enough stock. Already in cart: {item['quantity']}, Trying to add: {quantity}, Available: {available_stock}"
                    })
                
                # Update the quantity
                item["quantity"] = new_quantity
                
                # Calculate new cart total
                update_cart_total(data, current_user)
                
                return json.dumps({
                    "success": True,
                    "product": {
                        "product_id": product_id,
                        "name": product.get("name"),
                        "quantity": new_quantity,
                        "price": product.get("price")
                    },
                    "cart_total": cart.get("total", 0),
                    "message": f"Updated quantity of '{product.get('name')}' to {new_quantity}"
                })
        
        # Product not in cart, add it
        new_item = {
            "product_id": product_id,
            "name": product.get("name"),
            "quantity": quantity,
            "price": product.get("price"),
            "added_at": get_current_timestamp()
        }
        
        cart_items.append(new_item)
        
        # Update the cart's total price
        update_cart_total(data, current_user)
        
        return json.dumps({
            "success": True,
            "product": {
                "product_id": product_id,
                "name": product.get("name"),
                "quantity": quantity,
                "price": product.get("price")
            },
            "cart_total": cart.get("total", 0),
            "message": f"Added {quantity} x '{product.get('name')}' to cart"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_to_cart",
                "description": "Add a product to the user's shopping cart. If the product is already in the cart, increases the quantity. Checks for stock availability before adding.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The unique ID of the product to add to the cart."
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "Quantity of the product to add (minimum 1). Defaults to 1 if not specified."
                        }
                    },
                    "required": ["product_id"]
                },
                "error_cases": [
                    "No current user: Cart operations require a logged-in user",
                    "Missing product ID: The product ID parameter is not provided",
                    "Invalid quantity: Quantity must be at least 1",
                    "Product not found: No product exists with the specified ID",
                    "Insufficient stock: The requested quantity exceeds available stock"
                ]
            }
        }
