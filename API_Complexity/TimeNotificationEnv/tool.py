# Copyright TimeNotificationEnv

from common.base_tool import BaseTool
from typing import Dict, Any


class Tool(BaseTool):
    """Base class for all TimeNotificationEnv tools"""
    
    @staticmethod
    def invoke(data: Dict[str, Any], **kwargs) -> str:
        """
        Each tool must implement this method to handle its specific functionality.
        This is just a placeholder for the abstract method defined in BaseTool.
        
        Args:
            data: The shared data dictionary
            **kwargs: Tool-specific parameters
        
        Returns:
            A JSON string with the result of the operation
        """
        pass
    
    @staticmethod
    def get_info() -> Dict[str, Any]:
        """
        Each tool must implement this method to provide information about itself.
        This is just a placeholder for the abstract method defined in BaseTool.
        
        Returns:
            A dictionary containing the tool's metadata
        """
        pass
