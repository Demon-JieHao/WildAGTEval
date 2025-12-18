# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import find_restaurant_by_id, get_current_timestamp, generate_order_id


class PlaceDeliveryOrder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], restaurant_id: str, items: List[Dict[str, Any]], 
               delivery_address: Dict[str, Any], special_instructions: Optional[str] = None,
               tip_percentage: Optional[float] = 15.0) -> str:
        """
        Place a food delivery order from a restaurant.
        
        Args:
            data: The data dictionary
            restaurant_id: ID of the restaurant to order from
            items: List of items to order with quantities
            delivery_address: Address for delivery
            special_instructions: Special instructions for the delivery
            tip_percentage: Percentage of subtotal to add as tip
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_system_failure_error_enabled = os.getenv('ENABLE__SYSTEM_FAILURE_ERROR__PLACE_DELIVERY_ORDER', 'false').lower() == 'true'
        
        # Input validation
        if not restaurant_id:
            return json.dumps({
                "success": False,
                "message": "Restaurant ID is required"
            })
            
        if not items or len(items) == 0:
            return json.dumps({
                "success": False,
                "message": "At least one item is required"
            })
            
        if not delivery_address:
            return json.dumps({
                "success": False,
                "message": "Delivery address is required"
            })
            
        if tip_percentage is not None and (tip_percentage < 0 or tip_percentage > 30):
            return json.dumps({
                "success": False,
                "message": "Tip percentage must be between 0 and 30"
            })
        
        # Check if the current user is set
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user is currently selected"
            })
        
        # Find the restaurant
        restaurant = find_restaurant_by_id(data, restaurant_id)
        if not restaurant:
            return json.dumps({
                "success": False,
                "message": f"Restaurant with ID '{restaurant_id}' not found"
            })
            
        if not restaurant.get("delivery_available", False):
            return json.dumps({
                "success": False,
                "message": f"Restaurant '{restaurant.get('name')}' does not offer delivery"
            })
        
        # Validate items and calculate subtotal
        valid_items = []
        subtotal = 0.0
        menu_items = restaurant.get("menu", [])
        menu_item_dict = {item["item_id"]: item for item in menu_items}
        
        for order_item in items:
            item_id = order_item.get("item_id")
            quantity = order_item.get("quantity", 1)
            
            if not item_id:
                return json.dumps({
                    "success": False,
                    "message": "Item ID is required for each item"
                })
                
            if quantity <= 0:
                return json.dumps({
                    "success": False,
                    "message": f"Quantity must be positive for item ID '{item_id}'"
                })
                
            menu_item = menu_item_dict.get(item_id)
            if not menu_item:
                return json.dumps({
                    "success": False,
                    "message": f"Item with ID '{item_id}' not found in the restaurant's menu"
                })
            
            # Calculate item total
            item_price = menu_item.get("price", 0) * quantity
            subtotal += item_price
            
            # Add to valid items list
            valid_items.append({
                "item_id": item_id,
                "name": menu_item.get("name"),
                "quantity": quantity,
                "price": item_price,
                "special_instructions": order_item.get("special_instructions", "")
            })
        
        # Calculate taxes, delivery fee, and total
        tax_rate = 0.0875  # 8.75% tax rate
        taxes = round(subtotal * tax_rate, 2)
        delivery_fee = 5.99
        tip = round(subtotal * (tip_percentage / 100), 2) if tip_percentage is not None else 0.0
        total = subtotal + taxes + delivery_fee + tip
        
        # Generate a sequential order ID
        order_id = generate_order_id(data)
        
        ### ADDED: Simulate payment gateway infrastructure failure when uncertainty is enabled ###
        if uncertainty_system_failure_error_enabled:
            # Deterministic failure scenario (no randomization)
            error_scenario = {
                "error": "PAYMENT_GATEWAY_TLS_HANDSHAKE_FAILURE",
                "message": "SSL/TLS handshake failed during payment authorization: Certificate chain validation error at depth 2, issuer CN=DigiCert Global Root G2, subject CN=DigiCert TLS RSA SHA256 2020 CA1, OCSP responder timeout after 5000ms, fallback to CRL failed with HTTP 503, cipher suite negotiation failed on TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
                "error_code": "PCI_DSS_4.0_REQ_4.2.1_VIOLATION",
                "gateway_node": "payment-gateway-prod-us-east-1b.internal",
                "correlation_id": "fixed-correlation-12345-67890",  # Fixed instead of uuid
                "pci_compliance_note": "Transaction rollback initiated per PCI-DSS v4.0 requirement 4.2.1 - strong cryptography required",
                "datacenter": "us-east-1b",
                "service_version": "payment-service:v3.14.2"
            }
            
            return json.dumps({
                "success": False,
                **error_scenario
            })
        ### END ADDED ###
        
        # Create the new order
        current_time = get_current_timestamp()
        new_order = {
            "order_id": order_id,
            "user_id": current_user,
            "restaurant_id": restaurant_id,
            "order_time": current_time,
            "delivery_address": delivery_address,
            "items": valid_items,
            "payment": {
                "subtotal": round(subtotal, 2),
                "tax": taxes,
                "delivery_fee": delivery_fee,
                "tip": tip,
                "total": round(total, 2)
            },
            "status": "placed",
            "status_updates": [
                {
                    "status": "placed",
                    "timestamp": current_time
                }
            ],
            "estimated_delivery_time": "",
            "delivery_notes": special_instructions or "",
            "driver_info": None
        }
        
        # Add order to data
        if "delivery_orders" not in data:
            data["delivery_orders"] = []
            
        data["delivery_orders"].append(new_order)
        
        # Success response
        return json.dumps({
            "success": True,
            "order_id": order_id,
            "restaurant_name": restaurant.get("name"),
            "order_time": current_time,
            "status": "placed",
            "items_count": len(valid_items),
            "subtotal": round(subtotal, 2),
            "tax": taxes,
            "delivery_fee": delivery_fee,
            "tip": tip,
            "total": round(total, 2),
            "message": "Your order has been placed successfully"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "place_delivery_order",
                "description": "Place a food delivery order from a restaurant. The order will be processed and delivered to the specified address.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "restaurant_id": {
                            "type": "string",
                            "description": "The unique identifier of the restaurant to order from."
                        },
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "item_id": {
                                        "type": "string",
                                        "description": "The unique identifier of the menu item."
                                    },
                                    "quantity": {
                                        "type": "integer",
                                        "description": "The quantity of this item to order."
                                    },
                                    "special_instructions": {
                                        "type": "string",
                                        "description": "(Optional) Special instructions for preparing this item."
                                    }
                                },
                                "required": ["item_id", "quantity"]
                            },
                            "description": "List of items to order with their quantities and optional special instructions."
                        },
                        "delivery_address": {
                            "type": "object",
                            "properties": {
                                "street": {
                                    "type": "string",
                                    "description": "Street address for delivery."
                                },
                                "city": {
                                    "type": "string",
                                    "description": "City for delivery."
                                },
                                "state": {
                                    "type": "string",
                                    "description": "State for delivery."
                                },
                                "zip": {
                                    "type": "string",
                                    "description": "ZIP or postal code for delivery."
                                },
                                "special_instructions": {
                                    "type": "string",
                                    "description": "(Optional) Special instructions for delivery location."
                                }
                            },
                            "required": ["street", "city", "zip"],
                            "description": "Address where the order should be delivered."
                        },
                        "special_instructions": {
                            "type": "string",
                            "description": "(Optional) General special instructions for the entire order."
                        },
                        "tip_percentage": {
                            "type": "number",
                            "description": "(Optional) Percentage of subtotal to add as tip. Defaults to 15%."
                        }
                    },
                    "required": ["restaurant_id", "items", "delivery_address"]
                },
                "error_cases": [
                    "Restaurant ID is missing: The restaurant_id parameter is required.",
                    "Restaurant not found: No restaurant exists with the provided ID.",
                    "Restaurant doesn't offer delivery: The selected restaurant does not provide delivery service.",
                    "No items specified: At least one item must be included in the order.",
                    "Invalid item: One or more items are not found in the restaurant's menu.",
                    "Invalid quantity: Item quantities must be positive numbers.",
                    "Delivery address missing: A valid delivery address is required.",
                    "Invalid tip percentage: Tip percentage must be between 0 and 30.",
                    "No user selected: A user must be selected to place an order."
                ]
            }
        }
