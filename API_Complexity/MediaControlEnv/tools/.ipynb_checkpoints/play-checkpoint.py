# Copyright MediaControlEnv

import json
from typing import Any, Dict, List
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, find_media_by_id, update_device_playback_state,
    get_user_home_id, check_device_supports_media_type
)


class Play(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], media_id: str) -> str:
        """
        Play specified media on one or more devices.
        
        Args:
            data: The data dictionary containing devices and media
            endpoints: List of device endpoint IDs to play on
            media_id: ID of the media to play
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        # Get the media item
        media_item = find_media_by_id(data, media_id)
        if not media_item:
            return json.dumps({
                "success": False,
                "message": f"Media with ID '{media_id}' not found"
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
                
            if "play" not in device.get("supported_apis", []):
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Device {device['name']} does not support media playback"
                })
                continue
            
            # Check if the device supports the media type
            if not check_device_supports_media_type(device, media_item):
                media_type = media_item.get("type", "unknown")
                results.append({
                    "endpoint": endpoint,
                    "name": device["name"],
                    "success": False,
                    "message": f"Device {device['name']} cannot play {media_type} content"
                })
                continue
            
            # Update playback state
            update_device_playback_state(data, endpoint, {
                "status": "playing",
                "media_id": media_id,
                "title": media_item.get("title", "Unknown"),
                "type": media_item.get("type", "Unknown"),
                "artist": media_item.get("artist", ""),
                "position": 0,
                "duration": media_item.get("duration", 0),
                "playback_speed": 1.0,
                "shuffle": False,
                "loop": "off"
            })
            
            results.append({
                "endpoint": endpoint,
                "name": device["name"],
                "success": True,
                "message": f"Now playing '{media_item.get('title')}' on {device['name']}"
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
                "name": "play",
                "description": "Play specified media on one or more devices. This starts playback of a movie, TV show, song, or playlist on compatible devices. The system will automatically check device compatibility before attempting playback.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to play media on. Each endpoint must correspond to a device that supports the play API."
                        },
                        "media_id": {
                            "type": "string",
                            "description": "ID of the media item to play (e.g., 'movie1', 'song1', 'playlist1')"
                        }
                    },
                    "required": ["endpoints", "media_id"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Media not found: The specified media ID does not exist in the database.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the play API.",
                    "Incompatible media type: The device cannot play the specified type of media (e.g., trying to play video on an audio-only device)."
                ]
            }
        }
