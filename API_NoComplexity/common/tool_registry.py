# Copyright Common Tool Registry

"""
Unified tool registry that automatically matches tools to their environments
"""

from typing import Dict, Any, Optional, Tuple
import json


class ToolRegistry:
    """Registry for all tools across all environments"""
    
    def __init__(self):
        self.environments = {}
        self.tool_to_env = {}
    
    def register_environment(self, env_name: str, env_instance: Any) -> None:
        """Register an environment and its tools"""
        self.environments[env_name] = env_instance
        
        # Register all tools from this environment
        for tool_name, tool_class in env_instance.tools.items():
            if tool_name in self.tool_to_env:
                print(f"Warning: Tool '{tool_name}' already registered to {self.tool_to_env[tool_name]}")
            self.tool_to_env[tool_name] = env_name
    
    def get_environment_for_tool(self, tool_name: str) -> Optional[str]:
        """Get the environment name for a given tool"""
        return self.tool_to_env.get(tool_name)
    
    def invoke_tool(self, tool_name: str, **kwargs) -> str:
        """
        Invoke a tool by name, automatically finding the correct environment
        
        Args:
            tool_name: The name of the tool to invoke
            **kwargs: Tool-specific parameters
            
        Returns:
            JSON string with the result
        """
        env_name = self.tool_to_env.get(tool_name)
        if not env_name:
            return json.dumps({
                "success": False,
                "message": f"Tool '{tool_name}' not found in any environment",
                "available_tools": list(self.tool_to_env.keys())
            })
        
        env = self.environments.get(env_name)
        if not env:
            return json.dumps({
                "success": False,
                "message": f"Environment '{env_name}' not found"
            })
        
        # Invoke the tool through its environment
        result = env.invoke_tool(tool_name, **kwargs)
        
        # Add environment info to the result if it's successful
        try:
            result_dict = json.loads(result)
            if result_dict.get("success", False):
                result_dict["_environment"] = env_name
                result = json.dumps(result_dict)
        except:
            pass
        
        return result
    
    def get_all_tools(self) -> Dict[str, str]:
        """Get all tools and their environments"""
        return self.tool_to_env.copy()
    
    def get_tools_by_environment(self, env_name: str) -> list:
        """Get all tools for a specific environment"""
        return [tool for tool, env in self.tool_to_env.items() if env == env_name]
    
    def get_tool_info(self, tool_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific tool"""
        env_name = self.tool_to_env.get(tool_name)
        if not env_name:
            return None
        
        env = self.environments.get(env_name)
        if not env or tool_name not in env.tools:
            return None
        
        tool_info = env.tools[tool_name].get_info()
        tool_info["_environment"] = env_name
        return tool_info
    
    def list_all_tools(self) -> Dict[str, list]:
        """List all tools grouped by environment"""
        result = {}
        for tool_name, env_name in self.tool_to_env.items():
            if env_name not in result:
                result[env_name] = []
            result[env_name].append(tool_name)
        return result


# Global registry instance
global_registry = ToolRegistry()


def register_environment(env_name: str, env_instance: Any) -> None:
    """Register an environment with the global registry"""
    global_registry.register_environment(env_name, env_instance)


def invoke_tool(tool_name: str, **kwargs) -> str:
    """Invoke a tool through the global registry"""
    return global_registry.invoke_tool(tool_name, **kwargs)


def get_tool_info(tool_name: str) -> Optional[Dict[str, Any]]:
    """Get information about a tool"""
    return global_registry.get_tool_info(tool_name)


def list_all_tools() -> Dict[str, list]:
    """List all available tools grouped by environment"""
    return global_registry.list_all_tools()
