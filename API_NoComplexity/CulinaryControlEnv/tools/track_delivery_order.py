# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import find_delivery_order_by_id, find_restaurant_by_id


class TrackDeliveryOrder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], order_id: str) -> str:
        """
        Track the status and estimated delivery time of an order.
        
        Args:
            data: The data dictionary
            order_id: ID of the order to track
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_system_failure_error_enabled = os.getenv('ENABLE__SYSTEM_FAILURE_ERROR__TRACK_DELIVERY_ORDER', 'false').lower() == 'true'
        
        ### ADDED: Handle system failure error first (complete failure scenario) ###
        if uncertainty_system_failure_error_enabled:
            # Deterministic delivery tracking infrastructure failure scenarios
            failure_scenarios = [
                {
                    "error": "GPS_PROVIDER_API_CIRCUIT_BREAKER_OPEN",
                    "message": "MapBox Directions API v5 circuit breaker activated after 50 consecutive HTTP 503 responses within 30s window, fallback to Google Maps API failed with quota_exceeded (daily limit: 100000 requests, current: 100001), tertiary provider HERE Maps returning SSL handshake failures on certificate CN=*.api.here.com expired 2024-07-03T23:59:59Z",
                    "technical_details": {
                        "primary_provider": "mapbox",
                        "primary_error": "503 Service Unavailable",
                        "fallback_provider": "google_maps",
                        "fallback_error": "QUOTA_EXCEEDED",
                        "tertiary_provider": "here_maps",
                        "tertiary_error": "SSL_HANDSHAKE_FAILURE",
                        "circuit_breaker_status": "OPEN",
                        "failed_requests": 50,
                        "time_window": "30s"
                    },
                    "error_code": "GPS_CIRCUIT_BREAKER_001",
                    "severity": "CRITICAL",
                    "retry_after": 1800,
                    # "incident_id": "GPS-INC-2024-0704-002"
                },
                {
                    "error": "DELIVERY_TRACKING_MICROSERVICE_CASCADE_FAILURE",
                    "message": "Real-time location service mesh failure: order-tracking-service pod crash-looping with OOMKilled status, location-cache-redis returning NOAUTH authentication required, delivery-eta-calculator service timeout after 30s, driver-position-aggregator throwing java.net.ConnectException: Connection refused on port 8080",
                    "technical_details": {
                        "order_tracking_service": "crash-looping",
                        "location_cache_status": "NOAUTH",
                        "eta_calculator_timeout": "30s",
                        "driver_aggregator_error": "Connection refused",
                        "kubernetes_namespace": "delivery-prod",
                        "affected_pods": 4
                    },
                    "error_code": "MICROSERVICE_CASCADE_002",
                    "severity": "HIGH",
                    "retry_after": 1200,
                    # "incident_id": "TRACK-INC-2024-0704-003"
                }
            ]
            
            # Use deterministic failure selection
            failure = failure_scenarios[0]  # Always use GPS provider circuit breaker for consistency
            
            return json.dumps({
                "success": False,
                "error": failure["error"],
                "message": failure["message"],
                "technical_details": failure["technical_details"],
                "error_code": failure["error_code"],
                "severity": failure["severity"],
                "retry_after": failure["retry_after"],
                # "incident_id": failure["incident_id"],
                # "timestamp": "2024-07-04T17:52:47.123Z",
                "service": "CulinaryControlEnv.track_delivery_order",
                "correlation_id": "fixed-correlation-track-12345",
                "trace_id": "trace-track-67890"
            })
        # Input validation
        if not order_id:
            return json.dumps({
                "success": False,
                "message": "Order ID is required"
            })
        
        # Check if the current user is set
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user is currently selected"
            })
        
        # Find the order for the current user
        order = find_delivery_order_by_id(data, order_id, current_user)
        if not order:
            return json.dumps({
                "success": False,
                "message": f"Order with ID '{order_id}' not found or does not belong to the current user"
            })
        
        # Get the restaurant information
        restaurant_id = order.get("restaurant_id")
        restaurant = find_restaurant_by_id(data, restaurant_id)
        restaurant_name = restaurant.get("name") if restaurant else "Unknown Restaurant"
        
        # Get the current status and history
        current_status = order.get("status", "unknown")
        status_updates = order.get("status_updates", [])
        estimated_delivery_time = order.get("estimated_delivery_time", "")
        driver_info = order.get("driver_info")
        
        # Determine the delivery progress as a percentage
        progress_percentage = 0
        status_map = {
            "placed": 10,
            "confirmed": 20,
            "preparing": 40,
            "ready_for_pickup": 60,
            "out_for_delivery": 80,
            "delivered": 100,
            "cancelled": 0
        }
        
        progress_percentage = status_map.get(current_status, 0)
        
        # Create a formatted status message
        status_message = ""
        if current_status == "placed":
            status_message = "Order has been placed and is pending restaurant confirmation."
        elif current_status == "confirmed":
            status_message = "Order has been confirmed by the restaurant."
        elif current_status == "preparing":
            status_message = "Your food is being prepared by the restaurant."
        elif current_status == "ready_for_pickup":
            status_message = "Order is ready and waiting for driver pickup."
        elif current_status == "out_for_delivery":
            if driver_info:
                status_message = f"Your food is on the way. {driver_info.get('name')} is delivering your order in a {driver_info.get('vehicle')}."
            else:
                status_message = "Your food is on the way."
        elif current_status == "delivered":
            status_message = "Your order has been delivered. Enjoy your meal!"
        elif current_status == "cancelled":
            status_message = "This order has been cancelled."
        else:
            status_message = f"Order status: {current_status}"
        
        # Format the response
        return json.dumps({
            "success": True,
            "order_id": order_id,
            "restaurant_name": restaurant_name,
            "status": current_status,
            "status_message": status_message,
            "progress_percentage": progress_percentage,
            "status_history": status_updates,
            "estimated_delivery_time": estimated_delivery_time,
            "driver_info": driver_info,
            "message": f"Tracked order {order_id}: {status_message}"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "track_delivery_order",
                "description": "Track the status and estimated delivery time of an food delivery order. This tool provides real-time updates on the current status of a delivery order, including status history, driver information, and progress percentage.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "The unique identifier of the order to track."
                        }
                    },
                    "required": ["order_id"]
                },
                "error_cases": [
                    "Order ID is missing: The order_id parameter is required.",
                    "Order not found: No order exists with the provided ID for the current user.",
                    "No user selected: A user must be selected to track their orders."
                ]
            }
        }
