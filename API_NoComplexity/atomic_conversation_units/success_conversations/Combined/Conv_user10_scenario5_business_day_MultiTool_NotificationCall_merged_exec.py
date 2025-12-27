#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user10_scenario5_business_day_MultiTool_NotificationCall_merged.jsonl
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
    """Execute combined conversation for user10 - Unknown scenario"""
    try:
        # Initialize and register all environments with user user10
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
        smart_home_env.set_current_user('user10')
        info_control_env.set_current_user('user10')
        media_control_env.set_current_user('user10')
        time_notification_env.set_current_user('user10')
        communication_env.set_current_user('user10')
        culinary_env.set_current_user('user10')
        transaction_env.set_current_user('user10')
        
        print('Executing combined conversation script: Unknown')
        print('User: user10, Scenario: 5, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + 'Could you check how Alphabet stock is doing?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("stock_price", symbol='GOOGL')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: stock_price returned success:false")
    except Exception as e:
        print(f"ERROR in stock_price: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'Please lock the Garage Door Opener')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
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
        result = invoke_tool("lock_status", endpoints=['29'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_status returned success:false")
    except Exception as e:
        print(f"ERROR in lock_status: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + 'Check my recent calling record in about 10 weeks')
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("get_call_history", time_range='10w', limit=2)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_call_history returned success:false")
    except Exception as e:
        print(f"ERROR in get_call_history: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + 'Phone the last calling contact again')
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
    try:
        result = invoke_tool("find_call_device", )
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: find_call_device returned success:false")
    except Exception as e:
        print(f"ERROR in find_call_device: {e}")
        return False
    try:
        result = invoke_tool("power_on", endpoints=['18A'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: power_on returned success:false")
    except Exception as e:
        print(f"ERROR in power_on: {e}")
        return False
    try:
        result = invoke_tool("make_call", phone_number='414-271-4778', call_type='audio', device_endpoint='18A')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: make_call returned success:false")
    except Exception as e:
        print(f"ERROR in make_call: {e}")
        return False
    # Turn 5: User query
    print("\nUser: " + 'Release the Front Door Lock lock')
    print("Agent: I'll handle that for you.")

    # API calls for turn 5
    try:
        result = invoke_tool("lock_status", endpoints=['30'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_status returned success:false")
    except Exception as e:
        print(f"ERROR in lock_status: {e}")
        return False
    try:
        result = invoke_tool("lock_unlock", endpoints=['30'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_unlock returned success:false")
    except Exception as e:
        print(f"ERROR in lock_unlock: {e}")
        return False
    # Turn 6: User query
    print("\nUser: " + 'Check 4 recent notification')
    print("Agent: I'll handle that for you.")

    # API calls for turn 6
    try:
        result = invoke_tool("get_notifications", limit=4, include_read=False)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_notifications returned success:false")
    except Exception as e:
        print(f"ERROR in get_notifications: {e}")
        return False
    # Turn 7: User query
    print("\nUser: " + 'I should call that person now')
    print("Agent: I'll handle that for you.")

    # API calls for turn 7
    try:
        result = invoke_tool("find_contact", query='Sarah Evans', search_type='name', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: find_contact returned success:false")
    except Exception as e:
        print(f"ERROR in find_contact: {e}")
        return False
    try:
        result = invoke_tool("find_call_device", )
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: find_call_device returned success:false")
    except Exception as e:
        print(f"ERROR in find_call_device: {e}")
        return False
    try:
        result = invoke_tool("power_on", endpoints=['18A'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: power_on returned success:false")
    except Exception as e:
        print(f"ERROR in power_on: {e}")
        return False
    try:
        result = invoke_tool("make_call", phone_number='901-293-3282', call_type='audio', device_endpoint='18A')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: make_call returned success:false")
    except Exception as e:
        print(f"ERROR in make_call: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
