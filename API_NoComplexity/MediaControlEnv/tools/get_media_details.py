# Copyright MediaControlEnv

import json
from typing import Any, Dict
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import find_media_by_id, format_duration


class GetMediaDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], media_id: str) -> str:
        """
        Get detailed information about a specific media item.
        
        Args:
            data: The data dictionary containing media database
            media_id: ID of the media item
            
        Returns:
            A JSON string with the media details
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_informational_notice_enabled = os.getenv('ENABLE__INFORMATIONAL_NOTICE__GET_MEDIA_DETAILS', 'false').lower() == 'true'
        
        if not media_id:
            return json.dumps({
                "success": False,
                "message": "No media ID provided"
            })
        
        # Find the media item
        media_item = find_media_by_id(data, media_id)
        
        if media_item:
            # Format the details
            details = {
                "id": media_item.get("id"),
                "title": media_item.get("title"),
                "type": media_item.get("type"),
                "year": media_item.get("year", ""),
                "genre": media_item.get("genre", []),
                "services": media_item.get("services", []),
                "duration": media_item.get("duration", 0),
                "duration_formatted": format_duration(media_item.get("duration", 0))
            }
            
            # Add type-specific fields
            if media_item.get("type") == "song":
                details["artist"] = media_item.get("artist", "")
                details["album"] = media_item.get("album", "")
            elif media_item.get("type") == "album":
                details["artist"] = media_item.get("artist", "")
                details["tracks"] = media_item.get("tracks", 0)
            elif media_item.get("type") == "tv_show":
                details["seasons"] = media_item.get("seasons", 0)
                details["episodes"] = media_item.get("episodes", 0)
                details["episode_duration"] = media_item.get("episode_duration", 0)
            elif media_item.get("type") == "playlist":
                details["user_id"] = media_item.get("user_id", "")
                details["items"] = media_item.get("items", [])
                details["item_count"] = len(media_item.get("items", []))
            
            ### ADDED: Build response with informational notices when uncertainty is enabled ###
            response = {
                "success": True,
                "details": details,
                "message": f"Found details for '{media_item.get('title')}'"
            }
            
            if uncertainty_informational_notice_enabled:
                ### ADDED: Include multiple helpful but potentially confusing informational notices ###
                response["performance_tip"] = (
                    "FYI: get_batch_media_details() is available if you need to retrieve multiple media items. "
                    "It processes up to 50 items in a single request and includes automatic result caching for frequently accessed content."
                )
                
                response["metadata_notice"] = (
                    "Note: Media metadata is refreshed every 6 hours from streaming service APIs. "
                    "get_real_time_media_details() is also available for time-sensitive operations where you need the absolute latest information, "
                    "though it has higher latency due to live API calls."
                )
                
                response["optimization_info"] = (
                    "Background: This function uses our standard media database which balances performance and freshness. "
                    "For reference, alternative approaches include get_cached_media_details() for faster repeated lookups (sub-10ms response times) "
                    "or get_extended_media_details() which also includes user reviews, ratings history, and related content suggestions."
                )
                
                # Add type-specific notices
                if media_item.get("type") == "tv_show":
                    response["tv_tip"] = (
                        "TV Show Tip: get_episode_list() is available to retrieve detailed episode information including air dates and descriptions. "
                        "get_season_details() also provides season-specific metadata if you're interested in particular seasons."
                    )
            
            return json.dumps(response)
        else:
            return json.dumps({
                "success": False,
                "message": f"Media with ID '{media_id}' not found"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_media_details",
                "description": "Get detailed information about a specific media item including duration, genre, streaming services, and type-specific metadata.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "media_id": {
                            "type": "string",
                            "description": "ID of the media item to get details for"
                        }
                    },
                    "required": ["media_id"]
                },
                "error_cases": [
                    "No media ID: The media_id parameter is empty or not provided.",
                    "Media not found: The specified media ID does not exist in the database."
                ]
            }
        }
