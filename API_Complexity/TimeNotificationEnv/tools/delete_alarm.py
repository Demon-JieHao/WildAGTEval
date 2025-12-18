# Copyright TimeNotificationEnv

import json
from typing import Any, Dict, Optional
from TimeNotificationEnv.tool import Tool
from TimeNotificationEnv.helpers import get_current_user_id, find_alarm_by_id


class DeleteAlarm(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], alarm_id: str, deactivate_only: bool = False) -> str:
        """
        Delete or deactivate an alarm.
        
        Args:
            data: The data dictionary
            alarm_id: The ID of the alarm to delete
            deactivate_only: If True, just deactivate the alarm; if False, delete it completely
            
        Returns:
            A JSON string with the result of the operation
        """
        # Get the current user
        user_id = get_current_user_id(data)
        if not user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in"
            })
        
        # Find the alarm
        alarm = find_alarm_by_id(data, alarm_id, user_id)
        if not alarm:
            return json.dumps({
                "success": False,
                "message": f"Alarm with ID '{alarm_id}' not found"
            })
        
        if deactivate_only:
            # Just deactivate the alarm
            alarm["active"] = False
            
            return json.dumps({
                "success": True,
                "message": f"Alarm '{alarm.get('title')}' has been deactivated",
                "alarm": alarm
            })
        else:
            # Remove the alarm completely
            data["alarms"] = [a for a in data.get("alarms", []) if not (a.get("alarm_id") == alarm_id and a.get("user_id") == user_id)]
            
            return json.dumps({
                "success": True,
                "message": f"Alarm '{alarm.get('title')}' has been deleted"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "delete_alarm",
                "description": "Delete or deactivate an existing alarm.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "alarm_id": {
                            "type": "string",
                            "description": "The ID of the alarm to delete."
                        },
                        "deactivate_only": {
                            "type": "boolean",
                            "description": "If true, just deactivate the alarm rather than deleting it completely."
                        }
                    },
                    "required": ["alarm_id"]
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to delete an alarm.",
                    "Alarm not found: The specified alarm ID does not exist or does not belong to the current user."
                ]
            }
        }
