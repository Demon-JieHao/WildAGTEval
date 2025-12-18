# Copyright SmartHomeEnv

import json
from typing import Any, Dict, List, Optional
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import get_current_user, get_user_home_id


class GetUserInventory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None) -> str:
        """
        Get the inventory of devices and groups for a user.
        
        Args:
            data: The data dictionary
            user_id: (Optional) The user ID to get inventory for (if None, uses current user)
            
        Returns:
            A JSON string with the user's inventory
        """
        # Get the user and home ID
        if user_id is None:
            user = get_current_user(data)
            if not user:
                return json.dumps({
                    "success": False,
                    "message": "No current user set"
                })
            user_id = user["user_id"]
            home_id = user["home_id"]
        else:
            for u in data["users"]:
                if u["user_id"] == user_id:
                    user = u
                    home_id = u["home_id"]
                    break
            else:
                return json.dumps({
                    "success": False,
                    "message": f"User with ID '{user_id}' not found"
                })
        
        # Get the user's devices
        devices = []
        for device in data["devices"]:
            if device["home_id"] == home_id:
                devices.append({
                    "endpoint": device["endpoint"],
                    "name": device["name"],
                    "alternate_names": device["alternate_names"],
                    # "endpoint_categories": device["endpoint_categories"],
                    # "supported_apis": device["supported_apis"],
                    # "groups": device["groups"],
                    # "state": device.get("state", {})
                })
        
        # Get the user's groups
        groups = []
        for group in data["groups"]:
            if group["home_id"] == home_id:
                groups.append({
                    "id": group["id"],
                    "name": group["name"],
                    "type": group["type"],
                    "has_echo_device": group["has_echo_device"]
                })
        
        # Get the user's current space
        current_space = user.get("current_space")
        
        return json.dumps({
            "success": True,
            "user_id": user_id,
            "name": user["name"],
            "home_id": home_id,
            "current_space": current_space,
            "devices": devices,
            "groups": groups
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_inventory",
                "description": "Get the inventory of devices and groups for a user. This tool retrieves comprehensive information about all devices and groups associated with a user's home, including device states, supported APIs, and group memberships. It's particularly useful for discovering available devices and their capabilities before sending commands.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "(Optional) The user ID to get inventory for. If not provided, uses the current user."
                        }
                    }
                },
                "error_cases": [
                    "No current user set: This error occurs when no user_id is provided and no current user is set in the system.",
                    "User not found: The specified user_id does not exist in the system.",
                    "Home not found: The user exists but does not have an associated home."
                ]
            }
        }
