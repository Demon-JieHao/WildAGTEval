#!/usr/bin/env python3
"""
Extract scenario content from organized JSON files.

This script extracts the actual scenario content from the organized JSON files and saves
them as Markdown files, one per domain-function-uncertainty type combination.
"""

import os
import json
import re
from pathlib import Path

# Assessment package directory: this file lives in .../API_Complexity/complexity_integration/complexity_scenario_assessment
ASSESSMENT_DIR = Path(__file__).resolve().parent

def extract_scenario_content(json_path):
    """Extract the scenario content from a JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            return data.get('scenario', ''), data.get('run_id', 'unknown')
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in {json_path}: {e}")
            return '', 'unknown'

def main():
    base_dir = ASSESSMENT_DIR / "organized_scenarios"
    if not base_dir.exists():
        print(f"Error: organized_scenarios directory not found at {base_dir}.")
        return
    
    # Create output directory for extracted content
    output_dir = ASSESSMENT_DIR / "scenario_content"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    total_files_processed = 0
    total_content_files = 0
    
    # Process each domain
    for domain_dir in sorted(base_dir.glob("*")):
        if not domain_dir.is_dir():
            continue
        
        domain_name = domain_dir.name
        domain_output = output_dir / domain_name
        domain_output.mkdir(exist_ok=True, parents=True)
        
        print(f"Processing domain: {domain_name}...")
        
        # Process each function
        for function_dir in sorted(domain_dir.glob("*")):
            if not function_dir.is_dir():
                continue
            
            function_name = function_dir.name
            function_output = domain_output / function_name
            function_output.mkdir(exist_ok=True, parents=True)
            
            # Process each uncertainty type
            for uncertainty_dir in sorted(function_dir.glob("*")):
                if not uncertainty_dir.is_dir():
                    continue
                
                uncertainty_type = uncertainty_dir.name
                
                # Collect all scenarios for this uncertainty type
                scenarios = []
                
                for scenario_file in sorted(uncertainty_dir.glob("scenario_run_*.json")):
                    total_files_processed += 1
                    run_id = re.search(r'run_(\d+)', scenario_file.name).group(1)
                    content, _ = extract_scenario_content(scenario_file)
                    
                    if content:
                        scenarios.append({
                            "run_id": run_id,
                            "content": content
                        })
                
                if scenarios:
                    # Write all scenarios to a single markdown file
                    output_file = function_output / f"{uncertainty_type}.md"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"# {domain_name}.{function_name} - {uncertainty_type}\n\n")
                        
                        for i, scenario in enumerate(scenarios, 1):
                            f.write(f"## Run {scenario['run_id']}\n\n")
                            f.write(scenario["content"])
                            
                            # Add separator between scenarios
                            if i < len(scenarios):
                                f.write("\n\n---\n\n")
                    
                    total_content_files += 1
    
    print(f"\nProcessing complete!")
    print(f"Total JSON files processed: {total_files_processed}")
    print(f"Total content files created: {total_content_files}")

if __name__ == "__main__":
    main()
