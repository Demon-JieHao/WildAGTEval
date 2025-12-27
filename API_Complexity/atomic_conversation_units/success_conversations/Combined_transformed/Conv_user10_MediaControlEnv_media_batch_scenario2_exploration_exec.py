#!/usr/bin/env python3
"""
Automatically generated script from combined conversation JSONL file.
This script reproduces the API calls made during the conversation.
Source: Conv_user10_MediaControlEnv_media_batch_scenario2_exploration.jsonl
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
    print("\nUser: " + 'Please play Crazy Love on my Office Speaker')
    print("Agent: I'll handle that for you.")

    # API calls for turn 1
    try:
        result = invoke_tool("search_media", query='Crazy Love', media_type='song', limit=3)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_media returned success:false")
    except Exception as e:
        print(f"ERROR in search_media: {e}")
        return False
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
        result = invoke_tool("get_device_details", endpoint='28')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_device_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_device_details: {e}")
        return False
    try:
        result = invoke_tool("play", endpoints=['28'], media_id='song:song140')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: play returned success:false")
    except Exception as e:
        print(f"ERROR in play: {e}")
        return False
    # Turn 2: User query
    print("\nUser: " + 'Tell me the details of what we just played')
    print("Agent: I'll handle that for you.")

    # API calls for turn 2
    try:
        result = invoke_tool("get_media_details", media_id='song140')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_media_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_media_details: {e}")
        return False
    # Turn 3: User query
    print("\nUser: " + 'Move back 15 seconds on Office Speaker')
    print("Agent: I'll handle that for you.")

    # API calls for turn 3
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
        result = invoke_tool("get_playback_status", endpoints=['28'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_playback_status returned success:false")
    except Exception as e:
        print(f"ERROR in get_playback_status: {e}")
        return False
    try:
        result = invoke_tool("rewind", endpoints=['28'], seconds=15)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: rewind returned success:false")
    except Exception as e:
        print(f"ERROR in rewind: {e}")
        return False
    # Turn 4: User query
    print("\nUser: " + 'Turn off playback on the Office Speaker')
    print("Agent: I'll handle that for you.")

    # API calls for turn 4
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
        result = invoke_tool("get_playback_status", endpoints=['28'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_playback_status returned success:false")
    except Exception as e:
        print(f"ERROR in get_playback_status: {e}")
        return False
    try:
        result = invoke_tool("stop", endpoints=['28'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: stop returned success:false")
    except Exception as e:
        print(f"ERROR in stop: {e}")
        return False
    # Turn 5: User query
    print("\nUser: " + 'Begin playing Ocean Moon by U2 on Living Room Speaker')
    print("Agent: I'll handle that for you.")

    # API calls for turn 5
    try:
        result = invoke_tool("search_media", query='Ocean Moon', media_type='song', limit=3)
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: search_media returned success:false")
    except Exception as e:
        print(f"ERROR in search_media: {e}")
        return False
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
        result = invoke_tool("get_device_details", endpoint='18')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: get_device_details returned success:false")
    except Exception as e:
        print(f"ERROR in get_device_details: {e}")
        return False
    try:
        result = invoke_tool("power_on", endpoints=['18'])
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: power_on returned success:false")
    except Exception as e:
        print(f"ERROR in power_on: {e}")
        return False
    try:
        result = invoke_tool("play", endpoints=['18'], media_id='song:song177')
        print(f"Result: {result}")
        # Check for API failures
        if isinstance(result, dict) and result.get('success') == False:
            print(f"WARNING: play returned success:false")
    except Exception as e:
        print(f"ERROR in play: {e}")
        return False

    print('\n' + '='*80)
    print('Combined conversation execution completed successfully')
    print('='*80)
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
