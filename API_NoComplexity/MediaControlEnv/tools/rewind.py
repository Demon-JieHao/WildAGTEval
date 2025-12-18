# Copyright MediaControlEnv

import json
from typing import Any, Dict, List, Optional
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, get_device_playback_state, 
    update_device_playback_state, get_user_home_id
)


class Rewind(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], seconds: Optional[int] = 10) -> str:
        """
        Rewind playback by a specified number of seconds.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to control
            seconds: Number of seconds to skip backward (default: 10)
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        # Validate seconds parameter
        if seconds is None:
            seconds = 10
        elif seconds < 0:
            return json.dumps({
                "success": False,
                "message": "Seconds must be positive"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            
            if not device:
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"Device with endpoint {endpoint} not found"
                })
                continue
                
            if "rewind" not in device.get("supported_apis", []):
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Device {device['name']} does not support rewind"
                })
                continue
            
            playback_state = get_device_playback_state(data, endpoint)
            
            if playback_state.get("status") in ["playing", "paused"]:
                current_position = playback_state.get("position", 0)
                
                # Calculate new position
                new_position = max(0, current_position - seconds)
                
                # Update playback position
                update_device_playback_state(data, endpoint, {
                    "position": new_position
                })
                
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": True,
                    "message": f"Rewound {seconds} seconds on {device['name']}"
                })
            else:
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"No active playback on {device['name']}"
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
                "name": "rewind",
                "description": "Rewind the current media by a specified number of seconds. Useful for replaying content you missed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to control. Each endpoint must correspond to a device that supports the rewind API."
                        },
                        "seconds": {
                            "type": "integer",
                            "description": "Number of seconds to skip backward (default: 10). Must be positive.",
                            "default": 10
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the rewind API.",
                    "No active playback: There is no active playback on one or more devices.",
                    "Invalid seconds: The seconds parameter is negative."
                ]
            }
        }
