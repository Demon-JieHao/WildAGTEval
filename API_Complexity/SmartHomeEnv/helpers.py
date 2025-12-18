# Copyright SmartHomeEnv

from typing import Any, Dict, List, Optional


def get_current_user(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get the current user.
    
    Args:
        data: The data dictionary
        
    Returns:
        The current user dictionary
    """
    current_user_id = data.get("current_user_id")
    if not current_user_id:
        return None
    
    for user in data["users"]:
        if user["user_id"] == current_user_id:
            return user
    
    return None


def set_current_user(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Set the current user.
    
    Args:
        data: The data dictionary
        user_id: The user ID to set as current
        
    Returns:
        The updated data dictionary
    """
    data["current_user_id"] = user_id
    return data


def get_user_by_id(data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a user by ID.
    
    Args:
        data: The data dictionary
        user_id: The user ID to search for
        
    Returns:
        The user dictionary if found, None otherwise
    """
    for user in data["users"]:
        if user["user_id"] == user_id:
            return user
    return None


def get_user_by_name(data: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    """
    Get a user by name.
    
    Args:
        data: The data dictionary
        name: The name to search for
        
    Returns:
        The user dictionary if found, None otherwise
    """
    name_lower = name.lower()
    for user in data["users"]:
        if user["name"].lower() == name_lower:
            return user
    return None


def get_user_home_id(data: Dict[str, Any], user_id: Optional[str] = None) -> Optional[str]:
    """
    Get the home ID for a user.
    
    Args:
        data: The data dictionary
        user_id: The user ID (if None, uses current user)
        
    Returns:
        The home ID if found, None otherwise
    """
    if user_id is None:
        user = get_current_user(data)
    else:
        user = get_user_by_id(data, user_id)
    
    if user:
        return user.get("home_id")
    return None


def find_device_by_endpoint(data: Dict[str, Any], endpoint: str, home_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find a device by its endpoint ID.
    
    Args:
        data: The data dictionary containing devices
        endpoint: The endpoint ID to search for
        home_id: The home ID to filter by (if None, uses current user's home)
        
    Returns:
        The device dictionary if found, None otherwise
    """
    if home_id is None:
        home_id = get_user_home_id(data)
    
    devices = data["devices"]
    for device in devices:
        if device["endpoint"] == endpoint and (home_id is None or device["home_id"] == home_id):
            return device
    return None


def find_device_by_name(data: Dict[str, Any], name: str, home_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find a device by its name or alternate names.
    
    Args:
        data: The data dictionary containing devices
        name: The name to search for
        home_id: The home ID to filter by (if None, uses current user's home)
        
    Returns:
        The device dictionary if found, None otherwise
    """
    if home_id is None:
        home_id = get_user_home_id(data)
    
    devices = data["devices"]
    name_lower = name.lower()
    
    for device in devices:
        if (home_id is None or device["home_id"] == home_id):
            if device["name"].lower() == name_lower:
                return device
            
            for alt_name in device["alternate_names"]:
                if alt_name.lower() == name_lower:
                    return device
    
    return None


def find_group_by_id(data: Dict[str, Any], group_id: str, home_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find a group by its ID.
    
    Args:
        data: The data dictionary containing groups
        group_id: The group ID to search for
        home_id: The home ID to filter by (if None, uses current user's home)
        
    Returns:
        The group dictionary if found, None otherwise
    """
    if home_id is None:
        home_id = get_user_home_id(data)
    
    groups = data["groups"]
    for group in groups:
        if group["id"] == group_id and (home_id is None or group["home_id"] == home_id):
            return group
    return None


def find_group_by_name(data: Dict[str, Any], name: str, home_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Find a group by its name.
    
    Args:
        data: The data dictionary containing groups
        name: The name to search for
        home_id: The home ID to filter by (if None, uses current user's home)
        
    Returns:
        The group dictionary if found, None otherwise
    """
    if home_id is None:
        home_id = get_user_home_id(data)
    
    groups = data["groups"]
    name_lower = name.lower()
    
    for group in groups:
        if group["name"].lower() == name_lower and (home_id is None or group["home_id"] == home_id):
            return group
    
    return None


def get_devices_in_group(data: Dict[str, Any], group_id: str, home_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all devices in a group.
    
    Args:
        data: The data dictionary containing devices
        group_id: The group ID to search for
        home_id: The home ID to filter by (if None, uses current user's home)
        
    Returns:
        A list of device dictionaries in the group
    """
    if home_id is None:
        home_id = get_user_home_id(data)
    
    devices = data["devices"]
    return [device for device in devices if group_id in device["groups"] and (home_id is None or device["home_id"] == home_id)]


def get_devices_in_current_space(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get all devices in the current user's space.
    
    Args:
        data: The data dictionary
        
    Returns:
        A list of device dictionaries in the current space
    """
    user = get_current_user(data)
    if not user:
        return []
    
    current_space = user.get("current_space")
    if not current_space:
        return []
    
    return get_devices_in_group(data, current_space, user.get("home_id"))


def update_device_state(data: Dict[str, Any], endpoint: str, state_updates: Dict[str, Any], home_id: Optional[str] = None) -> bool:
    """
    Update a device's state.
    
    Args:
        data: The data dictionary
        endpoint: The endpoint ID of the device to update
        state_updates: Dictionary of state updates to apply
        home_id: The home ID to filter by (if None, uses current user's home)
        
    Returns:
        True if the update was successful, False otherwise
    """
    device = find_device_by_endpoint(data, endpoint, home_id)
    if not device:
        return False
    
    # Update the device state
    if "state" not in device:
        device["state"] = {}
    
    device["state"].update(state_updates)
    
    # Find the device in the original data and update it
    for i, d in enumerate(data["devices"]):
        if d["endpoint"] == endpoint and (home_id is None or d["home_id"] == device["home_id"]):
            data["devices"][i] = device
            return True
    
    return False


def update_user_context(data: Dict[str, Any], user_id: str, context_updates: Dict[str, Any]) -> bool:
    """
    Update a user's context.
    
    Args:
        data: The data dictionary
        user_id: The user ID to update
        context_updates: Dictionary of context updates to apply
        
    Returns:
        True if the update was successful, False otherwise
    """
    user = get_user_by_id(data, user_id)
    if not user:
        return False
    
    # Update the user context
    user.update(context_updates)
    
    # Find the user in the original data and update it
    for i, u in enumerate(data["users"]):
        if u["user_id"] == user_id:
            data["users"][i] = user
            return True
    
    return False
