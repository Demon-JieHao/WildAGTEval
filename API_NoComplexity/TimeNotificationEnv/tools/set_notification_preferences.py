# Copyright TimeNotificationEnv

import json
from typing import Any, Dict, Optional
from TimeNotificationEnv.tool import Tool
from TimeNotificationEnv.helpers import get_current_user_id


class SetNotificationPreferences(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], 
              do_not_disturb: Optional[bool] = None,
              notification_sounds: Optional[bool] = None,
              preferred_device_endpoint: Optional[str] = None) -> str:
        """
        Set notification preferences for the current user.
        
        Args:
            data: The data dictionary
            do_not_disturb: Whether do not disturb mode is enabled
            notification_sounds: Whether notification sounds are enabled
            preferred_device_endpoint: Preferred device endpoint for notifications
            
        Returns:
            A JSON string with the result of the operation
        """
        # Get current user
        user_id = get_current_user_id(data)
        if not user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in"
            })
        
        # Find the user
        user_obj = None
        user_index = -1
        for i, user in enumerate(data.get("users", [])):
            if user.get("user_id") == user_id:
                user_obj = user
                user_index = i
                break
        
        if user_obj is None:
            return json.dumps({
                "success": False,
                "message": f"User with ID '{user_id}' not found"
            })
        
        # Initialize notification preferences if they don't exist
        if "notification_preferences" not in user_obj:
            user_obj["notification_preferences"] = {
                "do_not_disturb": False,
                "notification_sounds": True,
                "preferred_device_endpoint": None
            }
        
        # Update notification preferences
        if do_not_disturb is not None:
            user_obj["notification_preferences"]["do_not_disturb"] = do_not_disturb
        
        if notification_sounds is not None:
            user_obj["notification_preferences"]["notification_sounds"] = notification_sounds
        
        if preferred_device_endpoint is not None:
            # Verify the device exists if an endpoint is provided
            if preferred_device_endpoint != "None":
                device_exists = False
                for device in data.get("devices", []):
                    if device.get("endpoint") == preferred_device_endpoint:
                        device_exists = True
                        break
                
                if not device_exists:
                    return json.dumps({
                        "success": False,
                        "message": f"Device with endpoint '{preferred_device_endpoint}' not found"
                    })
            else:
                # Special case: "None" string is used to clear the preferred device
                preferred_device_endpoint = None
            
            user_obj["notification_preferences"]["preferred_device_endpoint"] = preferred_device_endpoint
        
        # Update user object in data
        data["users"][user_index] = user_obj
        
        # Build response message
        changes = []
        if do_not_disturb is not None:
            changes.append(f"do_not_disturb: {do_not_disturb}")
        if notification_sounds is not None:
            changes.append(f"notification_sounds: {notification_sounds}")
        if preferred_device_endpoint is not None:
            changes.append(f"preferred_device: {preferred_device_endpoint if preferred_device_endpoint else 'None'}")
        
        return json.dumps({
            "success": True,
            "message": f"Notification preferences updated: {', '.join(changes)}",
            "preferences": user_obj["notification_preferences"]
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "set_notification_preferences",
                "description": "Set notification preferences for the current user, including do-not-disturb mode and device preferences.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "do_not_disturb": {
                            "type": "boolean",
                            "description": "Whether do-not-disturb mode should be enabled. When enabled, only high priority notifications will be shown immediately."
                        },
                        "notification_sounds": {
                            "type": "boolean",
                            "description": "Whether notification sounds should be played."
                        },
                        "preferred_device_endpoint": {
                            "type": "string",
                            "description": "Optional device endpoint ID to use as the preferred device for notifications. Use 'None' to clear the preferred device."
                        }
                    }
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to update preferences.",
                    "User not found: The specified user ID does not exist.",
                    "Device not found: The specified device endpoint does not exist."
                ]
            }
        }
