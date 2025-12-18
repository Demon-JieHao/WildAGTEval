# Copyright CommunicationController

import json
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool
from CommunicationController.helpers import get_user_messages, find_contact_by_id


class GetMessages(Tool):
    @staticmethod
    def _extract_message_id_number(message_id: str) -> int:
        """Extract number from message_id (e.g., msg6 -> 6, msg58 -> 58)"""
        import re
        match = re.match(r'msg(\d+)', message_id)
        return int(match.group(1)) if match else 0
    
    @staticmethod
    def _enrich_message_with_analytics_metadata(message):
        """Add system analytics and engagement data to message record using deterministic generation"""
        enriched_message = message.copy()
        message_id = message.get('message_id', 'msg0')
        
        # Extract message number for deterministic calculations
        msg_num = GetMessages._extract_message_id_number(message_id)
        
        # Add engagement analytics
        enriched_message["engagement_score"] = round(40 + (msg_num * 7) % 41, 1)  # 40.0-80.0
        enriched_message["response_time_percentile"] = 60 + (msg_num * 11) % 40  # 60-99
        enriched_message["conversation_health_index"] = round(0.5 + ((msg_num * 13) % 50) / 100, 3)  # 0.5-1.0
        
        # Add marketing/promotional data
        enriched_message["upsell_opportunity_score"] = 30 + (msg_num * 17) % 71  # 30-100
        enriched_message["retention_risk_indicator"] = ["low", "medium", "high"][(msg_num * 19) % 3]
        enriched_message["cross_sell_product_suggestions"] = [
            ["premium_messaging", "video_calls"],
            ["file_sharing", "group_chat"],
            ["voice_notes", "read_receipts"],
            ["message_encryption", "backup_service"]
        ][(msg_num * 23) % 4]
        
        # Add system performance metrics
        enriched_message["delivery_latency_ms"] = 50 + (msg_num * 29) % 201  # 50-250
        enriched_message["encryption_overhead_factor"] = round(1.0 + ((msg_num * 31) % 15) / 100, 3)  # 1.0-1.15
        enriched_message["storage_optimization_tier"] = ["standard", "compressed", "archived", "priority"][(msg_num * 37) % 4]
        
        # Add behavioral predictions
        enriched_message["predicted_next_contact_hours"] = 1 + (msg_num * 41) % 168  # 1-168 hours (1 week)
        enriched_message["sentiment_trend_vector"] = [
            round(0.3 + ((msg_num * 43) % 70) / 100, 3),  # 0.3-1.0
            round(0.4 + ((msg_num * 47) % 60) / 100, 3),  # 0.4-1.0
            round(0.2 + ((msg_num * 53) % 80) / 100, 3)   # 0.2-1.0
        ]
        enriched_message["communication_pattern_cluster"] = ["frequent_short", "sporadic_long", "burst_messaging", "scheduled_regular"][(msg_num * 59) % 4]
        
        # Add platform optimization data
        enriched_message["rendering_priority_score"] = 60 + (msg_num * 61) % 41  # 60-100
        enriched_message["cache_efficiency_rating"] = round(0.7 + ((msg_num * 67) % 30) / 100, 3)  # 0.7-1.0
        enriched_message["network_path_optimization"] = ["direct", "edge_cached", "cdn_routed", "peer_relay"][(msg_num * 71) % 4]
        
        # Add compliance and audit metadata
        enriched_message["data_retention_policy_days"] = [30, 90, 180, 365, 730][(msg_num * 73) % 5]
        enriched_message["gdpr_classification"] = ["personal_communication", "business_correspondence", "promotional_content", "system_notification"][(msg_num * 79) % 4]
        enriched_message["audit_trail_reference"] = f"msg_audit_2024_{1000 + (msg_num * 83) % 9000:04d}"  # msg_audit_2024_1000 to msg_audit_2024_9999
        
        return enriched_message

    @staticmethod
    def invoke(data: Dict[str, Any], contact_id: Optional[str] = None, limit: int = 10) -> str:
        """
        Get messages for the current user, optionally filtered by contact.
        
        Args:
            data: The data dictionary containing messages
            contact_id: Optional ID of the contact to filter messages
            limit: Maximum number of messages to return
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behaviors should be activated ###
        import os
        uncertainty_partially_irrelevant_information_enabled = os.getenv('ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_MESSAGES', 'false').lower() == 'true'
        uncertainty_feature_limitation_error_enabled = os.getenv('ENABLE__FEATURE_LIMITATION_ERROR__GET_MESSAGES', 'false').lower() == 'true'
        
        ### ADDED: Feature limitation check - restrict unfiltered message retrieval ###
        if uncertainty_feature_limitation_error_enabled:
            # When retrieving all messages (no contact_id), impose time restriction
            return json.dumps({
                "success": False,
                "message": "Retrieving all messages is temporarily limited to recent history"
            })
        ### END ADDED ###
        
        # Get the current user's ID
        user_id = data.get("current_user")
        if not user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in"
            })
        
        # If contact_id is provided, verify it exists and belongs to the user
        contact = None
        if contact_id:
            contact = find_contact_by_id(data, contact_id, user_id)
            if not contact:
                return json.dumps({
                    "success": False,
                    "message": f"Contact with ID {contact_id} not found"
                })
        
        # Get messages
        messages = get_user_messages(data, contact_id, user_id, limit)
        
        # Mark incoming messages as read
        for message in messages:
            if message.get("direction") == "incoming" and message.get("read") == False:
                message["read"] = True
        
        # Add contact names to messages for better display
        enhanced_messages = []
        for message in messages:
            msg_copy = message.copy()
            msg_contact_id = msg_copy.get("contact_id")
            
            if msg_contact_id:
                msg_contact = find_contact_by_id(data, msg_contact_id, user_id)
                if msg_contact:
                    msg_copy["contact_name"] = msg_contact.get("name")
            
            ### ADDED: Enrich message with extensive analytics and metadata when uncertainty is enabled ###
            if uncertainty_partially_irrelevant_information_enabled:
                msg_copy = GetMessages._enrich_message_with_analytics_metadata(msg_copy)
            ### END ADDED ###
            
            enhanced_messages.append(msg_copy)
        
        # Return result
        if contact:
            return json.dumps({
                "success": True,
                "message": f"Retrieved {len(messages)} messages with {contact.get('name')}",
                "contact_name": contact.get("name"),
                "contact_id": contact_id,
                "messages": enhanced_messages
            })
        else:
            return json.dumps({
                "success": True,
                "message": f"Retrieved {len(messages)} messages across all contacts",
                "messages": enhanced_messages
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_messages",
                "description": "Get message history for the current user, optionally filtered by contact. This tool retrieves message history and allows viewing conversations with specific contacts.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contact_id": {
                            "type": "string",
                            "description": "Optional ID of the contact to filter messages. If not provided, returns messages across all contacts."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of messages to return. Default is 10.",
                            "minimum": 1
                        }
                    }
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to view messages.",
                    "Contact not found: The specified contact ID does not exist in the user's contacts."
                ]
            }
        }
