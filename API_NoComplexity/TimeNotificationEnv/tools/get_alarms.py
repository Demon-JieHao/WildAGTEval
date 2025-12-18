# Copyright TimeNotificationEnv

import json
from typing import Any, Dict, List, Optional
from TimeNotificationEnv.tool import Tool
from TimeNotificationEnv.helpers import get_user_alarms


class GetAlarms(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], active_only: bool = False) -> str:
        """
        Get all alarms for the current user.
        
        Args:
            data: The data dictionary
            active_only: Whether to return only active alarms
            
        Returns:
            A JSON string with the result of the operation
        """
        # Get current user's alarms
        alarms = get_user_alarms(data)
        
        # Filter for active alarms if requested
        if active_only:
            alarms = [alarm for alarm in alarms if alarm.get("active", True)]
        
        # Sort alarms by time
        alarms.sort(key=lambda a: a.get("time", ""))
        
        if not alarms:
            message = "No alarms found"
            if active_only:
                message += " (active only)"
        else:
            message = f"Found {len(alarms)} alarm(s)"
            if active_only:
                message += " (active only)"
                
        # Return the alarms
        return json.dumps({
            "success": True,
            "message": message,
            "alarms": alarms
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_alarms",
                "description": "Get all alarms for the current user. Returns a list of alarm objects sorted by time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "active_only": {
                            "type": "boolean",
                            "description": "If true, return only active alarms. If false, return all alarms."
                        }
                    }
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to retrieve alarms."
                ]
            }
        }
