# Copyright MediaControlEnv

import json
from typing import Any, Dict, List, Optional
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, get_device_playback_state, 
    update_device_playback_state, get_user_home_id
)


class Shuffle(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], enabled: Optional[bool] = None) -> str:
        """
        Toggle or set shuffle mode for playback on one or more devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to control
            enabled: Optional boolean to set shuffle state (None toggles current state)
            
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
            
            if not device:
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"Device with endpoint {endpoint} not found"
                })
                continue
                
            if "shuffle" not in device.get("supported_apis", []):
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Device {device['name']} does not support shuffle"
                })
                continue
            
            playback_state = get_device_playback_state(data, endpoint)
            
            if playback_state.get("status") in ["playing", "paused"]:
                current_shuffle = playback_state.get("shuffle", False)
                
                # Determine new shuffle state
                if enabled is None:
                    new_shuffle = not current_shuffle
                else:
                    new_shuffle = enabled
                
                # Update shuffle state
                update_device_playback_state(data, endpoint, {
                    "shuffle": new_shuffle
                })
                
                state_text = "enabled" if new_shuffle else "disabled"
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": True,
                    "shuffle_enabled": new_shuffle,
                    "message": f"Shuffle {state_text} on {device['name']}"
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
                "name": "shuffle",
                "description": "Toggle or set shuffle mode for playback. When shuffle is enabled, tracks will play in random order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to control. Each endpoint must correspond to a device that supports the shuffle API."
                        },
                        "enabled": {
                            "type": "boolean",
                            "description": "Optional boolean to set shuffle state. If not provided, toggles current state."
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the shuffle API.",
                    "No active playback: There is no active playback on one or more devices."
                ]
            }
        }
