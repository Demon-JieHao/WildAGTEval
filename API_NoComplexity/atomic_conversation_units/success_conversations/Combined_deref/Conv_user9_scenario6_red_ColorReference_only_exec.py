#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user9_scenario6_red_ColorReference_only.jsonl
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
    """Execute combined conversation for user9 - Unknown scenario"""
    try:
        # Initialize and register all environments with user user9
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
        smart_home_env.set_current_user('user9')
        info_control_env.set_current_user('user9')
        media_control_env.set_current_user('user9')
        time_notification_env.set_current_user('user9')
        communication_env.set_current_user('user9')
        culinary_env.set_current_user('user9')
        transaction_env.set_current_user('user9')
        
        print('Executing combined conversation script: Unknown')
        print('User: user9, Scenario: 6, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + 'Turn the Bedroom Lamp red')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
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
        result = invoke_tool("get_device_details", endpoint='22')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_device_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_device_details: {e}")
        return False
    try:
        result = invoke_tool("power_on", endpoints=['22'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: power_on returned success:false")
    except Exception as e:
        print(f"ERROR in power_on: {e}")
        return False
    try:
        result = invoke_tool("color_set", endpoints=['22'], color='red')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: color_set returned success:false")
    except Exception as e:
        print(f"ERROR in color_set: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'I want a phone case in red, and add it to the cart')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("search_product", query='phone case', category='accessories', sort_by='rating', limit=10)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod82')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod80')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod78')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod84')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod77')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod83')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod79')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod81')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod77', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
