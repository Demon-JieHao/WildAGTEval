# Copyright TimeNotificationEnv

import json
from typing import Any, Dict, List, Optional
from TimeNotificationEnv.tool import Tool
from TimeNotificationEnv.helpers import get_current_user_id, generate_id


class CreateAlarm(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], 
              title: str, 
              time: str, 
              days: List[str], 
              sound: Optional[str] = "default", 
              device_endpoint: Optional[str] = None) -> str:
        """
        Create a new alarm for the current user.
        
        Args:
            data: The data dictionary
            title: The title of the alarm
            time: The time of the alarm in HH:MM:SS format
            days: List of days when the alarm should be active (e.g., ["monday", "tuesday"])
            sound: Optional sound to use for the alarm
            device_endpoint: Optional device to associate with the alarm
            
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
        
        # Validate time format (simple validation)
        try:
            hour, minute, second = time.split(":")
            hour_val = int(hour)
            minute_val = int(minute)
            second_val = int(second)
            
            if not (0 <= hour_val < 24 and 0 <= minute_val < 60 and 0 <= second_val < 60):
                raise ValueError("Invalid time values")
        except Exception:
            return json.dumps({
                "success": False,
                "message": "Invalid time format. Please use HH:MM:SS format."
            })
        
        # Validate days (convert to lowercase for consistency)
        valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        normalized_days = [day.lower() for day in days]
        invalid_days = [day for day in normalized_days if day not in valid_days]
        
        if invalid_days:
            return json.dumps({
                "success": False,
                "message": f"Invalid day(s): {', '.join(invalid_days)}"
            })
        
        # Validate device endpoint if provided
        if device_endpoint is not None:
            device_exists = False
            for device in data.get("devices", []):
                if device.get("endpoint") == device_endpoint:
                    device_exists = True
                    break
            
            if not device_exists:
                return json.dumps({
                    "success": False, 
                    "message": f"Device with endpoint '{device_endpoint}' not found"
                })
        
        # Generate a new alarm ID
        alarm_id = generate_id("alarm", data)
        
        # Create new alarm
        new_alarm = {
            "alarm_id": alarm_id,
            "user_id": user_id,
            "title": title,
            "time": time,
            "days": normalized_days,
            "active": True,
            "sound": sound,
            "device_endpoint": device_endpoint
        }
        
        # Add to alarms data
        if "alarms" not in data:
            data["alarms"] = []
        
        data["alarms"].append(new_alarm)
        
        return json.dumps({
            "success": True,
            "message": f"Alarm '{title}' created successfully",
            "alarm_id": alarm_id,
            "alarm": new_alarm
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_alarm",
                "description": "Create a new alarm with specified time, days, and optional device. Alarms are recurring events that happen on specified days at the given time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title or name of the alarm."
                        },
                        "time": {
                            "type": "string",
                            "description": "The time when the alarm should trigger in HH:MM:SS format (24-hour)."
                        },
                        "days": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of days when the alarm should be active (e.g., [\"monday\", \"tuesday\"])."
                        },
                        "sound": {
                            "type": "string",
                            "description": "Optional sound to use for the alarm. Defaults to 'default'."
                        },
                        "device_endpoint": {
                            "type": "string",
                            "description": "Optional device endpoint to associate with the alarm (e.g., for playing the alarm sound or triggering actions)."
                        }
                    },
                    "required": ["title", "time", "days"]
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to create an alarm.",
                    "Invalid time format: The time must be in HH:MM:SS format.",
                    "Invalid day: One or more specified days are invalid.",
                    "Device not found: The specified device endpoint does not exist."
                ]
            }
        }
