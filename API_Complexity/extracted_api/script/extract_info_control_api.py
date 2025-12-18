#!/usr/bin/env python3
# Script to extract tool information from InformationControlEnv tools

import json
import sys
import os

# Add parent directory to path so we can import modules correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from InformationControlEnv.tools import get_all_tools

def main():
    # Get all tool classes
    tool_classes = get_all_tools()
    
    # Dictionary to store all tool info
    api_info = {}
    
    # Extract info from each tool
    for tool_name, tool_class in tool_classes.items():
        tool_info = tool_class.get_info()
        api_info[tool_name] = tool_info
    
    # Wrap all functions under the InformationControlEnv key
    final_output = {"InformationControlEnv": api_info}
    
    # Get absolute path for api_file directory
    api_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api_file"))
    
    # Write to JSON file
    with open(os.path.join(api_file_dir, "InformationControlAPI.json"), "w") as f:
        json.dump(final_output, f, indent=2, sort_keys=True)
    
    print(f"Successfully extracted API info for {len(api_info)} tools to {os.path.join(api_file_dir, 'InformationControlAPI.json')}")

if __name__ == "__main__":
    main()
