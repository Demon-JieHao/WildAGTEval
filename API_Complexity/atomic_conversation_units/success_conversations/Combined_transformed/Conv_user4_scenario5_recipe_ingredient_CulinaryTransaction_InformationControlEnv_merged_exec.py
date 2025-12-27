#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user4_scenario5_recipe_ingredient_CulinaryTransaction_InformationControlEnv_merged.jsonl
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
    """Execute combined conversation for user4 - Unknown scenario"""
    try:
        # Initialize and register all environments with user user4
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
        smart_home_env.set_current_user('user4')
        info_control_env.set_current_user('user4')
        media_control_env.set_current_user('user4')
        time_notification_env.set_current_user('user4')
        communication_env.set_current_user('user4')
        culinary_env.set_current_user('user4')
        transaction_env.set_current_user('user4')
        
        print('Executing combined conversation script: Unknown')
        print('User: user4, Scenario: 5, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + 'I need the Mexican recipe with highest rating and buy all the ingredients')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("search_recipes", cuisine='Mexican', limit=5, sort_by='rating')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_recipes returned success:false")
    except Exception as e:
        print(f"ERROR in search_recipes: {e}")
        return False
    try:
        result = invoke_tool("get_recipe_details", recipe_id='recipe16')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_recipe_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_recipe_details: {e}")
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
        result = invoke_tool("search_product", query='avocado', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='cilantro', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='lime', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='butter', limit=1)
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
        result = invoke_tool("search_product", query='vinegar', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='herbs', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
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
    try:
        result = invoke_tool("add_to_cart", product_id='prod153', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod142', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod137', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod127', quantity=1)
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
        result = invoke_tool("add_to_cart", product_id='prod131', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod128', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'I will travel to london. Could you check the 7-day forecast for London?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("weather_forecast", location='london', days=7)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: weather_forecast returned success:false")
    except Exception as e:
        print(f"ERROR in weather_forecast: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + 'Ah I just found out I have to my travel today. Tell me the current weather there.')
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("weather_current", location='london')
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
