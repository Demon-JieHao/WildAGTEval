#!/usr/bin/env python3
"""
Extract uncertainty type details and instructions from reference files.
"""

import re
import os
import importlib.util
from pathlib import Path

# Base paths relative to this file:
# .../complexity_integration/complexity_scenario_assessment/scenario_uncertainty_extractor.py
BASE_DIR = Path(__file__).resolve().parent.parent  # .../complexity_integration
UNCERTAINTY_REF_PATH = BASE_DIR / "complexity_matching/uncertainty_types_reference.py"
TEMPLATE_PATH = BASE_DIR / "complexity_scenario_generation/inst_scenario_template.py"

def load_uncertainty_type_dictionaries():
    """
    Load uncertainty type dictionaries from uncertainty_types_reference.py
    
    Returns:
    - Dictionary mapping uncertainty type names to their full dictionary definition
    """
    # Load uncertainty_types_reference.py as a module
    spec = importlib.util.spec_from_file_location(
        "uncertainty_types_reference",
        str(UNCERTAINTY_REF_PATH),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Get all uncertainty type dictionaries
    uncertainty_types = {}
    for name, value in vars(module).items():
        if isinstance(value, dict) and 'name' in value and 'description' in value and 'criteria' in value:
            # Convert name to snake_case for consistent lookup
            snake_name = value['name'].lower().replace(' ', '_').replace('/', '_')
            uncertainty_types[snake_name] = value
    
    return uncertainty_types

# Cache for loaded dictionaries
_UNCERTAINTY_TYPES = None

def fallback_extract_uncertainty_type_details(uncertainty_type):
    """
    Fallback method to extract uncertainty type details using regex patterns when direct dictionary lookup fails
    
    Parameters:
    - uncertainty_type: The uncertainty type name
    
    Returns:
    - Dictionary containing the uncertainty type details extracted via regex
    """
    try:
        with open(UNCERTAINTY_REF_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Different possible formats of uncertainty type names
        possible_names = [
            uncertainty_type,
            uncertainty_type.replace("_", " "),
            uncertainty_type.title(),
            uncertainty_type.replace("_", " ").title()
        ]
        
        description = ""
        criteria = ""
        
        # Look for the uncertainty type
        for name in possible_names:
            # Try to find a definition for this uncertainty type
            match = re.search(rf'{re.escape(name)}.*?\n(.*?)(?=\n\n[A-Z]|\Z)', content, re.DOTALL | re.IGNORECASE)
            if match:
                raw_description = match.group(1).strip()
                # Clean up JSON formatting in the description
                description_match = re.search(r'"description": "([^"]+)"', raw_description)
                if description_match:
                    description = description_match.group(1).strip()
                else:
                    description = raw_description
                break
        
        # Special hardcoded criteria for common uncertainty types
        if uncertainty_type == "unclear_functionality_boundaries":
            criteria = "Naming Similarity vs. Behavior Difference Likelihood: The likelihood that the function has a name similar to other functions while having subtly different behavior"
        elif uncertainty_type == "ad_hoc_rules":
            criteria = """Special Value Semantics Likelihood: The likelihood that the function uses specific numeric or string values that carry special meanings beyond their literal value
            
Non-Standard Format Requirements Likelihood: The likelihood that the function requires data in specific formats that deviate from common industry standards
            
Counter-Intuitive Parameter Behavior Likelihood: The likelihood that parameters behave in ways that contradict what most developers would reasonably expect
            
Hidden Constraints Likelihood: The likelihood that the function has undocumented or obscurely documented restrictions on how it can be used
            
Legacy Compatibility Issues Likelihood: The likelihood that the function contains unusual behaviors primarily to maintain compatibility with older systems"""
        elif uncertainty_type == "ambiguous_documentation":
            criteria = """Parameter Purpose Ambiguity Likelihood: The likelihood that the function documentation does not clearly explain the purpose or expected values for parameters
            
Incomplete Behavior Documentation Likelihood: The likelihood that the function documentation does not completely describe how the function behaves in all situations
            
Inconsistent Terminology Likelihood: The likelihood that the API documentation uses inconsistent or domain-specific terminology without clear definitions
            
Measurement Unit Ambiguity Likelihood: The likelihood that the API documentation does not clearly specify measurement units (e.g., Celsius vs. Fahrenheit, milliseconds vs. seconds)
            
Return Value Interpretation Ambiguity Likelihood: The likelihood that the meaning or structure of return values is not clearly documented"""
        else:
            # Try to find criteria or metrics for this type
            for name in possible_names:
                criteria_match = re.search(rf'metrics.*?{re.escape(name)}.*?\n(.*?)(?=\n\n[A-Z]|\Z)', content, re.DOTALL | re.IGNORECASE)
                if criteria_match:
                    criteria = criteria_match.group(1).strip()
                    # Remove all comments (including multi-line comments with #)
                    criteria = re.sub(r'#.*?($|\n)', '', criteria)
                    
                    # Extract actual criteria entries
                    matches = re.findall(r'"name": "(.*?)",\s*"definition": "(.*?)",\s*"question":', criteria, re.DOTALL)
                    
                    if matches:
                        criteria_items = [f"{name}: {definition}" for name, definition in matches]
                        criteria = "\n".join(criteria_items)
                    else:
                        criteria = "Extracted criteria information not available in the expected format."
                    break
        
        return {
            "name": uncertainty_type,
            "description": description,
            "criteria": criteria
        }
    except Exception as e:
        print(f"Error in fallback extraction for {uncertainty_type}: {e}")
        return {
            "name": uncertainty_type,
            "description": "Description not found",
            "criteria": "Criteria not found"
        }

def extract_uncertainty_type_details(uncertainty_type):
    """
    Extract details about an uncertainty type from uncertainty_types_reference.py.
    
    Parameters:
    - uncertainty_type: The uncertainty type name
    
    Returns:
    - Dictionary containing the uncertainty type details
    """
    global _UNCERTAINTY_TYPES
    try:
        # Load the uncertainty type dictionaries if not already loaded
        if _UNCERTAINTY_TYPES is None:
            _UNCERTAINTY_TYPES = load_uncertainty_type_dictionaries()
        
        # Try to find the uncertainty type in different possible formats
        possible_names = [
            uncertainty_type,
            uncertainty_type.replace("_", " "),
            uncertainty_type.replace("_", "/"),
            uncertainty_type + "_arguments",
            "ambiguous_documentation_arguments" if uncertainty_type == "ambiguous_documentation" else uncertainty_type
        ]
        
        # Try to find the uncertainty type in the loaded dictionaries
        uncertainty_dict = None
        for name in possible_names:
            if name.lower() in _UNCERTAINTY_TYPES:
                uncertainty_dict = _UNCERTAINTY_TYPES[name.lower()]
                break
        
        # If not found, try more variations
        if uncertainty_dict is None:
            for loaded_name, loaded_dict in _UNCERTAINTY_TYPES.items():
                for name in possible_names:
                    if name.lower() in loaded_name or loaded_name in name.lower():
                        uncertainty_dict = loaded_dict
                        break
                if uncertainty_dict:
                    break
        
        # # If still not found, use fallback method
        # if uncertainty_dict is None:
        #     return fallback_extract_uncertainty_type_details(uncertainty_type)
        
        # Extract description and criteria
        description = uncertainty_dict.get("description", "Description not found")
        
        # Format criteria
        criteria_list = []
        for criteria_item in uncertainty_dict.get("criteria", []):
            if isinstance(criteria_item, dict) and "name" in criteria_item and "definition" in criteria_item:
                criteria_list.append(f"{criteria_item['name']}: {criteria_item['definition']}")
        
        # # If no criteria found, use fallback
        # if not criteria_list:
        #     return fallback_extract_uncertainty_type_details(uncertainty_type)
            
        criteria = "\n".join(criteria_list)
        
        return {
            "name": uncertainty_type,
            "description": description,
            "criteria": criteria
        }
    except Exception as e:
        print(f"Error extracting uncertainty type details for {uncertainty_type}: {e}")
        return {
            "name": uncertainty_type,
            "description": "Description not found",
            "criteria": "Criteria not found"
        }


def load_uncertainty_type_instructions_from_template():
    """
    Load uncertainty type-specific instructions from inst_scenario_template.py file directly.
    
    Returns:
    - Dictionary mapping uncertainty types to their specific instructions
    """
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        instructions_dict = {}
        
        # Direct manual extraction for common uncertainty types
        # 1. Ambiguous Documentation
        ambiguous_match = re.search(r'Special Instructions for Ambiguous Documentation Scenarios(.*?)(?=## Output Format for|## Special Instructions for|\Z)', 
                         content, re.DOTALL)
        if ambiguous_match:
            instructions_dict["ambiguous_documentation"] = ambiguous_match.group(1).strip()
            instructions_dict["ambiguous_documentation_arguments"] = ambiguous_match.group(1).strip()
        
        # 2. Ad Hoc Rules
        adhoc_match = re.search(r'Special Instructions for Ad Hoc Rules Scenarios(.*?)(?=## Output Format for|## Special Instructions for|\Z)', 
                      content, re.DOTALL)
        if adhoc_match:
            instructions_dict["ad_hoc_rules"] = adhoc_match.group(1).strip()
        
        # 3. Unclear Functionality Boundaries
        unclear_match = re.search(r'Special Instructions for Unclear Functionality Boundaries Scenarios(.*?)(?=## Output Format for|## Special Instructions for|\Z)', 
                       content, re.DOTALL)
        if unclear_match:
            instructions_dict["unclear_functionality_boundaries"] = unclear_match.group(1).strip()
        
        # Define other uncertainty types to look for
        other_types = [
            # "Complex Dependency Chains",
            "Informational Notice", 
            "Feature Limitation Error",
            "System Failure Error",
            "Partially Irrelevant Information",
            # "Completely Irrelevant Information"
        ]
        
        # Extract instructions for other uncertainty types
        for ut_name in other_types:
            # Find the special instructions section for this uncertainty type
            match = re.search(rf'Special Instructions for {re.escape(ut_name)} Scenarios(.*?)(?=## Output Format for|## Special Instructions for|\Z)', 
                             content, re.DOTALL)
            
            if match:
                # Convert to snake_case for consistent lookup
                dict_key = ut_name.lower().replace(" ", "_").replace("/", "_")
                instructions_dict[dict_key] = match.group(1).strip()
                
        # Clean up all entries - remove template artifacts
        for key in instructions_dict:
            instructions_dict[key] = re.sub(r'template \+= """', '', instructions_dict[key])
            instructions_dict[key] = re.sub(r'"""', '', instructions_dict[key])
            instructions_dict[key] = instructions_dict[key].strip()
        
        return instructions_dict
    except Exception as e:
        print(f"Error loading uncertainty type instructions: {e}")
        return {}

# Cache for loaded instructions
_UNCERTAINTY_TYPE_INSTRUCTIONS = None

def extract_uncertainty_type_instructions(uncertainty_type):
    """
    Extract specific instructions for an uncertainty type from inst_scenario_template.py.
    
    Parameters:
    - uncertainty_type: The uncertainty type name
    
    Returns:
    - String containing the instructions for this uncertainty type
    """
    global _UNCERTAINTY_TYPE_INSTRUCTIONS
    try:
        # Load instructions dictionary if not already loaded
        if _UNCERTAINTY_TYPE_INSTRUCTIONS is None:
            _UNCERTAINTY_TYPE_INSTRUCTIONS = load_uncertainty_type_instructions_from_template()
        
        # Try different variations of the uncertainty type name
        possible_names = [
            uncertainty_type,
            uncertainty_type.replace("_", " "),
            uncertainty_type.replace("_", "/"),
            "ambiguous_documentation_arguments" if uncertainty_type == "ambiguous_documentation" else uncertainty_type,
            uncertainty_type + "_arguments",
            "ad_hoc_rules" if uncertainty_type == "ad_hoc_rules" else uncertainty_type,
            "unclear_functionality_boundaries" if uncertainty_type == "unclear_functionality_boundaries" else uncertainty_type
        ]
        
        # Look for the uncertainty type in the loaded dictionary
        for name in possible_names:
            if name.lower() in _UNCERTAINTY_TYPE_INSTRUCTIONS:
                return _UNCERTAINTY_TYPE_INSTRUCTIONS[name.lower()]
        
        # If not found, use fallback method
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for general instructions section
        match = re.search(r'## Instructions\s*(.*?)(?=## Special Instructions for|$)', content, re.DOTALL)
        if match:
            return "General Instructions (no specific instructions found for this uncertainty type):\n\n" + match.group(1).strip()
        
        return "No instructions found for this uncertainty type."
    except Exception as e:
        print(f"Error extracting uncertainty type instructions for {uncertainty_type}: {e}")
        return "Instructions could not be extracted due to an error."

def extract_output_format_instructions(uncertainty_type):
    """
    Extract output format instructions for an uncertainty type from inst_scenario_template.py.
    
    Parameters:
    - uncertainty_type: The uncertainty type name
    
    Returns:
    - String containing the output format instructions for this uncertainty type
    """
    # Read the inst_scenario_template.py file
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Different possible formats of uncertainty type names
        possible_names = [
            uncertainty_type,
            uncertainty_type.replace("_", " "),
            "Ambiguous Documentation" if uncertainty_type == "ambiguous_documentation" else uncertainty_type,
            "Ad Hoc Rules" if uncertainty_type == "ad_hoc_rules" else uncertainty_type,
            "Unclear Functionality Boundaries" if uncertainty_type == "unclear_functionality_boundaries" else uncertainty_type
        ]
        
        output_format = ""
        
        # Look for output format for this uncertainty type
        for name in possible_names:
            match = re.search(rf'## Output Format for {re.escape(name)} Scenarios(.*?)(?=## Special Instructions for|## Output Format for|$)', 
                            content, re.DOTALL | re.IGNORECASE)
            
            if match:
                output_format = match.group(1).strip()
                break
        
        # If no specific output format found, use the general output format
        if not output_format:
            match = re.search(r'## Output Format\s*(.*?)(?=## Special Instructions for|$)', content, re.DOTALL)
            if match:
                output_format = "General Output Format (no specific format found for this uncertainty type):\n\n" + match.group(1).strip()
        
        return output_format
    except Exception as e:
        print(f"Error extracting output format instructions for {uncertainty_type}: {e}")
        return "Output format could not be extracted due to an error."

if __name__ == "__main__":
    # Simple test
    import sys
    if len(sys.argv) == 2:
        uncertainty_type = sys.argv[1]
        details = extract_uncertainty_type_details(uncertainty_type)
        instructions = extract_uncertainty_type_instructions(uncertainty_type)
        format_instructions = extract_output_format_instructions(uncertainty_type)
        
        print(f"Uncertainty Type: {details['name']}")
        print(f"Description: {details['description'][:200]}...")
        print(f"Instructions: {instructions[:200]}...")
        print(f"Output Format: {format_instructions[:200]}...")
