# Copyright TimeNotificationEnv

"""
Uncertainty Manifestation: Confusion Between Alarms, Timers, and Scheduled Actions

Description:
Developers using the TimeNotificationEnv ecosystem would likely be confused about when to use 
`create_alarm` versus this `create_timer` function with similar names but different behaviors. 
The confusion stems from the fact that in everyday language, terms like "alarm," "timer," and 
"scheduled action" are often used interchangeably, but in this API ecosystem, they represent 
distinct concepts with different behaviors, persistence models, and triggering mechanisms. 
While `create_alarm` is for recurring notifications at specific clock times on specific days,
this `create_timer` is for countdown-based notifications after a duration.
"""

import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from SmartHomeEnv.tool import Tool


def valid_duration_format(duration: str) -> bool:
    """Check if the duration string is in valid HH:MM:SS format."""
    try:
        parts = duration.split(":")
        if len(parts) != 3:
            return False
        
        hours, minutes, seconds = map(int, parts)
        if hours < 0 or minutes < 0 or seconds < 0:
            return False
        if minutes > 59 or seconds > 59:
            return False
            
        return True
    except ValueError:
        return False


def parse_duration_to_seconds(duration: str) -> int:
    """Convert a duration string in HH:MM:SS format to seconds."""
    hours, minutes, seconds = map(int, duration.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def calculate_end_time(duration: str) -> datetime:
    """Calculate the end time based on the current time and duration."""
    seconds = parse_duration_to_seconds(duration)
    return datetime.now() + timedelta(seconds=seconds)


class CreateTimer(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_timer",
                "description": "Create a countdown timer that triggers after a specified duration. Timers are one-time or repeating events that count down from a duration rather than triggering at specific times.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title or name of the timer."
                        },
                        "duration": {
                            "type": "string",
                            "description": "The duration of the timer in HH:MM:SS format."
                        },
                        "sound": {
                            "type": "string",
                            "description": "Optional sound to use for the timer. Defaults to 'default'."
                        },
                        "device_endpoint": {
                            "type": "string",
                            "description": "Optional device endpoint to associate with the timer."
                        },
                        "repeat": {
                            "type": "boolean",
                            "description": "Whether the timer should automatically restart after completion."
                        }
                    },
                    "required": ["title", "duration"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any],
              title: str,
              duration: str,
              sound: Optional[str] = "default",
              device_endpoint: Optional[str] = None,
              repeat: Optional[bool] = False) -> str:
        """
        Create a countdown timer that triggers after a specified duration.
        
        Args:
            data: The data dictionary
            title: The title of the timer
            duration: The duration of the timer in HH:MM:SS format
            sound: Optional sound to use when timer completes
            device_endpoint: Optional device to associate with the timer
            repeat: Whether the timer should automatically restart after completion
            
        Returns:
            A JSON string with the result of the operation
        """
        # Check if user is logged in
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user logged in: No user is currently logged in to create a timer."
            })
            
        # Validate duration format
        if not valid_duration_format(duration):
            return json.dumps({
                "success": False,
                "message": "Invalid duration format: The duration must be in HH:MM:SS format."
            })
            
        # Check if device exists if specified
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
                
        # Calculate end time based on duration
        end_time = calculate_end_time(duration)
        
        # Generate timer ID
        timer_id = f"timer_{int(time.time())}_{str(uuid.uuid4())[:8]}"
        
        # Create timer object
        timer = {
            "id": timer_id,
            "title": title,
            "user_id": current_user.get("id"),
            "created_at": datetime.now().isoformat(),
            "duration": duration,
            "duration_seconds": parse_duration_to_seconds(duration),
            "end_time": end_time.isoformat(),
            "sound": sound,
            "device_endpoint": device_endpoint,
            "repeat": repeat,
            "active": True
        }
        
        # Add to timers collection
        if "timers" not in data:
            data["timers"] = []
            
        data["timers"].append(timer)
        
        # Construct human-readable duration text for response
        hours, minutes, seconds = map(int, duration.split(":"))
        duration_text = []
        if hours > 0:
            duration_text.append(f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes > 0:
            duration_text.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        if seconds > 0:
            duration_text.append(f"{seconds} second{'s' if seconds > 1 else ''}")
            
        duration_str = ", ".join(duration_text)
        
        # Construct response
        response = {
            "success": True,
            "message": f"Timer '{title}' created for {duration_str} from now",
            "timer_id": timer_id,
            "end_time": end_time.isoformat(),
            "repeat": repeat
        }
        
        # Add device info if applicable
        if device_endpoint:
            response["device_endpoint"] = device_endpoint
            
        return json.dumps(response)
