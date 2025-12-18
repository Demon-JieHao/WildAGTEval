# Copyright InformationControlEnv

import json
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_user_preferences


class UserPreferences(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        """
        Get current user's preferences.
        
        Args:
            data: The data dictionary containing all information
            
        Returns:
            A JSON string with user preferences
        """
        # Get current user
        user = get_current_user(data)
        if not user:
            return json.dumps({
                "success": False,
                "message": "No user logged in"
            })
        
        # Get preferences
        preferences = get_user_preferences(data)
        
        return json.dumps({
            "success": True,
            "user_id": user["user_id"],
            "user_name": user["name"],
            "preferences": preferences
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "user_preferences",
                "description": "Get current user's preferences. Shows location, language, preferred news categories, stock watchlist, and other personalization settings, e.g., user_id.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
                "error_cases": [
                    "No user logged in: Returns error if no current user is set.",
                    "No preferences: Returns empty preferences object if user has no preferences configured."
                ]
            }
        }
