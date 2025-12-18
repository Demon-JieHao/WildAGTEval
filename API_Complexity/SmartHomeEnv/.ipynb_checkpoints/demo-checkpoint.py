#!/usr/bin/env python
"""
Demo script for the SmartHomeEnv
"""

import json
import argparse
from SmartHomeEnv import SmartHomeEnv


def print_json(data):
    """Print JSON data in a readable format"""
    print(json.dumps(json.loads(data), indent=2))


def run_demo():
    """Run a demonstration of the SmartHomeEnv"""
    print("\n===== Smart Home Environment Demo =====\n")
    
    # Initialize the environment
    env = SmartHomeEnv()
    
    # Print available tools
    print("Available Tools:")
    for tool_info in env.get_tool_info():
        print(f"- {tool_info['function']['name']}: {tool_info['function']['description']}")
    
    print("\n===== Demo Requests =====\n")
    
    # Demo 1: Get user inventory
    print("Request: 'Get inventory for the current user'")
    result = env.invoke_tool("get_user_inventory")
    print_json(result)
    print()
    
    # Demo 2: Switch to another user
    print("Request: 'Switch to user2'")
    env.set_current_user("user2")
    print(f"Current user: {env.get_current_user()['name']}")
    print()
    
    # Demo 3: Get inventory for the new user
    print("Request: 'Get inventory for the new current user'")
    result = env.invoke_tool("get_user_inventory")
    print_json(result)
    print()
    
    # Switch back to user1
    env.set_current_user("user1")
    print(f"Switched back to user: {env.get_current_user()['name']}")
    print()
    
    # Demo 4: Turn on living room light
    print("Request: 'Turn on the living room light'")
    result = env.invoke_tool("power_on", endpoints=["1"])
    print_json(result)
    print()
    
    # Demo 5: Check device state after turning on
    print("Request: 'Get device details for the living room light'")
    result = env.invoke_tool("get_device_details", endpoint="1")
    print_json(result)
    print()
    
    # Demo 6: Set bedroom lamp to blue
    print("Request: 'Set bedroom lamp to blue'")
    result = env.invoke_tool("color_set", endpoints=["3"], color="blue")
    print_json(result)
    print()
    
    # Demo 7: Check device state after setting color
    print("Request: 'Get device details for the bedroom lamp'")
    result = env.invoke_tool("get_device_details", endpoint="3")
    print_json(result)
    print()
    
    # Demo 8: Turn off all lights
    print("Request: 'Turn off all lights'")
    result = env.invoke_tool("get_group_devices", group_name="All Lights")
    devices_data = json.loads(result)
    if devices_data["success"]:
        endpoints = [device["endpoint"] for device in devices_data["devices"]]
        result = env.invoke_tool("power_off", endpoints=endpoints)
        print_json(result)
    print()
    
    # Demo 9: Check device states after turning off
    print("Request: 'Get inventory to check device states'")
    result = env.invoke_tool("get_user_inventory")
    print_json(result)
    print()


def run_interactive():
    """Run an interactive session with the SmartHomeEnv"""
    env = SmartHomeEnv()
    
    print("\n===== Smart Home Environment Interactive Mode =====")
    print("Type 'exit' to quit, 'help' for commands, 'tools' for available tools.")
    
    while True:
        try:
            user_input = input("\n> ")
            if user_input.lower() == "exit":
                break
            elif user_input.lower() == "help":
                print("\nAvailable commands:")
                print("  tools - List all available tools")
                print("  rules - Show the rules for the environment")
                print("  wiki - Show the wiki documentation")
                print("  users - List all users")
                print("  user - Show the current user")
                print("  switch <user_id> - Switch to another user")
                print("  inventory - Show the current user's inventory")
                print("  exit - Exit interactive mode")
                print("  help - Show this help message")
                print("  <tool_name> <param1>=<value1> <param2>=<value2> ... - Invoke a tool")
            elif user_input.lower() == "tools":
                print("\nAvailable tools:")
                for tool_info in env.get_tool_info():
                    print(f"- {tool_info['function']['name']}: {tool_info['function']['description']}")
                    if "parameters" in tool_info["function"] and "properties" in tool_info["function"]["parameters"]:
                        for param_name, param_info in tool_info["function"]["parameters"]["properties"].items():
                            print(f"  - {param_name}: {param_info.get('description', '')}")
            elif user_input.lower() == "rules":
                print("\nRules:")
                for i, rule in enumerate(env.get_rules(), 1):
                    print(f"{i}. {rule}")
            elif user_input.lower() == "wiki":
                print("\nWiki:")
                print(env.get_wiki())
            elif user_input.lower() == "users":
                print("\nUsers:")
                for user in env.get_all_users():
                    print(f"- {user['user_id']}: {user['name']} (Home: {user['home_id']})")
            elif user_input.lower() == "user":
                user = env.get_current_user()
                print(f"\nCurrent user: {user['name']} (ID: {user['user_id']}, Home: {user['home_id']})")
            elif user_input.lower().startswith("switch "):
                user_id = user_input.split(" ", 1)[1].strip()
                if env.set_current_user(user_id):
                    user = env.get_current_user()
                    print(f"\nSwitched to user: {user['name']} (ID: {user['user_id']}, Home: {user['home_id']})")
                else:
                    print(f"\nError: User with ID '{user_id}' not found")
            elif user_input.lower() == "inventory":
                result = env.invoke_tool("get_user_inventory")
                print_json(result)
            else:
                # Parse the input as a tool invocation
                parts = user_input.split()
                if not parts:
                    continue
                
                tool_name = parts[0]
                params = {}
                
                for part in parts[1:]:
                    if "=" in part:
                        key, value = part.split("=", 1)
                        # Try to convert to int or list if possible
                        if value.isdigit():
                            params[key] = int(value)
                        elif value.startswith("[") and value.endswith("]"):
                            # Parse as a list
                            items = value[1:-1].split(",")
                            params[key] = [item.strip() for item in items]
                        else:
                            params[key] = value
                
                try:
                    result = env.invoke_tool(tool_name, **params)
                    print_json(result)
                except Exception as e:
                    print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demo for the SmartHomeEnv")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive()
    else:
        run_demo()
