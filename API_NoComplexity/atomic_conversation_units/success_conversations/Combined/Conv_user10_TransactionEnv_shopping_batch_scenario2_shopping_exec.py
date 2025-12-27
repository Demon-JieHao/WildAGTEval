#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user10_TransactionEnv_shopping_batch_scenario2_shopping.jsonl
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
        print('User: user10, Scenario: 2, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + 'I need wireless earbuds with GPS for running, but my budget is tight, show me the cheapest one that actually has GPS and directly add it to my cart')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("search_product", query='wireless earbuds', category='wearables', sort_by='price', limit=10)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod41')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod57')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod31')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("get_product_details", product_id='prod14')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_product_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_product_details: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod41', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'Let me check my cart')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("view_cart", )
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: view_cart returned success:false")
    except Exception as e:
        print(f"ERROR in view_cart: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + "I'm ready to checkout")
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("checkout", )
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: checkout returned success:false")
    except Exception as e:
        print(f"ERROR in checkout: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + 'I actually find something better. Help me cancel this order')
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
    try:
        result = invoke_tool("cancel_order", order_id='order1', reason='Changed my mind')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: cancel_order returned success:false")
    except Exception as e:
        print(f"ERROR in cancel_order: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
