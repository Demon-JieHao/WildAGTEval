#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user3_msg_scenario9_msgcall_scenario28_Message_MessageCall_merged.jsonl
"""

import os
import sys
import json
import time

# Calculate camel_synthetic_api directory - go up 2 levels from combined_conversations
script_dir = os.path.dirname(os.path.abspath(__file__))
camel_synthetic_api_dir = os.path.dirname(os.path.dirname(script_dir))

# Debug: Print paths for troubleshooting
print(f'DEBUG: Script location: {script_dir}')
print(f'DEBUG: camel_synthetic_api directory: {camel_synthetic_api_dir}')

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
    """Execute combined conversation for user3 - Unknown scenario"""
    try:
        # Initialize and register all environments with user user3
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
        smart_home_env.set_current_user('user3')
        info_control_env.set_current_user('user3')
        media_control_env.set_current_user('user3')
        time_notification_env.set_current_user('user3')
        communication_env.set_current_user('user3')
        culinary_env.set_current_user('user3')
        transaction_env.set_current_user('user3')
        
        print('Executing combined conversation script: Unknown')
        print('User: user3, Scenario: 28, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + "Text Nancy Collins: 'Hi! Hope everything is going well.'")
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("find_contact", query='Nancy Collins', search_type='name', limit=5)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: find_contact returned success:false")
    except Exception as e:
        print(f"ERROR in find_contact: {e}")
        return False
    try:
        result = invoke_tool("send_message", contact_id='contact34', content='Hi! Hope everything is going well.')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: send_message returned success:false")
    except Exception as e:
        print(f"ERROR in send_message: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + "Ring 904-211-4481 and text Nancy Collins: 'Hey! How's your day going?'")
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("power_on", endpoints=['61A'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: power_on returned success:false")
    except Exception as e:
        print(f"ERROR in power_on: {e}")
        return False
    try:
        result = invoke_tool("make_call", phone_number='D:9042114481', device_endpoint='61A')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: make_call returned success:false")
    except Exception as e:
        print(f"ERROR in make_call: {e}")
        return False
    try:
        result = invoke_tool("find_contact", query='Nancy Collins', search_type='name', limit=5)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: find_contact returned success:false")
    except Exception as e:
        print(f"ERROR in find_contact: {e}")
        return False
    try:
        result = invoke_tool("send_message", contact_id='contact34', content="Hey! How's your day going?")
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: send_message returned success:false")
    except Exception as e:
        print(f"ERROR in send_message: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
