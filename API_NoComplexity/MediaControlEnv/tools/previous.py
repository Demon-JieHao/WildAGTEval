# Copyright MediaControlEnv

import json
from typing import Any, Dict, List
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, get_device_playback_state, 
    update_device_playback_state, get_user_home_id
)


class Previous(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str]) -> str:
        """
        Go to the previous track/episode on one or more devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to control
            
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
                
            if "previous" not in device.get("supported_apis", []):
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Device {device['name']} does not support previous track"
                })
                continue
            
            playback_state = get_device_playback_state(data, endpoint)
            
            if playback_state.get("status") in ["playing", "paused"]:
                # Check if we're at the beginning of current track
                position = playback_state.get("position", 0)
                
                if position > 5:  # If more than 5 seconds into track, restart current track
                    update_device_playback_state(data, endpoint, {
                        "position": 0
                    })
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": True,
                        "message": f"Restarted current track on {device['name']}"
                    })
                else:
                    # Go to previous track
                    previous_track = playback_state.get("previous_track", None)
                    if previous_track:
                        update_device_playback_state(data, endpoint, {
                            "position": 0,
                            "title": previous_track,
                            "previous_track": None
                        })
                        results.append({
                            "endpoint": endpoint,
                            "name": device["name"],
                            "success": True,
                            "message": f"Went to previous track on {device['name']}"
                        })
                    else:
                        results.append({
                            "endpoint": endpoint,
                            "name": device["name"],
                            "success": False,
                            "message": f"No previous track available on {device['name']}"
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
                "name": "previous",
                "description": "Go to the previous track or episode in the current playlist or queue. If more than 5 seconds into the current track, it will restart the current track instead.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to control. Each endpoint must correspond to a device that supports the previous API."
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the previous API.",
                    "No active playback: There is no active playback on one or more devices.",
                    "No previous track: There is no previous track in the playback history."
                ]
            }
        }
