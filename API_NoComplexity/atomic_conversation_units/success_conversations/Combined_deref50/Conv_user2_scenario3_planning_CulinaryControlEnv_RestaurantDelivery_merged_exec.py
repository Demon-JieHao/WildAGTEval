#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user2_scenario3_planning_CulinaryControlEnv_RestaurantDelivery_merged.jsonl
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
    """Execute combined conversation for user2 - Unknown scenario"""
    try:
        # Initialize and register all environments with user user2
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
        smart_home_env.set_current_user('user2')
        info_control_env.set_current_user('user2')
        media_control_env.set_current_user('user2')
        time_notification_env.set_current_user('user2')
        communication_env.set_current_user('user2')
        culinary_env.set_current_user('user2')
        transaction_env.set_current_user('user2')
        
        print('Executing combined conversation script: Unknown')
        print('User: user2, Scenario: 3, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + "I want to plan 'Weekend Special Menu' for 7 days starting 2025-07-17 with breakfast and dinner")
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("create_meal_plan", name='Weekend Special Menu', start_date='2025-07-17', end_date='2025-07-23', meals_per_day=['breakfast', 'dinner'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: create_meal_plan returned success:false")
    except Exception as e:
        print(f"ERROR in create_meal_plan: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'I need 6 evening meal options for my meal plan')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("get_meal_suggestions", meal_type='dinner', count=6)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_meal_suggestions returned success:false")
    except Exception as e:
        print(f"ERROR in get_meal_suggestions: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + 'Put Greek Salad in my Friday dinner slot')
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("schedule_meal", plan_id='plan24', recipe_id='recipe32', day='2025-07-18', meal_type='dinner')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: schedule_meal returned success:false")
    except Exception as e:
        print(f"ERROR in schedule_meal: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + "I'm looking for 2 breakfast suggestions that fit my preferences")
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
    try:
        result = invoke_tool("get_meal_suggestions", meal_type='breakfast', count=2)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_meal_suggestions returned success:false")
    except Exception as e:
        print(f"ERROR in get_meal_suggestions: {e}")
        return False
    # Turn 5: User query
    print("\nUser: " + 'Schedule Mango Sticky Rice for Sunday breakfast')
    print("Agent: I'll handle that for you.")

    # API calls for turn 5
    try:
        result = invoke_tool("schedule_meal", plan_id='plan24', recipe_id='recipe7', day='2025-07-20', meal_type='breakfast')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: schedule_meal returned success:false")
    except Exception as e:
        print(f"ERROR in schedule_meal: {e}")
        return False
    # Turn 6: User query
    print("\nUser: " + 'I want to find an French restaurant with the best rating')
    print("Agent: I'll handle that for you.")

    # API calls for turn 6
    try:
        result = invoke_tool("search_restaurants", cuisine_type='French', sort_by='rating', limit=5)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_restaurants returned success:false")
    except Exception as e:
        print(f"ERROR in search_restaurants: {e}")
        return False
    # Turn 7: User query
    print("\nUser: " + "I'd like to see the menu from Petit France")
    print("Agent: I'll handle that for you.")

    # API calls for turn 7
    try:
        result = invoke_tool("get_restaurant_menu", restaurant_id='rest3')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_restaurant_menu returned success:false")
    except Exception as e:
        print(f"ERROR in get_restaurant_menu: {e}")
        return False
    # Turn 8: User query
    print("\nUser: " + 'I want to order Pan-Seared Salmon for delivery from Petit France to my address at 2091 Broadway, Miami, FL 33124')
    print("Agent: I'll handle that for you.")

    # API calls for turn 8
    try:
        result = invoke_tool("place_delivery_order", restaurant_id='rest3', items=[{'item_id': 'item4', 'quantity': 1}], delivery_address={'street': '2091 Broadway', 'city': 'Miami', 'state': 'FL', 'zip': '33124'})
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: place_delivery_order returned success:false")
    except Exception as e:
        print(f"ERROR in place_delivery_order: {e}")
        return False
    # Turn 9: User query
    print("\nUser: " + 'Can you track my delivery order?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 9
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
