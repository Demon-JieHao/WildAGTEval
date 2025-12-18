# Copyright MediaControlEnv

import json
from typing import Any, Dict
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import create_playlist, get_current_user


class CreatePlaylist(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], title: str) -> str:
        """
        Create a new playlist for the current user.
        
        Args:
            data: The data dictionary containing media database
            title: Title for the new playlist
            
        Returns:
            A JSON string with the result of the operation
        """
        if not title:
            return json.dumps({
                "success": False,
                "message": "No playlist title provided"
            })
        
        # Get current user
        current_user = get_current_user(data)
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No current user set"
            })
        
        try:
            # Create the playlist
            playlist_id = create_playlist(data, title)
            
            return json.dumps({
                "success": True,
                "playlist_id": playlist_id,
                "title": title,
                "message": f"Created playlist '{title}' with ID '{playlist_id}'"
            })
        except Exception as e:
            return json.dumps({
                "success": False,
                "message": f"Failed to create playlist: {str(e)}"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_playlist",
                "description": "Create a new playlist for the current user. The playlist will be empty initially and can be populated using the add_to_playlist tool.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Title for the new playlist"
                        }
                    },
                    "required": ["title"]
                },
                "error_cases": [
                    "No title provided: The title parameter is empty or not provided.",
                    "No current user: No user is currently set in the system."
                ]
            }
        }
