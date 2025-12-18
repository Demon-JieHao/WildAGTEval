#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user8_msg_scenario10_msgcall_scenario74_Message_MessageCall_merged.jsonl
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
    """Execute combined conversation for user8 - Unknown scenario"""
    try:
        # Initialize and register all environments with user user8
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
        smart_home_env.set_current_user('user8')
        info_control_env.set_current_user('user8')
        media_control_env.set_current_user('user8')
        time_notification_env.set_current_user('user8')
        communication_env.set_current_user('user8')
        culinary_env.set_current_user('user8')
        transaction_env.set_current_user('user8')
        
        print('Executing combined conversation script: Unknown')
        print('User: user8, Scenario: 74, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + "Text the last person who messaged me: 'Hi there! Hope you're having a great day!'")
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("get_messages", limit=10)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_messages returned success:false")
    except Exception as e:
        print(f"ERROR in get_messages: {e}")
        return False
    try:
        result = invoke_tool("send_message", contact_id='contact2', content="Hi there! Hope you're having a great day!")
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: send_message returned success:false")
    except Exception as e:
        print(f"ERROR in send_message: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + "Dial 404-685-5545 and text Lisa Baker saying 'Hi! Hope you're doing well today.'")
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("power_on", endpoints=['61'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: power_on returned success:false")
    except Exception as e:
        print(f"ERROR in power_on: {e}")
        return False
    try:
        result = invoke_tool("make_call", phone_number='D:4046855545', device_endpoint='61')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: make_call returned success:false")
    except Exception as e:
        print(f"ERROR in make_call: {e}")
        return False
    try:
        result = invoke_tool("find_contact", query='Lisa Baker', search_type='name', limit=5)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: find_contact returned success:false")
    except Exception as e:
        print(f"ERROR in find_contact: {e}")
        return False
    try:
        result = invoke_tool("send_message", contact_id='contact35', content="Hi! Hope you're doing well today.")
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
