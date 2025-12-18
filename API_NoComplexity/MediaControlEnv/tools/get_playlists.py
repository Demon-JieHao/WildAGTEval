# Copyright MediaControlEnv

import json
from typing import Any, Dict, Optional
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import get_user_playlists, get_current_user


class GetPlaylists(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None) -> str:
        """
        Get playlists for a user.
        
        Args:
            data: The data dictionary containing media database
            user_id: Optional user ID (defaults to current user)
            
        Returns:
            A JSON string with the playlists
        """
        # If no user_id provided, use current user
        if not user_id:
            current_user = get_current_user(data)
            if current_user:
                user_id = current_user["user_id"]
            else:
                return json.dumps({
                    "success": False,
                    "message": "No current user set and no user_id provided"
                })
        
        # Get playlists
        playlists = get_user_playlists(data, user_id)
        
        # Format playlists
        formatted_playlists = []
        for playlist in playlists:
            # Get media items details
            items = []
            for media_id in playlist.get("items", []):
                # Find this media in the database
                media_db = data.get("media_database", {}).get("media", [])
                media_item = next((item for item in media_db if item.get("id") == media_id), None)
                
                if media_item:
                    items.append({
                        "id": media_id,
                        "title": media_item.get("title", "Unknown"),
                        "type": media_item.get("type", "Unknown")
                    })
                else:
                    # Just include the ID if we can't find details
                    items.append({
                        "id": media_id,
                        "title": "Unknown",
                        "type": "Unknown"
                    })
            
            formatted_playlist = {
                "id": playlist.get("id"),
                "title": playlist.get("title"),
                "user_id": playlist.get("user_id"),
                "item_count": len(playlist.get("items", [])),
                "items": items
            }
            formatted_playlists.append(formatted_playlist)
        
        return json.dumps({
            "success": True,
            "count": len(formatted_playlists),
            "playlists": formatted_playlists,
            "message": f"Found {len(formatted_playlists)} playlists for user {user_id}"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_playlists",
                "description": "Get all playlists for a user. If no user ID is provided, returns playlists for the current user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "Optional user ID to get playlists for (defaults to current user)"
                        }
                    },
                    "required": []
                },
                "error_cases": [
                    "No current user: No user is currently set when user_id is not provided."
                ]
            }
        }
