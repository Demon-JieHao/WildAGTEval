#!/usr/bin/env python3
"""
Generate assessment templates for uncertainty scenarios.

This script generates assessment templates for the uncertainty scenarios in organized_scenarios
based on domain, function, and uncertainty type.

The main workflow:
1. Takes command line arguments for domain, function, uncertainty type and output directory
2. Processes scenarios organized by domain/function/uncertainty type structure
3. Extracts necessary details and generates assessment templates
4. Saves templates as markdown files
"""

# Import required libraries for file/path handling, regex and argument parsing
import os
import json
import re
import argparse
from pathlib import Path
import sys

# Base directory for scenario assessment package
ASSESSMENT_DIR = Path(__file__).resolve().parent

# Import custom modules for extracting scenario details
from .scenario_api_function_extractor import extract_api_function_details
from .scenario_uncertainty_extractor import (
    extract_uncertainty_type_details,
    extract_uncertainty_type_instructions,
    extract_output_format_instructions,
)
from .scenario_assessment_template import generate_assessment_template

def extract_run_ids_from_json_files(directory):
    """
    Extract run IDs from scenario JSON files in a directory.
    Looks for files matching pattern 'scenario_run_*.json' and extracts the run number.
    
    Parameters:
    - directory: Path to the directory containing scenario files
    
    Returns:
    - List of run IDs found in the directory, sorted numerically
    """
    run_ids = []
    
    for json_file in directory.glob("scenario_run_*.json"):
        match = re.search(r'scenario_run_(\d+)\.json', json_file.name)
        if match:
            run_ids.append(match.group(1))
    
    return sorted(run_ids)

def read_scenario_content(json_file):
    """
    Read and parse scenario content from a JSON file.
    Extracts the 'scenario' field from the JSON data.
    
    Parameters:
    - json_file: Path to the JSON file containing scenario data
    
    Returns:
    - String containing the scenario content, empty string if error occurs
    """
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('scenario', '')
    except Exception as e:
        print(f"Error reading scenario content from {json_file}: {e}")
        return ""

def main():
    # Set up command line argument parser with options for customizing assessment generation
    parser = argparse.ArgumentParser(description="Generate assessment templates for uncertainty scenarios.")
    parser.add_argument("--domain", help="Specific domain to assess")
    parser.add_argument("--function", help="Specific function to assess")
    parser.add_argument("--uncertainty-type", help="Specific uncertainty type to assess")
    parser.add_argument("--run", help="Specific run to use")
    parser.add_argument("--output-dir", default="scenario_assessments", help="Output directory for assessment templates")
    args = parser.parse_args()
    
    # Set up directory paths and create output directory if needed
    scenarios_dir = ASSESSMENT_DIR / "organized_scenarios"
    output_dir = ASSESSMENT_DIR / args.output_dir
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Get list of domains to process - either specific domain from args or all domains
    domains = [args.domain] if args.domain else [d.name for d in scenarios_dir.glob("*") if d.is_dir()]
    print(domains)

    total_templates = 0
    
    # Process each domain
    for domain in sorted(domains):
        domain_dir = scenarios_dir / domain
        if not domain_dir.is_dir():
            print(f"Domain directory not found: {domain_dir}")
            continue
            
        print(f"Processing domain: {domain}")
        
        # Get list of functions to process - either specific function or all functions
        functions = [args.function] if args.function else [f.name for f in domain_dir.glob("*") if f.is_dir()]
        
        # Process each function
        for function in sorted(functions):
            function_dir = domain_dir / function
            if not function_dir.is_dir():
                print(f"Function directory not found: {function_dir}")
                continue
                
            # Get API function details for current function
            api_function_details = extract_api_function_details(domain, function)
            if not api_function_details:
                print(f"Could not extract API details for {domain}.{function}")
                continue
            
            # Get list of uncertainty types to process
            uncertainty_types = [args.uncertainty_type] if args.uncertainty_type else [
                ut.name for ut in function_dir.glob("*") if ut.is_dir()
            ]
            
            # Process each uncertainty type
            for uncertainty_type in sorted(uncertainty_types):
                uncertainty_dir = function_dir / uncertainty_type
                if not uncertainty_dir.is_dir():
                    print(f"Uncertainty type directory not found: {uncertainty_dir}")
                    continue
                
                print(f"  Processing {domain}.{function} - {uncertainty_type}")
                
                # Extract details and instructions for current uncertainty type
                uncertainty_type_details = extract_uncertainty_type_details(uncertainty_type)
                if not uncertainty_type_details:
                    print(f"Could not extract details for uncertainty type: {uncertainty_type}")
                    continue
                
                uncertainty_type_instructions = extract_uncertainty_type_instructions(uncertainty_type)
                output_format_instructions = extract_output_format_instructions(uncertainty_type)
                
                # Get run IDs for current uncertainty type
                run_ids = extract_run_ids_from_json_files(uncertainty_dir)
                if not run_ids:
                    print(f"No scenario runs found in {uncertainty_dir}")
                    continue
                
                # Filter for specific run if requested
                if args.run:
                    if args.run in run_ids:
                        run_ids = [args.run]
                    else:
                        print(f"Requested run {args.run} not found in {uncertainty_dir}")
                        continue
                
                # Process each run and generate assessment template
                for run_id in run_ids:
                    scenario_file = uncertainty_dir / f"scenario_run_{run_id}.json"
                    
                    if not scenario_file.exists():
                        print(f"Scenario file not found: {scenario_file}")
                        continue
                    
                    # Read scenario content from file
                    scenario_content = read_scenario_content(scenario_file)
                    if not scenario_content:
                        print(f"Could not read scenario content from {scenario_file}")
                        continue
                    
                    # Clean up instruction text
                    cleaned_instructions = re.sub(r'template \+= """', '', uncertainty_type_instructions)
                    cleaned_instructions = re.sub(r'"""$', '', cleaned_instructions)
                    
                    # Generate assessment template with gathered information
                    assessment_template = generate_assessment_template(
                        api_function_details,
                        uncertainty_type_details,
                        cleaned_instructions,
                        scenario_content,
                        None,  # Remove output_format_instructions from parameters
                        run_id  # Provide run_id as a simple string
                    )
                    
                    # Save generated template to output file
                    output_file = output_dir / f"{domain}__{function}__{uncertainty_type}__run_{run_id}_assessment.md"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(assessment_template)
                    
                    print(f"    Generated assessment template: {output_file}")
                    total_templates += 1
    
    # Print summary of template generation
    print(f"\nAssessment template generation complete. Generated {total_templates} templates.")
    print(f"Templates saved to: {output_dir}")
    
    # Return success if templates were generated, error if none were generated
    return 0 if total_templates > 0 else 1

# Execute main function if script is run directly
if __name__ == "__main__":
    sys.exit(main())
