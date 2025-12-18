# Copyright SmartHomeEnv

import json
from typing import Any, Dict, List, Optional
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class BrightnessAdjust(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], brightness: Optional[int] = None, direction: Optional[str] = None) -> str:
        """
        Adjust the brightness of one or more light devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to adjust
            brightness: (Optional) Specific brightness level (0-100)
            direction: (Optional) Direction to adjust ("increase" or "decrease")
            
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
        
        # Default adjustment amount if only direction is specified
        adjustment_amount = 20  # Default 20% change
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "brightness_adjust" in device["supported_apis"]:
                # Get the current brightness from the device state
                current_brightness = 50  # Default if not set
                if "state" in device and "brightness" in device["state"]:
                    current_brightness = device["state"]["brightness"]
                
                if brightness is not None:
                    # Set to specific brightness
                    new_brightness = max(0, min(100, brightness))
                    message = f"Set {device['name']} brightness to {new_brightness}%"
                elif direction == "increase":
                    # Increase brightness
                    new_brightness = min(100, current_brightness + adjustment_amount)
                    message = f"Increased {device['name']} brightness to {new_brightness}%"
                elif direction == "decrease":
                    # Decrease brightness
                    new_brightness = max(0, current_brightness - adjustment_amount)
                    message = f"Decreased {device['name']} brightness to {new_brightness}%"
                else:
                    # No valid brightness parameter
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": False,
                        "message": "No valid brightness parameter specified"
                    })
                    continue
                
                # Update the device state directly in the data dictionary
                for i, d in enumerate(data["devices"]):
                    if d["endpoint"] == endpoint and (home_id is None or d["home_id"] == home_id):
                        if "state" not in data["devices"][i]:
                            data["devices"][i]["state"] = {}
                        data["devices"][i]["state"]["brightness"] = new_brightness
                        success = True
                        break
                else:
                    success = False
                
                if success:
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": True,
                        "message": message,
                        "brightness": new_brightness
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
                    "message": f"Device with endpoint {endpoint} not found or does not support brightness adjustment"
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
                "name": "brightness_adjust",
                "description": "Adjust the brightness of one or more light devices. This tool allows setting specific brightness levels or making relative adjustments (increase/decrease) to light devices. Brightness is measured on a scale from 0% (off) to 100% (maximum brightness).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to adjust. Each endpoint must correspond to a light device that supports the brightness_adjust API."
                        },
                        "brightness": {
                            "type": "integer",
                            "description": "(Optional) Specific brightness level (0-100%). If provided, sets the light to this exact brightness level."
                        },
                        "direction": {
                            "type": "string",
                            "enum": ["increase", "decrease"],
                            "description": "(Optional) Direction to adjust brightness. If 'increase', brightness will be increased by 20%. If 'decrease', brightness will be decreased by 20%."
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "No valid brightness parameter: Neither brightness nor direction parameter is provided.",
                    "Invalid brightness value: The brightness value is outside the valid range (0-100%).",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the brightness_adjust API.",
                    "State update failure: The device state could not be updated due to a system error."
                ]
            }
        }
