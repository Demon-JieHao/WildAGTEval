# Copyright InformationControlEnv

import os
import importlib
import inspect
from typing import Dict, Any

def get_all_tools() -> Dict[str, Any]:
    """
    Dynamically import all tool classes from the tools directory.
    
    Returns:
        A dictionary mapping tool names to tool classes
    """
    tools = {}
    tools_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all Python files in the tools directory
    for filename in os.listdir(tools_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Remove .py extension
            
            # Import the module
            module = importlib.import_module(f'InformationControlEnv.tools.{module_name}')
            
            # Find the tool class in the module
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, 'invoke') and hasattr(obj, 'get_info'):
                    # Use the function name from get_info as the key
                    try:
                        info = obj.get_info()
                        if info and 'function' in info and 'name' in info['function']:
                            tool_name = info['function']['name']
                            tools[tool_name] = obj
                            break
                    except Exception as e:
                        print(f"Error loading tool from {module_name}: {e}")
                        continue
    
    return tools
