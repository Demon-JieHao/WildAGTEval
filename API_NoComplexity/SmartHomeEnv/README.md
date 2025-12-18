# SmartHomeEnv

A Python framework for controlling smart home devices through a structured API.

## Overview

SmartHomeEnv is a framework that provides a structured way to control various smart home devices. It is designed to be used with natural language processing systems to convert user requests into API calls.

## Features

- Control various smart home devices (lights, TVs, thermostats, locks, blinds)
- Multi-user architecture with separate homes for each user
- Group devices by location or function
- Context-aware device selection
- Data persistence for device states
- User inventory exploration
- Comprehensive API for device control
- Extensible architecture for adding new device types and capabilities

## Directory Structure

```
SmartHomeEnv/
├── data/                   # Data files
│   ├── devices.json        # Device definitions with state
│   ├── groups.json         # Group definitions
│   └── users.json          # User definitions
├── tools/                  # Tool implementations
│   ├── power_on.py         # Turn devices on
│   ├── power_off.py        # Turn devices off
│   ├── brightness_adjust.py # Adjust brightness
│   ├── get_user_inventory.py # Get user's inventory
│   └── ...                 # Other tools
├── env.py                  # Environment class
├── helpers.py              # Helper functions
├── rules.py                # Rules for the environment
├── tool.py                 # Base Tool class
├── wiki.md                 # Documentation
└── demo.py                 # Demo script
```

## Installation

No installation is required. Simply clone the repository and use the SmartHomeEnv class.

## Usage

### Basic Usage

```python
from SmartHomeEnv import SmartHomeEnv

# Initialize the environment
env = SmartHomeEnv()

# Get the current user's inventory
result = env.invoke_tool("get_user_inventory")
print(result)

# Turn on a light
result = env.invoke_tool("power_on", endpoints=["1"])
print(result)

# Set the color of a light
result = env.invoke_tool("color_set", endpoints=["3"], color="blue")
print(result)

# Switch to another user
env.set_current_user("user2")
```

### Running the Demo

```bash
# Run the demo script
python -m SmartHomeEnv.demo

# Run the interactive demo
python -m SmartHomeEnv.demo --interactive
```

## Tools

The SmartHomeEnv provides the following tools:

- **Power**: Turn devices on/off
- **Brightness**: Adjust brightness of light devices
- **Color**: Set color of light devices
- **Temperature**: Set temperature of thermostats
- **Mode**: Set mode of thermostats
- **Volume**: Adjust volume of audio devices
- **Channel**: Change channels on TV devices
- **Lock**: Lock, unlock, and check status of locks
- **Open**: Open, close, and set position of blinds/shades
- **Find**: Find devices by name or get details about devices
- **Group**: Get devices in a group
- **User**: Get user inventory and information
- **Think**: Internal reasoning tool

## Multi-User Architecture

The SmartHomeEnv supports multiple users, each with their own home and devices:

- Each user has a unique ID and home ID
- Devices and groups are associated with specific homes
- User context (like current location) is stored in the user object
- Tools filter devices and groups by the current user's home ID
- The environment maintains a "current user" that can be switched

## Data Persistence

All changes to device states are persisted to the data files:

- Device states are stored in the devices.json file
- Each tool updates the device state when invoked
- The environment saves the data after each tool invocation

## Extending

To add a new tool:

1. Create a new Python file in the `tools` directory
2. Define a class that inherits from `Tool`
3. Implement the `invoke` and `get_info` methods
4. Add the tool to the `ALL_TOOLS` list in `tools/__init__.py`

## License

This project is licensed under the MIT License.
