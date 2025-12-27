# Copyright TransactionEnv

import json
import re
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
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_feature_limitation_error_enabled = os.getenv('ENABLE__FEATURE_LIMITATION_ERROR__TRACK_ORDER', 'false').lower() == 'true'
        uncertainty_adhoc_enabled = os.getenv('ENABLE__ADHOC__TRACK_ORDER', 'false').lower() == 'true'

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
            
        # Validate order ID format (must be carrier-suffix)
        if uncertainty_adhoc_enabled:
            if "-" not in order_id:
                return json.dumps({
                    "success": False,
                    # "message": "Invalid order ID format. Order ID must be in the format 'CARRIER-SUFFIX'."
                    "message": "Invalid order ID format."
                })
        
        # Get carrier from order_id
        provided_carrier = order_id.split("-", 1)[0]
        
        ### ADDED: Feature limitation check - ALL carriers temporarily unavailable ###
        if uncertainty_feature_limitation_error_enabled:
            alternative_carriers = ["SwiftShip", "RapidCargo"]
            
            return json.dumps({
                "success": False,
                "message": f"{provided_carrier} tracking temporarily unavailable. It may have been changed to other shipping carriers like {', '.join(alternative_carriers)}"
            })
        ### END ADDED ###
        
        # Get the order, ensuring it belongs to the current user
        order = find_order_by_id(data, order_id, current_user)
        
        if uncertainty_adhoc_enabled:
            if order:
                # Verify the carrier matches the one in the order
                shipping = order.get("shipping", {})
                actual_carrier = shipping.get("carrier", "")
                
                if actual_carrier and provided_carrier != actual_carrier:
                    return json.dumps({
                        "success": False,
                        "message": f"Invalid order ID."
                    })
        
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
    def transform(input_value: str, data: Dict[str, Any] = None) -> str:
        """
        Convert an order ID to the required format (carrier-order_id_part).
        
        The following rules are applied:
        1. Transform the order_id parameter value inside an invoke_tool string.
        2. Look up the actual shipping carrier for the order in the data and adjust the format.
        
        Args:
            input_value: order ID or invoke_tool statement
            data: Database object 
                
        Returns:
            The transformed order ID or invoke_tool string
        """
        # 1. Handle invoke_tool strings
        if isinstance(input_value, str) and "invoke_tool" in input_value and "order_id=" in input_value:
            # Extract order_id parameter (supports both single and double quotes)
            order_id_pattern = r'order_id=["\']([^"\']+)["\']'
            match = re.search(order_id_pattern, input_value)
            
            if match:
                original_order_id = match.group(1)
                transformed_order_id = TrackOrder.transform(original_order_id, data)
                
                # replace with the transformed order_id
                if original_order_id != transformed_order_id:
                    if 'order_id="' in input_value:
                        return input_value.replace(f'order_id="{original_order_id}"', 
                                                f'order_id="{transformed_order_id}"')
                    else:
                        return input_value.replace(f"order_id='{original_order_id}'", 
                                                f"order_id='{transformed_order_id}'")
        
        # 2. Handle a plain order ID
        if isinstance(input_value, str):
            original_order_id = input_value
            order_suffix = ""
            raw_order_id = ""
            
            # 2.1 Check whether the ID already contains a hyphen
            if "-" in original_order_id:
                # If it's already in carrier-xxx format, split it
                parts = original_order_id.split("-", 1)
                if len(parts) == 2:
                    input_carrier = parts[0]  # Carrier code from input
                    order_suffix = parts[1]   # Order ID suffix
            else:
                # If this is a regular order ID
                raw_order_id = original_order_id
                # Use order_id[2:] to generate the suffix
                if len(original_order_id) > 2:
                    order_suffix = original_order_id[2:]
                else:
                    order_suffix = original_order_id
            
            # 2.2 Determine the actual shipping carrier from the order data
            if data and "orders" in data:
                # If order data is available
                
                # Search by original order ID
                for order in data["orders"]:
                    # Find the entry whose order_id matches
                    if order.get("order_id") == raw_order_id or order.get("order_id") == original_order_id:
                        # Check shipping information
                        shipping = order.get("shipping", {})
                        actual_carrier = shipping.get("carrier", "UPS")  # Actual shipping carrier
                        
                        # Convert to carrier-suffix format
                        return f"{actual_carrier}-{order_suffix}"
                
                # If no order is found but the ID already contains a hyphen, keep the original format
                if "-" in original_order_id:
                    return original_order_id
            else:
                # If there is no order data, keep the original if it already contains a hyphen
                if "-" in original_order_id:
                    return original_order_id
        
        # If no transformation is possible, return the original value
        return input_value

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
                            "description": "The unique ID of the order to track. This ID is prefixed with the shipping carrier code followed by a hyphen and the order suffix (e.g., 'UPS-345', 'FDX-678'). The suffix is typically extracted from the original order ID by excluding the initial characters (e.g., for order_id '12345', suffix is '345'; for order_id '345678', suffix is '5678')."
                            # "The suffix is typically extracted from the original order ID (e.g., for order_id '12345', suffix would be '345')."
                        }
                    },
                    "required": ["order_id"]
                },
                "error_cases": [
                    "No current user: Order operations require a logged-in user",
                    "Missing order ID: The order ID parameter is not provided",
                    "Order not found: No order exists with the specified ID for the current user",
                    "Not shipped: The order has not been shipped yet, so tracking information is limited",
                    "Invalid order ID format: Order ID must be in the format 'CARRIER-SUFFIX' where CARRIER is the shipping carrier code and SUFFIX is part of the original order ID."
                ]
            }
        }
