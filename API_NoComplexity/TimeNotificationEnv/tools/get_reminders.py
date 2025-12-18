# Copyright TimeNotificationEnv

import json
from typing import Any, Dict, List, Optional
from TimeNotificationEnv.tool import Tool
from TimeNotificationEnv.helpers import get_user_reminders


class GetReminders(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], 
              status: Optional[str] = None,
              date_from: Optional[str] = None,
              date_to: Optional[str] = None) -> str:
        """
        Get reminders for the current user with optional filters.
        
        Args:
            data: The data dictionary
            status: Optional filter for reminder status ("pending", "completed", "cancelled")
            date_from: Optional filter for earliest reminder date (YYYY-MM-DD)
            date_to: Optional filter for latest reminder date (YYYY-MM-DD)
            
        Returns:
            A JSON string with the result of the operation
        """
        # Get current user's reminders
        reminders = get_user_reminders(data)
        
        # Filter by status if specified
        if status:
            reminders = [reminder for reminder in reminders if reminder.get("status") == status]
        
        # Filter by date range if specified
        if date_from:
            reminders = [reminder for reminder in reminders if reminder.get("date", "") >= date_from]
        
        if date_to:
            reminders = [reminder for reminder in reminders if reminder.get("date", "") <= date_to]
        
        # Sort reminders by date and time
        reminders.sort(key=lambda r: (r.get("date", ""), r.get("time", "")))
        
        if not reminders:
            message = "No reminders found"
            if status or date_from or date_to:
                message += " matching the specified filters"
        else:
            message = f"Found {len(reminders)} reminder(s)"
            if status or date_from or date_to:
                message += " matching the specified filters"
                
        # Return the reminders
        return json.dumps({
            "success": True,
            "message": message,
            "reminders": reminders
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_reminders",
                "description": "Get reminders for the current user with optional filters. Returns a list of reminder objects sorted by date and time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["pending", "completed", "cancelled"],
                            "description": "Optional filter for reminder status."
                        },
                        "date_from": {
                            "type": "string",
                            "description": "Optional filter for earliest reminder date (YYYY-MM-DD)."
                        },
                        "date_to": {
                            "type": "string",
                            "description": "Optional filter for latest reminder date (YYYY-MM-DD)."
                        }
                    }
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to retrieve reminders."
                ]
            }
        }
