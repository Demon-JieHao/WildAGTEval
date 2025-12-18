# Copyright Common Transform Handler

"""
Handler that parses `invoke_tool` strings and finds/applies the appropriate transform function.
"""

import re
import importlib
from typing import Tuple, Optional, Callable, Any, Dict


def load_transform_function(function_name: str) -> Tuple[Optional[Callable], Optional[str]]:
    """Find and return the registered transform function by tool name.
    
    Args:
        function_name: Tool name (e.g., "make_call")
        
    Returns:
        A tuple of (transform_function, key_param), or (None, None) if not found.
    """
    from common.transform_registry import transform_registry
    
    if function_name not in transform_registry:
        return None, None
        
    tool_info = transform_registry[function_name]
    
    try:
        module = importlib.import_module(tool_info["module"])
        class_obj = getattr(module, tool_info["class"])
        transform_function = getattr(class_obj, "transform")
        return transform_function, tool_info["key_param"]
    except (ImportError, AttributeError) as e:
        print(f"Error loading transform function for {function_name}: {e}")
        return None, None


def transform_invoke_tool(invoke_tool_str: str, data: Dict[str, Any] = None) -> str:
    """Parse an `invoke_tool` string and apply the corresponding tool's transform function.
    
    Args:
        invoke_tool_str: String containing an `invoke_tool` call
        data: Optional data required by the tool
        
    Returns:
        The transformed `invoke_tool` string.
    """
    # If there is no `invoke_tool` call, return the string as-is
    if "invoke_tool" not in invoke_tool_str:
        return invoke_tool_str
    
    # Extract the function name
    func_match = re.search(r'invoke_tool\([\'\"]([^\'\"]+)[\'\"]', invoke_tool_str)
    if not func_match:
        return invoke_tool_str
    
    function_name = func_match.group(1)
    
    # Get the transform function and key parameter
    transform_func, key_param = load_transform_function(function_name)
    
    if transform_func is None or key_param is None:
        # If the transform function cannot be found or key_param is missing, return original string
        return invoke_tool_str
    
    # Originally, each transform function handled this logic internally,
    # but instead of applying it manually here, we simply call the transform function directly.
    return transform_func(invoke_tool_str, data)


def transform_batch(input_lines: list, data: Dict[str, Any] = None) -> list:
    """Find and apply transforms for `invoke_tool` calls across multiple text lines.
    
    Args:
        input_lines: List of text lines to transform
        data: Optional data required by the tool
        
    Returns:
        List of transformed text lines.
    """
    result = []
    for line in input_lines:
        result.append(transform_invoke_tool(line, data))
    return result
