#!/usr/bin/env python3
"""
Centralized Multi-Domain API Prompt Generator (SHORT VERSION)

This script dynamically generates a comprehensive prompt using wiki_short.py files by importing:
- API.json (complete API specifications)
- *InstructionShort.py files (domain-specific agent policies from wiki_short.py)
- Example conversation JSON (response format specification)

Usage:
    python generate_centralized_prompt_short.py [--output OUTPUT_FILE] [--format FORMAT]
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime


def load_api_specifications(api_file_path):
    """Load the complete API specifications from API.json"""
    try:
        with open(api_file_path, 'r') as f:
            api_data = json.load(f)
        return api_data
    except Exception as e:
        print(f"Error loading API specifications: {e}")
        return {}


def load_instruction_file(instruction_file_path):
    """Load instruction content from a Python file"""
    try:
        # Read the file and extract the instruction string
        with open(instruction_file_path, 'r') as f:
            content = f.read()
        
        # Extract the instruction string (assuming it's assigned to 'instruction' variable)
        # This is a simple extraction - in production, you might want to use ast parsing
        start_marker = 'instruction="""'
        end_marker = '"""'
        
        start_idx = content.find(start_marker)
        if start_idx == -1:
            print(f"Warning: Could not find instruction content in {instruction_file_path}")
            return ""
            
        start_idx += len(start_marker)
        end_idx = content.find(end_marker, start_idx)
        
        if end_idx == -1:
            print(f"Warning: Could not find end of instruction content in {instruction_file_path}")
            return ""
            
        instruction_content = content[start_idx:end_idx].strip()
        return instruction_content
        
    except Exception as e:
        print(f"Error loading instruction file {instruction_file_path}: {e}")
        return ""


def load_conversation_example(conversation_file_path):
    """Load example conversation from JSONL file"""
    try:
        with open(conversation_file_path, 'r') as f:
            # Read first line of JSONL file
            first_line = f.readline().strip()
            if first_line:
                conversation_data = json.loads(first_line)
                return conversation_data
            else:
                return {}
    except Exception as e:
        print(f"Error loading conversation example: {e}")
        # Return a fallback example
        return {
            "query": "Turn on the living room lights",
            "api_sequence": [
                {
                    "api": "get_user_inventory",
                    "params": {}
                },
                {
                    "api": "power_on",
                    "params": {
                        "endpoints": ["1"]
                    }
                }
            ]
        }


def format_api_reference(api_data):
    """Format API data into a readable reference"""
    api_reference = ""
    
    for env_name, apis in api_data.items():
        api_count = len(apis)
        api_reference += f"\n## {env_name} APIs ({api_count} APIs)\n\n"
        
        # Group APIs by category for better organization
        for api_name, api_spec in sorted(apis.items()):
            func_spec = api_spec.get('function', {})
            description = func_spec.get('description', 'No description available')
            parameters = func_spec.get('parameters', {})
            error_cases = func_spec.get('error_cases', [])
            
            api_reference += f"### {api_name}\n"
            api_reference += f"**Description:** {description}\n\n"
            
            # Parameters
            if parameters.get('properties'):
                api_reference += "**Parameters:**\n"
                required_params = parameters.get('required', [])
                
                for param_name, param_spec in parameters['properties'].items():
                    param_type = param_spec.get('type', 'unknown')
                    param_desc = param_spec.get('description', 'No description')
                    is_required = param_name in required_params
                    required_text = " (Required)" if is_required else " (Optional)"
                    
                    api_reference += f"- `{param_name}` ({param_type}){required_text}: {param_desc}\n"
                
                api_reference += "\n"
            
            # Error cases
            if error_cases:
                api_reference += "**Error Cases:**\n"
                for error_case in error_cases:
                    api_reference += f"- {error_case}\n"
                api_reference += "\n"
            
            api_reference += "---\n\n"
    
    return api_reference


