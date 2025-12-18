#!/usr/bin/env python3
"""
Demo script to test color_set with SYSTEM_FAILURE_ERROR uncertainty.
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
    """Execute color_set demo with system_failure_error uncertainty testing"""
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
        print('Demo: color_set SYSTEM_FAILURE_ERROR uncertainty')
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

    # Test 2: Color setting with SYSTEM_FAILURE_ERROR uncertainty
    print("\n" + "="*60)
    print("DEMO 2: Color Setting WITH Smart Home Hub Infrastructure Failure")
    print("="*60)
    
    print("\nUser: Let me try changing the lights to blue now.")
    print("Agent: I'll change your lights to blue.")
    
    print(f"\nExecuting: color_set(endpoints={test_endpoints}, color='#0000FF') WITH SYSTEM_FAILURE_ERROR uncertainty enabled")
    try:
        with enable_uncertainty('ENABLE__SYSTEM_FAILURE_ERROR__COLOR_SET'):
            result = invoke_tool("color_set", 
                               endpoints=test_endpoints,
                               color="#0000FF")
        
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

    # Test 3: Demonstrate ideal LLM error handling
    print("\n" + "="*60)
    print("DEMO 3: Ideal LLM Smart Home Error Communication Pattern")
    print("="*60)
    
    print("\nUser: My lights didn't change color. What's wrong?")
    print("Agent: Let me check the smart home system status.")
    
    # Simulate getting the error again
    print("\n🤖 Agent receives complex smart home infrastructure error:")
    try:
        with enable_uncertainty('ENABLE__SYSTEM_FAILURE_ERROR__COLOR_SET'):
            result = invoke_tool("color_set", 
                               endpoints=test_endpoints,
                               color="#00FF00")
        
        result_dict = json.loads(result)
        
        if not result_dict.get('success'):
            print(f"📡 Raw Technical Error:")
            print(f"   Error: {result_dict.get('error')}")
            print(f"   Message: {result_dict.get('message')}")
            
            print(f"\n🎯 Ideal Agent Response Pattern:")
            print(f"   [Problem Identification]")
            print(f"   'I'm unable to change your light colors right now because your smart home hub has crashed due to network coordination problems.'")
            
            print(f"\n   [User-Friendly Explanation]")
            print(f"   'This is a critical system error that has caused the smart home hub to stop working.'")
            
            print(f"\n   [Status Confirmation]")
            print(f"   'Your color change command was not processed and your lights remain at their current color.'")
            
            print(f"\n   [Manual Alternative Solutions]")
            print(f"   'Your lights can still be controlled manually using their physical switches.'")
            
            print(f"\n   [Technical Details Filtered]")
            print(f"   'You may need to restart your smart home hub or contact support for assistance.'")
            
    except Exception as e:
        print(f"ERROR in demonstration: {e}")

    # Test 4: Technical terminology analysis
    print("\n" + "="*60)
    print("DEMO 4: Smart Home Technical Terminology Translation Requirements")
    print("="*60)
    
    print("🔍 Technical terms LLM should understand and translate:")
    
    technical_terms = [
        ("ZIGBEE_MESH_COORDINATOR_PANIC", "smart home hub network coordination crash"),
        ("ZigBee coordinator firmware kernel panic", "smart home hub system crash"),
        ("mesh routing table overflow", "network capacity overload"),
        ("coordinator reset failed with EEPROM corruption", "hub memory corruption preventing restart"),
        ("Z-Wave controller fatal exception", "wireless controller system crash"),
        ("inclusion_table corruption", "device connection database corruption"),
        ("network management task", "device coordination system"),
        ("embedded OS kernel panic", "smart home hub operating system crash")
    ]
    
    print(f"\n📋 Translation Requirements:")
    for technical, friendly in technical_terms:
        print(f"  '{technical}' → '{friendly}'")
    
    print(f"\n🧠 LLM Understanding Requirements:")
    print(f"1. Parse complex smart home infrastructure error messages")
    print(f"2. Identify root cause: Hub system failure, not user or light device problem")
    print(f"3. Translate ZigBee/Z-Wave terminology to user-friendly language")
    print(f"4. Provide clear explanation + status confirmation + manual alternatives")
    print(f"5. Filter out unnecessary technical infrastructure details")

    # Test 5: Error message complexity analysis
    print("\n" + "="*60)
    print("DEMO 5: Smart Home Error Message Complexity Analysis")
    print("="*60)
    
    print("💡 Testing LLM's ability to handle complex smart home infrastructure errors:")
    
    # Show the full error structure
    try:
        with enable_uncertainty('ENABLE__SYSTEM_FAILURE_ERROR__COLOR_SET'):
            result = invoke_tool("color_set", 
                               endpoints=test_endpoints,
                               color="#FFFF00")
        
        result_dict = json.loads(result)
        
        if not result_dict.get('success'):
            print(f"\n📊 Full Error Structure Analysis:")
            print(f"✓ Error Code: {result_dict.get('error')}")
            print(f"✓ Detailed Message: {len(result_dict.get('message', ''))} characters")
            print(f"✓ Service: {result_dict.get('service')}")
            print(f"✓ Hub ID: {result_dict.get('hub_id')}")
            print(f"✓ Correlation ID: {result_dict.get('correlation_id')}")
            print(f"✓ Trace ID: {result_dict.get('trace_id')}")
            print(f"✓ Technical Details: {len(result_dict.get('technical_details', {}))} fields")
            
            print(f"\n🎯 LLM Evaluation Criteria:")
            print(f"- Can parse JSON structure correctly")
            print(f"- Identifies key smart home infrastructure failure information")
            print(f"- Ignores correlation IDs and trace details for user communication")
            print(f"- Focuses on user-relevant information (light control status, manual alternatives)")
            print(f"- Provides actionable guidance without technical complexity")
            
    except Exception as e:
        print(f"ERROR in complexity analysis: {e}")

    # Test 6: LLM response quality evaluation
    print("\n" + "="*60)
    print("DEMO 6: LLM Response Quality Evaluation Framework")
    print("="*60)
    
    print("🎯 LLM Evaluation Dimensions:")
    
    print(f"\n📝 Scoring Framework (5-point scale):")
    print(f"✅ Excellent (5/5): Perfect Smart Home Infrastructure Translation & User Communication")
    print(f"   - Accurately parses complex smart home infrastructure error")
    print(f"   - Translates all technical terms to user-friendly language")
    print(f"   - Provides clear problem explanation + status confirmation + manual alternatives")
    print(f"   - Appropriately filters technical infrastructure details")
    print(f"")
    print(f"⚠️ Good (4/5): Basic Translation & Explanation")
    print(f"   - Understands main smart home error content and explains situation") 
    print(f"   - Translates most technical terms appropriately")
    print(f"   - Provides basic situation explanation to user")
    print(f"   - Some technical terms may leak through")
    print(f"")
    print(f"📊 Average (3/5): Partial Understanding")
    print(f"   - Recognizes smart home error occurred but lacks detailed analysis") 
    print(f"   - Basic 'system failed' level explanation")
    print(f"   - Limited technical cause explanation")
    print(f"")
    print(f"❌ Below Average (2/5): Poor Error Comprehension")
    print(f"   - Passes complex smart home error message directly to user")
    print(f"   - Fails to translate technical terminology")
    print(f"   - Increases user confusion about smart home system")
    print(f"")
    print(f"🚫 Poor (1/5): Response Failure")
    print(f"   - Ignores or misinterprets smart home error situation")
    print(f"   - Provides unhelpful response to user")
    print(f"   - May cause user concern about smart home security or reliability")

    print('\n' + '='*70)
    print('🎯 color_set SYSTEM_FAILURE_ERROR uncertainty demo completed')
    print('='*70)
    print('\n📋 Summary for LLM Evaluation:')
    print('- Function fails with complex smart home infrastructure error when uncertainty is enabled')
    print('- Error contains technical ZigBee/Z-Wave terminology requiring translation')
    print('- Key challenge: Parse smart home infrastructure details and communicate clearly to user')
    print('- LLM should provide user-friendly explanation + status confirmation + manual alternatives')
    print('- Success measured by smart home communication clarity and user confidence in system')
    print('- Error message complexity tests LLM ability to filter smart home infrastructure information')
    print('- Evaluation focuses on user experience and smart home error communication skills')
    
    return True


if __name__ == "__main__":
    success = main()
    print(f"\n🎯 Demo Result: {'SUCCESS' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
