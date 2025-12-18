# Copyright TransactionEnv

import json
from typing import Any, Dict, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import find_order_by_id, get_current_timestamp


class CancelOrder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str, reason: Optional[str] = None) -> str:
        """
        Cancel an existing order if it's in a cancellable state.
        
        Args:
            data: The data dictionary containing orders
            order_id: ID of the order to cancel
            reason: Optional reason for cancellation
            
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
        
        # Find the order (ensuring it belongs to the current user)
        order = find_order_by_id(data, order_id, current_user)
        
        if not order:
            return json.dumps({
                "success": False,
                "message": f"Order with ID '{order_id}' not found or does not belong to the current user."
            })
        
        # Check if the order can be cancelled (only if status is pending or processing)
        status = order.get("status", "")
        if status not in ["pending", "processing"]:
            return json.dumps({
                "success": False,
                "message": f"Cannot cancel order with status '{status}'. Only orders in 'pending' or 'processing' status can be cancelled."
            })
        
        # Process cancellation
        timestamp = get_current_timestamp()
        
        # Update order status to cancelled
        order["status"] = "cancelled"
        
        # Update shipping status
        if "shipping" in order:
            order["shipping"]["status"] = "cancelled"
        
        # Process refund if payment was already made
        payment = order.get("payment", {})
        if payment.get("status") == "paid":
            payment["status"] = "refunded"
            payment["refunded_at"] = timestamp
            
            # Add cancellation details
            order["cancellation"] = {
                "reason": reason or "User requested cancellation",
                "cancelled_at": timestamp,
                "refunded": True
            }
            
            return json.dumps({
                "success": True,
                "order_id": order_id,
                "status": "cancelled",
                "refunded": True,
                "message": f"Order {order_id} has been cancelled and payment has been refunded."
            })
        else:
            # Add cancellation details without refund
            order["cancellation"] = {
                "reason": reason or "User requested cancellation",
                "cancelled_at": timestamp,
                "refunded": False
            }
            
            return json.dumps({
                "success": True,
                "order_id": order_id,
                "status": "cancelled",
                "refunded": False,
                "message": f"Order {order_id} has been cancelled."
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "cancel_order",
                "description": "Cancel an existing order if it's in a cancellable state (pending or processing). If payment was made, it will be refunded.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The unique ID of the order to cancel."
                        },
                        "reason": {
                            "type": "string",
                            "description": "(Optional) Reason for cancellation."
                        }
                    },
                    "required": ["order_id"]
                },
                "error_cases": [
                    "No current user: Order operations require a logged-in user",
                    "Missing order ID: The order ID parameter is not provided", 
                    "Order not found: No order exists with the specified ID for the current user",
                    "Cannot cancel: Orders that have been shipped, delivered, or already cancelled cannot be cancelled"
                ]
            }
        }
