# Copyright CulinaryControlEnv

"""
Uncertainty Manifestation: Confusion Between Order Placement Functions

Description:
Developers using the CulinaryControlEnv API face significant confusion due to the existence of 
multiple similarly-named order placement functions that handle different order types but share 
similar parameters. The primary function `place_delivery_order` handles food delivery to a customer's 
address, while this function `place_pickup_order` handles customer pickup orders, and 
`place_restaurant_order` handles dine-in reservations with pre-orders. Despite their similar 
names and parameter structures, these functions have fundamentally different behaviors, side 
effects, and requirements. Developers frequently use the wrong function for their intended use 
case, leading to unexpected behaviors in production environments.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool


class PlacePickupOrder(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "place_pickup_order",
                "description": "Place a food pickup order from a restaurant. The order will be processed and prepared for customer pickup at the specified time.",
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
                        "pickup_time": {
                            "type": "string",
                            "format": "date-time",
                            "description": "The time when the customer will pick up the order."
                        },
                        "special_instructions": {
                            "type": "string",
                            "description": "(Optional) General special instructions for the entire order."
                        }
                    },
                    "required": ["restaurant_id", "items", "pickup_time"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], restaurant_id: str, items: List[Dict[str, Any]],
              pickup_time: datetime, special_instructions: Optional[str] = None) -> str:
        """
        Place a food pickup order from a restaurant.
        
        Args:
            data: The data dictionary
            restaurant_id: ID of the restaurant to order from
            items: List of items to order with quantities
            pickup_time: The time when the customer will pick up the order
            special_instructions: Special instructions for the order
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if not restaurant_id:
            return json.dumps({"success": False, "error": "Restaurant ID is missing"})
            
        if restaurant_id not in data.get("restaurants", {}):
            return json.dumps({"success": False, "error": "Restaurant not found"})
            
        restaurant = data["restaurants"][restaurant_id]
        if not restaurant.get("offers_pickup", True):
            return json.dumps({"success": False, "error": "Restaurant doesn't offer pickup"})
            
        if not items or len(items) == 0:
            return json.dumps({"success": False, "error": "No items specified"})
            
        # Validate menu items
        menu = restaurant.get("menu", {})
        order_items = []
        subtotal = 0.0
        
        for item in items:
            item_id = item.get("item_id")
            quantity = item.get("quantity", 0)
            
            if not item_id or item_id not in menu:
                return json.dumps({"success": False, "error": f"Invalid item: {item_id}"})
                
            if quantity <= 0:
                return json.dumps({"success": False, "error": f"Invalid quantity for item {item_id}"})
                
            menu_item = menu[item_id]
            price = menu_item.get("price", 0.0) * quantity
            subtotal += price
            
            order_items.append({
                "item_id": item_id,
                "name": menu_item.get("name", "Unknown Item"),
                "quantity": quantity,
                "price": price,
                "special_instructions": item.get("special_instructions", "")
            })
            
        # Validate pickup time
        current_time = datetime.now()
        if not pickup_time:
            return json.dumps({"success": False, "error": "Pickup time missing"})
            
        if pickup_time < current_time:
            return json.dumps({"success": False, "error": "Pickup time must be in the future"})
            
        # TODO: Check restaurant hours
        
        # Create the order
        order_id = f"pickup-{restaurant_id}-{int(current_time.timestamp())}"
        
        order = {
            "order_id": order_id,
            "type": "pickup",
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant.get("name", "Unknown Restaurant"),
            "items": order_items,
            "subtotal": subtotal,
            "tax": subtotal * 0.0725,  # 7.25% tax rate example
            "total": subtotal * 1.0725,  # Subtotal + tax
            "pickup_time": pickup_time.isoformat(),
            "special_instructions": special_instructions or "",
            "status": "placed",
            "created_at": current_time.isoformat()
        }
        
        # Save order to data
        if "orders" not in data:
            data["orders"] = {}
        data["orders"][order_id] = order
        
        return json.dumps({
            "success": True,
            "order_id": order_id,
            "order": order
        })
