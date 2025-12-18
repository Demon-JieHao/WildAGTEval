#!/usr/bin/env python3
# Script to extract tool information from SmartHomeEnv tools

import json
import sys
import os

# Add parent directory to path so we can import modules correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from SmartHomeEnv.tools import ALL_TOOLS

def main():
    # Dictionary to store all tool info
    api_info = {}
    
    # Extract info from each tool
    for tool_class in ALL_TOOLS:
        tool_info = tool_class.get_info()
        function_name = tool_info["function"]["name"]
        api_info[function_name] = tool_info
    
    # Wrap all functions under the SmartHomeEnv key
    final_output = {"SmartHomeEnv": api_info}
    
    # Get absolute path for api_file directory
    api_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api_file"))
    
    # Write to JSON file
    with open(os.path.join(api_file_dir, "SmartHomeAPI.json"), "w") as f:
        json.dump(final_output, f, indent=2, sort_keys=True)
    
    print(f"Successfully extracted API info for {len(api_info)} tools to {os.path.join(api_file_dir, 'SmartHomeAPI.json')}")

if __name__ == "__main__":
    main()
