# Copyright MediaControlEnv

import json
from typing import Any, Dict, List
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, get_device_playback_state, 
    get_user_home_id, format_duration
)


class GetPlaybackStatus(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str]) -> str:
        """
        Get the current playback status for one or more devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to check
            
        Returns:
            A JSON string with the playback status
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
            
            # Get playback state
            playback_state = get_device_playback_state(data, endpoint)
            
            status_info = {
                "endpoint": endpoint,
                "name": device["name"],
                "success": True,
                "status": playback_state.get("status", "idle")
            }
            
            # Add additional info if playing or paused
            if playback_state.get("status") in ["playing", "paused"]:
                status_info.update({
                    "media_id": playback_state.get("media_id", ""),
                    "title": playback_state.get("title", "Unknown"),
                    "type": playback_state.get("type", "Unknown"),
                    "position": playback_state.get("position", 0),
                    "duration": playback_state.get("duration", 0),
                    "position_formatted": format_duration(playback_state.get("position", 0)),
                    "duration_formatted": format_duration(playback_state.get("duration", 0)),
                    "playback_speed": playback_state.get("playback_speed", 1.0),
                    "shuffle": playback_state.get("shuffle", False),
                    "loop": playback_state.get("loop", "off")
                })
                
                # Add artist for music
                if playback_state.get("artist"):
                    status_info["artist"] = playback_state.get("artist")
            
            results.append(status_info)
        
        return json.dumps({
            "success": any(result["success"] for result in results),
            "results": results
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_playback_status",
                "description": "Get the current playback status for one or more devices, including what's playing, position, and playback settings.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to check status for"
                        }
                    },
                    "required": ["endpoints"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home."
                ]
            }
        }
