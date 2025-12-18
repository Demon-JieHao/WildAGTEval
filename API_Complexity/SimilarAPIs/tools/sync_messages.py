# Copyright CommunicationController

"""
Uncertainty Manifestation: Confusion Between Message Management Functions

Description:
Developers face significant confusion between the `get_messages` function which retrieves 
messages from the local device storage, and this `sync_messages` function which synchronizes 
messages with a remote server, updating the local database. The similar naming and overlapping 
parameter sets create a situation where developers frequently use the wrong function, expecting 
to either retrieve local messages when they're actually triggering a network synchronization, 
or expecting synchronization when they're simply querying local data. This leads to unexpected 
behaviors, unnecessary network calls, and integration issues.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool


def find_contact_by_id(data: Dict[str, Any], contact_id: str, user_id: str) -> Dict[str, Any]:
    """Find a contact by ID in a user's contacts."""
    user_contacts = data.get("contacts", {}).get(user_id, [])
    for contact in user_contacts:
        if contact.get("id") == contact_id:
            return contact
    return None


def check_network_connectivity() -> bool:
    """Check if network connectivity is available."""
    # In a real implementation, this would check actual network connectivity
    # For this example, we'll assume connectivity is available
    return True


def get_last_sync_timestamp(data: Dict[str, Any], user_id: str, contact_id: Optional[str] = None) -> str:
    """Get the timestamp of the last synchronization."""
    sync_info = data.get("sync_info", {}).get(user_id, {})
    if contact_id:
        return sync_info.get(f"contact_{contact_id}", "1970-01-01T00:00:00Z")
    else:
        return sync_info.get("all_contacts", "1970-01-01T00:00:00Z")


def perform_message_sync(
    data: Dict[str, Any], 
    user_id: str, 
    contact_id: Optional[str] = None, 
    last_sync: str = "1970-01-01T00:00:00Z", 
    sync_type: str = "incremental"
) -> Dict[str, Any]:
    """Perform message synchronization with the server."""
    # In a real implementation, this would make API calls to a remote server
    # For this example, we'll simulate the synchronization

    # Get messages from "server" (just using data for simulation)
    server_messages = data.get("server_messages", {}).get(user_id, [])
    
    # Filter by contact if needed
    if contact_id:
        server_messages = [msg for msg in server_messages if msg.get("contact_id") == contact_id]
    
    # Get only messages after the last sync if doing incremental sync
    if sync_type == "incremental":
        server_messages = [
            msg for msg in server_messages 
            if msg.get("timestamp", "1970-01-01T00:00:00Z") > last_sync
        ]
    
    # Simulate some deleted message IDs
    deleted_ids = data.get("deleted_message_ids", {}).get(user_id, [])
    
    # Simulate conflicts (messages edited both locally and on server)
    # In a real implementation, this would detect actual conflicts
    conflicts = []
    
    return {
        "messages": server_messages,
        "deleted_ids": deleted_ids,
        "conflicts": conflicts
    }


def update_local_messages(data: Dict[str, Any], messages: List[Dict[str, Any]]) -> int:
    """Update local message store with messages from the server."""
    if "messages" not in data:
        data["messages"] = {}
    
    updated_count = 0
    
    for message in messages:
        user_id = message.get("user_id")
        message_id = message.get("id")
        
        if user_id and message_id:
            if user_id not in data["messages"]:
                data["messages"][user_id] = {}
            
            data["messages"][user_id][message_id] = message
            updated_count += 1
    
    return updated_count


def delete_removed_messages(data: Dict[str, Any], message_ids: List[str]) -> int:
    """Delete messages that have been removed on the server."""
    if not message_ids:
        return 0
    
    deleted_count = 0
    
    for user_id in data.get("messages", {}):
        for message_id in list(data["messages"][user_id].keys()):
            if message_id in message_ids:
                del data["messages"][user_id][message_id]
                deleted_count += 1
    
    return deleted_count


def update_sync_timestamp(data: Dict[str, Any], user_id: str, contact_id: Optional[str] = None) -> None:
    """Update the last synchronization timestamp."""
    if "sync_info" not in data:
        data["sync_info"] = {}
    
    if user_id not in data["sync_info"]:
        data["sync_info"][user_id] = {}
    
    timestamp = datetime.now().isoformat() + "Z"
    
    if contact_id:
        data["sync_info"][user_id][f"contact_{contact_id}"] = timestamp
    else:
        data["sync_info"][user_id]["all_contacts"] = timestamp


class SyncMessages(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "sync_messages",
                "description": "Synchronize messages with the server. This tool performs two-way synchronization between the local message store and the server, updating both as needed. It can sync all messages or only messages for a specific contact.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "contact_id": {
                            "type": "string",
                            "description": "Optional ID of the contact to sync messages for. If not provided, all contacts' messages will be synchronized."
                        },
                        "force_full_sync": {
                            "type": "boolean",
                            "description": "Whether to force a full synchronization instead of incremental. Default is false (incremental sync)."
                        }
                    }
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], contact_id: Optional[str] = None, force_full_sync: bool = False) -> str:
        """
        Synchronize messages with the server for the current user, optionally filtered by contact.
        
        Args:
            data: The data dictionary containing messages
            contact_id: Optional ID of the contact to sync messages for
            force_full_sync: Whether to force a full synchronization instead of incremental
            
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
        
        # If contact_id is provided, verify it exists and belongs to the user
        contact = None
        if contact_id:
            contact = find_contact_by_id(data, contact_id, user_id)
            if not contact:
                return json.dumps({
                    "success": False,
                    "message": f"Contact with ID {contact_id} not found"
                })
        
        # Check network connectivity
        if not check_network_connectivity():
            return json.dumps({
                "success": False,
                "message": "Network connectivity required for message synchronization"
            })
        
        # Get last sync timestamp
        last_sync = get_last_sync_timestamp(data, user_id, contact_id)
        
        # Determine sync type
        sync_type = "full" if force_full_sync else "incremental"
        
        # Perform synchronization with server
        sync_result = perform_message_sync(data, user_id, contact_id, last_sync, sync_type)
        
        # Update local message store with changes
        updated_count = update_local_messages(data, sync_result["messages"])
        deleted_count = delete_removed_messages(data, sync_result["deleted_ids"])
        
        # Update sync timestamp
        update_sync_timestamp(data, user_id, contact_id)
        
        # Return result
        context = ""
        if contact_id and contact:
            context = f" with {contact.get('name', '')}"
            
        return json.dumps({
            "success": True,
            "message": f"Synchronized messages{context}",
            "sync_type": sync_type,
            "updated": updated_count,
            "deleted": deleted_count,
            "conflicts": sync_result["conflicts"]
        })
