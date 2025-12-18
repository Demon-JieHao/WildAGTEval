# Copyright CommunicationController

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base_env import BaseEnvironment
from common.shared_memory_service import SharedMemoryService
from CommunicationController.tools import ALL_TOOLS
from CommunicationController.rules import RULES
from CommunicationController.wiki import WIKI
from CommunicationController.helpers import (
    get_user_contacts, find_contact_by_id, find_contact_by_name, find_contact_by_phone, 
    find_contact_by_email, get_user_call_history, get_user_messages,
    find_communication_devices, get_active_call
)
from typing import Optional, Dict, Any, List


class CommunicationController(BaseEnvironment):
    """
    Communication Controller Environment for managing contacts, calls, and messages.
    """
    
    def __init__(self):
        """
        Initialize the Communication Controller Environment.
        """
        self.rules = RULES
        self.wiki = WIKI
        super().__init__()  # This will call _initialize_environment_data and _load_tools
        
    def _initialize_environment_data(self) -> None:
        """Initialize CommunicationController-specific data structures"""
        # Initialize contacts data if it doesn't exist
        if "contacts" not in self.data:
            self.data["contacts"] = []
        
        # Initialize call history data if it doesn't exist
        if "call_history" not in self.data:
            self.data["call_history"] = []
        
        # Initialize message history data if it doesn't exist
        if "message_history" not in self.data:
            self.data["message_history"] = []
        
        # Initialize active calls tracking
        if "active_calls" not in self.data:
            self.data["active_calls"] = {}
        
        # Ensure users have communication info
        for user in self.data.get("users", []):
            if "communication_info" not in user:
                user["communication_info"] = {
                    "preferred_device": None,
                    "video_enabled": True,
                    "do_not_disturb": False
                }
    
    def _load_tools(self) -> Dict[str, Any]:
        """Load CommunicationController-specific tools"""
        # Convert from list to dict format expected by base class
        tools_dict = {}
        for tool in ALL_TOOLS:
            tool_info = tool.get_info()
            if 'function' in tool_info and 'name' in tool_info['function']:
                tool_name = tool_info['function']['name']
                tools_dict[tool_name] = tool
        return tools_dict
    
    def _save_data(self) -> None:
        """
        Legacy method required by base class.
        In the new design, data is only stored in memory and never saved to disk.
        """
        # Don't save to disk, just update memory service
        self.memory_service.update_data(self.data)
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all available tools.
        
        Returns:
            List of tool information dictionaries
        """
        return [tool.get_info() for tool in self.tools.values()]
    
    def get_rules(self) -> List[str]:
        """
        Get all rules for the environment.
        
        Returns:
            List of rule strings
        """
        return self.rules
    
    def get_wiki(self) -> str:
        """
        Get the wiki documentation for the environment.
        
        Returns:
            Wiki documentation string
        """
        return self.wiki
    
    def get_user_contacts(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all contacts for a specific user.
        
        Args:
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            List of contact dictionaries for the user
        """
        return get_user_contacts(self.data, user_id)
    
    def find_contact(
        self,
        query: str,
        search_type: str = "name",
        user_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Find contacts based on search criteria.
        
        Args:
            query: The search term
            search_type: Type of search ('name', 'phone', 'email')
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            List of matching contact dictionaries
        """
        if search_type == "name":
            return find_contact_by_name(self.data, query, user_id)
        elif search_type == "phone":
            return find_contact_by_phone(self.data, query, user_id)
        elif search_type == "email":
            return find_contact_by_email(self.data, query, user_id)
        else:
            # Default to searching by name
            return find_contact_by_name(self.data, query, user_id)
    
    def get_contact(self, contact_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get a specific contact by ID.
        
        Args:
            contact_id: The ID of the contact to retrieve
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            The contact dictionary if found and belongs to the user, None otherwise
        """
        return find_contact_by_id(self.data, contact_id, user_id)
    
    def get_call_history(self, user_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get call history for a user.
        
        Args:
            user_id: The ID of the user (if None, uses current user)
            limit: Maximum number of calls to return
            
        Returns:
            List of call history entries
        """
        return get_user_call_history(self.data, user_id, limit)
    
    def get_messages(
        self, 
        contact_id: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Get messages for a user, optionally filtered by contact.
        
        Args:
            contact_id: If provided, only return messages with this contact
            user_id: The ID of the user (if None, uses current user)
            limit: Maximum number of messages to return
            
        Returns:
            List of message entries
        """
        return get_user_messages(self.data, contact_id, user_id, limit)
    
    def get_communication_devices(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get devices that can be used for communication.
        
        Args:
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            List of device dictionaries that support communication
        """
        return find_communication_devices(self.data, user_id)
    
    def get_active_call(self, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get the active call for a user, if any.
        
        Args:
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            The active call dictionary if found, None otherwise
        """
        return get_active_call(self.data, user_id)
