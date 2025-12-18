# Copyright CommunicationController

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import uuid


def get_user_contacts(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all contacts for a specific user.
    
    Args:
        data: The shared data dictionary
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        List of contact dictionaries for the user
    """
    if user_id is None:
        user_id = data.get("current_user")
        
    if not user_id:
        return []
        
    return [
        contact for contact in data.get("contacts", [])
        if contact.get("user_id") == user_id
    ]


def find_contact_by_id(data: Dict[str, Any], contact_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find a contact by ID for a specific user.
    
    Args:
        data: The shared data dictionary
        contact_id: The ID of the contact to find
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        The contact dictionary if found, None otherwise
    """
    user_contacts = get_user_contacts(data, user_id)
    return next((contact for contact in user_contacts if contact.get("contact_id") == contact_id), None)


def find_contact_by_name(data: Dict[str, Any], name: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Find contacts by name for a specific user.
    
    Args:
        data: The shared data dictionary
        name: The name (or partial name) to search for
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        List of matching contact dictionaries
    """
    user_contacts = get_user_contacts(data, user_id)
    name_lower = name.lower()
    return [
        contact for contact in user_contacts
        if name_lower in contact.get("name", "").lower()
    ]


def find_contact_by_phone(data: Dict[str, Any], phone: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Find contacts by phone number for a specific user.
    
    Args:
        data: The shared data dictionary
        phone: The phone number (or partial number) to search for
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        List of matching contact dictionaries
    """
    user_contacts = get_user_contacts(data, user_id)
    return [
        contact for contact in user_contacts
        if any(phone in phone_info.get("number", "") for phone_info in contact.get("phone_numbers", []))
    ]


def find_contact_by_email(data: Dict[str, Any], email: str, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Find contacts by email for a specific user.
    
    Args:
        data: The shared data dictionary
        email: The email (or partial email) to search for
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        List of matching contact dictionaries
    """
    user_contacts = get_user_contacts(data, user_id)
    email_lower = email.lower()
    return [
        contact for contact in user_contacts
        if email_lower in contact.get("email", "").lower()
    ]


def get_user_call_history(
    data: Dict[str, Any], 
    user_id: Optional[str] = None, 
    start_time: Optional[datetime] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get call history for a specific user, optionally filtered by time range.
    
    Args:
        data: The shared data dictionary
        user_id: The ID of the user (if None, uses current user)
        start_time: If provided, only include calls after this time
        limit: Maximum number of calls to return
        
    Returns:
        List of call dictionaries for the user, sorted by timestamp (newest first)
    """
    if user_id is None:
        user_id = data.get("current_user")
        
    if not user_id:
        return []
    
    # Get all calls for the user
    calls = [
        call for call in data.get("call_history", [])
        if call.get("user_id") == user_id
    ]
    
    # Filter by start_time if provided
    if start_time:
        filtered_calls = []
        for call in calls:
            # Parse the timestamp (removing Z suffix if present)
            try:
                call_time_str = call.get("timestamp", "")
                
                # Parse ISO timestamp without relying on fromisoformat
                if 'T' in call_time_str:
                    # Remove Z suffix or replace with +00:00
                    if call_time_str.endswith('Z'):
                        call_time_str = call_time_str[:-1]
                    
                    # Split date and time parts
                    date_part, time_part = call_time_str.split('T')
                    
                    # Handle timezone in time part
                    timezone_offset = None
                    if '+' in time_part:
                        time_part, timezone_offset = time_part.split('+')
                    elif '-' in time_part and time_part.count('-') == 1:
                        time_part, timezone_offset = time_part.split('-')
                    
                    # Parse date and time components
                    year, month, day = map(int, date_part.split('-'))
                    
                    # Parse time components
                    time_components = time_part.split(':')
                    hour = int(time_components[0]) if len(time_components) > 0 else 0
                    minute = int(time_components[1]) if len(time_components) > 1 else 0
                    second = int(float(time_components[2])) if len(time_components) > 2 else 0
                    
                    # Create datetime object
                    call_time = datetime(year, month, day, hour, minute, second)
                else:
                    # Simple date only
                    year, month, day = map(int, call_time_str.split('-'))
                    call_time = datetime(year, month, day)
                
                # Compare with start_time
                if call_time >= start_time:
                    filtered_calls.append(call)
            except (ValueError, IndexError):
                # Skip calls with invalid timestamps
                continue
                
        calls = filtered_calls
    
    # Sort by timestamp (newest first)
    sorted_calls = sorted(
        calls, 
        key=lambda x: x.get("timestamp", ""), 
        reverse=True
    )
    
    # Apply limit if specified
    if limit and limit > 0:
        sorted_calls = sorted_calls[:limit]
        
    return sorted_calls


def get_user_messages(
    data: Dict[str, Any], 
    contact_id: Optional[str] = None, 
    user_id: Optional[str] = None, 
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Get message history for a specific user, optionally filtered by contact.
    
    Args:
        data: The shared data dictionary
        contact_id: If provided, only return messages with this contact
        user_id: The ID of the user (if None, uses current user)
        limit: Maximum number of messages to return
        
    Returns:
        List of message dictionaries, sorted by timestamp (newest first)
    """
    if user_id is None:
        user_id = data.get("current_user")
        
    if not user_id:
        return []
    
    # Get all messages for the user
    messages = [
        message for message in data.get("message_history", [])
        if message.get("user_id") == user_id
    ]
    
    # Filter by contact if specified
    if contact_id:
        messages = [
            message for message in messages
            if message.get("contact_id") == contact_id
        ]
    
    # Sort by timestamp (newest first)
    sorted_messages = sorted(
        messages, 
        key=lambda x: x.get("timestamp", ""), 
        reverse=True
    )
    
    # Apply limit if specified
    if limit and limit > 0:
        sorted_messages = sorted_messages[:limit]
        
    return sorted_messages


def get_active_call(data: Dict[str, Any], user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Get the active call for a user, if any.
    
    Args:
        data: The shared data dictionary
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        The active call dictionary if found, None otherwise
    """
    if user_id is None:
        user_id = data.get("current_user")
        
    if not user_id:
        return None
    
    # Check if there's an active call field in data
    if "active_calls" not in data:
        data["active_calls"] = {}
        
    return data["active_calls"].get(user_id)


def find_communication_devices(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Find devices that can be used for communication.
    
    Args:
        data: The shared data dictionary
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        List of devices that support communication functions
    """
    if user_id is None:
        user_id = data.get("current_user")
        
    if not user_id:
        return []
    
    # Find user's home ID
    user = next((u for u in data.get("users", []) if u.get("user_id") == user_id), None)
    if not user:
        return []
    
    home_id = user.get("home_id")
    
    # Get all devices in the user's home
    devices = [
        device for device in data.get("devices", [])
        if device.get("home_id") == home_id
    ]
    
    # Filter for devices that support communication (only devices with make_call API)
    comm_devices = [
        device for device in devices
        if "make_call" in device.get("supported_apis", [])
    ]
    
    return comm_devices


def find_device_by_endpoint(data: Dict[str, Any], endpoint: str, home_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find a device by its endpoint ID.
    
    Args:
        data: The shared data dictionary
        endpoint: The endpoint ID to look for
        home_id: If provided, only search devices in this home
        
    Returns:
        The device dictionary if found, None otherwise
    """
    devices = data.get("devices", [])
    
    for device in devices:
        if device.get("endpoint") == endpoint:
            if home_id is None or device.get("home_id") == home_id:
                return device
    
    return None


def get_user_home_id(data: Dict[str, Any], user_id: Optional[str] = None) -> Optional[str]:
    """
    Get the home ID for a user.
    
    Args:
        data: The shared data dictionary
        user_id: The ID of the user (if None, uses current user)
        
    Returns:
        The user's home ID if found, None otherwise
    """
    if user_id is None:
        user_id = data.get("current_user")
        
    if not user_id:
        return None
    
    user = next((u for u in data.get("users", []) if u.get("user_id") == user_id), None)
    if not user:
        return None
    
    return user.get("home_id")
