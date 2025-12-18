# Copyright TimeNotificationEnv

"""
Uncertainty Manifestation: Confusion Between Reminder Creation and Calendar Event Creation

Description:
Developers would be confused between `create_reminder` and this `create_calendar_event` function. 
Both functions appear to handle time-based notifications but serve fundamentally different purposes. 
While reminders are designed for one-time notifications with pre-event alerts, calendar events 
represent blocks of time with different properties like duration, recurrence, and attendees. 
The similarity in naming and parameter structure creates significant confusion about which function 
to use for scheduling time-based activities, especially since many modern applications blend 
these concepts together.
"""

import json
from datetime import datetime, timedelta
import uuid
from typing import Any, Dict, List, Optional
from SmartHomeEnv.tool import Tool


def validate_date_format(date_str: str) -> bool:
    """Validate date string format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_time_format(time_str: str) -> bool:
    """Validate time string format (HH:MM:SS)."""
    try:
        datetime.strptime(time_str, "%H:%M:%S")
        return True
    except ValueError:
        return False


def parse_datetime(date_str: str, time_str: str) -> datetime:
    """Parse date and time strings into a datetime object."""
    date_part = datetime.strptime(date_str, "%Y-%m-%d").date()
    time_part = datetime.strptime(time_str, "%H:%M:%S").time()
    return datetime.combine(date_part, time_part)


def calculate_end_datetime(start_date: str, start_time: str, end_date: Optional[str], end_time: Optional[str]) -> tuple:
    """Calculate end date and time if not provided."""
    start_dt = parse_datetime(start_date, start_time)
    
    if end_date is None and end_time is None:
        # Default: 1 hour after start time
        end_dt = start_dt + timedelta(hours=1)
        end_date = end_dt.strftime("%Y-%m-%d")
        end_time = end_dt.strftime("%H:%M:%S")
    elif end_date is None:
        # Same date, specified end time
        end_date = start_date
        # Validate end_time is provided (should be)
        if not end_time:
            end_dt = start_dt + timedelta(hours=1)
            end_time = end_dt.strftime("%H:%M:%S")
    elif end_time is None:
        # Specified end date, default end time (same as start time)
        end_time = start_time
    
    return end_date, end_time


def validate_recurrence_pattern(pattern: Optional[str]) -> bool:
    """Validate recurrence pattern."""
    if pattern is None:
        return True
        
    valid_patterns = ["DAILY", "WEEKLY", "MONTHLY", "YEARLY"]
    return pattern.upper() in valid_patterns


class CreateCalendarEvent(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_calendar_event",
                "description": "Create a new calendar event with specified start date/time, end date/time, and optional parameters like location, attendees, and recurrence pattern. Calendar events represent blocks of time in a user's schedule.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title or name of the calendar event."
                        },
                        "start_date": {
                            "type": "string",
                            "description": "The start date of the event in YYYY-MM-DD format."
                        },
                        "start_time": {
                            "type": "string",
                            "description": "The start time of the event in HH:MM:SS format (24-hour)."
                        },
                        "end_date": {
                            "type": "string",
                            "description": "Optional end date of the event in YYYY-MM-DD format. Defaults to start_date if not provided."
                        },
                        "end_time": {
                            "type": "string",
                            "description": "Optional end time of the event in HH:MM:SS format. Defaults to 1 hour after start_time if not provided."
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional detailed description or additional information about the event."
                        },
                        "location": {
                            "type": "string",
                            "description": "Optional physical or virtual location of the event."
                        },
                        "attendees": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Optional list of user IDs to invite to the event."
                        },
                        "recurrence": {
                            "type": "string",
                            "description": "Optional recurrence pattern (e.g., 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY')."
                        },
                        "notify_before_minutes": {
                            "type": "integer",
                            "description": "How many minutes before the event to send a notification. Defaults to 15 minutes."
                        }
                    },
                    "required": ["title", "start_date", "start_time"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any],
              title: str,
              start_date: str,
              start_time: str,
              end_date: Optional[str] = None,
              end_time: Optional[str] = None,
              description: Optional[str] = None,
              location: Optional[str] = None,
              attendees: Optional[List[str]] = None,
              recurrence: Optional[str] = None,
              notify_before_minutes: Optional[int] = 15) -> str:
        """
        Create a new calendar event for the current user.
        
        Args:
            data: The data dictionary
            title: The title of the calendar event
            start_date: The start date of the event in YYYY-MM-DD format
            start_time: The start time of the event in HH:MM:SS format
            end_date: Optional end date of the event in YYYY-MM-DD format (defaults to start_date)
            end_time: Optional end time of the event in HH:MM:SS format (defaults to 1 hour after start_time)
            description: Optional detailed description of the event
            location: Optional location of the event
            attendees: Optional list of user IDs to invite to the event
            recurrence: Optional recurrence pattern (e.g., "DAILY", "WEEKLY", "MONTHLY", "YEARLY")
            notify_before_minutes: Optional minutes before to notify (default: 15 minutes)
            
        Returns:
            A JSON string with the result of the operation
        """
        # Check if user is logged in
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user logged in: No user is currently logged in to create a calendar event."
            })
        
        # Validate date format
        if not validate_date_format(start_date):
            return json.dumps({
                "success": False,
                "message": "Invalid date format: The start date must be in YYYY-MM-DD format."
            })
            
        if end_date and not validate_date_format(end_date):
            return json.dumps({
                "success": False,
                "message": "Invalid date format: The end date must be in YYYY-MM-DD format."
            })
            
        # Validate time format
        if not validate_time_format(start_time):
            return json.dumps({
                "success": False,
                "message": "Invalid time format: The start time must be in HH:MM:SS format."
            })
            
        if end_time and not validate_time_format(end_time):
            return json.dumps({
                "success": False,
                "message": "Invalid time format: The end time must be in HH:MM:SS format."
            })
        
        # Calculate end date/time if not provided
        end_date, end_time = calculate_end_datetime(start_date, start_time, end_date, end_time)
        
        # Parse dates for validation
        start_dt = parse_datetime(start_date, start_time)
        end_dt = parse_datetime(end_date, end_time)
        now = datetime.now()
        
        # Check if event is in the past
        if start_dt < now:
            return json.dumps({
                "success": False,
                "message": "Past date/time: Cannot set an event in the past."
            })
            
        # Check if end is after start
        if end_dt <= start_dt:
            return json.dumps({
                "success": False,
                "message": "Invalid end date/time: End date/time must be after start date/time."
            })
            
        # Validate recurrence pattern
        if recurrence and not validate_recurrence_pattern(recurrence):
            return json.dumps({
                "success": False,
                "message": "Invalid recurrence pattern: Must be one of 'DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'."
            })
            
        # Validate notification time
        if notify_before_minutes is not None and notify_before_minutes < 0:
            return json.dumps({
                "success": False,
                "message": "Invalid notify_before_minutes: Must be a non-negative number."
            })
            
        # Generate event ID
        event_id = f"event_{int(datetime.now().timestamp())}_{str(uuid.uuid4())[:8]}"
        
        # Create event object
        event = {
            "id": event_id,
            "title": title,
            "user_id": current_user.get("id"),
            "start_date": start_date,
            "start_time": start_time,
            "end_date": end_date,
            "end_time": end_time,
            "description": description,
            "location": location,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "notify_before_minutes": notify_before_minutes
        }
        
        # Add optional fields if provided
        if attendees:
            event["attendees"] = attendees
            event["attendee_responses"] = {attendee: "PENDING" for attendee in attendees}
            
        if recurrence:
            event["recurrence"] = recurrence.upper()
            
        # Add to calendar events collection
        if "calendar_events" not in data:
            data["calendar_events"] = []
            
        data["calendar_events"].append(event)
        
        # Check for conflicts with existing events if needed
        conflicts = []
        for existing_event in data.get("calendar_events", []):
            # Skip the event we just created
            if existing_event["id"] == event_id:
                continue
                
            # Skip events for other users
            if existing_event["user_id"] != current_user.get("id"):
                continue
                
            # Simple overlap check (could be more sophisticated)
            existing_start = parse_datetime(existing_event["start_date"], existing_event["start_time"])
            existing_end = parse_datetime(existing_event["end_date"], existing_event["end_time"])
            
            if (start_dt < existing_end and end_dt > existing_start):
                conflicts.append({
                    "event_id": existing_event["id"],
                    "title": existing_event["title"],
                    "start_time": f"{existing_event['start_date']} {existing_event['start_time']}",
                    "end_time": f"{existing_event['end_date']} {existing_event['end_time']}"
                })
                
        # Prepare response
        response = {
            "success": True,
            "message": f"Calendar event '{title}' created successfully",
            "event_id": event_id,
            "start": f"{start_date} {start_time}",
            "end": f"{end_date} {end_time}",
        }
        
        if location:
            response["location"] = location
            
        if attendees:
            response["attendees_count"] = len(attendees)
            
        if recurrence:
            response["recurrence"] = recurrence.upper()
            
        if conflicts:
            response["warnings"] = {
                "conflicts": conflicts,
                "message": f"Event overlaps with {len(conflicts)} existing calendar event(s)"
            }
            
        return json.dumps(response)
