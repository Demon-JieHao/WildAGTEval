# Copyright TimeNotificationEnv

"""
Uncertainty Manifestation: Confusion Between Reminders and Calendar Events Retrieval

Description:
Developers would be confused between `get_reminders()` and this `get_calendar_events()` function. 
Both functions retrieve time-based notifications for users, but they operate on fundamentally 
different data models with different behaviors. Developers frequently mistake one for the other 
because both deal with time-based user notifications, leading to incorrect implementation and 
unexpected application behavior. The confusion is particularly problematic because reminders and 
calendar events appear similar to end-users (both are time-based notifications), but have different 
properties, filtering capabilities, and usage patterns in the API.
"""

import json
from typing import Any, Dict, Optional
from SmartHomeEnv.tool import Tool


def get_user_calendar_events(data: Dict[str, Any]) -> list:
    """
    Get calendar events for the current user from the data dictionary.
    
    Args:
        data: The data dictionary containing calendar events
        
    Returns:
        A list of calendar event objects
    """
    # Get current user's ID
    current_user = data.get("current_user", {})
    user_id = current_user.get("id")
    
    if not user_id:
        return []
    
    # Get all calendar events
    all_events = data.get("calendar_events", [])
    
    # Filter events for current user
    user_events = []
    for event in all_events:
        if event.get("user_id") == user_id:
            user_events.append(event)
            
    return user_events


class GetCalendarEvents(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_calendar_events",
                "description": "Get calendar events for the current user with optional filters. Returns a list of calendar event objects sorted by start date and time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "calendar_id": {
                            "type": "string",
                            "description": "Optional filter for specific calendar."
                        },
                        "event_type": {
                            "type": "string",
                            "enum": ["meeting", "appointment", "personal", "other"],
                            "description": "Optional filter for event type."
                        },
                        "date_from": {
                            "type": "string",
                            "description": "Optional filter for earliest event date (YYYY-MM-DD)."
                        },
                        "date_to": {
                            "type": "string",
                            "description": "Optional filter for latest event date (YYYY-MM-DD)."
                        },
                        "include_recurring": {
                            "type": "boolean",
                            "description": "Whether to include recurring events (default: True)."
                        }
                    }
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any],
              calendar_id: Optional[str] = None,
              event_type: Optional[str] = None,
              date_from: Optional[str] = None,
              date_to: Optional[str] = None,
              include_recurring: bool = True) -> str:
        """
        Get calendar events for the current user with optional filters.
        
        Args:
            data: The data dictionary
            calendar_id: Optional filter for specific calendar
            event_type: Optional filter for event type ("meeting", "appointment", "personal", "other")
            date_from: Optional filter for earliest event date (YYYY-MM-DD)
            date_to: Optional filter for latest event date (YYYY-MM-DD)
            include_recurring: Whether to include recurring events (default: True)
            
        Returns:
            A JSON string with the result of the operation
        """
        # Check if user is logged in
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user logged in: No user is currently logged in to retrieve calendar events."
            })
        
        # Validate event type if provided
        valid_event_types = ["meeting", "appointment", "personal", "other"]
        if event_type and event_type not in valid_event_types:
            return json.dumps({
                "success": False,
                "message": f"Invalid event type: Must be one of {', '.join(valid_event_types)}."
            })
        
        # Get user's calendar events
        events = get_user_calendar_events(data)
        
        # Filter by calendar if specified
        if calendar_id:
            events = [event for event in events if event.get("calendar_id") == calendar_id]
        
        # Filter by event type if specified
        if event_type:
            events = [event for event in events if event.get("event_type") == event_type]
        
        # Filter by date range if specified
        if date_from:
            events = [event for event in events if event.get("start_date", "") >= date_from]
        
        if date_to:
            events = [event for event in events if event.get("end_date", "") <= date_to]
        
        # Handle recurring events
        if not include_recurring:
            events = [event for event in events if not event.get("is_recurring", False)]
        
        # Sort events by start date and time
        events.sort(key=lambda e: (e.get("start_date", ""), e.get("start_time", "")))
        
        # Construct response message
        if not events:
            message = "No calendar events found"
            if any([calendar_id, event_type, date_from, date_to, not include_recurring]):
                message += " matching the specified filters"
        else:
            message = f"Found {len(events)} event(s)"
            if any([calendar_id, event_type, date_from, date_to, not include_recurring]):
                # Add summary of filters applied
                filters_applied = []
                if calendar_id:
                    filters_applied.append(f"calendar: {calendar_id}")
                if event_type:
                    filters_applied.append(f"type: {event_type}")
                if date_from:
                    filters_applied.append(f"from: {date_from}")
                if date_to:
                    filters_applied.append(f"to: {date_to}")
                if not include_recurring:
                    filters_applied.append("non-recurring only")
                    
                message += f" matching the specified filters ({', '.join(filters_applied)})"
        
        # Return the events with metadata
        response = {
            "success": True,
            "message": message,
            "events": events
        }
        
        # Add metadata about the events
        if events:
            # Count events by type
            type_counts = {}
            for event in events:
                event_type_key = event.get("event_type", "other")
                if event_type_key not in type_counts:
                    type_counts[event_type_key] = 0
                type_counts[event_type_key] += 1
                
            # Count recurring vs non-recurring
            recurring_count = sum(1 for event in events if event.get("is_recurring", False))
            non_recurring_count = len(events) - recurring_count
            
            response["metadata"] = {
                "total_count": len(events),
                "type_counts": type_counts,
                "recurring_count": recurring_count,
                "non_recurring_count": non_recurring_count,
                "earliest_event": events[0].get("start_date") if events else None,
                "latest_event": events[-1].get("start_date") if events else None
            }
            
            # Add calendar info if events are from different calendars
            calendar_ids = set(event.get("calendar_id") for event in events if "calendar_id" in event)
            if len(calendar_ids) > 1:
                calendar_counts = {}
                for event in events:
                    cal_id = event.get("calendar_id", "default")
                    if cal_id not in calendar_counts:
                        calendar_counts[cal_id] = 0
                    calendar_counts[cal_id] += 1
                response["metadata"]["calendar_counts"] = calendar_counts
        
        return json.dumps(response)
