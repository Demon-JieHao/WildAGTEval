#!/usr/bin/env python3
"""
Extract API function details from the function implementation files or scenario descriptions.
"""

import os
import json
import re
from pathlib import Path

# Base paths for INST templates used as fallback when tool files are missing
BASE_DIR = Path(__file__).resolve().parent  # .../complexity_scenario_assessment
SCENARIO_GEN_DIR = BASE_DIR.parent / "complexity_scenario_generation"
INST_SCENARIOS_DIR = SCENARIO_GEN_DIR / "inst_scenarios"

def extract_api_function_details(domain, function_name):
    """
    Extract API function details from the appropriate source files.
    
    Parameters:
    - domain: The domain name (e.g., "SmartHomeEnv")
    - function_name: The function name (e.g., "volume_adjust")
    
    Returns:
    - Dictionary containing the API function details
    """
    # First, try to find the function implementation file
    function_file = Path(f"{domain}/tools/{function_name}.py")
    
    if not function_file.exists():
        # Look in INST scenario templates directory for a matching file
        for scenario_file in INST_SCENARIOS_DIR.glob(f"{domain}_{function_name}__*.md"):
            # Extract function details from scenario file
            return extract_from_scenario_file(scenario_file)
    
    # Extract from function file
    description = ""
    implementation = ""
    signature = ""
    
    try:
        with open(function_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract docstring (description)
            doc_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
            if doc_match:
                description = doc_match.group(1).strip()
            
            # Extract function signature
            sig_match = re.search(r'def\s+invoke\s*\((.*?)\):', content, re.DOTALL)
            if sig_match:
                signature = f"def invoke({sig_match.group(1)})"
            
            # Extract implementation
            implementation = content
        
        return {
            "domain": domain,
            "name": function_name,
            "description": description,
            "implementation": implementation,
            "signature": signature
        }
    except Exception as e:
        print(f"Error extracting API function details for {domain}.{function_name}: {e}")
        return None

def extract_from_scenario_file(scenario_file):
    """
    Extract function details from an inst_scenarios file.
    
    Parameters:
    - scenario_file: Path to the scenario file
    
    Returns:
    - Dictionary containing the API function details
    """
    try:
        with open(scenario_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Extract API Function Information
            description = ""
            implementation = ""
            
            desc_match = re.search(r'### Description\s*(.*?)```', content, re.DOTALL)
            if desc_match:
                description = desc_match.group(1).strip()
            
            impl_match = re.search(r'### Implementation\s*```python\s*(.*?)```', content, re.DOTALL)
            if impl_match:
                implementation = impl_match.group(1).strip()
            
            # Extract domain and function name from filename
            parts = scenario_file.stem.split("__")[0].split("_")
            domain = parts[0]
            function_name = "_".join(parts[1:])
            
            # Extract signature
            signature = extract_signature(implementation)
            
            return {
                "domain": domain,
                "name": function_name,
                "description": description,
                "implementation": implementation,
                "signature": signature
            }
    except Exception as e:
        print(f"Error extracting from scenario file {scenario_file}: {e}")
        return None

def extract_signature(code):
    """
    Extract the function signature from code.
    
    Parameters:
    - code: The function implementation code
    
    Returns:
    - The function signature as a string
    """
    match = re.search(r'def\s+\w+\s*\((.*?)\):', code, re.DOTALL)
    if match:
        return f"def invoke({match.group(1)})"
    return ""

if __name__ == "__main__":
    # Simple test
    import sys
    if len(sys.argv) == 3:
        domain = sys.argv[1]
        function = sys.argv[2]
        details = extract_api_function_details(domain, function)
        if details:
            print(f"Domain: {details['domain']}")
            print(f"Function: {details['name']}")
            print(f"Signature: {details['signature']}")
            print(f"Description: {details['description'][:200]}...")
        else:
            print(f"Could not extract details for {domain}.{function}")
