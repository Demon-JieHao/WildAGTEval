# Copyright SmartHomeEnv

from SmartHomeEnv.data import load_data, save_data
from SmartHomeEnv.tools import ALL_TOOLS
from SmartHomeEnv.rules import RULES
from SmartHomeEnv.wiki import WIKI
from SmartHomeEnv.helpers import get_current_user, set_current_user, get_user_by_id, get_user_by_name
from typing import Optional, Dict, Any, List


class SmartHomeEnv:
    """
    Smart Home Environment for controlling smart home devices.
    """
    
    def __init__(self):
        """
        Initialize the Smart Home Environment.
        """
        self.data = load_data()
        self.tools = ALL_TOOLS
        self.rules = RULES
        self.wiki = WIKI
        
    def get_tools(self) -> List:
        """
        Get all available tools.
        
        Returns:
            List of tool classes
        """
        return self.tools
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all available tools.
        
        Returns:
            List of tool information dictionaries
        """
        return [tool.get_info() for tool in self.tools]
    
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
    
    def invoke_tool(self, tool_name: str, **kwargs) -> str:
        """
        Invoke a tool by name with the given parameters.
        
        Args:
            tool_name: The name of the tool to invoke
            **kwargs: Tool-specific parameters
            
        Returns:
            The result of the tool invocation
        """
        for tool in self.tools:
            tool_info = tool.get_info()
            if tool_info["function"]["name"] == tool_name:
                result = tool.invoke(self.data, **kwargs)
                # Save data after each tool invocation to ensure persistence
                save_data(self.data)
                return result
        
        return f"Error: Tool '{tool_name}' not found"
    
    def get_current_user(self) -> Dict[str, Any]:
        """
        Get the current user.
        
        Returns:
            The current user dictionary
        """
        return get_current_user(self.data)
    
    def set_current_user(self, user_id: str) -> bool:
        """
        Set the current user.
        
        Args:
            user_id: The user ID to set as current
            
        Returns:
            True if successful, False otherwise
        """
        if get_user_by_id(self.data, user_id):
            set_current_user(self.data, user_id)
            save_data(self.data)
            return True
        return False
    
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
