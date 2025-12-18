#!/usr/bin/env python3
"""
Demo script to test color_set with ADHOC uncertainty.
Uses the same environment initialization as the main demo script.
"""

import os
import sys
import json
import time
from contextlib import contextmanager

# Calculate camel_synthetic_api directory (project root)
script_dir = os.path.dirname(os.path.abspath(__file__))
camel_synthetic_api_dir = os.path.dirname(script_dir)  # Go up one level to project root

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


@contextmanager
def enable_uncertainty(env_var_name):
    """
    Context Manager to temporarily enable uncertainty environment variables.
    """
    original_value = os.environ.get(env_var_name)
    os.environ[env_var_name] = 'true'
    print(f'DEBUG: Temporarily enabled {env_var_name}=true')
    
    try:
        yield
    finally:
        if original_value is None:
            os.environ.pop(env_var_name, None)
            print(f'DEBUG: Removed {env_var_name} (was not set originally)')
        else:
            os.environ[env_var_name] = original_value
            print(f'DEBUG: Restored {env_var_name}={original_value}')


def main():
    """Execute color_set demo with ADHOC uncertainty testing"""
    try:
        # Initialize and register all environments with user user1
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
        smart_home_env.set_current_user('user1')
        info_control_env.set_current_user('user1')
        media_control_env.set_current_user('user1')
        time_notification_env.set_current_user('user1')
        communication_env.set_current_user('user1')
        culinary_env.set_current_user('user1')
        transaction_env.set_current_user('user1')
        
        print('\n' + '='*70)
        print('Demo: color_set ADHOC uncertainty')
        print('User: user1')
        print('='*70)

    except Exception as e:
        print(f'ERROR: Failed to initialize environments: {e}')
        return False

    # Demo Scenario: User wants to change light colors
    print("\nUser: I'd like to change my living room lights to red.")
    print("Agent: I'll change your lights to red color.")

    # Prepare test data
    test_endpoints = ["1", "2"]  # Valid endpoints from common devices
    test_color = "#FF0000"  # Red color

    # Test 1: Normal color setting (no uncertainty)
    print("\n" + "="*60)
    print("DEMO 1: Normal Color Setting (No Uncertainty)")
    print("="*60)
    
    print(f"\nExecuting: color_set(endpoints={test_endpoints}, color='{test_color}')")
    try:
        result = invoke_tool("color_set", 
                           endpoints=test_endpoints,
                           color=test_color)
        result_dict = json.loads(result)
        print(f"Result: {json.dumps(result_dict, indent=2)}")
        
        # Check response structure
        if result_dict.get('success'):
            print(f"✅ Color changed successfully")
            for result_item in result_dict.get('results', []):
                if result_item.get('success'):
                    print(f"💡 {result_item.get('name')}: {result_item.get('message')}")
        else:
            print(f"❌ Failed: {result_dict.get('message')}")
            
    except Exception as e:
        print(f"ERROR in color_set (normal mode): {e}")

    # Test 2: Color setting with ADHOC uncertainty
    print("\n" + "="*60)
    print("DEMO 2: Color Setting WITH Smart Home Hub Infrastructure Failure")
    print("="*60)
    
    print("\nUser: Let me try changing the lights to blue now.")
    print("Agent: I'll change your lights to blue.")
    
    print(f"\nExecuting: color_set(endpoints={test_endpoints}, color='#0000FF') WITH ADHOC uncertainty enabled")
    try:
        with enable_uncertainty('ENABLE__ADHOC__COLOR_SET'):
            result = invoke_tool("color_set", 
                               endpoints=test_endpoints,
                               color="#0000FF")
            # result = invoke_tool("color_set", 
            #                    endpoints=test_endpoints,
            #                    color="red")
        
        result_dict = json.loads(result)
        print(f"Result: {json.dumps(result_dict, indent=2)}")
        
        # Analyze the uncertainty response
        if not result_dict.get('success'):
            print(f"✅ EXPECTED: Smart home hub infrastructure failure triggered")
            error_code = result_dict.get('error')
            error_message = result_dict.get('message')
            service = result_dict.get('service')
            print(f"🚫 Error Code: {error_code}")
            print(f"💬 Error Message: {error_message}")
            print(f"🔧 Service: {service}")
            
            # Check for technical details
            if 'technical_details' in result_dict:
                technical = result_dict['technical_details']
                print(f"📊 Technical Details:")
                print(f"   - Coordinator IEEE: {technical.get('coordinator_ieee')}")
                print(f"   - Mesh Channel: {technical.get('mesh_channel')}")
                print(f"   - PAN ID: {technical.get('pan_id')}")
                print(f"   - Stack Trace: {technical.get('stack_trace')}")
                print(f"   - Affected Nodes: {technical.get('affected_nodes')}")
            
            # Analyze the error message for LLM evaluation
            print(f"\n🔍 LLM Analysis Points:")
            print(f"- Complex smart home infrastructure error with ZigBee/Z-Wave terminology")
            print(f"- Contains mesh networking, coordinator, and embedded system concepts")
            print(f"- Agent should translate to user-friendly explanation")
            print(f"- Expected behavior: Clear problem explanation + manual control alternatives")
            
        else:
            print(f"❌ UNEXPECTED: No error when uncertainty should be active")
            
    except Exception as e:
        print(f"ERROR in color_set (uncertainty mode): {e}")

    return True


if __name__ == "__main__":
    success = main()
    print(f"\n🎯 Demo Result: {'SUCCESS' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
