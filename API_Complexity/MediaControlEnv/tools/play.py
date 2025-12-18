# Copyright MediaControlEnv

import json
import os
import re
from typing import Any, Dict, List, Tuple
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    find_device_by_endpoint, find_media_by_id, update_device_playback_state,
    get_user_home_id, check_device_supports_media_type
)


class Play(Tool):
    @staticmethod
    def transform(input_value: str, data: Dict[str, Any] = None) -> str:
        """Convert a media ID into the required format `{type}:{id}`.
        
        The following rules apply:
        1. If the value is already in the correct format (`type:id`), return it unchanged.
        2. If a plain ID is provided, look up the media in `media_database` to determine its type.
        3. When used inside an `invoke_tool` expression, support transforming the value of
           the `media_id` parameter.
        
        Args:
            input_value: The value to transform (a media ID or an `invoke_tool` expression).
            data: Optional data dictionary (not required for this transformation).
            
        Returns:
            The transformed media ID or the transformed `invoke_tool` expression.
        """
        # Handle `invoke_tool` expressions
        if isinstance(input_value, str) and "invoke_tool" in input_value and "media_id=" in input_value:
            # Extract the media_id value via regex
            media_id_pattern = r'media_id=["\']([^"\']+)["\']'
            match = re.search(media_id_pattern, input_value)
            
            if match:
                media_id = match.group(1)
                # Recursively transform the ID value itself
                transformed_id = Play.transform(media_id)
                
                # Replace the original ID with the transformed ID in the original string
                if 'media_id="' in input_value:
                    return input_value.replace(f'media_id="{media_id}"', f'media_id="{transformed_id}"')
                else:
                    return input_value.replace(f"media_id='{media_id}'", f"media_id='{transformed_id}'")
        
        # If the value itself is not a string, return it as-is
        if not isinstance(input_value, str):
            return input_value
        
        # If already in the correct format (`type:id`), return as-is
        if ":" in input_value:
            # Assume it is valid; additional checks are performed in `validate_media_id`
            return input_value
            
        # Look for an entry with this ID in the media database
        try:
            # Load media database
            with open("common/data/media_database.json", "r") as f:
                media_db = json.load(f)
            
            # Search across all categories
            for category_name, items in media_db.items():
                # Skip non-media categories such as `streaming_services`
                if not isinstance(items, list):
                    continue
                    
                # Inspect each item
                for item in items:
                    if item.get("id") == input_value:
                        # When found, return in `type:id` format
                        item_type = item.get("type")
                        if item_type:
                            return f"{item_type}:{input_value}"
        except Exception:
            # On any file access or parsing error, fall back to returning the original value
            pass
        
        # If no matching item is found, return the original value by default
        return input_value
        
    @staticmethod
    def validate_media_id(data: Dict[str, Any], media_id: str) -> Tuple[bool, str]:
        """Validate that a media ID is in the correct format `type:id`.
        
        Args:
            data: Data dictionary containing the media database.
            media_id: Media ID to validate.
            
        Returns:
            Tuple[bool, str]: `(is_valid, error_message_or_empty_string)`.
        """
        # Obtain the canonical format via `transform`
        correct_format = Play.transform(media_id)
        
        # Compare with the original: input must already be in the canonical `type:id` format
        if media_id != correct_format or ":" not in media_id:
            # If not valid, provide a generic message (expected vs. actual is not exposed)
            error_msg = f"Invalid media ID format."
            return False, error_msg
            
        # Extract type prefix and ID part
        type_prefix = media_id.split(":", 1)[0]
        id_part = media_id.split(":", 1)[1]
        
        # Look up the media item
        media_db = data.get("media_database", {})
        
        # Search all categories
        for category_name, items in media_db.items():
            if not isinstance(items, list):
                continue
                
            for item in items:
                if item.get("id") == id_part:
                    # Item found, but type does not match
                    if item.get("type") != type_prefix:
                        # error_msg = f"Media type mismatch: ID '{id_part}' is of type '{item.get('type')}', not '{type_prefix}'"
                        error_msg = f"Invalid media ID format."
                        return False, error_msg
                    # Type and ID are consistent
                    return True, ""
        
        # Media item not found
        return False, f"Invalid media ID format."  # f"Media with ID '{id_part}' not found"
    
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], media_id: str) -> str:
        """Play specified media on one or more devices.
        
        Args:
            data: The data dictionary containing devices and media
            endpoints: List of device endpoint IDs to play on
            media_id: ID of the media to play
            
        Returns:
            A JSON string with the result of the operation
        """
        # Check for system failure error uncertainty
        uncertainty_system_failure_error_enabled = os.getenv("ENABLE__SYSTEM_FAILURE_ERROR__PLAY", "false").lower() == "true"
        uncertainty_adhoc_enabled = os.getenv("ENABLE__ADHOC__PLAY", "false").lower() == "true"
        
        if uncertainty_system_failure_error_enabled:
            # Simulate CDN infrastructure failure with complex technical errors
            failure_scenario = {
                "error": "CDN_EDGE_NODE_FAILURE_0x7F3A",
                "message": "Content delivery network edge node cdn-edge-us-west-2a.mediastream.internal experiencing packet loss >15% on BGP peer 64512:65001, failover to cdn-edge-us-west-2b unsuccessful due to cache miss ratio exceeding 0.85, origin shield timeout after 45s",
                "technical_details": {
                    "affected_pops": ["LAX1", "SFO2", "SEA1"],
                    "bgp_session_state": "IDLE",
                    "cache_hit_ratio": 0.12,
                    "origin_latency_ms": 4500,
                    "edge_node_cpu": 98.7,
                    "memory_pressure": "HIGH"
                },
                "error_code": "CDN_EDGE_FAILURE_001",
                "severity": "CRITICAL",
                "service": "MediaControlEnv.play",
                "correlation_id": "fixed-correlation-play-12345",
                "trace_id": "trace-play-67890"
            }
            
            return json.dumps({
                "success": False,
                "error": failure_scenario["error"],
                "message": failure_scenario["message"],
                "technical_details": failure_scenario["technical_details"],
                "error_code": failure_scenario["error_code"],
                "severity": failure_scenario["severity"],
                "service": failure_scenario["service"],
                "correlation_id": failure_scenario["correlation_id"],
                "trace_id": failure_scenario["trace_id"]
            })
        
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        # Validate media_id under ad-hoc rule
        if uncertainty_adhoc_enabled:
            is_valid, error_msg = Play.validate_media_id(data, media_id)
            if not is_valid:
                return json.dumps({
                    "success": False,
                    "message": error_msg
                })
            
            # Extract actual ID from media_id
            actual_id = media_id.split(":", 1)[1]
            media_item = find_media_by_id(data, actual_id)
            if not media_item:
                return json.dumps({
                    "success": False,
                    "message": f"Media with ID '{actual_id}' not found"
                })
        else:
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
                            "description": "ID of the media item to play. ID should be formatted as {type}:{id} where type is one of 'movie', 'song', 'playlist', or 'show' (e.g., 'movie:inception', NOT just 'inception')."
                        }
                    },
                    "required": ["endpoints", "media_id"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "Media not found: The specified media ID does not exist in the database.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the play API.",
                    "Incompatible media type: The device cannot play the specified type of media (e.g., trying to play video on an audio-only device).",
                    "Invalid media ID format: The media ID must include type prefix (e.g., 'movie:', 'song:', 'playlist:', 'show:').",
                    "Media type mismatch: The media type in the ID doesn't match the actual media type (e.g., using 'song:inception' for a movie)."
                ]
            }
        }
