#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user1_scenario3_reminder_TimeManagement_SmartHomeEnv_merged.jsonl
"""

import os
import sys
import json
import time

# Calculate camel_synthetic_api directory - go up 2 levels from combined_conversations
script_dir = os.path.dirname(os.path.abspath(__file__))
camel_synthetic_api_dir = os.path.dirname(os.path.dirname(script_dir))


# Add camel_synthetic_api directory to Python path
if camel_synthetic_api_dir not in sys.path:
    sys.path.insert(0, camel_synthetic_api_dir)

try:
    # Import necessary modules with error handling
    from SmartHomeEnv import SmartHomeEnv
    from InformationControlEnv import InformationControlEnv
    from MediaControlEnv import MediaControlEnv
    from TimeNotificationEnv import TimeNotificationEnv
    from CommunicationController import CommunicationController
    from CulinaryControlEnv import CulinaryControlEnv
    from TransactionEnv import TransactionEnv
    from common import invoke_tool, register_environment
    print('DEBUG: All imports successful')
except ImportError as e:
    print(f'ERROR: Failed to import required modules: {e}')
    print(f'ERROR: Current sys.path: {sys.path}')
    sys.exit(1)

def main():
    """Execute combined conversation for user1 - Unknown scenario"""
    try:
        # Initialize and register all environments with user user1
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
        smart_home_env.set_current_user('user1')
        info_control_env.set_current_user('user1')
        media_control_env.set_current_user('user1')
        time_notification_env.set_current_user('user1')
        communication_env.set_current_user('user1')
        culinary_env.set_current_user('user1')
        transaction_env.set_current_user('user1')
        
        print('Executing combined conversation script: Unknown')
        print('User: user1, Scenario: 3, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + 'Let me check my current reminders What do I need to be reminded about?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("get_reminders", status='pending')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_reminders returned success:false")
    except Exception as e:
        print(f"ERROR in get_reminders: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'Set up a reminder for 2025-07-24 at 12:45 PM - organize closet')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("create_reminder", title='Organize closet', date='2025-07-24', time='12:45:00', description="Don't forget to bring the project files", notify_before_minutes=60)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: create_reminder returned success:false")
    except Exception as e:
        print(f"ERROR in create_reminder: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + 'Unsecure the Garage Door Opener')
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("get_user_inventory", )
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_user_inventory returned success:false")
    except Exception as e:
        print(f"ERROR in get_user_inventory: {e}")
        return False
    try:
        result = invoke_tool("lock_status", endpoints=['16'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_status returned success:false")
    except Exception as e:
        print(f"ERROR in lock_status: {e}")
        return False
    try:
        result = invoke_tool("lock_unlock", endpoints=["GarageDoorOpener_16"])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_unlock returned success:false")
    except Exception as e:
        print(f"ERROR in lock_unlock: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
