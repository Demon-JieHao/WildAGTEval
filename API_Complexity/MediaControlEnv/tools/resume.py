# Copyright MediaControlEnv

import json
from typing import Any, Dict, List
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, get_device_playback_state, 
    update_device_playback_state, get_user_home_id
)


class Resume(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str]) -> str:
        """
        Resume paused playback on one or more devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to resume
            
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
                
            if "resume" not in device.get("supported_apis", []):
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Device {device['name']} does not support resume"
                })
                continue
            
            playback_state = get_device_playback_state(data, endpoint)
            
            if playback_state.get("status") == "paused":
                # Resume from paused position
                paused_position = playback_state.get("paused_position", 0)
                update_device_playback_state(data, endpoint, {
                    "status": "playing",
                    "position": paused_position
                })
                
                title = playback_state.get("title", "Unknown")
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": True,
                    "message": f"Resumed playback of '{title}' on {device['name']}"
                })
            elif playback_state.get("status") == "playing":
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Playback is already active on {device['name']}"
                })
            else:
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"No paused playback to resume on {device['name']}"
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
                "name": "resume",
                "description": "Resume paused media playback on one or more devices. This continues playback from the position where it was paused.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to resume. Each endpoint must correspond to a device that supports the resume API."
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the resume API.",
                    "No paused playback: There is no paused playback to resume on one or more devices.",
                    "Already playing: Playback is already active on one or more devices."
                ]
            }
        }
