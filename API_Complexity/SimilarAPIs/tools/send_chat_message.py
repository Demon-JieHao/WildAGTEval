# Copyright CommunicationController

"""
Uncertainty Manifestation: Confusion Between Message Sending Functions

Description:
Developers face significant confusion between the `send_message` function which sends 
direct messages to individual contacts, and this `send_chat_message` function which sends 
messages to group chat rooms with multiple participants. The similar naming and overlapping 
parameter sets create a situation where developers frequently use the wrong function for their 
intended purpose, leading to messages being sent to incorrect recipients or unexpected behaviors 
in communication applications.
"""

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool


class SendChatMessage(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_chat_message",
                "description": "Send a message to a chat room with multiple participants. This tool allows sending text and attachments to group conversations where multiple users can interact.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "chat_room_id": {
                            "type": "string",
                            "description": "ID of the chat room to send the message to."
                        },
                        "content": {
                            "type": "string",
                            "description": "The message content to send."
                        },
                        "attachments": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string"},
                                    "url": {"type": "string"},
                                    "name": {"type": "string"}
                                }
                            },
                            "description": "Optional list of attachment objects."
                        }
                    },
                    "required": ["chat_room_id", "content"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], chat_room_id: str, content: str, 
              attachments: List[Dict] = None) -> str:
        """
        Send a message to a chat room with multiple participants.
        
        Args:
            data: The data dictionary containing chat rooms and messages
            chat_room_id: ID of the chat room to send the message to
            content: The message content to send
            attachments: Optional list of attachment objects
            
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
        
        # Check if content is provided (can be empty if attachments exist)
        if (not content or content.strip() == "") and not attachments:
            return json.dumps({
                "success": False,
                "message": "Empty content and no attachments: Message must contain either content or attachments"
            })
        
        # Check if chat room exists and user is a member
        chat_room = None
        for room in data.get("chat_rooms", []):
            if room.get("id") == chat_room_id:
                if user_id in room.get("participants", []):
                    chat_room = room
                    break
        
        if not chat_room:
            return json.dumps({
                "success": False,
                "message": f"Chat room not found: The chat room with ID {chat_room_id} does not exist or user is not a member"
            })
        
        # Generate a unique message ID
        message_id = f"chat_msg_{str(uuid.uuid4())[:8]}"
        
        # Create a message record
        timestamp = datetime.utcnow().isoformat() + "Z"
        message = {
            "message_id": message_id,
            "chat_room_id": chat_room_id,
            "sender_id": user_id,
            "timestamp": timestamp,
            "content": content,
            "attachments": attachments or [],
            "read_by": [user_id]  # Initially read only by sender
        }
        
        # Add to chat message history
        if "chat_messages" not in data:
            data["chat_messages"] = []
        data["chat_messages"].append(message)
        
        # Return success
        return json.dumps({
            "success": True,
            "message": f"Message sent to chat room {chat_room.get('name')}",
            "message_id": message_id,
            "chat_room_name": chat_room.get('name'),
            "timestamp": timestamp
        })
