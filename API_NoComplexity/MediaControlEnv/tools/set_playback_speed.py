# Copyright MediaControlEnv

import json
from typing import Any, Dict, List
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, get_device_playback_state, 
    update_device_playback_state, get_user_home_id
)


class SetPlaybackSpeed(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], speed: float) -> str:
        """
        Set the playback speed for media on one or more devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to control
            speed: Playback speed multiplier (0.5 = half speed, 2.0 = double speed)
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        # Validate speed parameter
        if speed < 0.5 or speed > 2.0:
            return json.dumps({
                "success": False,
                "message": "Speed must be between 0.5 and 2.0"
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
                
            if "set_playback_speed" not in device.get("supported_apis", []):
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Device {device['name']} does not support playback speed adjustment"
                })
                continue
            
            playback_state = get_device_playback_state(data, endpoint)
            
            if playback_state.get("status") in ["playing", "paused"]:
                # Update playback speed
                update_device_playback_state(data, endpoint, {
                    "speed": speed
                })
                
                speed_text = f"{speed}x"
                if speed == 1.0:
                    speed_text = "normal"
                
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": True,
                    "message": f"Set playback speed to {speed_text} on {device['name']}"
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
                "name": "set_playback_speed",
                "description": "Set the playback speed for media. Useful for watching content faster or slower than normal speed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to control. Each endpoint must correspond to a device that supports the set_playback_speed API."
                        },
                        "speed": {
                            "type": "number",
                            "description": "Playback speed multiplier (0.5 = half speed, 1.0 = normal, 2.0 = double speed). Must be between 0.5 and 2.0."
                        }
                    },
                    "required": ["endpoints", "speed"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the set_playback_speed API.",
                    "No active playback: There is no active playback on one or more devices.",
                    "Invalid speed: The speed parameter is outside the valid range (0.5-2.0)."
                ]
            }
        }
