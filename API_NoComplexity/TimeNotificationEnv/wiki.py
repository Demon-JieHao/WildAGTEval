# Copyright TimeNotificationEnv

# Define the wiki documentation for the Time Notification Environment
WIKI = """
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
"""
