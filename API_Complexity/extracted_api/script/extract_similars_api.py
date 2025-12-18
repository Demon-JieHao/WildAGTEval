#!/usr/bin/env python3
# Script to extract tool information from TransactionEnv tools

import json
import sys
import os

# Add parent directory to path so we can import modules correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from SimilarAPIs.tools import ALL_TOOLS

def main():
    # Convert ALL_TOOLS list to dictionary format
    tool_classes = {}
    for tool_class in ALL_TOOLS:
        tool_info = tool_class.get_info()
        tool_name = tool_info['function']['name']
        tool_classes[tool_name] = tool_class
    
    # Dictionary to store all tool info
    api_info = {}
    
    # Extract info from each tool
    for tool_name, tool_class in tool_classes.items():
        tool_info = tool_class.get_info()
        api_info[tool_name] = tool_info
    
    # Wrap all functions under the RealEnv key
    final_output = {"RealEnv": api_info}
    
    # Get absolute path for api_file directory
    api_file_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api_file"))
    
    # Write to JSON file
    with open(os.path.join(api_file_dir, "RealEnvAPI.json"), "w") as f:
        json.dump(final_output, f, indent=2, sort_keys=True)
    
    print(f"Successfully extracted API info for {len(api_info)} tools to {os.path.join(api_file_dir, 'RealEnvAPI.json')}")

if __name__ == "__main__":
    main()
