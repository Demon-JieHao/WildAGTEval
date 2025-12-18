# Copyright CommunicationController

"""
Uncertainty Manifestation: Confusion Between `make_call` and `initiate_call_session`

Description:
Developers face significant confusion between two similarly named functions that handle communication 
but with fundamentally different purposes and behaviors. The `CommunicationController.make_call` 
function is designed for initiating standard phone/video calls between users and contacts, while 
this hypothetical `CommunicationController.initiate_call_session` is designed for establishing 
multi-party conference sessions with advanced features. The similar naming and overlapping 
parameter sets create a situation where developers frequently use the wrong function for their 
intended purpose, leading to unexpected behaviors and integration issues.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool


class CallSessionManager(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function", 
            "function": {
                "name": "initiate_call_session",
                "description": "Initiate a call session with one or multiple participants. This tool creates a communication session that can include multiple participants and advanced features like recording and screen sharing.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "session_name": {
                            "type": "string",
                            "description": "Optional name for the call session."
                        },
                        "participants": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of participant IDs or phone numbers for multi-party calls."
                        },
                        "contact_id": {
                            "type": "string",
                            "description": "ID of the contact to call (for single-party calls)."
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "Phone number to call (alternative to contact_id)."
                        },
                        "device_endpoint": {
                            "type": "string",
                            "description": "Endpoint ID of the device to use for calling. If not specified, a suitable device will be selected automatically."
                        },
                        "call_type": {
                            "type": "string",
                            "enum": ["audio", "video", "conference"],
                            "description": "Type of call to make. Default is 'audio'."
                        },
                        "session_features": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["recording", "transcription", "screen_sharing"]
                            },
                            "description": "List of features to enable for this call session."
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        recipient_id: Optional[str] = None,
        phone_number: Optional[str] = None,
        session_type: str = "standard",
        with_recording: bool = False,
        virtual_background: Optional[str] = None
    ) -> str:
        """
        Initiate a virtual call session in the cloud communication platform.
        
        Args:
            data: The data dictionary containing user and session information
            recipient_id: ID of the recipient to call (user ID, not contact ID)
            phone_number: Phone number to call (alternative to recipient_id)
            session_type: Type of session ('standard', 'conference', 'webinar')
            with_recording: Whether to record the call session
            virtual_background: Optional background image URL for video calls
            
        Returns:
            A JSON string with the session details and join URL
        """
        # Validate current user is logged in
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "error": "No user logged in: No user is currently logged in to create sessions."
            })
        
        # Validate session parameters
        valid_session_types = ["standard", "conference", "webinar"]
        if session_type not in valid_session_types:
            return json.dumps({
                "success": False,
                "error": f"Invalid session type: {session_type}. Valid types are {', '.join(valid_session_types)}"
            })
        
        # Check user permissions for recording
        if with_recording and not current_user.get("can_record_calls", False):
            return json.dumps({
                "success": False,
                "error": "Recording not permitted: The user does not have permission to record calls."
            })
        
        # Check session limits
        active_sessions = data.get("active_sessions", {}).get(current_user["user_id"], [])
        max_sessions = current_user.get("max_concurrent_sessions", 3)
        if len(active_sessions) >= max_sessions:
            return json.dumps({
                "success": False,
                "error": f"Session limit reached: The user has reached their maximum number of concurrent sessions ({max_sessions})."
            })
        
        # Validate recipient
        recipient = None
        if recipient_id:
            # Look up the recipient in users, not contacts
            users = data.get("users", {})
            if recipient_id not in users:
                return json.dumps({
                    "success": False,
                    "error": "Invalid recipient: The specified recipient ID does not exist in the system."
                })
            recipient = users[recipient_id]
        elif phone_number:
            # External phone number recipient
            recipient = {"phone_number": phone_number, "type": "external"}
        else:
            # No recipient specified - creating an open session
            recipient = {"type": "open_session"}
        
        # Generate session details
        timestamp = datetime.now().isoformat()
        session_id = f"session-{current_user['user_id']}-{int(datetime.now().timestamp())}"
        join_url = f"https://meetings.example.com/join/{session_id}"
        
        # Create the session object
        session = {
            "session_id": session_id,
            "creator_id": current_user["user_id"],
            "creator_name": current_user.get("name", "Unknown User"),
            "recipient": recipient,
            "session_type": session_type,
            "with_recording": with_recording,
            "virtual_background": virtual_background,
            "status": "created",
            "join_url": join_url,
            "created_at": timestamp,
            "active": True
        }
        
        # Save the session in the data store
        if "sessions" not in data:
            data["sessions"] = {}
        data["sessions"][session_id] = session
        
        # Update active sessions for the user
        if "active_sessions" not in data:
            data["active_sessions"] = {}
        if current_user["user_id"] not in data["active_sessions"]:
            data["active_sessions"][current_user["user_id"]] = []
        data["active_sessions"][current_user["user_id"]].append(session_id)
        
        return json.dumps({
            "success": True,
            "session_id": session_id,
            "join_url": join_url,
            "session": session
        })
