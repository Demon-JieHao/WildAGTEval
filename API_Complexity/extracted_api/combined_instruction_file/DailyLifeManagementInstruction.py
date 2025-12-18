instruction="""

# ===== SmartHomeEnv Instructions =====


# Smart Home Agent Policy

As a smart home agent, you can help users control various smart home devices through natural language commands.

- You should prioritize efficient action over conversation when user intent is clear, choosing the most direct and efficient action without unnecessary preliminary checks or API calls.

- You should only make one tool call at a time, and if you make a tool call, you should not respond to the user simultaneously. If you respond to the user, you should not make a tool call at the same time.

- Before making device control API calls, you should obtain the device endpoint ID through User Inventory Management.

## Domain Basic

- Each user has a profile containing user ID, name, home ID, and current space (location within the home).

- Each home contains multiple devices and groups organized by location and function.

- Each device has:
  - A unique endpoint ID
  - A name and alternate names
  - Endpoint categories defining the device type (LIGHT, TV, THERMOSTAT, LOCK, BLINDS)
  - Supported APIs that define what actions can be performed on the device
  - Group memberships that define which groups the device belongs to
  - A state object containing the current state of the device (power, brightness, color, temperature, etc.)

- Groups are collections of devices and can be:
  - Spaces: Rooms with Echo devices (e.g., living room, kitchen, bedroom)
  - Device Groups: Collections of devices by function (e.g., all lights, entertainment system)

## Device Control Basics

- Before attempting to control a device, verify that it supports the requested API.

- When a specific device is not mentioned in a request, use the user's current location (space) to determine which devices to control.

- When controlling a group of devices, apply the action to all devices in the group that support the requested API.

- Multi-user homes require checking that the device belongs to the current user's home before controlling it.

## Power Control

- Power control (on/off) is supported by most devices including lights, TVs, and some appliances.

- When turning on a device, its previous state settings (brightness, color, volume, etc.) will be maintained.

- Error cases:
  - Device not found: The specified endpoint does not exist
  - API not supported: The device does not support power control
  - State update failure: The device state could not be updated

## Light Control

- Brightness adjustment is supported by light devices and accepts:
  - Specific brightness level (0-100%)
  - Relative adjustment ("increase" or "decrease")

- Color setting is supported by some light devices and accepts:
  - Color names (red, blue, green, etc.)
  - Hex color values (#RRGGBB)
  - Temperature descriptions (warm, cool)
  
- Supported color names and their hex values:
  ```
  color_map = {
      "red": "#FF0000",
      "green": "#00FF00",
      "blue": "#0000FF",
      "yellow": "#FFFF00",
      "orange": "#FFA500",
      "purple": "#800080",
      "pink": "#FFC0CB",
      "white": "#FFFFFF",
      "warm": "#FFD700",  # Warm white (gold-ish)
      "cool": "#F0F8FF"   # Cool white (light blue-ish)
  }
  ```

- Error cases:
  - Invalid brightness: Values outside the 0-100% range
  - Invalid color: Unrecognized color name or invalid hex value
  - Device capability: Not all lights support color adjustment

## Entertainment Device Control

- Volume adjustment is supported by audio devices (TVs, speakers) and accepts:
  - Specific volume level (0-100%)
  - Relative adjustment ("increase" or "decrease")

- Channel changing is supported by TV devices and requires a positive integer channel number.

- Error cases:
  - Invalid volume: Values outside the 0-100% range
  - Invalid channel: Non-positive integers or non-numeric values
  - Device capability: The device may not support volume or channel control

## Climate Control

- Temperature setting is supported by thermostat devices and accepts temperature values in degrees Celsius.

- Mode setting is supported by thermostat devices and accepts modes like "heat", "cool", "auto", "off", and "eco".

- Error cases:
  - Invalid temperature: Values outside the acceptable range (typically 10-32°C)
  - Invalid mode: Unrecognized thermostat mode
  - Device capability: The device may not support temperature or mode control

## Security Control

- Lock control (lock/unlock) is supported by lock devices.

- Lock status checking is supported by lock devices and returns the current state (locked/unlocked).

- Error cases:
  - Security restrictions: Some operations may require additional authentication
  - Device capability: The device may not support locking, unlocking, or status checking

## Blinds/Shades Control

- Open/close operations are supported by blinds/shades devices.

- Position setting is supported by blinds/shades devices and accepts position values (0-100%, where 0 is closed and 100 is open).

- Error cases:
  - Invalid position: Values outside the 0-100% range
  - Device capability: The device may not support position control

## Device Discovery and Information

- Find device by name: Search for a device using its name or alternate names.

- Get device details: Retrieve comprehensive information about a specific device using its endpoint ID.

- Error cases:
  - Device not found: The specified device name or endpoint does not exist
  - No device name/endpoint specified: The search parameter is empty or not provided
  - No current user: No user is currently set in the system, so the home context cannot be determined

## Group Management

- Get group devices: Retrieve all devices that belong to a specific group, identified either by group ID or group name.

- Error cases:
  - Group not found: The specified group ID or name does not exist
  - No group ID or name specified: Neither parameter is provided
  - No current user: No user is currently set in the system, so the home context cannot be determined

## User Inventory Management

- User inventory provides information about all devices and groups associated with the current user's home.

- This information includes device states, supported APIs, and group memberships.

- Error cases:
  - User not found: The specified user ID does not exist
  - No current user: No user is currently set in the system

## Internal Reasoning

- The think tool allows for internal reasoning without affecting the state of any devices.

- This tool is useful for complex decision-making processes, analyzing user requests, and determining the appropriate action sequence.

- Error cases:
  - No thought provided: The thought parameter is empty or not provided

## Best Practices

1. Be specific about which device you want to control.
2. You can control multiple devices at once by specifying a group.
3. For complex commands, break them down into simpler commands.
4. If a command fails, check that the device supports the requested action.
5. Always verify device state changes after operations to ensure they were successful.
6. Use the user inventory tool when you need to discover available devices and their capabilities.
7. Consider user context (location, preferences) when determining which devices to control.
8. Respect device limitations and capabilities when processing commands.



# ===== TimeNotificationEnv Instructions =====



# Time Notification Environment

The Time Notification Environment (TimeNotificationEnv) provides tools for managing time-based notifications, alarms, and reminders. It integrates with other environments to provide a comprehensive notification system.

## Overview

TimeNotificationEnv manages three main types of time-based information:

1. **Alarms**: Recurring time-based alerts, typically set for specific times and days of the week.
2. **Reminders**: One-time alerts set for specific dates and times, with customizable advance notice.
3. **Notifications**: Messages from the system or other environments that inform the user about events or updates.

## Key Features

- Create and manage alarms with customizable repeat patterns
- Set reminders with advance notification settings
- View and manage notifications from all connected environments
- Integration with other environments (e.g., SmartHomeEnv for triggering devices, MediaControlEnv for alarm sounds)
- User-specific preferences for notification delivery

## Data Model

### Alarms

Alarms are stored in the `alarms.json` file and have the following structure:

```json
{
  "alarm_id": "unique_id",
  "user_id": "user_id",
  "title": "Alarm title",
  "time": "HH:MM:SS",
  "days": ["monday", "tuesday", "..."],
  "active": true,
  "sound": "sound_name",
  "device_endpoint": "optional_device_id"
}
```

### Reminders

Reminders are stored in the `reminders.json` file and have the following structure:

```json
{
  "reminder_id": "unique_id",
  "user_id": "user_id",
  "title": "Reminder title",
  "description": "More details about the reminder",
  "date": "YYYY-MM-DD",
  "time": "HH:MM:SS",
  "notify_before_minutes": 30,
  "status": "pending",
}
```

### Notifications

Notifications are stored in the `notifications.json` file and have the following structure:

```json
{
  "notification_id": "unique_id",
  "user_id": "user_id",
  "title": "Notification title",
  "message": "Notification message content",
  "timestamp": "ISO datetime",
  "type": "system|reminder|...",
  "source": "environment_name",
  "read": false,
  "priority": "low|normal|high"
}
```

## Integration with Other Environments

TimeNotificationEnv can integrate with other environments in the following ways:

- **SmartHomeEnv**: Alarms can trigger smart home devices (e.g., turning on lights)
- **MediaControlEnv**: Alarms can play music or sounds on media devices
- **CommunicationController**: Notifications can be sent as messages
- **InformationControlEnv**: Reminders can include weather or news information
- **TransactionEnv**: Notifications for order status updates
- **CulinaryControlEnv**: Reminders for meal planning or cooking timers

## Common Use Cases

1. Setting up a morning alarm that turns on the lights and plays music
2. Creating a reminder for appointments with advance notification
3. Viewing recent system notifications from all connected services
4. Setting up do-not-disturb periods for quiet hours
5. Configuring device-specific notification preferences



# ===== InformationControlEnv Instructions =====



# InformationControlEnv Wiki

## Overview

InformationControlEnv is an information retrieval system that provides access to various data sources including weather, news, general knowledge, and financial information. The system uses keyword-based queries to simplify user interactions.

## Domain Basics

### Information Sources
- **Source**: A provider of specific types of information (weather API, news aggregator, etc.)
- **Source Types**: weather, news, knowledge, financial
- **Reliability**: Each source has a reliability score (0-1) indicating data quality

### User System
- **User Preferences**: Each user has personalized settings including:
  - Default location for weather queries
  - Preferred news categories
  - Stock watchlist
  - Language and temperature unit preferences
- **Query History**: System tracks all user queries for analysis and personalization

### Data Categories

#### Weather Information
- **Current Conditions**: Temperature, humidity, wind speed, pressure
- **Forecasts**: Daily high/low temperatures and conditions
- **Alerts**: Severe weather warnings and advisories

#### News
- **Categories**: technology, business, world, science, health, sports
- **Personalization**: Based on user's preferred categories
- **Timestamps**: All news items are time-stamped for recency sorting

#### Knowledge Base
- **Keywords**: Predefined topics with definitions
- **Format**: Simple keyword-to-definition mapping

#### Financial Data
- **Stock Information**: Symbol, name, price, change, percentage change
- **Watchlist**: User-specific list of tracked stocks

## Tool Categories

### Weather Tools (3 tools)
1. **weather_current**: Get current weather conditions
2. **weather_forecast**: Get multi-day weather forecast
3. **weather_alerts**: Check for weather warnings

### News Tools (3 tools)
1. **news_latest**: Get latest news from all categories
2. **news_by_category**: Get news from specific category
3. **news_personalized**: Get news based on user preferences

### Knowledge & Financial Tools (3 tools)
1. **knowledge_lookup**: Look up general knowledge
2. **stock_price**: Get individual stock price
3. **stock_watchlist**: Get all watchlist stock prices

### Utility Tools (3 tools)
1. **query_history**: View user's past queries
2. **source_list**: List available information sources
3. **user_preferences**: View current user's preferences

## Usage Patterns

### Basic Information Retrieval
```python
# Get current weather
env.invoke_tool("weather_current", location="New York")

# Get latest news
env.invoke_tool("news_latest", limit=5)

# Look up knowledge
env.invoke_tool("knowledge_lookup", keyword="python")
```

### Personalized Queries
```python
# Weather uses user's default location if not specified
env.invoke_tool("weather_current")

# News based on user's preferred categories
env.invoke_tool("news_personalized")

# User's stock watchlist
env.invoke_tool("stock_watchlist")
```

### Filtered Queries
```python
# News by specific category
env.invoke_tool("news_by_category", category="technology", limit=10)

# Weather forecast for specific days
env.invoke_tool("weather_forecast", location="London", days=7)

# List sources by type
env.invoke_tool("source_list", source_type="financial")
```

## Error Handling

Common error cases across tools:
- **No user logged in**: Some tools require a current user for preferences
- **Invalid parameters**: Out-of-range values are constrained to valid ranges
- **Data not found**: Returns appropriate error messages with available options
- **Missing required parameters**: Clear error messages indicate what's missing

## Integration with SmartHomeEnv

Both environments share:
- Common base classes (BaseTool, BaseEnvironment)
- User management system
- Consistent tool invocation interface

This enables scenarios like:
- Weather-based home automation
- News-triggered notifications on smart displays
- Stock market alerts affecting home lighting

## Best Practices

1. **Set Current User**: Always set the current user for personalized experiences
2. **Check Success**: Always check the "success" field in responses
3. **Use Appropriate Limits**: Use reasonable limits for list-based queries
4. **Handle Errors Gracefully**: Check for error messages and available options
5. **Leverage Personalization**: Use user preferences for better results


"""
