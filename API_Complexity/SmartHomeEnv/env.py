# Copyright SmartHomeEnv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base_env import BaseEnvironment
from common.shared_memory_service import SharedMemoryService
# Import only what we need for legacy support
from SmartHomeEnv.data import load_data
from SmartHomeEnv.tools import ALL_TOOLS
from SmartHomeEnv.rules import RULES
from SmartHomeEnv.wiki import WIKI
from SmartHomeEnv.helpers import get_current_user, set_current_user, get_user_by_id, get_user_by_name
from typing import Optional, Dict, Any, List


class SmartHomeEnv(BaseEnvironment):
    """
    Smart Home Environment for controlling smart home devices.
    """
    
    def __init__(self):
        """
        Initialize the Smart Home Environment.
        """
        self.rules = RULES
        self.wiki = WIKI
        super().__init__()  # This will call _load_data and _load_tools
        
    def _initialize_environment_data(self) -> None:
        """Initialize SmartHomeEnv-specific data structures"""
        # Setup any environment-specific data structures if needed
        # Most data is already loaded by the shared memory service
        pass
    
    def _load_tools(self) -> Dict[str, Any]:
        """Load SmartHomeEnv-specific tools"""
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
    
    def get_current_user_details(self) -> Dict[str, Any]:
        """
        Get the current user details.
        
        Returns:
            The current user dictionary
        """
        return get_current_user(self.data)
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a user by ID.
        
        Args:
            user_id: The user ID to search for
            
        Returns:
            The user dictionary if found, None otherwise
        """
        return get_user_by_id(self.data, user_id)
    
    def get_user_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a user by name.
        
        Args:
            name: The name to search for
            
        Returns:
            The user dictionary if found, None otherwise
        """
        return get_user_by_name(self.data, name)
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users.
        
        Returns:
            List of all user dictionaries
        """
        return self.data["users"]
