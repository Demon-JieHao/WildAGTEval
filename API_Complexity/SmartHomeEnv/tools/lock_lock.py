# Copyright SmartHomeEnv

import os
import json
import re
from typing import Any, Dict, List
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class LockLock(Tool):
    @staticmethod
    def transform(input_value: str, data: Dict[str, Any] = None) -> str:
        """Convert a device endpoint ID into the required format `[device_name]_[id]`.
        
        Rules:
        1. If the value is already in the correct format `[device_name]_[id]`, return it as-is.
        2. If only an ID is provided, look up the device in `devices.json` and prepend the device name.
        3. Support transforming `endpoints` parameter values inside an `invoke_tool` expression.
        
        Args:
            input_value: Value to transform (endpoint ID or `invoke_tool` string)
            
        Returns:
            Transformed endpoint ID or transformed `invoke_tool` string
        """
        # Handle `invoke_tool` strings
        if isinstance(input_value, str) and "invoke_tool" in input_value and "endpoints=" in input_value:
            # Extract the endpoints array
            endpoints_pattern = r'endpoints=\[(.*?)\]'
            match = re.search(endpoints_pattern, input_value)
            
            if match:
                endpoints_str = match.group(1)
                # Extract each endpoint
                endpoint_ids = re.findall(r'["\']([^"\']+)["\']', endpoints_str)
                
                # Transform each endpoint
                transformed_ids = [LockLock.transform(endpoint_id) for endpoint_id in endpoint_ids]
                
                # Rebuild the array with transformed endpoints
                transformed_endpoints = ', '.join([f'"{endpoint}"' for endpoint in transformed_ids])
                transformed_array = f'[{transformed_endpoints}]'
                
                # Replace the original endpoints array with the transformed one
                return re.sub(r'endpoints=\[.*?\]', f'endpoints={transformed_array}', input_value)
        
        # Handle a single ID (if already in correct format, return as-is)
        if isinstance(input_value, str) and "_" not in input_value:
            try:
                # Load device information from devices.json
                with open("common/data/devices.json", "r") as f:
                    devices = json.load(f)
                
                # Search for the device by endpoint ID
                for device in devices:
                    if device.get("endpoint") == input_value:
                        # Remove spaces from device name and combine with ID
                        device_name = device.get("name", "").replace(" ", "")
                        return f"{device_name}_{input_value}"
            except Exception:
                # On file load failure or any error, return the original value
                pass
        
        # If no transformation can be applied, return the original value
        return input_value
    
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str]) -> str:
        """Lock one or more lock devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to lock
            
        Returns:
            A JSON string with the result of the operation
        """
        uncertainty_adhoc_enabled = os.getenv("ENABLE__ADHOC__LOCK_LOCK", "false").lower() == "true"

        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
            
        # Validate endpoint ID format when ad-hoc uncertainty is enabled
        if uncertainty_adhoc_enabled:
            for endpoint in endpoints:
                # Step 1: Basic format check ([name]_[id])
                if "_" not in endpoint:
                    return json.dumps({
                        "success": False,
                        "message": "Invalid format."
                    })
                
                # Step 2: Validate the exact device_name
                # Extract ID portion (part after the last '_')
                endpoint_id = endpoint.split("_")[-1]
                
                # Use transform to generate the correct format
                correct_format = LockLock.transform(endpoint_id, data)
                
                # Compare input with the correct format
                if endpoint != correct_format:
                    return json.dumps({
                        "success": False,
                        "message": "Invalid format."
                    })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        results = []
        for endpoint in endpoints:
            # Extract the actual ID from the endpoint ([name]_[id] -> id)
            if "_" in endpoint:
                actual_id = endpoint.split("_")[-1]
            else:
                actual_id = endpoint
            
            device = find_device_by_endpoint(data, actual_id, home_id)
            if device and "lock_lock" in device["supported_apis"]:
                # Update the device state directly in the data dictionary
                for i, d in enumerate(data["devices"]):
                    if d["endpoint"] == actual_id and (home_id is None or d["home_id"] == home_id):
                        if "state" not in data["devices"][i]:
                            data["devices"][i]["state"] = {}
                        data["devices"][i]["state"]["locked"] = True
                        success = True
                        break
                else:
                    success = False
                
                if success:
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": True,
                        "message": f"Locked {device['name']}",
                        "state": "locked"
                    })
                else:
                    results.append({
                        "endpoint": endpoint,
                        "success": False,
                        "message": f"Failed to update state for device with endpoint {endpoint}"
                    })
            else:
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"Device with endpoint {endpoint} not found or does not support locking"
                })
        
        return json.dumps({
            "success": any(result["success"] for result in results),
            "results": results
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "lock_lock",
                "description": "Lock one or more lock devices. This tool secures doors, windows, and other lockable devices by setting them to the locked state. This is a security-critical operation that should be used with appropriate confirmation from the user, especially when unlocking devices.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to lock. Each endpoint follows the format '[device_name]_[id]' where [device_name] is the device name with spaces removed (e.g., 'FrontDoorLock_6' for a device named 'Front Door Lock') and must correspond to a lock device that supports the lock_lock API."
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the lock_lock API.",
                    "State update failure: The device state could not be updated due to a system error.",
                    "Security restrictions: Some lock operations may require additional authentication or authorization."
                ]
            }
        }
