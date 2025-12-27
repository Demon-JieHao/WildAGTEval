#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user9_scenario1_planning_CulinaryControlEnv_RestaurantDelivery_merged.jsonl
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
        print('User: user9, Scenario: 1, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + "Help me create 'Home Chef Weekly Plan' - a one-week meal plan starting 2025-07-17 for breakfast, lunch, dinner and snack")
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("create_meal_plan", name='Home Chef Weekly Plan', start_date='2025-07-17', end_date='2025-07-23', meals_per_day=['breakfast', 'lunch', 'dinner', 'snack'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: create_meal_plan returned success:false")
    except Exception as e:
        print(f"ERROR in create_meal_plan: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'I want 3 personalized dinner suggestions options')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("get_meal_suggestions", meal_type='dinner', count=3)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_meal_suggestions returned success:false")
    except Exception as e:
        print(f"ERROR in get_meal_suggestions: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + 'I want Beef Ramen for dinner on 2025-07-22')
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("schedule_meal", plan_id='plan24', recipe_id='recipe38', day='2025-07-22', meal_type='dinner')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: schedule_meal returned success:false")
    except Exception as e:
        print(f"ERROR in schedule_meal: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + "I'm looking for 4 midday meal options that fit my preferences")
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
    try:
        result = invoke_tool("get_meal_suggestions", meal_type='lunch', count=4)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_meal_suggestions returned success:false")
    except Exception as e:
        print(f"ERROR in get_meal_suggestions: {e}")
        return False
    # Turn 5: User query
    print("\nUser: " + 'I want Chocolate Chip Cookies for lunch on 2025-07-23')
    print("Agent: I'll handle that for you.")

    # API calls for turn 5
    try:
        result = invoke_tool("schedule_meal", plan_id='plan24', recipe_id='recipe36', day='2025-07-23', meal_type='lunch')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: schedule_meal returned success:false")
    except Exception as e:
        print(f"ERROR in schedule_meal: {e}")
        return False
    # Turn 6: User query
    print("\nUser: " + 'I want to find an Italian restaurant with the best rating')
    print("Agent: I'll handle that for you.")

    # API calls for turn 6
    try:
        result = invoke_tool("search_restaurants", cuisine_type='Italian', sort_by='rating', limit=5)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_restaurants returned success:false")
    except Exception as e:
        print(f"ERROR in search_restaurants: {e}")
        return False
    # Turn 7: User query
    print("\nUser: " + 'What food options does it have?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 7
    try:
        result = invoke_tool("get_restaurant_menu", restaurant_id='rest24')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_restaurant_menu returned success:false")
    except Exception as e:
        print(f"ERROR in get_restaurant_menu: {e}")
        return False
    # Turn 8: User query
    print("\nUser: " + 'I want to order Chicken Parmigiana for delivery from Roma Restaurant to my address at 4094 Oak Ave, Chicago, IL 60687')
    print("Agent: I'll handle that for you.")

    # API calls for turn 8
    try:
        result = invoke_tool("place_delivery_order", restaurant_id='rest24', items=[{'item_id': 'item5', 'quantity': 1}], delivery_address={'street': '4094 Oak Ave', 'city': 'Chicago', 'state': 'IL', 'zip': '60687'})
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: place_delivery_order returned success:false")
    except Exception as e:
        print(f"ERROR in place_delivery_order: {e}")
        return False
    # Turn 9: User query
    print("\nUser: " + 'Where is my delivery right now?')
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
