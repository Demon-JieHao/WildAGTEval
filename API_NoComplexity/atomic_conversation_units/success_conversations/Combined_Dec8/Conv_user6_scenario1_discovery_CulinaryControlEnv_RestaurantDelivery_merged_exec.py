#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user6_scenario1_discovery_CulinaryControlEnv_RestaurantDelivery_merged.jsonl
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
        print('User: user6, Scenario: 1, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + 'Can you suggest top 10 American dishes?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("search_recipes", sort_by='rating', cuisine='American', limit=10)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_recipes returned success:false")
    except Exception as e:
        print(f"ERROR in search_recipes: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + "I'm interested in the 3rd and 4th ones, show me the details")
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("get_recipe_details", recipe_id='recipe33')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_recipe_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_recipe_details: {e}")
        return False
    try:
        result = invoke_tool("get_recipe_details", recipe_id='recipe36')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_recipe_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_recipe_details: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + 'Great choices, add them to my collection')
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("save_favorite_recipe", recipe_id='recipe33')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: save_favorite_recipe returned success:false")
    except Exception as e:
        print(f"ERROR in save_favorite_recipe: {e}")
        return False
    try:
        result = invoke_tool("save_favorite_recipe", recipe_id='recipe36')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: save_favorite_recipe returned success:false")
    except Exception as e:
        print(f"ERROR in save_favorite_recipe: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + 'Find me the best Italian restaurant near me')
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
    try:
        result = invoke_tool("search_restaurants", cuisine_type='Italian', sort_by='rating', limit=5)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_restaurants returned success:false")
    except Exception as e:
        print(f"ERROR in search_restaurants: {e}")
        return False
    # Turn 5: User query
    print("\nUser: " + 'What does the restaurant have on their menu?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 5
    try:
        result = invoke_tool("get_restaurant_menu", restaurant_id='rest24')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_restaurant_menu returned success:false")
    except Exception as e:
        print(f"ERROR in get_restaurant_menu: {e}")
        return False
    # Turn 6: User query
    print("\nUser: " + "I'd like to order Spaghetti Carbonara from Roma Restaurant and deliver it to 3903 Broadway, Dallas, TX 75254")
    print("Agent: I'll handle that for you.")

    # API calls for turn 6
    try:
        result = invoke_tool("place_delivery_order", restaurant_id='rest24', items=[{'item_id': 'item6', 'quantity': 1}], delivery_address={'street': '3903 Broadway', 'city': 'Dallas', 'state': 'TX', 'zip': '75254'})
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: place_delivery_order returned success:false")
    except Exception as e:
        print(f"ERROR in place_delivery_order: {e}")
        return False
    # Turn 7: User query
    print("\nUser: " + 'Where is my delivery right now?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 7
    try:
        result = invoke_tool("track_delivery_order", order_id='dorder1')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: track_delivery_order returned success:false")
    except Exception as e:
        print(f"ERROR in track_delivery_order: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
