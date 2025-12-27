# Copyright CommunicationController

import json
from datetime import datetime
from typing import Any, Dict, Optional
from CommunicationController.tool import Tool
from CommunicationController.helpers import find_contact_by_id


class SendMessage(Tool):
    @staticmethod
    def generate_sequential_message_id(data):

        if "message_history" not in data:
            data["message_history"] = []
        
        existing_ids = []
        for message in data["message_history"]:
            if "message_id" in message and message["message_id"].startswith("msg"):
                try:
                    num = int(message["message_id"].replace("msg", ""))
                    existing_ids.append(num)
                except ValueError:
                    continue
        
        next_num = 1
        if existing_ids:
            next_num = max(existing_ids) + 1
        
        return f"msg{next_num}" 
    
    @staticmethod
    def invoke(data: Dict[str, Any], contact_id: str, content: str) -> str:
        """
        Send a message to a specific contact.
        
        Args:
            data: The data dictionary containing contacts and messages
            contact_id: ID of the contact to send the message to
            content: The message content to send
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_system_failure_error_enabled = os.getenv('ENABLE__SYSTEM_FAILURE_ERROR__SEND_MESSAGE', 'false').lower() == 'true'
        
        # Get the current user's ID
        user_id = data.get("current_user")
        if not user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in"
            })
        
        # Check if content is provided
        if not content or content.strip() == "":
            return json.dumps({
                "success": False,
                "message": "Message content cannot be empty"
            })
        
        # Check if contact exists and belongs to the user
        contact = find_contact_by_id(data, contact_id, user_id)
        if not contact:
            return json.dumps({
                "success": False,
                "message": f"Contact with ID {contact_id} not found"
            })
        
        # Generate a sequential message ID
        message_id = SendMessage.generate_sequential_message_id(data)
        
        ### ADDED: Simulate message queue infrastructure failure when uncertainty is enabled ###
        if uncertainty_system_failure_error_enabled:
            # Deterministic failure scenario (no randomization)
            failure_scenario = {
                "error": "MQ_BROKER_UNREACHABLE_ERR_0x7F3A",
                "message": "RabbitMQ cluster node rabbit@mq-prod-03.messaging.internal unreachable after 3 heartbeat intervals (15000ms), AMQP connection failed on port 5672, vhost '/production' inaccessible, cluster quorum lost (2/5 nodes responding), message persistence cannot be guaranteed",
                "technical_details": {
                    "connection_string": "amqp://msg-service:****@mq-prod-03.messaging.internal:5672/production",
                    "queue_depth": "unknown",
                    "consumer_count": 0,
                    "cluster_state": "DEGRADED"
                },
                "correlation_id": "fixed-correlation-msg-12345"  # Fixed instead of uuid
            }
            
            return json.dumps({
                "success": False,
                **failure_scenario,
                "service": "CommunicationController.send_message",
                "trace_id": "trace-msg-67890"  # Fixed trace_id
            })
        ### END ADDED ###
        
        # Create a message record
        timestamp = datetime.utcnow().isoformat() + "Z"
        message = {
            "message_id": message_id,
            "user_id": user_id,
            "contact_id": contact_id,
            "direction": "outgoing",
            "timestamp": timestamp,
            "content": content,
            "read": True  # Outgoing messages are marked as read
        }
        
        # Add to message history
        if "message_history" not in data:
            data["message_history"] = []
        data["message_history"].append(message)
        
        # # Simulate a response message if this is a demo
        # if data.get("demo_mode", False):
        #     # 자동 응답 메시지도 순차적 ID 사용
        #     response_id = SendMessage.generate_sequential_message_id(data)
        #     response_timestamp = datetime.utcnow().isoformat() + "Z"
        #     response = {
        #         "message_id": response_id,
        #         "user_id": user_id,
        #         "contact_id": contact_id,
        #         "direction": "incoming",
        #         "timestamp": response_timestamp,
        #         "content": f"Auto-reply: I received your message: '{content}'",
        #         "read": False
        #     }
        #     data["message_history"].append(response)
        #     has_response = True
        # else:
        has_response = False
        
        # Return success
        return json.dumps({
            "success": True,
            "message": f"Message sent to {contact.get('name')}",
            "message_id": message_id,
            "contact_name": contact.get('name'),
            "timestamp": timestamp,
            "has_response": has_response
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "send_message",
                "description": "Send a text message to a specific contact. This tool allows sending messages to contacts in the user's contact list.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contact_id": {
                            "type": "string",
                            "description": "ID of the contact to send the message to."
                        },
                        "content": {
                            "type": "string",
                            "description": "The message content to send."
                        }
                    },
                    "required": ["contact_id", "content"]
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to send messages.",
                    "Empty content: Message content cannot be empty.",
                    "Contact not found: The specified contact ID does not exist in the user's contacts."
                ]
            }
        }
