#!/usr/bin/env python3
"""Automatic invoke_tool transformation script (supports batch processing).

Converts invoke_tool calls in multiple files using transform_invoke_tool and
saves the results to new files.
"""

import os
import sys
import re
import json
import glob
import argparse
from pathlib import Path

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from common.transform_handler import transform_invoke_tool
from SmartHomeEnv import SmartHomeEnv
from InformationControlEnv import InformationControlEnv
from MediaControlEnv import MediaControlEnv
from TimeNotificationEnv import TimeNotificationEnv
from CommunicationController import CommunicationController
from CulinaryControlEnv import CulinaryControlEnv
from TransactionEnv import TransactionEnv
from common import register_environment, invoke_tool


def extract_user_id(content):
    """Extract the user ID from file content."""
    # Find pattern like: set_current_user('user1')
    pattern = r"set_current_user\(['\"]([^'\"]+)['\"]\)"
    matches = re.findall(pattern, content)
    if matches:
        # Return the first matched user ID
        return matches[0]
    # Default value if no explicit user ID is found
    return 'user1'


def extract_invoke_tool_calls(content):
    """Extract invoke_tool calls from the file content."""
    # Regex pattern: start at invoke_tool and continue until the closing parenthesis
    pattern = r'invoke_tool\([^)]*(?:\([^)]*\)[^)]*)*\)'
    matches = re.findall(pattern, content)
    return matches


def setup_environments(user_id):
    """Initialize and register all environments using the given user ID."""
    smart_home_env = SmartHomeEnv()
    info_control_env = InformationControlEnv()
    media_control_env = MediaControlEnv()
    time_notification_env = TimeNotificationEnv()
    communication_env = CommunicationController()
    culinary_env = CulinaryControlEnv()
    transaction_env = TransactionEnv()
    
    # Register all environments
    register_environment('SmartHomeEnv', smart_home_env)
    register_environment('InformationControlEnv', info_control_env)
    register_environment('MediaControlEnv', media_control_env)
    register_environment('TimeNotificationEnv', time_notification_env)
    register_environment('CommunicationController', communication_env)
    register_environment('CulinaryControlEnv', culinary_env)
    register_environment('TransactionEnv', transaction_env)
    
    # Set current user for all environments
    smart_home_env.set_current_user(user_id)
    info_control_env.set_current_user(user_id)
    media_control_env.set_current_user(user_id)
    time_notification_env.set_current_user(user_id)
    communication_env.set_current_user(user_id)
    culinary_env.set_current_user(user_id)
    transaction_env.set_current_user(user_id)
    
    return smart_home_env


def transform_single_file(input_file, output_file, mapping_file):
    """Transform a single file containing invoke_tool calls."""
    print(f"📖 Input file: {input_file}")
    print(f"📝 Output file: {output_file}")
    print(f"🗂️  Mapping file: {mapping_file}")
    
    # Read original file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✅ Finished reading original file: {len(content)} characters")
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        return False, {}
    
    # Extract user ID from file
    user_id = extract_user_id(content)
    print(f"📋 Extracted user ID: {user_id}")
    
    # Set up environments
    smart_home_env = setup_environments(user_id)
    
    # Extract invoke_tool calls
    invoke_calls = extract_invoke_tool_calls(content)
    print(f"🔍 Found {len(invoke_calls)} invoke_tool call(s)")
    
    if not invoke_calls:
        print("❌ No invoke_tool calls found.")
        return False, {}
    
    # Store mappings for transforms
    transform_mappings = []
    updated_content = content
    
    # Transform and execute each invoke_tool call
    for i, call in enumerate(invoke_calls):
        print(f"🔄 Transforming ({i+1}/{len(invoke_calls)}): {call}")
        
        try:
            # Apply transform_invoke_tool (passing actual environment data)
            transformed_call = transform_invoke_tool(call, smart_home_env.data)
            print(f"✅ Transform complete: {transformed_call}")
            
            # Execute the transformed call
            execution_result = None
            execution_success = False
            try:
                # Use eval to execute the transformed invoke_tool call
                execution_result = eval(transformed_call)
                execution_success = True
                print(f"🚀 Execution result: {execution_result}")
            except Exception as exec_e:
                execution_result = str(exec_e)
                execution_success = False
                print(f"⚠️ Execution failed: {exec_e}")
            
            # Save mapping (including execution result)
            mapping = {
                "index": i + 1,
                "before": call,
                "after": transformed_call,
                "execution_result": execution_result,
                "execution_success": execution_success
            }
            transform_mappings.append(mapping)
            
            # Replace only the first occurrence in the file content
            # (There may be multiple identical calls.)
            updated_content = updated_content.replace(call, transformed_call, 1)
            
        except Exception as e:
            print(f"❌ Transform failed: {str(e)}")
            # Even on failure, record the mapping
            mapping = {
                "index": i + 1,
                "before": call,
                "after": call,  # Keep original when transform fails
                "transform_error": str(e),
                "execution_result": None,
                "execution_success": False
            }
            transform_mappings.append(mapping)
    
    # Save transformed file
    try:
        # Create the output directory if it exists as a path
        output_dir = os.path.dirname(output_file)
        if output_dir:  # Only when the directory path is non-empty
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"✅ Saved transformed file: {output_file}")
    except Exception as e:
        print(f"❌ Failed to save transformed file: {str(e)}")
        return False, {}
    
    # Save mapping JSON
    try:
        mapping_data = {
            "source_file": input_file,
            "target_file": output_file,
            "total_transforms": len(invoke_calls),
            "successful_transforms": len([m for m in transform_mappings if "transform_error" not in m]),
            "mappings": transform_mappings
        }
        
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping_data, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved transform mapping: {mapping_file}")
    except Exception as e:
        print(f"❌ Failed to save mapping file: {str(e)}")
    
    # Compute statistics
    successful = len([m for m in transform_mappings if "transform_error" not in m])
    failed = len(transform_mappings) - successful
    execution_successful = len([m for m in transform_mappings if m.get("execution_success", False)])
    
    stats = {
        "total_calls": len(invoke_calls),
        "transform_successful": successful,
        "transform_failed": failed,
        "execution_successful": execution_successful
    }
    
    print("📊 Transform and execution summary:")
    print(f"   Total calls: {stats['total_calls']}")
    print(f"   Transforms succeeded: {stats['transform_successful']}")
    print(f"   Transforms failed: {stats['transform_failed']}")
    print(f"   Executions succeeded: {stats['execution_successful']}")
    
    return True, stats


def main():
    """Main function – focuses on transforming a single file."""
    parser = argparse.ArgumentParser(description='Transform invoke_tool calls in a single Python file')
    parser.add_argument('--input', required=True, help='Input file path')
    parser.add_argument('--output', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    # Automatically generate mapping file path
    mapping_file = args.output.replace('.py', '_mapping.json')
    
    print("🔧 Starting single-file transform")
    success, stats = transform_single_file(args.input, args.output, mapping_file)
    
    if success:
        print(f"✅ Transform completed: {args.input} → {args.output}")
        sys.exit(0)
    else:
        print(f"❌ Transform failed: {args.input}")
        sys.exit(1)


if __name__ == "__main__":
    main()
