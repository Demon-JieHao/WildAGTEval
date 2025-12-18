# Copyright SmartHomeEnv

import json
from typing import Any, Dict
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class GetDeviceDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoint: str) -> str:
        """
        Get details about a specific device.
        
        Args:
            data: The data dictionary containing devices
            endpoint: The endpoint ID of the device
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoint:
            return json.dumps({
                "success": False,
                "message": "No device endpoint specified"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        device = find_device_by_endpoint(data, endpoint, home_id)
        
        if device:
            # Check if device has lock-related APIs
            supported_apis = device.get("supported_apis", [])
            lock_apis = ["lock_lock", "lock_unlock", "lock_status"]
            
            # Check if any lock-related API exists in device's supported APIs
            has_lock_api = any(api in lock_apis for api in supported_apis)
            
            if has_lock_api:
                return json.dumps({
                    "success": False,
                    "message": f"This device has lock-related APIs. Please use 'lock_status' tool for lock devices instead of 'get_device_details'."
                })
            else:
                return json.dumps({
                    "success": True,
                    "device": device
                })
        else:
            return json.dumps({
                "success": False,
                "message": f"Device with endpoint '{endpoint}' not found"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_device_details",
                "description": "Get details about a specific device. This tool retrieves comprehensive information about a device using its endpoint ID, including its name, supported APIs, group memberships, and current state.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoint": {
                            "type": "string",
                            "description": "The endpoint ID of the device to retrieve details for."
                        }
                    },
                    "required": ["endpoint"]
                },
                "error_cases": [
                    "No device endpoint specified: The endpoint parameter is empty or not provided.",
                    "Device not found: The specified endpoint does not exist in the current user's home.",
                    "No current user: No user is currently set in the system, so the home context cannot be determined."
                ]
            }
        }
