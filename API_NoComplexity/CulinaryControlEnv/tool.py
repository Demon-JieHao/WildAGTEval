# Copyright CulinaryControlEnv

"""
Base Tool class for CulinaryControlEnv.
This provides the foundation for all culinary-related tools.
"""

from typing import Any, Dict, Optional
from abc import ABC, abstractmethod


class Tool(ABC):
    """
    Abstract base class for all CulinaryControlEnv tools.
    
    Each tool must implement:
    1. invoke: Static method to execute the tool's functionality
    2. get_info: Static method to provide tool metadata
    """
    
    @staticmethod
    @abstractmethod
    def invoke(data: Dict[str, Any], **kwargs) -> str:
        """
        Execute the tool's functionality.
        
        Args:
            data: The shared data dictionary
            **kwargs: Tool-specific parameters
            
        Returns:
            A JSON string with the result of the operation
        """
        raise NotImplementedError("Tool must implement invoke method")
    
    @staticmethod
    @abstractmethod
    def get_info() -> Dict[str, Any]:
        """
        Get metadata about the tool for documentation and interface generation.
        
        Returns:
            A dictionary containing tool metadata in the OpenAI function format
        """
        raise NotImplementedError("Tool must implement get_info method")
