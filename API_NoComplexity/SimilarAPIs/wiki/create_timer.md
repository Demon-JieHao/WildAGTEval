## Timer Creation

Timer creation is specifically designed for managing countdown-based notifications. This function allows users to set up notifications that trigger after a specified duration has elapsed.

### Key Features

- Creates countdown timers based on durations rather than specific clock times
- Durations are specified in precise HH:MM:SS format
- Can be configured as one-time events or automatically repeating timers
- Supports custom notification sounds for timer completion
- Can be associated with specific devices for targeted notifications
- Provides human-readable duration presentation in responses

### Timer Operation

Timers operate through a countdown mechanism:
1. User specifies a duration (e.g., "1:30:00" for 1 hour and 30 minutes)
2. System calculates the exact future end time from the current moment
3. When the end time is reached, the notification is triggered
4. If repeat is enabled, the timer automatically restarts the countdown

### Parameters

- **title**: The title or name of the timer
- **duration**: The duration of the timer in HH:MM:SS format
- **sound**: Optional custom sound to use when the timer completes
- **device_endpoint**: Optional device endpoint to associate with the timer
- **repeat**: Whether the timer should automatically restart after completion

### Error Cases

- **No user logged in**: No user is currently logged in to create a timer
- **Invalid duration format**: The duration must be in HH:MM:SS format
- **Device not found**: The specified device endpoint does not exist
