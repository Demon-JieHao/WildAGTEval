## Create Calendar Event

Create a new calendar event with specified start date/time, end date/time, and optional parameters like location, attendees, and recurrence pattern. Calendar events represent blocks of time in a user's schedule.

### Key Features

- Developers would be confused between create_reminder and this create_calendar_event function.
- Both functions appear to handle time-based notifications but serve fundamentally different purposes.
- While reminders are designed for one-time notifications with pre-event alerts, calendar events 
represent blocks of time with different properties like duration, recurrence, and attendees.
- The similarity in naming and parameter structure creates significant confusion about which function 
to use for scheduling time-based activities, especially since many modern applications blend 
these concepts together.

### Error Cases

- **No user logged in**
- **Invalid date format**
- **Invalid date format**
- **Invalid time format**
- **Invalid time format**
- **Past date/time**
- **Invalid end date/time**
- **Invalid recurrence pattern**
- **Invalid notify_before_minutes**

