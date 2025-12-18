"""
Generate Uncertainty Assessments for All API Functions

This script extracts API function descriptions from all 7 environments and generates 
uncertainty assessment instructions for each API function against each uncertainty type.
"""

import os
import json
import re
import glob
# Import assessment system
from .api_uncertainty_assessment_system import perform_assessment
from .uncertainty_types_reference import UNCERTAINTY_TYPES

def extract_api_description(file_path):
    """
    Extract API function description from a Python file by looking for get_info() method.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Function name is the file name without extension
        function_name = os.path.basename(file_path).replace('.py', '')
        
        # Extract information from get_info method
        description = ""
        parameters = []
        return_value = "A response based on the function's purpose"
        
        # Extract description
        desc_match = re.search(r'"description"\s*:\s*"([^"]+)"', content)
        if desc_match:
            description = desc_match.group(1)
            
        # Extract return value from invoke method docstring
        invoke_returns_match = re.search(r'@staticmethod\s+def\s+invoke.*?Returns:\s+(.*?)(?:\s+"""|\s+$|\s+Raises:)', content, re.DOTALL)
        if invoke_returns_match:
            return_value = invoke_returns_match.group(1).strip()
        
        # Extract parameters
        if '"parameters"' in content:
            # Find the parameters section
            param_section_match = re.search(r'"parameters"\s*:\s*\{([^}]+)\}', content, re.DOTALL)
            if param_section_match:
                param_section = param_section_match.group(1)
                
                # Extract individual parameter names
                param_names = re.findall(r'"(\w+)"\s*:', param_section)
                
                # Remove common property names that aren't parameters
                param_names = [p for p in param_names if p not in ['type', 'properties', 'items', 'description', 'additionalProperties', 'required']]
                
                # Extract required parameters list
                required_params = []
                required_match = re.search(r'"required"\s*:\s*\[\s*([^\]]+)\s*\]', content)
                if required_match:
                    required_str = required_match.group(1)
                    required_params = re.findall(r'"([^"]+)"', required_str)
                
                # For each parameter, try to find its description and type
                for param in param_names:
                    param_desc = ""
                    param_type = ""
                    
                    # Extract description
                    param_desc_match = re.search(f'"{param}"[^{{]*\\{{[^{{]*"description"\\s*:\\s*"([^"]+)"', content)
                    if param_desc_match:
                        param_desc = param_desc_match.group(1)
                    
                    # Extract type
                    param_type_match = re.search(f'"{param}"[^{{]*\\{{[^{{]*"type"\\s*:\\s*"([^"]+)"', content)
                    if param_type_match:
                        param_type = param_type_match.group(1)
                    
                    parameters.append({
                        "name": param,
                        "description": param_desc,
                        "type": param_type,
                        "required": param in required_params
                    })
        
        # Format the API description
        api_description = f"Function: {function_name}\nDescription: {description}\n\nParameters:\n"
        for param in parameters:
            param_type_str = f" ({param['type']})" if param['type'] else ""
            required_str = " (required)" if param.get('required', False) else " (optional)"
            param_desc = f" - {param['description']}" if param['description'] else ""
            api_description += f"- {param['name']}{param_type_str}{required_str}{param_desc}\n"
        
        api_description += f"\nReturns: {return_value}"
        
        return {
            "file_path": file_path,
            "function_name": function_name,
            "description": description,
            "parameters": parameters,
            "formatted_description": api_description
        }
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def main():
    # Define the 7 environments
    environments = [
        "SmartHomeEnv",
        "InformationControlEnv",
        "MediaControlEnv",
        "TransactionEnv",
        "CulinaryControlEnv",
        "CommunicationController",
        "TimeNotificationEnv"
    ]
    
    # Find all Python files in the tools directories of each environment
    all_tool_files = []
    for env in environments:
        tool_dir = os.path.join(env, "tools")
        if os.path.exists(tool_dir):
            python_files = glob.glob(os.path.join(tool_dir, "*.py"))
            # Exclude __init__.py files
            python_files = [f for f in python_files if not os.path.basename(f).startswith("__")]
            all_tool_files.extend(python_files)
    
    print(f"Found {len(all_tool_files)} API function files across {len(environments)} environments")
    
    # Extract API descriptions from all tool files
    api_descriptions = []
    total_files = len(all_tool_files)
    print(f"Extracting API descriptions from {total_files} files...")
    for i, file_path in enumerate(all_tool_files):
        if (i + 1) % 10 == 0 or (i + 1) == total_files:
            print(f"Progress: {i + 1}/{total_files} files processed")
        api_info = extract_api_description(file_path)
        if api_info:
            api_descriptions.append(api_info)
    
    print(f"Successfully extracted {len(api_descriptions)} API function descriptions")
    
    # Display a few examples
    for i, api_info in enumerate(api_descriptions[:3]):
        print(f"\nExample #{i+1}: {api_info['function_name']}")
        print("-" * 50)
        print(api_info['formatted_description'])
    
    # Use the API uncertainty types from the reference file
    uncertainty_types = list(UNCERTAINTY_TYPES.keys())
    
    print(f"Found {len(uncertainty_types)} uncertainty types:")
    for utype in uncertainty_types:
        print(f"- {utype}")
    
    # Create output directory for assessment instructions
    output_dir = "api_assessments"
    os.makedirs(output_dir, exist_ok=True)
    
    # Track statistics
    assessment_count = 0
    failed_assessments = 0
    
    # Show progress during assessment generation
    total_combinations = len(api_descriptions) * len(uncertainty_types)
    print(f"Generating {total_combinations} assessments...")
    progress_step = max(1, total_combinations // 20)  # Show progress roughly every 5%
    
    # For each API function description
    count = 0
    for api_info in api_descriptions:
        function_name = api_info['function_name']
        api_description = api_info['formatted_description']
        environment = api_info['file_path'].split(os.path.sep)[0]
        
        # Create a subdirectory for this function
        function_dir = os.path.join(output_dir, environment, function_name)
        os.makedirs(function_dir, exist_ok=True)
        
        # For each uncertainty type
        for uncertainty_type_key in uncertainty_types:
            try:
                # Generate assessment instruction
                assessment = perform_assessment(api_description, uncertainty_type_key)
                
                # Write to file
                output_file = os.path.join(function_dir, f"{uncertainty_type_key}.txt")
                with open(output_file, 'w') as f:
                    f.write(assessment)
                
                assessment_count += 1
            except Exception as e:
                print(f"Error generating assessment for {function_name} x {uncertainty_type_key}: {str(e)}")
                failed_assessments += 1
            
            count += 1
            if count % progress_step == 0 or count == total_combinations:
                print(f"Progress: {count}/{total_combinations} assessments generated")
    
    print(f"Generated {assessment_count} assessment instructions")
    if failed_assessments > 0:
        print(f"Failed to generate {failed_assessments} assessments")
    
    # Create an index file that lists all the generated assessments
    index_file = os.path.join(output_dir, "index.md")
    
    with open(index_file, 'w') as f:
        f.write("# API Uncertainty Assessments Index\n\n")
        
        # Group by environment
        for environment in sorted(environments):
            env_functions = [api for api in api_descriptions if api['file_path'].split(os.path.sep)[0] == environment]
            
            if env_functions:
                f.write(f"## {environment}\n\n")
                
                # List functions with links to their uncertainty assessments
                for api_info in sorted(env_functions, key=lambda x: x['function_name']):
                    function_name = api_info['function_name']
                    description = api_info['description']
                    
                    f.write(f"### {function_name}\n\n")
                    f.write(f"Description: {description}\n\n")
                    f.write("Uncertainty assessments:\n\n")
                    
                    for uncertainty_type_key in uncertainty_types:
                        uncertainty_name = UNCERTAINTY_TYPES[uncertainty_type_key]["name"]
                        rel_path = f"{environment}/{function_name}/{uncertainty_type_key}.txt"
                        
                        f.write(f"- [{uncertainty_name}]({rel_path})\n")
                    
                    f.write("\n")
    
    print(f"Created index file at {index_file}")
    
    # Count the number of API functions per environment
    env_counts = {}
    for api_info in api_descriptions:
        environment = api_info['file_path'].split(os.path.sep)[0]
        env_counts[environment] = env_counts.get(environment, 0) + 1
    
    print("API Functions per Environment:")
    for env, count in env_counts.items():
        print(f"- {env}: {count} functions")
    
    print(f"\nTotal API Functions: {len(api_descriptions)}")
    print(f"Total Uncertainty Types: {len(uncertainty_types)}")
    print(f"Total Assessment Instructions Generated: {assessment_count}")

if __name__ == "__main__":
    main()
