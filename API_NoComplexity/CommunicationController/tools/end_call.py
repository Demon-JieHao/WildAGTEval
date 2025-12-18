# Copyright CommunicationController

import json
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from CommunicationController.tool import Tool
from CommunicationController.helpers import get_active_call


class EndCall(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        """
        End the current active call for the user.
        
        Args:
            data: The data dictionary containing call information
            
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
        
        # Check if user has an active call
        active_call = get_active_call(data, user_id)
        if not active_call:
            return json.dumps({
                "success": False,
                "message": "No active call found"
            })
        
        call_id = active_call.get("call_id")
        
        # Update the call record in call history
        call_record = None
        for call in data.get("call_history", []):
            if call.get("call_id") == call_id:
                call_record = call
                
                # Calculate duration
                start_time = datetime.fromisoformat(call["timestamp"].replace("Z", "+00:00"))
                end_time = datetime.now(timezone.utc)
                duration_seconds = int((end_time - start_time).total_seconds())
                
                # Update call record
                call["status"] = "completed"
                call["duration"] = duration_seconds
                break
        
        # Remove from active calls
        if "active_calls" in data and user_id in data["active_calls"]:
            data["active_calls"].pop(user_id)
        
        # Return success
        contact_name = None
        if call_record and call_record.get("contact_id"):
            # Find contact name for better message
            for contact in data.get("contacts", []):
                if contact.get("contact_id") == call_record["contact_id"] and contact.get("user_id") == user_id:
                    contact_name = contact.get("name")
                    break
        
        return json.dumps({
            "success": True,
            "message": f"Call with {contact_name if contact_name else 'contact'} ended",
            "call_id": call_id,
            "duration": call_record["duration"] if call_record else 0,
            "status": "completed"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "end_call",
                "description": "End the current active call for the user. This tool terminates any ongoing call session and updates the call history with the relevant details.",
                "parameters": {
                    "type": "object",
                    "properties": {}  # No parameters needed for this function
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to end a call.",
                    "No active call: The user does not have any active call to end."
                ]
            }
        }
