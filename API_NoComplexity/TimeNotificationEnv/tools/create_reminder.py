# Copyright TimeNotificationEnv

import json
import re
from datetime import datetime
from typing import Any, Dict, Optional
from TimeNotificationEnv.tool import Tool
from TimeNotificationEnv.helpers import get_current_user_id, generate_id


class CreateReminder(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], 
              title: str, 
              date: str, 
              time: str, 
              description: Optional[str] = None, 
              notify_before_minutes: Optional[int] = 30) -> str:
        """
        Create a new reminder for the current user.
        
        Args:
            data: The data dictionary
            title: The title of the reminder
            date: The date of the reminder in YYYY-MM-DD format
            time: The time of the reminder in HH:MM:SS format
            description: Optional detailed description of the reminder
            notify_before_minutes: Optional minutes before to notify (default: 30 minutes)
            
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
        
        # Validate date format (YYYY-MM-DD)
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if not date_pattern.match(date):
            return json.dumps({
                "success": False,
                "message": "Invalid date format. Please use YYYY-MM-DD format."
            })
        
        # Validate time format (HH:MM:SS)
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
        
        # Check if the date and time are valid (not in the past)
        try:
            reminder_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
            current_datetime = datetime.now()
            
            if reminder_datetime < current_datetime:
                return json.dumps({
                    "success": False,
                    "message": "Cannot set reminder in the past"
                })
        except ValueError:
            return json.dumps({
                "success": False,
                "message": "Invalid date or time values"
            })
        
        # Validate notify_before_minutes
        if notify_before_minutes is not None and notify_before_minutes < 0:
            return json.dumps({
                "success": False,
                "message": "notify_before_minutes must be a non-negative number"
            })
        
        # Generate a new reminder ID
        reminder_id = generate_id("reminder", data)
        
        # Create new reminder
        new_reminder = {
            "reminder_id": reminder_id,
            "user_id": user_id,
            "title": title,
            "description": description,
            "date": date,
            "time": time,
            "notify_before_minutes": notify_before_minutes,
            "status": "pending"
        }
        
        # Add to reminders data
        if "reminders" not in data:
            data["reminders"] = []
        
        data["reminders"].append(new_reminder)
        
        return json.dumps({
            "success": True,
            "message": f"Reminder '{title}' created successfully for {date} at {time}",
            "reminder_id": reminder_id,
            "reminder": new_reminder
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_reminder",
                "description": "Create a new reminder with specified date, time, and optional description. Reminders are one-time events that happen at a specific date and time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title or name of the reminder."
                        },
                        "date": {
                            "type": "string",
                            "description": "The date of the reminder in YYYY-MM-DD format."
                        },
                        "time": {
                            "type": "string",
                            "description": "The time of the reminder in HH:MM:SS format (24-hour)."
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional detailed description or additional information about the reminder."
                        },
                        "notify_before_minutes": {
                            "type": "integer",
                            "description": "How many minutes before the reminder time to send a notification. Defaults to 30 minutes."
                        }
                    },
                    "required": ["title", "date", "time"]
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to create a reminder.",
                    "Invalid date format: The date must be in YYYY-MM-DD format.",
                    "Invalid time format: The time must be in HH:MM:SS format.",
                    "Past date/time: Cannot set a reminder in the past.",
                    "Invalid notify_before_minutes: Must be a non-negative number."
                ]
            }
        }