def format_conversation_example(conversation_data):
    """Format conversation example for the response specification"""
    
    # Handle JSONL format (single conversation object) vs JSON format (conversations array)
    if conversation_data.get('query') and conversation_data.get('api_sequence'):
        # JSONL format - single conversation block
        query = conversation_data.get('query', 'User query text')
        api_sequence = conversation_data.get('api_sequence', [])
        
        example_text = f"""
## Response Format Example

Based on atomic conversation unit format:

```json
{{
  "name": "Smart Home Control Session",
  "description": "User requests smart home device control operations",
  "user": "user1",
  "conversation_turns": [
    {{
      "turn": 1,
      "user_query": "{query}",
      "api_calls": [
"""
        
        # Show API calls from the sequence
        for j, api_call in enumerate(api_sequence):
            api_name = api_call.get('api', 'api_name')
            params = json.dumps(api_call.get('params', {}), indent=8).replace('\n', '\n        ')
            comma = "," if j < len(api_sequence) - 1 else ""
            
            example_text += f"""        {{
          "api": "{api_name}",
          "params": {params}
        }}{comma}
"""
        
        example_text += """      ]
    }
  ]
}
```
"""
        
    elif conversation_data.get('conversations'):
        # Original JSON format with conversations array
        example_conv = conversation_data['conversations'][0]
        
        example_text = f"""
## Response Format Example

Based on the conversation: "{example_conv.get('name', 'Unknown')}"

```json
{{
  "name": "{example_conv.get('name', 'conversation_name')}",
  "description": "{example_conv.get('description', 'Conversation description')}",
  "user": "{example_conv.get('user', 'user_id')}",
  "conversation_turns": [
"""
        
        # Show first few turns as examples
        for i, turn in enumerate(example_conv.get('conversation_turns', [])[:3]):
            example_text += f"""    {{
      "turn": {turn.get('turn', i+1)},
      "user_query": "{turn.get('user_query', 'User query text')}",
      "api_calls": [
"""
            
            for j, api_call in enumerate(turn.get('api_calls', [])):
                api_name = api_call.get('api', 'api_name')
                params = json.dumps(api_call.get('params', {}), indent=8).replace('\n', '\n        ')
                comma = "," if j < len(turn.get('api_calls', [])) - 1 else ""
                
                example_text += f"""        {{
          "api": "{api_name}",
          "params": {params}
        }}{comma}
"""
            
            comma = "," if i < 2 else ""
            example_text += f"""      ]
    }}{comma}
"""
        
        example_text += """  ]
}
```
"""
    else:
        # Fallback example
        example_text = """
## Response Format Example

```json
{
  "name": "Smart Home Control Session",
  "description": "User requests smart home device control operations",
  "user": "user1",
  "conversation_turns": [
    {
      "turn": 1,
      "user_query": "Turn on the living room lights",
      "api_calls": [
        {
          "api": "get_user_inventory",
          "params": {}
        },
        {
          "api": "power_on",
          "params": {
            "endpoints": ["1"]
          }
        }
      ]
    }
  ]
}
```
"""
    
    example_text += """
### Response Format Requirements

Your response must be a valid JSON object with:
1. **name**: Descriptive name for the conversation
2. **description**: Brief description of what the conversation accomplishes  
3. **user**: User ID (e.g., "user1")
4. **conversation_turns**: Array of conversation turns

Each turn must contain:
- **turn**: Turn number (integer)
- **user_query**: Natural language user request
- **api_calls**: Array of API calls to fulfill the request

Each API call must contain:
- **api**: Exact API name from the reference above
- **params**: Object with required and optional parameters
"""
    
    return example_text


