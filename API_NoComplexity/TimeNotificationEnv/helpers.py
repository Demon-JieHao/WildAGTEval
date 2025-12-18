# Copyright TimeNotificationEnv

from typing import Dict, Any, List, Optional


def get_current_user_id(data: Dict[str, Any]) -> Optional[str]:
    """
    Get the current user ID from the data.
    
    Args:
        data: The data dictionary
        
    Returns:
        The current user ID, or None if no user is logged in
    """
    return data.get("current_user")


def get_user_alarms(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all alarms for a specific user.
    
    Args:
        data: The data dictionary
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        List of alarm dictionaries for the user
    """
    # Get user ID (use current user if not specified)
    if user_id is None:
        user_id = get_current_user_id(data)
        if user_id is None:
            return []
    
    # Get all alarms for the user
    alarms = [
        alarm for alarm in data.get("alarms", [])
        if alarm.get("user_id") == user_id
    ]
    
    return alarms


def get_user_reminders(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all reminders for a specific user.
    
    Args:
        data: The data dictionary
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        List of reminder dictionaries for the user
    """
    # Get user ID (use current user if not specified)
    if user_id is None:
        user_id = get_current_user_id(data)
        if user_id is None:
            return []
    
    # Get all reminders for the user
    reminders = [
        reminder for reminder in data.get("reminders", [])
        if reminder.get("user_id") == user_id
    ]
    
    return reminders


def get_user_notifications(
    data: Dict[str, Any],
    user_id: Optional[str] = None,
    limit: Optional[int] = None,
    include_read: bool = False
) -> List[Dict[str, Any]]:
    """
    Get notifications for a specific user.
    
    Args:
        data: The data dictionary
        user_id: The ID of the user (if None, uses current user)
        limit: Maximum number of notifications to return
        include_read: Whether to include read notifications
        
    Returns:
        List of notification dictionaries for the user
    """
    # Get user ID (use current user if not specified)
    if user_id is None:
        user_id = get_current_user_id(data)
        if user_id is None:
            return []
    
    # Get notifications for the user
    notifications = [
        notification for notification in data.get("notifications", [])
        if notification.get("user_id") == user_id and (include_read or not notification.get("read", False))
    ]
    
    # Sort by timestamp (newest first)
    notifications.sort(key=lambda n: n.get("timestamp", ""), reverse=True)
    
    # Apply limit if specified
    if limit is not None and limit > 0:
        notifications = notifications[:limit]
    
    return notifications


def find_alarm_by_id(data: Dict[str, Any], alarm_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find an alarm by its ID.
    
    Args:
        data: The data dictionary
        alarm_id: The ID of the alarm to find
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        The alarm dictionary if found, None otherwise
    """
    # Get user ID (use current user if not specified)
    if user_id is None:
        user_id = get_current_user_id(data)
        if user_id is None:
            return None
    
    # Find the alarm
    for alarm in data.get("alarms", []):
        if alarm.get("alarm_id") == alarm_id and alarm.get("user_id") == user_id:
            return alarm
    
    return None


def find_reminder_by_id(data: Dict[str, Any], reminder_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find a reminder by its ID.
    
    Args:
        data: The data dictionary
        reminder_id: The ID of the reminder to find
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        The reminder dictionary if found, None otherwise
    """
    # Get user ID (use current user if not specified)
    if user_id is None:
        user_id = get_current_user_id(data)
        if user_id is None:
            return None
    
    # Find the reminder
    for reminder in data.get("reminders", []):
        if reminder.get("reminder_id") == reminder_id and reminder.get("user_id") == user_id:
            return reminder
    
    return None


def find_notification_by_id(data: Dict[str, Any], notification_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find a notification by its ID.
    
    Args:
        data: The data dictionary
        notification_id: The ID of the notification to find
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        The notification dictionary if found, None otherwise
    """
    # Get user ID (use current user if not specified)
    if user_id is None:
        user_id = get_current_user_id(data)
        if user_id is None:
            return None
    
    # Find the notification
    for notification in data.get("notifications", []):
        if notification.get("notification_id") == notification_id and notification.get("user_id") == user_id:
            return notification
    
    return None


def generate_id(prefix: str, data: Dict[str, Any]) -> str:
    """
    Generate a sequential ID with the given prefix.
    
    Args:
        prefix: The prefix for the ID (e.g., 'alarm', 'reminder', 'notif')
        data: The data dictionary
        
    Returns:
        A sequential ID string
        
    Raises:
        ValueError: If the prefix is not one of the supported values
    """
    # Map prefix to corresponding data collection
    collection_map = {
        "alarm": "alarms",
        "reminder": "reminders",
        "notif": "notifications"
    }
    
    # Get the collection name for the given prefix
    collection_name = collection_map.get(prefix)
    if not collection_name:
        # Raise error if prefix is not mapped
        raise ValueError(f"Unsupported ID prefix: '{prefix}'. Must be one of: {', '.join(collection_map.keys())}")
    
    # Initialize collection if it doesn't exist
    if collection_name not in data:
        data[collection_name] = []
    
    collection = data[collection_name]
    
    # Extract numeric parts from existing IDs
    import re
    
    existing_ids = []
    id_field = f"{prefix}_id"  # alarm_id, reminder_id, notification_id
    
    # Special case: notification IDs should actually use 'notification_id'
    if prefix == "notif":
        id_field = "notification_id"
    
    for item in collection:
        if id_field in item:
            item_id = item[id_field]
            
            # Handle single format (prefix123)
            if item_id.startswith(prefix):
                try:
                    # Extract only the numeric part using regex
                    match = re.search(r'^' + prefix + r'(\d+)$', item_id)
                    if match:
                        num = int(match.group(1))
                        existing_ids.append(num)
                except (ValueError, AttributeError):
                    continue
    
    # Start from 1 if no existing IDs, otherwise max + 1
    next_num = 1
    if existing_ids:
        next_num = max(existing_ids) + 1
    
    # Return new ID (all prefixes use a format without underscore)
    return f"{prefix}{next_num}"
