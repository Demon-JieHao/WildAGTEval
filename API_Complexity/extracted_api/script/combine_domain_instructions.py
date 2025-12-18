#!/usr/bin/env python3
# Configurable script to combine instruction files based on domain selection guide

import os
import sys
import importlib.util
from typing import Dict, List

# Domain combination configurations based on domain_selection_guide.md
DOMAIN_COMBINATIONS = {
    "home_entertainment": {
        "name": "Home & Entertainment Package",
        "description": "Smart home device control + Media playback + Information retrieval",
        "domains": ["SmartHomeEnv", "MediaControlEnv", "InformationControlEnv"],
        "output_file": "HomeEntertainmentInstruction.py"
    },
    "daily_life_management": {
        "name": "Daily Life Management", 
        "description": "Smart home automation + Time-based notifications + Information retrieval",
        "domains": ["SmartHomeEnv", "TimeNotificationEnv", "InformationControlEnv"],
        "output_file": "DailyLifeManagementInstruction.py"
    },
    "social_entertainment": {
        "name": "Social & Entertainment Hub",
        "description": "Communication services + Media playback + Food/recipe coordination",
        "domains": ["CommunicationController", "MediaControlEnv", "CulinaryControlEnv"],
        "output_file": "SocialEntertainmentInstruction.py"
    },
    "shopping_planning": {
        "name": "Shopping & Planning Assistant",
        "description": "E-commerce transactions + Food/recipe planning + Time-based reminders",
        "domains": ["TransactionEnv", "CulinaryControlEnv", "TimeNotificationEnv"],
        "output_file": "ShoppingPlanningInstruction.py"
    },
    "complete_daily_assistant": {
        "name": "Complete Daily Assistant",
        "description": "Smart home + Information + Time notifications + Communication",
        "domains": ["SmartHomeEnv", "InformationControlEnv", "TimeNotificationEnv", "CommunicationController"],
        "output_file": "CompleteDailyAssistantInstruction.py"
    },
    "entertainment_social_coordinator": {
        "name": "Entertainment & Social Coordinator",
        "description": "Media control + Communication + Food coordination + Time management",
        "domains": ["MediaControlEnv", "CommunicationController", "CulinaryControlEnv", "TimeNotificationEnv"],
        "output_file": "EntertainmentSocialCoordinatorInstruction.py"
    }
}

# Mapping of domain names to their instruction file names (removing 'Env' suffix)
DOMAIN_TO_INSTRUCTION_FILE = {
    "SmartHomeEnv": "SmartHomeInstruction.py",
    "InformationControlEnv": "InformationControlInstruction.py",
    "MediaControlEnv": "MediaControlInstruction.py",
    "CommunicationController": "CommunicationControllerInstruction.py",
    "CulinaryControlEnv": "CulinaryControlInstruction.py",
    "TimeNotificationEnv": "TimeNotificationInstruction.py",
    "TransactionEnv": "TransactionInstruction.py"
}

def load_instruction_content(input_dir: str, domain: str) -> str:
    """Load instruction content from a domain's instruction file"""
    file_name = DOMAIN_TO_INSTRUCTION_FILE[domain]
    file_path = os.path.join(input_dir, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Instruction file not found: {file_path}")
    
    try:
        # Load the module to get the instruction content
        spec = importlib.util.spec_from_file_location(f"{domain}_instruction", file_path)
        instruction_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(instruction_module)
        
        if hasattr(instruction_module, 'instruction'):
            return instruction_module.instruction
        else:
            raise ValueError(f"No 'instruction' variable found in {file_path}")
            
    except Exception as e:
        raise Exception(f"Error loading instruction from {file_path}: {e}")

def create_combined_instruction(combination_key: str, input_dir: str, output_dir: str) -> bool:
    """Create a combined instruction file for a specific domain combination"""
    if combination_key not in DOMAIN_COMBINATIONS:
        print(f"❌ Unknown combination: {combination_key}")
        return False
    
    config = DOMAIN_COMBINATIONS[combination_key]
    
    print(f"Creating {config['name']}...")
    print(f"   Description: {config['description']}")
    print(f"   Domains: {', '.join(config['domains'])}")
    
    try:
        # Load instruction content from each domain
        combined_instructions = []
        domain_info = []
        
        for domain in config['domains']:
            instruction_content = load_instruction_content(input_dir, domain)
            combined_instructions.append(f"# ===== {domain} Instructions =====\n\n{instruction_content}")
            
            # Calculate content size for reporting
            lines = len(instruction_content.split('\n'))
            chars = len(instruction_content)
            domain_info.append(f"{domain}: {lines} lines, {chars} characters")
        
        # Combine all instructions with separators
        final_instruction = "\n\n" + "\n\n".join(combined_instructions) + "\n"
        
        # Create the combined instruction file
        output_path = os.path.join(output_dir, config['output_file'])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f'instruction="""{final_instruction}"""\n')
        
        print(f"✅ Successfully created {config['output_file']}")
        print(f"   Content breakdown:")
        for info in domain_info:
            print(f"   - {info}")
        
        total_lines = sum(len(load_instruction_content(input_dir, domain).split('\n')) for domain in config['domains'])
        total_chars = sum(len(load_instruction_content(input_dir, domain)) for domain in config['domains'])
        print(f"   Combined total: {total_lines} lines, {total_chars} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create {config['name']}: {e}")
        return False

def list_combinations():
    """List all available combinations"""
    print("Available Domain Instruction Combinations:")
    print("=" * 70)
    
    for key, config in DOMAIN_COMBINATIONS.items():
        print(f"{key}:")
        print(f"   Name: {config['name']}")
        print(f"   Description: {config['description']}")
        print(f"   Domains: {', '.join(config['domains'])}")
        print(f"   Output File: {config['output_file']}")
        print()

def main():
    # Get absolute paths for input and output directories
    input_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api_file"))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../combined_instruction_file"))
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
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
        print("🚀 Creating all domain instruction combinations...")
        print("=" * 70)
        
        successful = 0
        failed = 0
        
        for combination_key in DOMAIN_COMBINATIONS.keys():
            success = create_combined_instruction(combination_key, input_dir, output_dir)
            if success:
                successful += 1
            else:
                failed += 1
            print()  # Add spacing between combinations
        
        print("=" * 70)
        print("📊 COMBINATION SUMMARY")
        print("=" * 70)
        print(f"Total combinations: {len(DOMAIN_COMBINATIONS)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        
        if successful > 0:
            print(f"\n✅ Successfully created {successful} instruction combination(s)")
            print("📁 Check extracted_api/combined_instruction_file/ for generated files")
        
        if failed > 0:
            print(f"\n❌ {failed} combination(s) failed")
            sys.exit(1)
    
    elif command in DOMAIN_COMBINATIONS:
        print("🚀 Creating domain instruction combination...")
        print("=" * 70)
        
        success = create_combined_instruction(command, input_dir, output_dir)
        
        if success:
            print("\n🎉 Domain instruction combination completed successfully!")
        else:
            print("\n❌ Failed to create domain instruction combination")
            sys.exit(1)
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'list' to see available combinations")
        sys.exit(1)

if __name__ == "__main__":
    main()
