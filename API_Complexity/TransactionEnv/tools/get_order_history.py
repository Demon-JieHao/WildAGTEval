# Copyright TransactionEnv

import json
from typing import Any, Dict, List, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import get_user_orders


class GetOrderHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], limit: Optional[int] = None) -> str:
        """
        Get the order history for the current user.
        
        Args:
            data: The data dictionary containing orders
            limit: Maximum number of orders to return
            
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
        
        if limit is not None and limit < 1:
            return json.dumps({
                "success": False,
                "message": "Limit must be at least 1."
            })
        
        # Get the user's orders
        orders = get_user_orders(data, current_user, limit)
        
        # Format orders for display (compact version)
        formatted_orders = []
        for order in orders:
            formatted_orders.append({
                "order_id": order.get("order_id"),
                "created_at": order.get("created_at"),
                "total": order.get("total"),
                # "status": order.get("status"),
                "items_count": len(order.get("items", [])),
                # "shipping_status": order.get("shipping", {}).get("status"),
                "carrier": order.get("shipping", {}).get("carrier", "UPS")
            })
        
        return json.dumps({
            "success": True,
            "count": len(orders),
            "orders": formatted_orders,
            "message": f"Found {len(orders)} order(s)" if orders else "No orders found for the current user."
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_order_history",
                "description": "Get the order history for the current user. Returns a list of the user's past orders, sorted by creation date (newest first).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "(Optional) Maximum number of orders to return. If not provided, all orders will be returned."
                        }
                    }
                },
                "error_cases": [
                    "No current user: Order operations require a logged-in user",
                    "Invalid limit: Limit must be at least 1"
                ]
            }
        }
