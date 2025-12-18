# Copyright SmartHomeEnv

import json
import random
from typing import Any, Dict, List
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class LockStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str]) -> str:
        """
        Get the status of one or more lock devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to check
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "lock_status" in device["supported_apis"]:
                # Get the current lock state from the device state
                lock_state_text = "unknown"
                lock_state_bool = None
                
                if "state" in device and "locked" in device["state"]:
                    lock_state_bool = device["state"]["locked"]
                    lock_state_text = "locked" if lock_state_bool else "unlocked"
                else:
                    # If no state is stored, use a random state for demonstration
                    lock_state_bool = random.choice([True, False])
                    lock_state_text = "locked" if lock_state_bool else "unlocked"
                
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": True,
                    "message": f"{device['name']} is {lock_state_text}",
                    "state": {
                        "locked": lock_state_bool
                    }
                })
            else:
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"Device with endpoint {endpoint} not found or does not support status checking"
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
                "name": "lock_status",
                "description": "Get the status of one or more lock devices. This tool checks the current state (locked or unlocked) of door locks, window locks, and other security devices. This is a read-only operation that does not change the state of any devices.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to check. Each endpoint must correspond to a lock device that supports the lock_status API."
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the lock_status API.",
                    "No current user: No user is currently set in the system, so the home context cannot be determined.",
                    "Security restrictions: Some lock status operations may require additional authentication or authorization."
                ]
            }
        }
