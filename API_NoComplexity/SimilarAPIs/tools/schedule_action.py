# Copyright TimeNotificationEnv

"""
Uncertainty Manifestation: Confusion Between Alarms, Timers, and Scheduled Actions

Description:
Developers using the TimeNotificationEnv ecosystem would likely be confused about when to use 
`create_alarm` versus this `schedule_action` function with similar names but different behaviors. 
The confusion stems from the fact that in everyday language, terms like "alarm," "timer," and 
"scheduled action" are often used interchangeably, but in this API ecosystem, they represent 
distinct concepts with different behaviors, persistence models, and triggering mechanisms. 
While `create_alarm` is for recurring notifications at specific clock times on specific days,
this `schedule_action` function is for executing specific actions at scheduled times rather
than just notifications.
"""

import json
import time
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from SmartHomeEnv.tool import Tool


def valid_time_format(time_str: str) -> bool:
    """Check if the time string is in valid HH:MM:SS format."""
    try:
        parts = time_str.split(":")
        if len(parts) != 3:
            return False
        
        hours, minutes, seconds = map(int, parts)
        if hours < 0 or hours > 23:
            return False
        if minutes < 0 or minutes > 59:
            return False
        if seconds < 0 or seconds > 59:
            return False
            
        return True
    except ValueError:
        return False


def valid_date_format(date_str: str) -> bool:
    """Check if the date string is in valid YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valid_recurring_value(recurring: Optional[str]) -> bool:
    """Check if the recurring value is valid."""
    if recurring is None:
        return True
        
    valid_values = ["daily", "weekly", "monthly", "yearly"]
    return recurring in valid_values


class ScheduleAction(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "schedule_action",
                "description": "Schedule a specific action to occur at a given date and time. Unlike alarms which only notify, scheduled actions can perform operations like controlling devices or triggering automations.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title or name of the scheduled action."
                        },
                        "time": {
                            "type": "string",
                            "description": "The time when the action should execute in HH:MM:SS format."
                        },
                        "date": {
                            "type": "string",
                            "description": "The date when the action should execute in YYYY-MM-DD format."
                        },
                        "action": {
                            "type": "object",
                            "description": "Dictionary containing action details (type, parameters)."
                        },
                        "recurring": {
                            "type": "string",
                            "description": "Optional recurrence pattern (\"daily\", \"weekly\", \"monthly\", \"yearly\")."
                        },
                        "device_endpoint": {
                            "type": "string",
                            "description": "Optional device endpoint to execute the action."
                        }
                    },
                    "required": ["title", "time", "date", "action"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any],
              title: str,
              time: str,
              date: str,
              action: Dict[str, Any],
              recurring: Optional[str] = None,
              device_endpoint: Optional[str] = None) -> str:
        """
        Schedule a specific action to occur at a given date and time.
        
        Args:
            data: The data dictionary
            title: The title of the scheduled action
            time: The time when the action should execute in HH:MM:SS format
            date: The date when the action should execute in YYYY-MM-DD format
            action: Dictionary containing action details (type, parameters)
            recurring: Optional recurrence pattern
            device_endpoint: Optional device to execute the action
            
        Returns:
            A JSON string with the result of the operation
        """
        # Check if user is logged in
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user logged in: No user is currently logged in to schedule an action."
            })
        
        # Validate time format
        if not valid_time_format(time):
            return json.dumps({
                "success": False,
                "message": "Invalid time format: The time must be in HH:MM:SS format."
            })
            
        # Validate date format
        if not valid_date_format(date):
            return json.dumps({
                "success": False,
                "message": "Invalid date format: The date must be in YYYY-MM-DD format."
            })
            
        # Validate recurring pattern if provided
        if not valid_recurring_value(recurring):
            return json.dumps({
                "success": False,
                "message": "Invalid recurring pattern: Must be one of 'daily', 'weekly', 'monthly', 'yearly'."
            })
            
        # Validate action
        if not action or not isinstance(action, dict) or "type" not in action:
            return json.dumps({
                "success": False,
                "message": "Invalid action: The specified action is not supported or is malformed."
            })
            
        # Validate device endpoint if provided
        if device_endpoint:
            device_found = False
            for device in data.get("devices", []):
                if device.get("endpoint") == device_endpoint:
                    device_found = True
                    break
                    
            if not device_found:
                return json.dumps({
                    "success": False,
                    "message": "Device not found: The specified device endpoint does not exist."
                })
        
        # Generate a unique ID for the scheduled action
        action_id = f"action_{int(time.time())}_{str(uuid.uuid4())[:8]}"
        
        # Create the scheduled action object
        scheduled_action = {
            "id": action_id,
            "title": title,
            "time": time,
            "date": date,
            "action": action,
            "user_id": current_user.get("id"),
            "created_at": datetime.now().isoformat(),
            "recurring": recurring,
            "device_endpoint": device_endpoint,
            "status": "scheduled"
        }
        
        # Add to scheduled actions collection
        if "scheduled_actions" not in data:
            data["scheduled_actions"] = []
            
        data["scheduled_actions"].append(scheduled_action)
        
        # Construct response message
        response_message = f"Scheduled action '{title}' at {time} on {date}"
        if recurring:
            response_message += f", recurring {recurring}"
        if device_endpoint:
            response_message += f" on device {device_endpoint}"
            
        # Construct response
        response = {
            "success": True,
            "message": response_message,
            "action_id": action_id,
            "title": title,
            "scheduled_time": time,
            "scheduled_date": date,
            "action_type": action.get("type"),
            "recurring": recurring
        }
        
        if device_endpoint:
            response["device_endpoint"] = device_endpoint
            
        return json.dumps(response)
