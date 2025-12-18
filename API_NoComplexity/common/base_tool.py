# Copyright Common Base Classes

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """Abstract base class for all tools across different environments"""
    
    @staticmethod
    @abstractmethod
    def invoke(data: Dict[str, Any], **kwargs) -> str:
        """
        Execute the tool's functionality.
        
        Args:
            data: The data dictionary containing all information
            **kwargs: Tool-specific parameters
            
        Returns:
            A JSON string with the result of the operation
        """
        pass
    
    @staticmethod
    @abstractmethod
    def get_info() -> Dict[str, Any]:
        """
        Get information about the tool.
        
        Returns:
            A dictionary containing the tool's metadata including name,
            description, and parameters
        """
        pass
