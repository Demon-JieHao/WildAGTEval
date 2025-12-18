#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user2_SmartRoutines_scenario9_smart_security_night.jsonl
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
        print('User: user2, Scenario: 9, Type: default')

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Turn 1: User query
    print("\nUser: " + "I'd like the Garage Door Opener locked")
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
        result = invoke_tool("lock_status", endpoints=['16'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_status returned success:false")
    except Exception as e:
        print(f"ERROR in lock_status: {e}")
        return False
    try:
        result = invoke_tool("lock_lock", endpoints=['16'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: lock_lock returned success:false")
    except Exception as e:
        print(f"ERROR in lock_lock: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'Close the blinds in the Dining Room Blinds')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("get_device_details", endpoint='5')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_device_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_device_details: {e}")
        return False
    try:
        result = invoke_tool("open_close", endpoints=['5'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: open_close returned success:false")
    except Exception as e:
        print(f"ERROR in open_close: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + 'Would you set the Thermostat to 32 degrees?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
    try:
        result = invoke_tool("get_device_details", endpoint='5A')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_device_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_device_details: {e}")
        return False
    try:
        result = invoke_tool("temperature_set", endpoints=['5A'], temperature=32)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: temperature_set returned success:false")
    except Exception as e:
        print(f"ERROR in temperature_set: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + 'Set the Office Light brightness to 20%')
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
    try:
        result = invoke_tool("get_device_details", endpoint='14')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_device_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_device_details: {e}")
        return False
    try:
        result = invoke_tool("power_on", endpoints=['14'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: power_on returned success:false")
    except Exception as e:
        print(f"ERROR in power_on: {e}")
        return False
    try:
        result = invoke_tool("brightness_adjust", endpoints=['14'], brightness=20)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: brightness_adjust returned success:false")
    except Exception as e:
        print(f"ERROR in brightness_adjust: {e}")
        return False
    # Turn 5: User query
    print("\nUser: " + "What's the current weather in San Francisco?")
    print("Agent: I'll handle that for you.")

    # API calls for turn 5
    try:
        result = invoke_tool("weather_current", location='san_francisco')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: weather_current returned success:false")
    except Exception as e:
        print(f"ERROR in weather_current: {e}")
        return False
    # Turn 6: User query
    print("\nUser: " + 'Do we have any weather alerts in Vancouver?')
    print("Agent: I'll handle that for you.")

    # API calls for turn 6
    try:
        result = invoke_tool("weather_alerts", location='vancouver')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: weather_alerts returned success:false")
    except Exception as e:
        print(f"ERROR in weather_alerts: {e}")
        return False
    # Turn 7: User query
    print("\nUser: " + 'Change my notification preferences to enable do not disturb and disable notification sounds')
    print("Agent: I'll handle that for you.")

    # API calls for turn 7
    try:
        result = invoke_tool("set_notification_preferences", do_not_disturb=True, notification_sounds=False)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: set_notification_preferences returned success:false")
    except Exception as e:
        print(f"ERROR in set_notification_preferences: {e}")
        return False
    # Turn 8: User query
    print("\nUser: " + 'Send low alert: Emergency Contacts Active')
    print("Agent: I'll handle that for you.")

    # API calls for turn 8
    try:
        result = invoke_tool("create_notification", title='Emergency Contacts Active', message='Emergency calls will bypass do-not-disturb mode', source='CulinaryControlEnv', type='security', priority='low')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: create_notification returned success:false")
    except Exception as e:
        print(f"ERROR in create_notification: {e}")
        return False
    # Turn 9: User query
    print("\nUser: " + 'Create recurring alarm - Morning wake-up on weekdays 07:30')
    print("Agent: I'll handle that for you.")

    # API calls for turn 9
    try:
        result = invoke_tool("create_alarm", title='Morning wake-up', time='07:30:00', days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday'], sound='gentle')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: create_alarm returned success:false")
    except Exception as e:
        print(f"ERROR in create_alarm: {e}")
        return False
    # Turn 10: User query
    print("\nUser: " + 'Display enabled alarms')
    print("Agent: I'll handle that for you.")

    # API calls for turn 10
    try:
        result = invoke_tool("get_alarms", active_only=True)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_alarms returned success:false")
    except Exception as e:
        print(f"ERROR in get_alarms: {e}")
        return False
    # Turn 11: User query
    print("\nUser: " + 'I want the Master Bedroom Lamp at 30% brightness')
    print("Agent: I'll handle that for you.")

    # API calls for turn 11
    try:
        result = invoke_tool("get_device_details", endpoint='9')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_device_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_device_details: {e}")
        return False
    try:
        result = invoke_tool("power_on", endpoints=['9'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: power_on returned success:false")
    except Exception as e:
        print(f"ERROR in power_on: {e}")
        return False
    try:
        result = invoke_tool("brightness_adjust", endpoints=['9'], brightness=30)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: brightness_adjust returned success:false")
    except Exception as e:
        print(f"ERROR in brightness_adjust: {e}")
        return False
    # Turn 12: User query
    print("\nUser: " + 'Generate notification about weather security alert')
    print("Agent: I'll handle that for you.")

    # API calls for turn 12
    try:
        result = invoke_tool("create_notification", title='Weather Security Alert', message='Enhanced security mode activated due to weather conditions', source='CulinaryControlEnv', type='security', priority='normal')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: create_notification returned success:false")
    except Exception as e:
        print(f"ERROR in create_notification: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
