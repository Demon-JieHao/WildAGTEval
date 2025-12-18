# Copyright SmartHomeEnv

import json
from typing import Any, Dict, List, Optional
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class VolumeAdjust(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], volume: Optional[int] = None, direction: Optional[str] = None) -> str:
        """
        Adjust the volume of one or more audio devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to adjust
            volume: (Optional) Specific volume level (0-100)
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
        adjustment_amount = 10  # Default 10% change
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "volume_adjust" in device["supported_apis"]:
                # Get the current volume from the device state
                current_volume = 30  # Default if not set
                if "state" in device and "volume" in device["state"]:
                    current_volume = device["state"]["volume"]
                
                if volume is not None:
                    # Set to specific volume
                    new_volume = max(0, min(100, volume))
                    message = f"Set {device['name']} volume to {new_volume}%"
                elif direction == "increase":
                    # Increase volume
                    new_volume = min(100, current_volume + adjustment_amount)
                    message = f"Increased {device['name']} volume to {new_volume}%"
                elif direction == "decrease":
                    # Decrease volume
                    new_volume = max(0, current_volume - adjustment_amount)
                    message = f"Decreased {device['name']} volume to {new_volume}%"
                else:
                    # No valid volume parameter
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": False,
                        "message": "No valid volume parameter specified"
                    })
                    continue
                
                # Update the device state directly in the data dictionary
                for i, d in enumerate(data["devices"]):
                    if d["endpoint"] == endpoint and (home_id is None or d["home_id"] == home_id):
                        if "state" not in data["devices"][i]:
                            data["devices"][i]["state"] = {}
                        data["devices"][i]["state"]["volume"] = new_volume
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
                        "volume": new_volume
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
                    "message": f"Device with endpoint {endpoint} not found or does not support volume adjustment"
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
                "name": "volume_adjust",
                "description": "Adjust the volume of one or more audio devices. This tool controls the volume level of TVs, speakers, and other audio devices. Volume can be set to a specific level or adjusted relatively (increase/decrease) from the current level.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to adjust. Each endpoint must correspond to an audio device that supports the volume_adjust API."
                        },
                        "volume": {
                            "type": "integer",
                            "description": "(Optional) Specific volume level (0-100%). If provided, sets the device to this exact volume level."
                        },
                        "direction": {
                            "type": "string",
                            "enum": ["increase", "decrease"],
                            "description": "(Optional) Direction to adjust volume. If 'increase', volume will be increased by 10%. If 'decrease', volume will be decreased by 10%."
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "No valid volume parameter: Neither volume nor direction parameter is provided.",
                    "Invalid volume value: The volume value is outside the valid range (0-100%).",
                    "Invalid direction: The direction is not one of the valid options (increase, decrease).",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the volume_adjust API.",
                    "State update failure: The device state could not be updated due to a system error."
                ]
            }
        }
