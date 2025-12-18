# Copyright CommunicationController

import json
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool
from CommunicationController.helpers import get_user_call_history, find_contact_by_id


class GetCallHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], time_range: str, limit: int = 10) -> str:
        """
        Get call history for the current user within a specified time range.
        
        Args:
            data: The data dictionary containing call history
            time_range: Time range in various formats:
                        - "7", "14" - Days (e.g. "7" for last 7 days)
                        - "7d", "2w", "3m", "1y" - Days, weeks, months, years
                        - "24h", "60min" - Hours, minutes
            limit: Maximum number of calls to return
            
        Returns:
            A JSON string with the result of the operation
        """
        # Get the current user's ID
        user_id = data.get("current_user")
        if not user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in"
            })
        
        # Get call history with time range
        calls = get_user_call_history(data, user_id, time_range, limit)
        
        # Add contact names to calls for better display
        enhanced_calls = []
        for call in calls:
            call_copy = call.copy()
            contact_id = call_copy.get("contact_id")
            
            if contact_id:
                contact = find_contact_by_id(data, contact_id, user_id)
                if contact:
                    call_copy["contact_name"] = contact.get("name")
            
            # Format duration in minutes and seconds
            duration = call_copy.get("duration", 0)
            if duration > 0:
                minutes = duration // 60
                seconds = duration % 60
                if minutes > 0:
                    call_copy["duration_formatted"] = f"{minutes} min {seconds} sec"
                else:
                    call_copy["duration_formatted"] = f"{seconds} sec"
            else:
                call_copy["duration_formatted"] = "0 sec"
            
            enhanced_calls.append(call_copy)
        
        # Return result
        return json.dumps({
            "success": True,
            "message": f"Retrieved {len(calls)} call records",
            "calls": enhanced_calls
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_call_history",
                "description": "Get call history for the current user within a specified time range. This tool retrieves the user's call records from the last N days, including incoming and outgoing calls, with details such as duration and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time_range": {
                            "type": "string",
                            "description": "Time range in various formats: '7' (days), '2w' (weeks), '3m' (months), '1y' (years), '24h' (hours), '60min' (minutes)."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of call records to return. Default is 10.",
                            "minimum": 1
                        }
                    },
                    "required": ["time_range"]
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to view call history."
                ]
            }
        }
