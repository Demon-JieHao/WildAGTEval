# Copyright TransactionEnv

import json
from typing import Any, Dict, List, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import (
    get_user_cart, find_product_by_id, get_user_payment_methods,
    get_user_addresses, generate_order_id, get_current_timestamp
)


class Checkout(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], payment_method_id: Optional[str] = None,
               address_id: Optional[str] = None, shipping_carrier: Optional[str] = "STD") -> str:
        """
        Process checkout for the current user's cart.
        
        Args:
            data: The data dictionary containing carts, products, and orders
            payment_method_id: ID of the payment method to use
            address_id: ID of the shipping address to use
            shipping_carrier: Shipping carrier to use for the order
            
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
        
        # Check if cart is empty
        if not cart.get("items", []):
            return json.dumps({
                "success": False,
                "message": "Cannot checkout with an empty cart."
            })
        
        ##############################################################################
        # # Validate payment method
        # if not payment_method_id:
        #     return json.dumps({
        #         "success": False,
        #         "message": "Payment method ID is required."
        #     })
        
        if not payment_method_id:
            payment_methods = get_user_payment_methods(data, current_user)
            payment_method = next((pm for pm in payment_methods if pm.get("id") == payment_methods[0].get("id")), None)  
            payment_method_id = payment_method.get("id")
            print("GET")     

        if not address_id:
            address = get_user_addresses(data, current_user)[0]
            address_id = address.get("id")
            
        payment_methods = get_user_payment_methods(data, current_user)
        payment_method = next((pm for pm in payment_methods if pm.get("id") == payment_method_id), None)
        if not payment_method:
            return json.dumps({
                "success": False,
                "message": f"Payment method with ID '{payment_method_id}' not found."
            })
        
        # # Validate shipping address
        # if not address_id:
        #     return json.dumps({
        #         "success": False,
        #         "message": "Shipping address ID is required."
        #     })
        
        addresses = get_user_addresses(data, current_user)
        address = next((addr for addr in addresses if addr.get("id") == address_id), None)
        if not address:
            return json.dumps({
                "success": False,
                "message": f"Address with ID '{address_id}' not found."
            })
        ##############################################################################
        
        # Verify product availability and update stock
        items_for_order = []
        stock_issues = []
        
        for item in cart.get("items", []):
            product_id = item.get("product_id")
            quantity = item.get("quantity", 0)
            
            # Find the product
            product = find_product_by_id(data, product_id)
            if not product:
                stock_issues.append({
                    "product_id": product_id,
                    "name": item.get("name", "Unknown Product"),
                    "requested": quantity,
                    "available": 0,
                    "issue": "Product not found"
                })
                continue
            
            # Check stock
            available_stock = product.get("stock", 0)
            if quantity > available_stock:
                stock_issues.append({
                    "product_id": product_id,
                    "name": product.get("name", "Unknown Product"),
                    "requested": quantity,
                    "available": available_stock,
                    "issue": "Insufficient stock"
                })
                continue
            
            # Decrease product stock
            product["stock"] = available_stock - quantity
            
            # Add to order items
            items_for_order.append({
                "product_id": product_id,
                "name": product.get("name"),
                "quantity": quantity,
                "price": product.get("price")
            })
        
        # If there are stock issues, abort checkout
        if stock_issues:
            return json.dumps({
                "success": False,
                "message": "Cannot complete checkout due to stock issues.",
                "stock_issues": stock_issues
            })
        
        # All validation successful, create the order
        timestamp = get_current_timestamp()
        order_id = generate_order_id(data)
        
        # Process payment (simulated)
        payment_info = {
            "method_id": payment_method_id,
            "method_type": payment_method.get("type"),
            "last4": payment_method.get("last4"),
            "status": "paid",
            "transaction_id": f"tx{order_id[5:]}",  # Use part of order_id as transaction_id
            "paid_at": timestamp
        }
        
        shipping_info = {
            "address_id": address_id,
            "address": {
                "street": address.get("street"),
                "city": address.get("city"),
                "state": address.get("state", ""),
                "zip": address.get("zip"),
                "country": address.get("country")
            },
            "carrier": shipping_carrier,
            "status": "processing",
            "tracking_number": f"TRK{order_id[5:]}",  # Use part of order_id as tracking number
            "estimated_delivery": ""  # This would be calculated based on shipping method
        }
        
        # Create the order object
        order = {
            "order_id": order_id,
            "user_id": current_user,
            "items": items_for_order,
            "total": cart.get("total", 0),
            "payment": payment_info,
            "shipping": shipping_info,
            "status": "processing",
            "created_at": timestamp
        }
        
        # Add order to orders list
        if "orders" not in data:
            data["orders"] = []
        
        data["orders"].append(order)
        
        # Clear the cart
        cart["items"] = []
        cart["total"] = 0
        
        # Return success response
        return json.dumps({
            "success": True,
            "order_id": order_id,
            "total": order["total"],
            "status": order["status"],
            "items_count": len(items_for_order),
            "message": f"Order {order_id} created successfully. Your payment of ${order['total']:.2f} has been processed. Your order will be shipped via {shipping_carrier}."
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "checkout",
                "description": "Process checkout for the user's cart, creating an order and processing payment. Verifies stock availability, creates an order record, processes payment, and clears the cart.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "payment_method_id": {
                            "type": "string",
                            "description": "ID of the payment method to use for the order."
                        },
                        "address_id": {
                            "type": "string",
                            "description": "ID of the shipping address to use for the order."
                        },
                        "shipping_carrier": {
                            "type": "string",
                            "description": "Shipping carrier to use for the order. Examples: UPS, DHL. Defaults to STD."
                        }
                    }
                },
                "error_cases": [
                    "No current user: Checkout requires a logged-in user",
                    "Empty cart: Cannot checkout with an empty cart",
                    "Invalid payment method: The specified payment method ID doesn't exist for the user",
                    "Invalid shipping address: The specified address ID doesn't exist for the user",
                    "Stock issues: Some products are no longer available in the requested quantities"
                ]
            }
        }
