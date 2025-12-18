"""
API Uncertainty Assessment System

This script demonstrates how to use all components together to assess
the likelihood of different uncertainty types in API functions.
"""

import json
from .api_uncertainty_assessment_template import assess_api_uncertainty
from .uncertainty_types_reference import (
    get_uncertainty_type,
    get_all_uncertainty_types,
    format_criteria_for_assessment
)

def perform_assessment(api_function_description, uncertainty_type_key):
    """
    Perform an uncertainty assessment for a given API function and uncertainty type.
    
    Args:
        api_function_description: String describing the API function
        uncertainty_type_key: Key of the uncertainty type to assess
        
    Returns:
        Assessment instruction string
    """
    uncertainty_type = get_uncertainty_type(uncertainty_type_key)
    if not uncertainty_type:
        return f"Unknown uncertainty type: {uncertainty_type_key}"
    
    formatted_criteria = format_criteria_for_assessment(uncertainty_type)
    return assess_api_uncertainty(api_function_description, formatted_criteria)

def assess_multiple_uncertainty_types(api_function_description, uncertainty_type_keys=None):
    """
    Assess an API function against multiple uncertainty types.
    
    Args:
        api_function_description: String describing the API function
        uncertainty_type_keys: List of uncertainty type keys to assess (if None, assesses all types)
        
    Returns:
        Dictionary mapping uncertainty type names to assessment instructions
    """
    if uncertainty_type_keys is None:
        uncertainty_type_keys = get_all_uncertainty_types()
    
    assessments = {}
    for key in uncertainty_type_keys:
        assessments[key] = perform_assessment(api_function_description, key)
    
    return assessments

def save_assessments_to_file(assessments, output_file):
    """
    Save assessment instructions to a file.
    
    Args:
        assessments: Dictionary mapping uncertainty type names to assessment instructions
        output_file: Path to the output file
    """
    with open(output_file, "w") as f:
        for uncertainty_type, assessment in assessments.items():
            f.write(f"{'=' * 80}\n")
            f.write(f"UNCERTAINTY TYPE: {uncertainty_type}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(assessment)
            f.write("\n\n\n")

# Example usage
if __name__ == "__main__":
    # Example API function from SmartHomeEnv
    temperature_set_api = """
    Function: temperature_set
    Description: Set target temperature on one or more thermostats.
    
    Parameters:
    - endpoints: List of device endpoint IDs to set temperature on. Each endpoint must correspond to a thermostat device.
    - temperature: Target temperature to set. The value interpretation depends on the thermostat's configuration.
    
    Returns: A JSON string with the result of the operation, including success status for each device and any error messages.
    
    Additional context:
    - The function works with smart home thermostats to control temperature settings
    - Thermostats may be in different modes (heating, cooling, auto, etc.)
    - Different regions may use different temperature scales (Celsius/Fahrenheit)
    """
    
    # Example 1: Assess against one uncertainty type
    print("Assessing temperature_set against Ad Hoc Rules uncertainty type...")
    assessment = perform_assessment(temperature_set_api, "ad_hoc_rules")
    print(f"Generated assessment instruction with {len(assessment)} characters.")
    
    # Example 2: Assess against multiple uncertainty types
    print("\nAssessing temperature_set against multiple uncertainty types...")
    selected_types = ["ambiguous_documentation", "ad_hoc_rules", "complex_dependency_chains"]
    assessments = assess_multiple_uncertainty_types(temperature_set_api, selected_types)
    print(f"Generated {len(assessments)} assessments.")
    
    # Example 3: Save assessments to file
    output_file = "temperature_set_assessments.txt"
    save_assessments_to_file(assessments, output_file)
    print(f"Saved assessments to {output_file}")
    
    print("\nExample completed! The system can now be used to assess any API function against any uncertainty type.")
    print("For real-world usage:")
    print("1. Extract API function descriptions from documentation")
    print("2. Select relevant uncertainty types to assess")
    print("3. Generate assessment instructions")
    print("4. Use the instructions with an LLM to perform the assessment")
    print("5. Analyze the results to improve API design")
