#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user7_scenario7_ingredient_reference_CulinaryTransaction_InformationControlEnv_merged.jsonl
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
    """Execute combined conversation for user7 - Unknown scenario"""
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
        
        print('Executing combined conversation script: Unknown')
        print('User: user7, Scenario: 7, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + 'Show me top 10 Indian dishes')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("search_recipes", sort_by='rating', cuisine='Indian', limit=10)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_recipes returned success:false")
    except Exception as e:
        print(f"ERROR in search_recipes: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'I need to buy all these ingredients from Chole')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("search_product", query='turmeric', limit=1)
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
        result = invoke_tool("search_product", query='yogurt', limit=1)
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
        result = invoke_tool("search_product", query='canola oil', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='lemon', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("search_product", query='salt', limit=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_product returned success:false")
    except Exception as e:
        print(f"ERROR in search_product: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod158', quantity=1)
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
    try:
        result = invoke_tool("add_to_cart", product_id='prod140', quantity=1)
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
        result = invoke_tool("add_to_cart", product_id='prod168', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod130', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    try:
        result = invoke_tool("add_to_cart", product_id='prod133', quantity=1)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: add_to_cart returned success:false")
    except Exception as e:
        print(f"ERROR in add_to_cart: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + "I will travel to sydney. What's the 5-day weather forecast for Sydney?")
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("weather_forecast", location='sydney', days=5)
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
        result = invoke_tool("weather_current", location='sydney')
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
