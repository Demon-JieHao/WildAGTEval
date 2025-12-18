# Copyright CulinaryControlEnv

"""
Uncertainty Manifestation: Confusion Between Order Placement Functions

Description:
Developers using the CulinaryControlEnv API face significant confusion due to the existence of 
multiple similarly-named order placement functions that handle different order types but share 
similar parameters. The primary function `place_delivery_order` handles food delivery to a customer's 
address, while `place_pickup_order` handles customer pickup orders, and this function 
`place_restaurant_order` handles dine-in reservations with pre-orders. Despite their similar 
names and parameter structures, these functions have fundamentally different behaviors, side 
effects, and requirements. Developers frequently use the wrong function for their intended use 
case, leading to unexpected behaviors in production environments.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool


class PlaceRestaurantOrder(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "place_restaurant_order",
                "description": "Place a pre-order for dine-in with reservation at a restaurant. The order will be processed and prepared for the customer's arrival.",
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
                            "description": "List of items to pre-order with their quantities and optional special instructions."
                        },
                        "reservation_details": {
                            "type": "object",
                            "properties": {
                                "reservation_time": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "The time of the reservation."
                                },
                                "party_size": {
                                    "type": "integer",
                                    "description": "Number of people in the party."
                                },
                                "seating_preferences": {
                                    "type": "string",
                                    "description": "(Optional) Preferences for seating location."
                                }
                            },
                            "required": ["reservation_time", "party_size"],
                            "description": "Details about the reservation."
                        },
                        "special_instructions": {
                            "type": "string",
                            "description": "(Optional) General special instructions for the entire order."
                        },
                        "gratuity_percentage": {
                            "type": "number",
                            "description": "(Optional) Percentage of subtotal to add as gratuity. Defaults to 18%."
                        }
                    },
                    "required": ["restaurant_id", "items", "reservation_details"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], restaurant_id: str, items: List[Dict[str, Any]],
              reservation_details: Dict[str, Any], special_instructions: Optional[str] = None,
              gratuity_percentage: Optional[float] = 18.0) -> str:
        """
        Place a pre-order for dine-in with reservation at a restaurant.
        
        Args:
            data: The data dictionary
            restaurant_id: ID of the restaurant to order from
            items: List of items to pre-order with quantities
            reservation_details: Details about the reservation (time, party size, etc.)
            special_instructions: Special instructions for the order
            gratuity_percentage: Percentage of subtotal to add as gratuity
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if not restaurant_id:
            return json.dumps({"success": False, "error": "Restaurant ID is missing"})
            
        if restaurant_id not in data.get("restaurants", {}):
            return json.dumps({"success": False, "error": "Restaurant not found"})
            
        restaurant = data["restaurants"][restaurant_id]
        if not restaurant.get("accepts_reservations", False):
            return json.dumps({"success": False, "error": "Restaurant doesn't accept reservations"})
            
        if not items or len(items) == 0:
            return json.dumps({"success": False, "error": "No items specified"})
            
        # Validate reservation details
        if not reservation_details:
            return json.dumps({"success": False, "error": "Reservation details missing"})
            
        reservation_time = reservation_details.get("reservation_time")
        party_size = reservation_details.get("party_size", 0)
        
        if not reservation_time:
            return json.dumps({"success": False, "error": "Reservation time missing"})
        
        if isinstance(reservation_time, str):
            try:
                reservation_time = datetime.fromisoformat(reservation_time)
            except ValueError:
                return json.dumps({"success": False, "error": "Invalid reservation time format"})
                
        current_time = datetime.now()
        if reservation_time < current_time:
            return json.dumps({"success": False, "error": "Reservation time must be in the future"})
            
        if party_size <= 0:
            return json.dumps({"success": False, "error": "Invalid party size"})
            
        if gratuity_percentage < 0 or gratuity_percentage > 30:
            return json.dumps({"success": False, "error": "Invalid gratuity percentage"})
            
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
            
        # Calculate gratuity
        gratuity = subtotal * (gratuity_percentage / 100)
            
        # Create the reservation and pre-order
        reservation_id = f"res-{restaurant_id}-{int(current_time.timestamp())}"
        
        reservation = {
            "reservation_id": reservation_id,
            "type": "dine-in",
            "restaurant_id": restaurant_id,
            "restaurant_name": restaurant.get("name", "Unknown Restaurant"),
            "items": order_items,
            "subtotal": subtotal,
            "tax": subtotal * 0.0725,  # 7.25% tax rate example
            "gratuity": gratuity,
            "total": subtotal * 1.0725 + gratuity,  # Subtotal + tax + gratuity
            "reservation_time": reservation_time.isoformat() if isinstance(reservation_time, datetime) else reservation_time,
            "party_size": party_size,
            "seating_preferences": reservation_details.get("seating_preferences", ""),
            "special_instructions": special_instructions or "",
            "status": "confirmed",
            "created_at": current_time.isoformat()
        }
        
        # Save reservation to data
        if "reservations" not in data:
            data["reservations"] = {}
        data["reservations"][reservation_id] = reservation
        
        return json.dumps({
            "success": True,
            "reservation_id": reservation_id,
            "reservation": reservation
        })
