# Copyright Common Base Classes

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json
from common.shared_memory_service import SharedMemoryService


class BaseEnvironment(ABC):
    """Abstract base class for all environments"""
    
    def __init__(self):
        # Get shared memory service instance
        self.memory_service = SharedMemoryService.get_instance()
        
        # Register as observer for data updates
        self.memory_service.register_observer(self)
        
        # Get reference to shared data
        self.data = self.memory_service.get_data()
        
        # Initialize environment-specific data
        self._initialize_environment_data()
        
        # Load tools
        self.tools = self._load_tools()
    
    def _initialize_environment_data(self) -> None:
        """
        Initialize environment-specific data.
        This is called after getting the shared data but before loading tools.
        Environments can override this to set up their specific data structures.
        """
        pass
        
    def on_data_updated(self, updated_keys=None) -> None:
        """
        Called when shared data is updated by another environment.
        Environments can override this to react to specific data changes.
        
        Args:
            updated_keys: List of keys that were updated, or None if unknown
        """
        pass
        
    def on_data_reset(self, new_data: Dict[str, Any]) -> None:
        """
        Called when shared memory service resets the data.
        This makes sure the environment's data reference is updated.
        
        Args:
            new_data: The new data dictionary from the shared memory service
        """
        # Update our reference to the new data object
        self.data = new_data
    
    @abstractmethod
    def _load_tools(self) -> Dict[str, Any]:
        """Load environment-specific tools"""
        pass
    
    @abstractmethod
    def _save_data(self) -> None:
        """Save environment-specific data"""
        pass
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get information about all available tools"""
        tool_info = []
        for tool_name, tool_class in self.tools.items():
            info = tool_class.get_info()
            tool_info.append(info)
        return tool_info
    
    def invoke_tool(self, tool_name: str, **kwargs) -> str:
        """
        Invoke a specific tool.
        
        Args:
            tool_name: The name of the tool to invoke
            **kwargs: Tool-specific parameters
            
        Returns:
            A JSON string with the result of the operation
        """
        if tool_name not in self.tools:
            return json.dumps({
                "success": False,
                "message": f"Tool '{tool_name}' not found"
            })
        
        tool_class = self.tools[tool_name]
        try:
            # Use shared data reference
            result = tool_class.invoke(self.data, **kwargs)
            
            # Notify shared memory service about updates (but don't save to disk)
            self.memory_service.update_data(self.data)
            
            return result
        except Exception as e:
            return json.dumps({
                "success": False,
                "message": f"Error invoking tool '{tool_name}': {str(e)}"
            })
    
    def set_current_user(self, user_id: str) -> bool:
        """
        Set the current user.
        
        Args:
            user_id: The ID of the user to set as current
            
        Returns:
            True if successful, False otherwise
        """
        # Use the shared memory service to set user across all environments
        return self.memory_service.set_current_user(user_id)
    
    def get_current_user(self) -> Optional[str]:
        """Get the current user ID"""
        return self.data.get("current_user")
