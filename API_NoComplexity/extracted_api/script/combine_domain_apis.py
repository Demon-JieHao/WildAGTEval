#!/usr/bin/env python3
# Configurable script to combine APIs based on domain selection guide

import json
import os
import sys
from typing import Dict, List, Tuple

# Domain combination configurations based on domain_selection_guide.md
DOMAIN_COMBINATIONS = {
    "home_entertainment": {
        "name": "Home & Entertainment Package",
        "description": "Smart home device control + Media playback + Information retrieval",
        "domains": ["SmartHomeEnv", "MediaControlEnv", "InformationControlEnv"],
        "expected_tools": 47,
        "output_file": "HomeEntertainmentAPI.json"
    },
    "daily_life_management": {
        "name": "Daily Life Management",
        "description": "Smart home automation + Time-based notifications + Information retrieval",
        "domains": ["SmartHomeEnv", "TimeNotificationEnv", "InformationControlEnv"],
        "expected_tools": 39,
        "output_file": "DailyLifeManagementAPI.json"
    },
    "social_entertainment": {
        "name": "Social & Entertainment Hub",
        "description": "Communication services + Media playback + Food/recipe coordination",
        "domains": ["CommunicationController", "MediaControlEnv", "CulinaryControlEnv"],
        "expected_tools": 35,
        "output_file": "SocialEntertainmentAPI.json"
    },
    "shopping_planning": {
        "name": "Shopping & Planning Assistant",
        "description": "E-commerce transactions + Food/recipe planning + Time-based reminders",
        "domains": ["TransactionEnv", "CulinaryControlEnv", "TimeNotificationEnv"],
        "expected_tools": 32,
        "output_file": "ShoppingPlanningAPI.json"
    },
    "complete_daily_assistant": {
        "name": "Complete Daily Assistant",
        "description": "Smart home + Information + Time notifications + Communication",
        "domains": ["SmartHomeEnv", "InformationControlEnv", "TimeNotificationEnv", "CommunicationController"],
        "expected_tools": 46,
        "output_file": "CompleteDailyAssistantAPI.json"
    },
    "entertainment_social_coordinator": {
        "name": "Entertainment & Social Coordinator",
        "description": "Media control + Communication + Food coordination + Time management",
        "domains": ["MediaControlEnv", "CommunicationController", "CulinaryControlEnv", "TimeNotificationEnv"],
        "expected_tools": 43,
        "output_file": "EntertainmentSocialCoordinatorAPI.json"
    }
}

# Mapping of domain names to their API file names
DOMAIN_TO_FILE = {
    "SmartHomeEnv": "SmartHomeAPI.json",
    "InformationControlEnv": "InformationControlAPI.json",
    "MediaControlEnv": "MediaControlAPI.json",
    "CommunicationController": "CommunicationControllerAPI.json",
    "CulinaryControlEnv": "CulinaryControlEnvAPI.json",
    "TimeNotificationEnv": "TimeNotificationEnvAPI.json",
    "TransactionEnv": "TransactionEnvAPI.json"
}

def load_domain_api(api_file_dir: str, domain: str) -> Tuple[Dict, int]:
    """Load API data for a specific domain and return the data and tool count"""
    file_name = DOMAIN_TO_FILE[domain]
    file_path = os.path.join(api_file_dir, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"API file not found: {file_path}")
    
    with open(file_path, "r") as f:
        api_data = json.load(f)
    
    # Count tools in this domain
    tool_count = len(api_data.get(domain, {}))
    
    return api_data, tool_count

def create_combination(combination_key: str, input_api_dir: str, output_api_dir: str) -> bool:
    """Create a specific domain combination and return success status"""
    if combination_key not in DOMAIN_COMBINATIONS:
        print(f"❌ Unknown combination: {combination_key}")
        return False
    
    config = DOMAIN_COMBINATIONS[combination_key]
    
    print(f"Creating {config['name']}...")
    print(f"   Description: {config['description']}")
    print(f"   Domains: {', '.join(config['domains'])}")
    
    try:
        # Load all required domain APIs
        combined_api = {}
        total_tools = 0
        domain_tool_counts = {}
        
        for domain in config['domains']:
            api_data, tool_count = load_domain_api(input_api_dir, domain)
            combined_api.update(api_data)
            total_tools += tool_count
            domain_tool_counts[domain] = tool_count
        
        # Write combined API file
        output_path = os.path.join(output_api_dir, config['output_file'])
        with open(output_path, "w") as f:
            json.dump(combined_api, f, indent=2, sort_keys=True)
        
        # Verify tool count matches expectation
        expected_tools = config['expected_tools']
        if total_tools != expected_tools:
            print(f"⚠️  Warning: Expected {expected_tools} tools, but got {total_tools}")
        
        print(f"✅ Successfully created {config['output_file']}")
        print(f"   Tool breakdown:")
        for domain, count in domain_tool_counts.items():
            print(f"   - {domain}: {count} tools")
        print(f"   Total: {total_tools} tools")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create {config['name']}: {e}")
        return False

def list_combinations():
    """List all available combinations"""
    print("Available Domain Combinations:")
    print("=" * 60)
    
    for key, config in DOMAIN_COMBINATIONS.items():
        print(f"{key}:")
        print(f"   Name: {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Domains: {', '.join(config['domains'])}")
        print(f"   Expected Tools: {config['expected_tools']}")
        print(f"   Output File: {config['output_file']}")
        print()

def main():
    # Get absolute paths for input and output directories
    input_api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api_file"))
    output_api_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../combined_api_file"))
    
    # Create output directory if it doesn't exist
    os.makedirs(output_api_dir, exist_ok=True)
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print(f"  {sys.argv[0]} <combination_key>     # Create specific combination")
        print(f"  {sys.argv[0]} all                   # Create all combinations")
        print(f"  {sys.argv[0]} list                  # List available combinations")
        print()
        list_combinations()
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_combinations()
        return
    
    elif command == "all":
        print("🚀 Creating all domain combinations...")
        print("=" * 60)
        
        successful = 0
        failed = 0
        
        for combination_key in DOMAIN_COMBINATIONS.keys():
            success = create_combination(combination_key, input_api_dir, output_api_dir)
            if success:
                successful += 1
            else:
                failed += 1
            print()  # Add spacing between combinations
        
        print("=" * 60)
        print("📊 COMBINATION SUMMARY")
        print("=" * 60)
        print(f"Total combinations: {len(DOMAIN_COMBINATIONS)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        
        if successful > 0:
            print(f"\n✅ Successfully created {successful} combination(s)")
            print("📁 Check extracted_api/combined_api_file/ for generated JSON files")
        
        if failed > 0:
            print(f"\n❌ {failed} combination(s) failed")
            sys.exit(1)
    
    elif command in DOMAIN_COMBINATIONS:
        print("🚀 Creating domain combination...")
        print("=" * 60)
        
        success = create_combination(command, input_api_dir, output_api_dir)
        
        if success:
            print("\n🎉 Domain combination completed successfully!")
        else:
            print("\n❌ Failed to create domain combination")
            sys.exit(1)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'list' to see available combinations")
        sys.exit(1)

if __name__ == "__main__":
    main()
