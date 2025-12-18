#!/usr/bin/env python3
"""
Generate a summary report of the organized scenarios.
This script will analyze the organized_scenarios directory and create a report
of the number of scenarios for each domain, function, and uncertainty type.
"""

import os
import json
from pathlib import Path
from collections import defaultdict, Counter

# Assessment package directory: this file lives in .../API_Complexity/complexity_integration/complexity_scenario_assessment
ASSESSMENT_DIR = Path(__file__).resolve().parent

def count_scenarios_by_run(directory):
    """Count the number of scenario files by run in a directory."""
    counts = Counter()
    for file_path in directory.glob("scenario_run_*.json"):
        run_id = file_path.name.split("_")[-1].split(".")[0]
        counts[run_id] += 1
    return counts

def main():
    base_dir = ASSESSMENT_DIR / "organized_scenarios"
    if not base_dir.exists():
        print(f"Error: organized_scenarios directory not found at {base_dir}.")
        return
    
    # Store statistics
    domain_counts = defaultdict(int)
    function_counts = defaultdict(int)
    uncertainty_counts = defaultdict(int)
    function_uncertainty_counts = defaultdict(lambda: defaultdict(int))
    
    # Detailed report data
    domains_data = {}
    
    # Process all domains
    for domain_dir in sorted(base_dir.glob("*")):
        if not domain_dir.is_dir():
            continue
            
        domain_name = domain_dir.name
        domain_counts[domain_name] = 0
        domains_data[domain_name] = {"functions": {}}
        
        # Process all functions
        for function_dir in sorted(domain_dir.glob("*")):
            if not function_dir.is_dir():
                continue
                
            function_name = function_dir.name
            function_key = f"{domain_name}.{function_name}"
            function_counts[function_key] = 0
            domains_data[domain_name]["functions"][function_name] = {"uncertainty_types": {}}
            
            # Process all uncertainty types
            for uncertainty_dir in sorted(function_dir.glob("*")):
                if not uncertainty_dir.is_dir():
                    continue
                    
                uncertainty_type = uncertainty_dir.name
                uncertainty_counts[uncertainty_type] += 1
                function_uncertainty_counts[function_key][uncertainty_type] += 1
                
                # Count scenarios by run
                run_counts = count_scenarios_by_run(uncertainty_dir)
                total_scenarios = sum(run_counts.values())
                
                domain_counts[domain_name] += total_scenarios
                function_counts[function_key] += total_scenarios
                
                # Add to detailed report data
                domains_data[domain_name]["functions"][function_name]["uncertainty_types"][uncertainty_type] = {
                    "counts_by_run": dict(run_counts),
                    "total": total_scenarios
                }
    
    # Generate report
    summary_path = ASSESSMENT_DIR / "organized_scenarios_summary.md"
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Organized Scenarios Summary\n\n")
        
        # Overview
        f.write("## Overview\n\n")
        f.write(f"Total number of scenarios organized: {sum(domain_counts.values())}\n\n")
        
        # Summary by domain
        f.write("## Scenarios by Domain\n\n")
        for domain, count in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{domain}**: {count} scenarios\n")
        f.write("\n")
        
        # Summary by uncertainty type
        f.write("## Uncertainty Types\n\n")
        total_combinations = sum(len(v) for v in function_uncertainty_counts.values())
        f.write(f"Total unique function-uncertainty type combinations: {total_combinations}\n\n")
        
        uncertainty_scenario_counts = defaultdict(int)
        for function_data in function_uncertainty_counts.values():
            for uncertainty, count in function_data.items():
                uncertainty_scenario_counts[uncertainty] += count
        
        for uncertainty, count in sorted(uncertainty_scenario_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"- **{uncertainty}**: {count} function combinations\n")
        f.write("\n")
        
        # Detailed breakdown by domain
        f.write("## Detailed Breakdown\n\n")
        
        for domain, domain_data in sorted(domains_data.items()):
            f.write(f"### {domain}\n\n")
            
            for function, function_data in sorted(domain_data["functions"].items()):
                f.write(f"#### {function}\n\n")
                
                for uncertainty, uncertainty_data in sorted(function_data["uncertainty_types"].items()):
                    f.write(f"##### {uncertainty}\n\n")
                    f.write(f"Total scenarios: {uncertainty_data['total']}\n\n")
                    
                    # Show scenarios by run
                    f.write("Scenarios by run:\n")
                    for run_id in sorted(uncertainty_data["counts_by_run"].keys()):
                        f.write(f"- Run {run_id}: {uncertainty_data['counts_by_run'][run_id]} scenario(s)\n")
                    f.write("\n")
        
    print(f"Summary report generated: {summary_path}")

if __name__ == "__main__":
    main()
