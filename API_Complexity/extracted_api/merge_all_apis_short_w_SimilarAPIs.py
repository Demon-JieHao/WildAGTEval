#!/usr/bin/env python3
"""
Merge all individual API files into a single API.json file INCLUDING SimilarAPIs (SHORT VERSION)
"""

import json
import os
from pathlib import Path

def main():
    script_dir = Path(__file__).parent
    api_file_dir = script_dir / "api_file"
    
    # List of individual API files INCLUDING SimilarAPIs
    api_files = [
        "SmartHomeAPI.json",
        "InformationControlAPI.json", 
        "MediaControlAPI.json",
        "TransactionEnvAPI.json",
        "CulinaryControlEnvAPI.json",
        "CommunicationControllerAPI.json",
        "TimeNotificationEnvAPI.json",
        "RealEnvAPI.json"  # SimilarAPIs API file
    ]
    
    merged_apis = {}
    total_apis = 0
    
    for api_file in api_files:
        api_path = api_file_dir / api_file
        if api_path.exists():
            print(f"Loading {api_file}...")
            with open(api_path, 'r') as f:
                api_data = json.load(f)
                
            # Merge the API data
            for env_name, apis in api_data.items():
                if env_name not in merged_apis:
                    merged_apis[env_name] = {}
                merged_apis[env_name].update(apis)
                print(f"  Added {len(apis)} APIs from {env_name}")
                total_apis += len(apis)
        else:
            print(f"⚠️ Warning: {api_file} not found")
    
    # Write merged API file
    output_path = api_file_dir / "API_short_w_SimilarAPIs.json"
    with open(output_path, 'w') as f:
        json.dump(merged_apis, f, indent=2)
    
    print(f"\n✅ Merged {total_apis} APIs from {len(merged_apis)} environments")
    print(f"📁 Output: {output_path}")
    
    # Print summary
    for env_name, apis in merged_apis.items():
        print(f"  {env_name}: {len(apis)} APIs")

if __name__ == "__main__":
    main()
