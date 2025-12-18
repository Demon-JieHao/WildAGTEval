# Copyright MediaControlEnv

import json
from typing import Any, Dict, List
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, get_device_playback_state, 
    update_device_playback_state, get_user_home_id
)


class Stop(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str]) -> str:
        """
        Stop playback on one or more devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to stop
            
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
                
            if "stop" not in device.get("supported_apis", []):
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Device {device['name']} does not support stop"
                })
                continue
            
            playback_state = get_device_playback_state(data, endpoint)
            
            if playback_state.get("status") in ["playing", "paused"]:
                # Clear playback state
                update_device_playback_state(data, endpoint, {
                    "status": "stopped",  # Changed from "idle" to "stopped" for consistency
                    "media_id": None,
                    "title": None,
                    "position": 0,
                    "duration": 0
                })
                
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": True,
                    "message": f"Stopped playback on {device['name']}"
                })
            else:
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"No active playback to stop on {device['name']}"
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
                "name": "stop",
                "description": "Stop media playback on one or more devices. This completely stops playback and clears the current media from the device.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to stop. Each endpoint must correspond to a device that supports the stop API."
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the stop API.",
                    "No active playback: There is no active playback to stop on one or more devices."
                ]
            }
        }
