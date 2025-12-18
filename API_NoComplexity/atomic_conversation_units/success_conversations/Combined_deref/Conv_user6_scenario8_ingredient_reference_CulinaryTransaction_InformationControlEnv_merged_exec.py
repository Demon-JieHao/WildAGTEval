#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user6_scenario8_ingredient_reference_CulinaryTransaction_InformationControlEnv_merged.jsonl
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
    """Execute combined conversation for user6 - Unknown scenario"""
    try:
        # Initialize and register all environments with user user6
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
        smart_home_env.set_current_user('user6')
        info_control_env.set_current_user('user6')
        media_control_env.set_current_user('user6')
        time_notification_env.set_current_user('user6')
        communication_env.set_current_user('user6')
        culinary_env.set_current_user('user6')
        transaction_env.set_current_user('user6')
        
        print('Executing combined conversation script: Unknown')
        print('User: user6, Scenario: 8, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + 'Find top 10 Italian food recipes')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("search_recipes", sort_by='rating', cuisine='Italian', limit=10)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_recipes returned success:false")
    except Exception as e:
        print(f"ERROR in search_recipes: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'Help me purchase all the ingredients for Margherita Pizza')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("search_product", query='tomatoes', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='basil', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='oregano', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='mozzarella', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='vinegar', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='garlic', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='onions', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod135', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod148', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod145', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod144', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod131', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod125', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod126', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + "I will travel to berlin. What's the weather going to be like in Berlin?")
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("weather_forecast", location='berlin', days=7)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: weather_forecast returned success:false")
    except Exception as e:
        print(f"ERROR in weather_forecast: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + 'Ah I just found out I have to my travel today. Tell me the current weather there.')
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
    try:
        result = invoke_tool("weather_current", location='berlin')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: weather_current returned success:false")
    except Exception as e:
        print(f"ERROR in weather_current: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
