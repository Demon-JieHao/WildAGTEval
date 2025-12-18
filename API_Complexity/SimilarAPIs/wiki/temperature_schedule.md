## Temperature Scheduling

Temperature scheduling is designed for creating future temperature settings for thermostat devices. This function enables planning of temperature changes without affecting the current temperature settings.

### Key Features

- Creates scheduled temperature changes for the future without modifying current settings
- Allows setting temperature changes to activate at specific times
- Can be scheduled for specific days of the week
- Supports optional end times for temporary temperature changes
- Temperature values are automatically constrained to safe ranges (10-32°C)
- Creates persistent schedule entries that remain until explicitly modified
- Supports scheduling across multiple thermostat devices simultaneously

### Schedule Parameters

- Time-based scheduling with start times in HH:MM format
- Optional end times to automatically revert the temperature change
- Day-specific scheduling for recurring patterns
- Temperature values specified in degrees Celsius
- Multiple device support for consistent temperature scheduling

### Parameters

- **endpoints**: List of device endpoint IDs to schedule
- **temperature**: Temperature value to set in degrees Celsius
- **start_time**: Time to start the temperature setting (format: "HH:MM")
- **end_time**: Optional time to end the temperature setting (format: "HH:MM")
- **days**: Optional list of days to apply the schedule (e.g., ["Monday", "Wednesday", "Friday"])

### Error Cases

- **No devices specified**: The endpoints parameter is empty or not provided
- **No temperature specified**: The temperature parameter is not provided
- **No start time specified**: The start_time parameter is not provided
- **Invalid time format**: The time is not in the correct format (HH:MM)
- **Temperature out of range**: Values outside 10-32°C will be constrained
- **Invalid days**: The specified days are not valid weekday names
- **Device not found**: Device with endpoint not found
- **API not supported**: Device does not support temperature scheduling
- **Schedule update failure**: The device schedule could not be updated
