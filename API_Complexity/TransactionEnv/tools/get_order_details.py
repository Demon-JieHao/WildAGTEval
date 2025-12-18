# Copyright TransactionEnv

import json
from typing import Any, Dict, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import find_order_by_id


class GetOrderDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str) -> str:
        """
        Get detailed information about a specific order.
        
        Args:
            data: The data dictionary containing orders
            order_id: ID of the order to retrieve
            
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
        
        # Get the order details, ensuring it belongs to the current user
        order = find_order_by_id(data, order_id, current_user)
        # del(order["shipping"]["carrier"])
        order.pop("shipping", None)
        order.pop("status", None)
        order.pop("status_history", None)
        order.pop("cancellation", None)        

        if not order:
            return json.dumps({
                "success": False,
                "message": f"Order with ID '{order_id}' not found or does not belong to the current user."
            })
        
        # Return the full order details
        return json.dumps({
            "success": True,
            "order": order,
            "message": f"Retrieved details for order {order_id}"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_order_details",
                "description": "Get detailed information about a specific order by its ID. Returns comprehensive order details including items purchased, and payment information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The unique ID of the order to retrieve details for."
                        }
                    },
                    "required": ["order_id"]
                },
                "error_cases": [
                    "No current user: Order operations require a logged-in user",
                    "Missing order ID: The order ID parameter is not provided",
                    "Order not found: No order exists with the specified ID for the current user"
                ]
            }
        }
