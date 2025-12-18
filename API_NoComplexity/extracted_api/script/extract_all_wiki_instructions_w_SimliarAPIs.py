#!/usr/bin/env python3
# Script to extract wiki instructions from all environments

import os
import sys
import importlib.util
import time
from pathlib import Path

def extract_wiki_from_file(env_path, env_name):
    """Extract WIKI content from a wiki.py file"""
    wiki_file_path = os.path.join(env_path, "wiki.py")
    
    if not os.path.exists(wiki_file_path):
        return None, f"wiki.py not found in {env_path}"
    
    try:
        # Load the module
        spec = importlib.util.spec_from_file_location(f"{env_name}_wiki", wiki_file_path)
        wiki_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(wiki_module)
        
        # Get the WIKI content
        if hasattr(wiki_module, 'WIKI'):
            return wiki_module.WIKI, None
        else:
            return None, f"WIKI variable not found in {wiki_file_path}"
            
    except Exception as e:
        return None, f"Error loading {wiki_file_path}: {e}"

def convert_env_name_to_instruction_name(env_name):
    """Convert environment name to instruction file name (remove 'Env' suffix)"""
    if env_name.endswith('Env'):
        return env_name[:-3] + 'Instruction'
    else:
        return env_name + 'Instruction'

def create_instruction_file(wiki_content, output_path):
    """Create a Python instruction file with the wiki content"""
    instruction_content = f'''instruction="""
{wiki_content}
"""
'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(instruction_content)

def extract_wiki_instruction(env_name, env_path, output_dir):
    """Extract wiki instruction from a single environment"""
    print(f"Processing {env_name}...")
    
    try:
        # Extract wiki content
        wiki_content, error = extract_wiki_from_file(env_path, env_name)
        
        if error:
            print(f"❌ {env_name}: {error}")
            return False
        
        if not wiki_content:
            print(f"❌ {env_name}: No wiki content found")
            return False
        
        # Generate output filename
        instruction_name = convert_env_name_to_instruction_name(env_name)
        output_file = f"{instruction_name}.py"
        output_path = os.path.join(output_dir, output_file)
        
        # Create instruction file
        create_instruction_file(wiki_content, output_path)
        
        # Calculate content size for reporting
        content_lines = len(wiki_content.split('\n'))
        content_size = len(wiki_content)
        
        print(f"✅ {env_name} -> {output_file}")
        print(f"   Content: {content_lines} lines, {content_size} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ {env_name}: Unexpected error - {e}")
        return False

def main():
    # Define environments to process
    environments = [
        "SmartHomeEnv",
        "InformationControlEnv", 
        "MediaControlEnv",
        "CommunicationController",
        "CulinaryControlEnv",
        "TimeNotificationEnv",
        "TransactionEnv",
        "SimilarAPIs"
    ]
    
    print("🚀 Starting wiki instruction extraction for all environments...")
    print("=" * 70)
    
    # Get absolute paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../api_file"))
    
    # Check which environments exist
    existing_envs = []
    missing_envs = []
    
    for env_name in environments:
        env_path = os.path.join(base_dir, env_name)
        if os.path.exists(env_path):
            existing_envs.append((env_name, env_path))
        else:
            missing_envs.append(env_name)
    
    if missing_envs:
        print("⚠️  Warning: The following environments were not found:")
        for env in missing_envs:
            print(f"   - {env}")
        print()
    
    # Process existing environments
    successful = 0
    failed = 0
    start_time = time.time()
    
    for env_name, env_path in existing_envs:
        success = extract_wiki_instruction(env_name, env_path, output_dir)
        if success:
            successful += 1
        else:
            failed += 1
        print()  # Add spacing between environments
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("=" * 70)
    print("📊 EXTRACTION SUMMARY")
    print("=" * 70)
    print(f"Total environments found: {len(existing_envs)}")
    print(f"Successful extractions: {successful}")
    print(f"Failed extractions: {failed}")
    print(f"Missing environments: {len(missing_envs)}")
    print(f"Total time: {duration:.2f} seconds")
    
    if successful > 0:
        print(f"\n✅ Successfully extracted wiki instructions from {successful} environment(s)")
        print("📁 Check extracted_api/api_file/ for generated instruction files")
    
    if failed > 0:
        print(f"\n❌ {failed} extraction(s) failed - check error messages above")
        sys.exit(1)
    
    if missing_envs:
        print(f"\n⚠️  {len(missing_envs)} environment(s) not found - see warnings above")
    
    print("\n🎉 Wiki instruction extraction completed!")

if __name__ == "__main__":
    main()
