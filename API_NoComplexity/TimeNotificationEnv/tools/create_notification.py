# Copyright TimeNotificationEnv

import json
from datetime import datetime
from typing import Any, Dict, Optional
from TimeNotificationEnv.tool import Tool
from TimeNotificationEnv.helpers import get_current_user_id, generate_id


class CreateNotification(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], 
              title: str, 
              message: str, 
              user_id: Optional[str] = None,
              source: Optional[str] = "TimeNotificationEnv",
              type: Optional[str] = "system",
              priority: Optional[str] = "normal") -> str:
        """
        Create a new notification for a user.
        
        Args:
            data: The data dictionary
            title: The title of the notification
            message: The notification message content
            user_id: Optional user ID to target (defaults to current user)
            source: Optional source of the notification (environment name)
            type: Optional type of notification (system, reminder, etc.)
            priority: Optional priority level (low, normal, high)
            
        Returns:
            A JSON string with the result of the operation
        """
        # Get target user ID (use current user if not specified)
        target_user_id = user_id if user_id else get_current_user_id(data)
        if not target_user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in and no user_id specified"
            })
        
        # Verify the user exists (validation is skipped in test environments)
        # Skip user verification when in test mode
        if "test_mode" not in data:
            user_exists = False
            for user in data.get("users", []):
                if user.get("user_id") == target_user_id:
                    user_exists = True
                    break
            
            if not user_exists:
                return json.dumps({
                    "success": False,
                    "message": f"User with ID '{target_user_id}' not found"
                })
        
        # Validate priority
        valid_priorities = ["low", "normal", "high"]
        if priority not in valid_priorities:
            return json.dumps({
                "success": False,
                "message": f"Invalid priority. Must be one of: {', '.join(valid_priorities)}"
            })
        
        # # Generate a new notification ID
        # if "notifications" not in data:
        #     data["notifications"] = []
            
        notification_id = generate_id("notif", data)
        
        # Get current timestamp in ISO format
        timestamp = datetime.now().isoformat()
        
        # Create new notification
        new_notification = {
            "notification_id": notification_id,
            "user_id": target_user_id,
            "title": title,
            "message": message,
            "timestamp": timestamp,
            "type": type,
            "source": source,
            "read": False,
            "priority": priority
        }
        
        # Add to notifications data
        data["notifications"].append(new_notification)
        
        # Check if user has do_not_disturb enabled
        do_not_disturb = False
        for user in data.get("users", []):
            if user.get("user_id") == target_user_id:
                do_not_disturb = user.get("notification_preferences", {}).get("do_not_disturb", False)
                break
        
        message = f"Notification created for user {target_user_id}"
        if do_not_disturb and priority != "high":
            message += " (will be shown when do-not-disturb is disabled)"
        
        return json.dumps({
            "success": True,
            "message": message,
            "notification_id": notification_id,
            "notification": new_notification,
            "do_not_disturb": do_not_disturb
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_notification",
                "description": "Create a new notification for a user. This allows environments to send messages to users about events or updates.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the notification."
                        },
                        "message": {
                            "type": "string",
                            "description": "The detailed notification message content."
                        },
                        "user_id": {
                            "type": "string",
                            "description": "Optional user ID to target with the notification. If not provided, uses current user."
                        },
                        "source": {
                            "type": "string",
                            "description": "Source of the notification (typically environment name). Defaults to 'TimeNotificationEnv'."
                        },
                        "type": {
                            "type": "string",
                            "description": "Type of notification (e.g., system, reminder, alert). Defaults to 'system'."
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "normal", "high"],
                            "description": "Priority level of the notification. High priority notifications will show even during do-not-disturb periods."
                        }
                    },
                    "required": ["title", "message"]
                },
                "error_cases": [
                    "No user target: No user is currently logged in and no user_id was specified.",
                    "User not found: The specified user ID does not exist.",
                    "Invalid priority: Priority must be one of: low, normal, high."
                ]
            }
        }