def generate_prompt(api_data, instructions_dict, conversation_example):
    """Generate the complete centralized prompt"""
    
    # Count APIs for overview
    total_apis = sum(len(apis) for apis in api_data.values())
    api_counts = {env: len(apis) for env, apis in api_data.items()}
    
    # Format API reference
    # api_reference = format_api_reference(api_data)
    api_reference = api_data
    
    # Format conversation example
    conversation_format = format_conversation_example(conversation_example)
    
    # Environment descriptions
    env_descriptions = {
        'SmartHomeEnv': 'Device control, security, climate management',
        'InformationControlEnv': 'Weather, news, financial data, knowledge lookup',
        'MediaControlEnv': 'Media playback, content discovery, playlist management',
        'TransactionEnv': 'E-commerce, shopping, order management',
        'CulinaryControlEnv': 'Recipe search, meal planning, restaurant ordering',
        'CommunicationController': 'Messaging, calls, meetings, contacts',
        'TimeNotificationEnv': 'Alarms, reminders, timers, scheduling'
    }
    
    # Build environment overview
    env_overview = ""
    for env_name, count in api_counts.items():
        if count > 0:
            description = env_descriptions.get(env_name, 'Domain-specific functionality')
            env_overview += f"- **{env_name}** ({count} APIs): {description}\n"
    
    # Build capabilities list
    capabilities = [
        "**Control smart home devices** - lights, thermostats, locks, blinds, TVs, and more",
        "**Retrieve information** - weather, news, financial data, and general knowledge", 
        "**Manage media playback** - play content, control playback, manage playlists",
        "**Handle transactions** - search products, manage shopping cart, process orders",
        "**Assist with cooking** - find recipes, plan meals, order food delivery",
        "**Manage communications** - send messages, make calls, schedule meetings",
        "**Set reminders and alarms** - time management, notifications, scheduling",
        "**Coordinate across domains** - use information from one area to inform actions in another",
        "**Handle complex requests** - break down multi-step scenarios into appropriate API calls"
    ]
    
    # Build agent policies section
    agent_policies = ""
    policy_titles = {
        'SmartHomeEnv': 'Smart Home Agent Policy',
        'InformationControlEnv': 'Information Control Agent Policy', 
        'MediaControlEnv': 'Media Control Agent Policy',
        'TransactionEnv': 'Transaction Agent Policy',
        'CulinaryControlEnv': 'Culinary Control Agent Policy',
        'CommunicationController': 'Communication Agent Policy',
        'TimeNotificationEnv': 'Time & Notification Agent Policy'
    }
    
    for env_name, instruction in instructions_dict.items():
        if instruction.strip():
            title = policy_titles.get(env_name, f'{env_name} Agent Policy')
            agent_policies += f"## {title}\n\n{instruction}\n\n"
    
    prompt = f"""# Multi-Domain Smart Assistant API Reference (SHORT VERSION)

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

You are a comprehensive multi-domain smart assistant with access to APIs across integrated environments:

{env_overview}
**Total: {total_apis} APIs** spanning home automation, information retrieval, media control, e-commerce, culinary assistance, communication, and time management domains.

## Your Capabilities

As a smart assistant, you can:
{chr(10).join([f"{i+1}. {cap}" for i, cap in enumerate(capabilities)])}

---

# DOMAIN-SPECIFIC AGENT POLICIES (STREAMLINED)

{agent_policies}

---

# COMPLETE API REFERENCE

{api_reference}

---

# RESPONSE FORMAT SPECIFICATION

{conversation_format}

---

# GLOBAL API CALL EFFICIENCY GUIDELINES

## Universal Principles to Prevent Repetitive Function Calls

**CRITICAL: Avoid Redundant API Calls**
- **Context Memory**: Always remember and reuse information from previous API calls within the same conversation
- **Single Source of Truth**: If you already have device endpoints, media IDs, user preferences, or other data from earlier calls, do NOT call the same APIs again
- **Smart Skipping**: Skip preliminary checks (inventory, search, preferences) when you already have the required information
- **Termination Awareness**: Stop making API calls as soon as you have sufficient information to fulfill the user's request

**Context-Aware Decision Making**
- **Conversation History**: Reference previous API responses in the same conversation before making new calls
- **User Intent Recognition**: Understand when a user's request can be fulfilled with existing information
- **Efficient Pathfinding**: Choose the shortest API call sequence to achieve the desired outcome
- **Redundancy Detection**: Recognize when you're about to repeat an API call you've already made

**When to Call APIs**
- **First Time Only**: Call discovery/search APIs only when you don't have the required IDs or information
- **State Changes**: Call status-checking APIs only when state verification is critical or explicitly requested
- **Fresh Data**: Call information APIs only when data freshness is important or previous data is stale
- **Error Recovery**: Call APIs again only when previous calls failed or returned errors


## Parameter Best Practices

### Universal Guidelines
- **Use exact API names**: No prefixes like "SmartHome:" or "Media:" or "Transaction:"
- **Follow parameter types**: Strings, integers, booleans, arrays as specified
- **Validate input ranges**: Check min/max values and constraints

### Domain-Specific Parameters
- **SmartHome**: Always use arrays for endpoints `["1", "2"]`, validate ranges (brightness 0-100, temperature 10-32°C, volume 0-100)
- **Information**: Use proper location formats, validate date ranges for forecasts
- **Media**: Use exact content IDs, validate playlist names, check device compatibility
- **Transaction**: Use proper product IDs, validate quantities, ensure valid payment methods
- **Culinary**: Use specific cuisine types, validate serving sizes, check dietary restrictions
- **Communication**: Use valid contact IDs, proper message formats, valid phone numbers
- **Time/Notification**: Use ISO date formats, validate time zones, check notification types

### Error Prevention
- **Check device compatibility**: Not all devices support all APIs
- **Validate user permissions**: Ensure user has access to requested resources
- **Handle missing data**: Provide fallback values or graceful error handling
- **Verify prerequisites**: Ensure required setup (user accounts, device pairing) exists

---

**INSTRUCTIONS**: You will receive user requests that may span multiple domains. Respond with appropriate API calls in the JSON conversation format specified above. Use your knowledge of the available APIs and their parameters to fulfill user requests effectively.
"""
    
    return prompt


