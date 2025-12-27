#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user7_DailyInvestmentMonitor_scenario2.jsonl
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
    """Execute combined conversation for user7 - DailyInvestmentMonitor scenario"""
    try:
        # Initialize and register all environments with user user7
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
        smart_home_env.set_current_user('user7')
        info_control_env.set_current_user('user7')
        media_control_env.set_current_user('user7')
        time_notification_env.set_current_user('user7')
        communication_env.set_current_user('user7')
        culinary_env.set_current_user('user7')
        transaction_env.set_current_user('user7')
        
        print('Executing combined conversation script: DailyInvestmentMonitor')
        print('User: user7, Scenario: 2, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + "I need to review With confidence What's the status of my stock portfolio?")
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("stock_watchlist", )
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: stock_watchlist returned success:false")
    except Exception as e:
        print(f"ERROR in stock_watchlist: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'I want to see switch to my analytical lighting setup Make the Dining Room Light blue')
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
        result = invoke_tool("get_device_details", endpoint='21')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_device_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_device_details: {e}")
        return False
    try:
        result = invoke_tool("color_set", endpoints=['21'], color='blue')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: color_set returned success:false")
    except Exception as e:
        print(f"ERROR in color_set: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + "I'm ready to review With confidence, I need to understand these market movements, let me contact my financial advisor Dial Deborah Ramirez")
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
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
        result = invoke_tool("make_call", phone_number='713-968-1737', call_type='audio', device_endpoint='18A')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: make_call returned success:false")
    except Exception as e:
        print(f"ERROR in make_call: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + 'Let me analyze The data shows significant activity, I should get the latest financial news Show me the latest business news')
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
    try:
        result = invoke_tool("news_by_category", category='business', limit=7)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: news_by_category returned success:false")
    except Exception as e:
        print(f"ERROR in news_by_category: {e}")
        return False
    # Turn 5: User query
    print("\nUser: " + 'Let me explore The data shows significant activity, I should secure my environment for analysis Lock up the Garage Door Opener')
    print("Agent: I'll handle that for you.")

    # API calls for turn 5
    try:
        result = invoke_tool("lock_status", endpoints=['29'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_status returned success:false")
    except Exception as e:
        print(f"ERROR in lock_status: {e}")
        return False
    try:
        result = invoke_tool("lock_lock", endpoints=['29'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_lock returned success:false")
    except Exception as e:
        print(f"ERROR in lock_lock: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
