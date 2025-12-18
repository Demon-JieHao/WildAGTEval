## Action Scheduling

Action scheduling is specifically designed for executing operations at predetermined dates and times. This function goes beyond notifications to enable automation of specific actions and device controls.

### Key Features

- Schedules concrete actions rather than just notifications
- Actions are triggered at specific clock times on specific calendar dates
- Can perform operations like controlling devices or triggering automations
- Supports recurring execution patterns (daily, weekly, monthly, yearly)
- Actions are defined as structured data objects with types and parameters
- Can target specific devices for action execution

### Schedule Operation

Scheduled actions operate through a calendar-based timing system:
1. User specifies an exact date (YYYY-MM-DD) and time (HH:MM:SS)
2. User defines a concrete action to be performed (not just a notification)
3. System executes the specified action at the designated time and date
4. If recurrence is configured, the action repeats on the defined schedule

### Parameters

- **title**: The title or name of the scheduled action
- **time**: The time when the action should execute (HH:MM:SS format)
- **date**: The date when the action should execute (YYYY-MM-DD format)
- **action**: Dictionary containing action details (type, parameters)
- **recurring**: Optional recurrence pattern (daily, weekly, monthly, yearly)
- **device_endpoint**: Optional device endpoint to execute the action

### Error Cases

- **No user logged in**: No user is currently logged in to schedule an action
- **Invalid time format**: The time must be in HH:MM:SS format
- **Invalid date format**: The date must be in YYYY-MM-DD format
- **Invalid recurring pattern**: Must be one of 'daily', 'weekly', 'monthly', 'yearly'
- **Invalid action**: The specified action is not supported or is malformed
- **Device not found**: The specified device endpoint does not exist