def main():
    parser = argparse.ArgumentParser(description='Generate centralized API prompt (SHORT VERSION)')
    parser.add_argument('--output', '-o', default='centralized_prompt_short.md',
                       help='Output file path (default: centralized_prompt_short.md)')
    parser.add_argument('--format', '-f', choices=['markdown', 'text'], default='markdown',
                       help='Output format (default: markdown)')
    parser.add_argument('--api-file', default='./api_file/API.json',
                       help='Path to API.json file')
    parser.add_argument('--conversation-example',
                       default='../atomic_conversation_units/success_conversations/SmartHomeEnv/Conv_user1_SmartHomeEnv_batch_scenario1.jsonl',
                       help='Path to conversation example JSONL')
    
    args = parser.parse_args()
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    # Load API specifications
    api_file = Path(args.api_file)
    if not api_file.is_absolute():
        api_file = script_dir / api_file
    api_data = load_api_specifications(api_file)
    
    # Load SHORT instruction files for all environments
    instruction_dir = script_dir / "api_file"
    instruction_files = {
        'SmartHomeEnv': 'SmartHomeInstructionShort.py',
        'InformationControlEnv': 'InformationControlInstructionShort.py',
        'MediaControlEnv': 'MediaControlInstructionShort.py',
        'TransactionEnv': 'TransactionInstructionShort.py',
        'CulinaryControlEnv': 'CulinaryControlInstructionShort.py',
        'CommunicationController': 'CommunicationControllerInstructionShort.py',
        'TimeNotificationEnv': 'TimeNotificationInstructionShort.py'
    }
    
    instructions_dict = {}
    for env_name, file_name in instruction_files.items():
        instruction_file = instruction_dir / file_name
        if instruction_file.exists():
            instruction = load_instruction_file(instruction_file)
            instructions_dict[env_name] = instruction
            print(f"✓ Loaded {env_name} SHORT instructions")
        else:
            print(f"⚠️ Warning: {file_name} not found, skipping {env_name}")
            instructions_dict[env_name] = f"# {env_name} Instructions\n\nNo specific instructions available for this environment."
    
    # Load conversation example
    conv_file = Path(args.conversation_example)
    if not conv_file.is_absolute():
        conv_file = script_dir / conv_file
    conversation_example = load_conversation_example(conv_file)
    
    # Generate the prompt
    prompt = generate_prompt(
        api_data,
        instructions_dict,
        conversation_example
    )
    
    # Output the prompt
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        f.write(prompt)
    print(f"Centralized SHORT prompt generated: {output_path}")
    print(f"Total APIs: {sum(len(apis) for apis in api_data.values())}")
    print(f"Environments: {', '.join(instructions_dict.keys())}")
    print(f"📦 SHORT Version: Optimized policies from wiki_short.py files")


if __name__ == "__main__":
    main()
