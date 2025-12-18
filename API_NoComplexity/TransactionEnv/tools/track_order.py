# Copyright TransactionEnv

import json
from typing import Any, Dict, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import find_order_by_id


class TrackOrder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str) -> str:
        """
        Track the shipping status of an order.
        
        Args:
            data: The data dictionary containing orders
            order_id: ID of the order to track
            
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
        
        if not order_id:
            return json.dumps({
                "success": False,
                "message": "Order ID is required."
            })
        
        # Get the order, ensuring it belongs to the current user
        order = find_order_by_id(data, order_id, current_user)
        
        if not order:
            return json.dumps({
                "success": False,
                "message": f"Order with ID '{order_id}' not found or does not belong to the current user."
            })
        
        # Get shipping information
        shipping = order.get("shipping", {})
        status = shipping.get("status", "unknown")
        tracking_number = shipping.get("tracking_number", "")
        estimated_delivery = shipping.get("estimated_delivery", "")
        delivered_at = shipping.get("delivered_at", "")
        
        # Check if the order has been shipped
        if status == "processing":
            return json.dumps({
                "success": True,
                "tracking": {
                    "order_id": order_id,
                    "status": status,
                    "tracking_number": tracking_number,
                    "message": "Your order is being processed and will ship soon."
                },
                "message": "Your order is being processed."
            })
        elif status == "shipped" or status == "in_transit":
            # Provide tracking details
            return json.dumps({
                "success": True,
                "tracking": {
                    "order_id": order_id,
                    "status": status,
                    "tracking_number": tracking_number,
                    "estimated_delivery": estimated_delivery,
                    "message": f"Your order is {status} and expected to arrive soon."
                },
                "message": f"Order {order_id} is {status}."
            })
        elif status == "out_for_delivery":
            return json.dumps({
                "success": True,
                "tracking": {
                    "order_id": order_id,
                    "status": status,
                    "tracking_number": tracking_number,
                    "message": "Your order is out for delivery today."
                },
                "message": "Your order is out for delivery today."
            })
        elif status == "delivered":
            return json.dumps({
                "success": True,
                "tracking": {
                    "order_id": order_id,
                    "status": status,
                    "tracking_number": tracking_number,
                    "delivered_at": delivered_at,
                    "message": f"Your order was delivered on {delivered_at}."
                },
                "message": f"Order {order_id} was delivered on {delivered_at}."
            })
        elif status == "cancelled":
            return json.dumps({
                "success": True,
                "tracking": {
                    "order_id": order_id,
                    "status": status,
                    "message": "This order was cancelled."
                },
                "message": "This order was cancelled and will not be shipped."
            })
        else:
            return json.dumps({
                "success": True,
                "tracking": {
                    "order_id": order_id,
                    "status": status,
                    "message": "Tracking information is not available for this order."
                },
                "message": "Unable to retrieve detailed tracking information."
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "track_order",
                "description": "Track the shipping status of a specific order. Provides current status, tracking number, and estimated delivery date if available.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The unique ID of the order to track."
                        }
                    },
                    "required": ["order_id"]
                },
                "error_cases": [
                    "No current user: Order operations require a logged-in user",
                    "Missing order ID: The order ID parameter is not provided",
                    "Order not found: No order exists with the specified ID for the current user",
                    "Not shipped: The order has not been shipped yet, so tracking information is limited"
                ]
            }
        }
