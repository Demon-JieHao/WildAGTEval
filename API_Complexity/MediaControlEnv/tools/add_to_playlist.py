# Copyright MediaControlEnv

import json
from typing import Any, Dict, List
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import (
    get_playlist_by_id, find_media_by_id, get_current_user
)
# Only using in-memory playlists now


class AddToPlaylist(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], playlist_id: str, media_ids: List[str]) -> str:
        """
        Add media items to an existing playlist.
        
        Args:
            data: The data dictionary containing media database
            playlist_id: ID of the playlist to add to
            media_ids: List of media IDs to add
            
        Returns:
            A JSON string with the result of the operation
        """
        if not playlist_id:
            return json.dumps({
                "success": False,
                "message": "No playlist ID provided"
            })
        
        if not media_ids:
            return json.dumps({
                "success": False,
                "message": "No media IDs provided"
            })
        
        # Get current user
        current_user = get_current_user(data)
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No current user set"
            })
        
        current_user_id = current_user["user_id"]
        
        # Get the playlist
        playlist = get_playlist_by_id(data, playlist_id)
        if not playlist:
            return json.dumps({
                "success": False,
                "message": f"Playlist with ID '{playlist_id}' not found"
            })
        
        # Check ownership
        playlist_owner_id = playlist.get("user_id")
        if playlist_owner_id != current_user_id:
            return json.dumps({
                "success": False,
                "message": "Cannot modify playlist owned by another user"
            })
        
        # Validate media IDs
        valid_media_ids = []
        invalid_media_ids = []
        
        for media_id in media_ids:
            media_item = find_media_by_id(data, media_id)
            if media_item:
                valid_media_ids.append(media_id)
            else:
                invalid_media_ids.append(media_id)
        
        if valid_media_ids:
            # Add media to playlist
            if "items" not in playlist:
                playlist["items"] = []
            
            # Add only media IDs that aren't already in the playlist
            added_count = 0
            for media_id in valid_media_ids:
                if media_id not in playlist["items"]:
                    playlist["items"].append(media_id)
                    added_count += 1
            
            # Update the playlist in memory at the top level
            if "playlists" not in data:
                data["playlists"] = []
            
            playlists = data.get("playlists", [])
            
            # Update or add to in-memory playlists
            playlist_updated = False
            for i, p in enumerate(playlists):
                if p.get("id") == playlist_id:
                    playlists[i] = playlist
                    playlist_updated = True
                    break
            
            if not playlist_updated:
                playlists.append(playlist)
            
            message = f"Added {added_count} items to playlist '{playlist.get('title')}'"
            if invalid_media_ids:
                message += f". {len(invalid_media_ids)} invalid media IDs were skipped"
            
            return json.dumps({
                "success": True,
                "added_count": added_count,
                "playlist_id": playlist_id,
                "message": message
            })
        else:
            return json.dumps({
                "success": False,
                "message": "No valid media IDs provided"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "add_to_playlist",
                "description": "Add one or more media items to an existing playlist. Only the playlist owner can add items.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "playlist_id": {
                            "type": "string",
                            "description": "ID of the playlist to add media to"
                        },
                        "media_ids": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of media IDs to add to the playlist"
                        }
                    },
                    "required": ["playlist_id", "media_ids"]
                },
                "error_cases": [
                    "No playlist ID: The playlist_id parameter is empty or not provided.",
                    "No media IDs: The media_ids parameter is empty or not provided.",
                    "No current user: No user is currently set in the system.",
                    "Playlist not found: The specified playlist ID does not exist.",
                    "Permission denied: Cannot modify playlist owned by another user.",
                    "Invalid media IDs: One or more media IDs do not exist in the database."
                ]
            }
        }
