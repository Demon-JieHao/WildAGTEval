#!/usr/bin/env python3
"""
Organize scenarios from all runs by domain, function, and uncertainty type.
This script collects JSON files from all runs in inst_scenarios_gen and organizes them
into a single directory structure based on domain, function, and uncertainty type.
"""

import os
import json
import shutil
import re
from pathlib import Path

# Assessment package directory: .../API_Complexity/complexity_integration/complexity_scenario_assessment
ASSESSMENT_DIR = Path(__file__).resolve().parent.parent / "complexity_scenario_assessment"
# Generation package directory: .../API_Complexity/complexity_integration/complexity_scenario_generation
GEN_DIR = Path(__file__).resolve().parent


def main():
    # Define paths
    source_dir = GEN_DIR / "inst_scenarios_gen"
    output_dir = ASSESSMENT_DIR / "organized_scenarios"
    
    # Create output directory
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Track statistics
    total_files = 0
    organized_files = 0
    domains_count = set()
    functions_count = set()
    uncertainty_types_count = set()
    
    # Process all run directories
    run_dirs = [d for d in source_dir.glob("inst_scenarios_gen_run_*") if d.is_dir()]
    
    for run_dir in sorted(run_dirs):
        run_id = run_dir.name.split("_")[-1]  # Extract run number
        print(f"Processing {run_dir.name}...")
        
        # Process each domain directory
        for domain_dir in [d for d in run_dir.glob("*") if d.is_dir()]:
            domain_name = domain_dir.name
            domains_count.add(domain_name)
            
            # Process each function directory
            for function_dir in [d for d in domain_dir.glob("*") if d.is_dir()]:
                function_name = function_dir.name
                functions_count.add(f"{domain_name}.{function_name}")
                
                # Create output directory for this function
                output_function_dir = output_dir / domain_name / function_name
                output_function_dir.mkdir(exist_ok=True, parents=True)
                
                # Process each scenario file
                for scenario_file in function_dir.glob("*.json"):
                    total_files += 1
                    
                    # Extract uncertainty type from filename
                    match = re.match(r"(.+?)\.md_scenario\.json", scenario_file.name)
                    if not match:
                        print(f"  Skipping file with unexpected name format: {scenario_file}")
                        continue
                        
                    uncertainty_type = match.group(1)
                    uncertainty_types_count.add(uncertainty_type)
                    
                    # Create output directory for this uncertainty type
                    output_uncertainty_dir = output_function_dir / uncertainty_type
                    output_uncertainty_dir.mkdir(exist_ok=True, parents=True)
                    
                    # Copy file with run_id in the filename
                    output_file = output_uncertainty_dir / f"scenario_run_{run_id}.json"
                    shutil.copy2(scenario_file, output_file)
                    organized_files += 1
    
    # Print summary
    print("\nOrganization complete!")
    print(f"Total files processed: {total_files}")
    print(f"Files organized: {organized_files}")
    print(f"Domains: {len(domains_count)}")
    print(f"Functions: {len(functions_count)}")
    print(f"Uncertainty types: {len(uncertainty_types_count)}")

if __name__ == "__main__":
    main()
