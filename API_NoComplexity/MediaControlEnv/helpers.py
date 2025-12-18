# Copyright MediaControlEnv

from typing import Any, Dict, List, Optional


def get_current_user(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get the current user from the data"""
    current_user_id = data.get("current_user") or data.get("current_user_id")
    if not current_user_id:
        return None
    
    for user in data.get("users", []):
        if user["user_id"] == current_user_id:
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


def get_user_by_id(data: Dict[str, Any], user_id: str) -> Optional[Dict[str, Any]]:
    """Get a user by ID"""
    for user in data.get("users", []):
        if user["user_id"] == user_id:
            return user
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
    
    devices = data.get("devices", [])
    for device in devices:
        if device["endpoint"] == endpoint and (home_id is None or device["home_id"] == home_id):
            return device
    return None


def get_media_devices(data: Dict[str, Any], home_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all devices with media capabilities.
    
    Args:
        data: The data dictionary containing devices
        home_id: The home ID to filter by (if None, uses current user's home)
        
    Returns:
        List of devices with media capabilities
    """
    if home_id is None:
        home_id = get_user_home_id(data)
    
    media_devices = []
    for device in data.get("devices", []):
        if home_id is None or device.get("home_id") == home_id:
            # Check for media-related APIs
            apis = device.get("supported_apis", [])
            if any(api.startswith("Media_") for api in apis):
                media_devices.append(device)
    
    return media_devices


def find_media_by_id(data: Dict[str, Any], media_id: str) -> Optional[Dict[str, Any]]:
    """
    Find a media item by its ID.
    
    Args:
        data: The data dictionary
        media_id: The media ID to search for
        
    Returns:
        The media item if found, None otherwise
    """
    media_db = data.get("media_database", {})
    
    # Search in each media category
    categories = ["movies", "tv_shows", "music",] # ["movies", "tv_shows", "music", "playlists"]
    for category in categories:
        items = media_db.get(category, [])
        for item in items:
            if item.get("id") == media_id:
                return item
    
    media_db = data.get("playlists", {})
    for item in media_db:
        if item.get("id") == media_id:
            return item

    return None


def find_media_by_title(data: Dict[str, Any], title: str, media_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Find media items by title (partial match).
    
    Args:
        data: The data dictionary
        title: The title to search for
        media_type: Optional filter by type (movie, tv_show, song, album, playlist)
        
    Returns:
        List of matching media items
    """
    media_db = data.get("media_database", {})
    results = []
    title_lower = title.lower()
    
    # Define which categories to search based on media_type
    if media_type:
        if media_type == "movie":
            categories = ["movies"]
        elif media_type == "tv_show":
            categories = ["tv_shows"]
        elif media_type in ["song", "album"]:
            categories = ["music"]
        elif media_type == "playlist":
            categories = ["playlists"]
        else:
            categories = ["movies", "tv_shows", "music", "playlists"]
    else:
        categories = ["movies", "tv_shows", "music", "playlists"]
    
    # Search in each media category
    for category in categories:
        items = media_db.get(category, [])
        for item in items:
            if title_lower in item.get("title", "").lower():
                # Filter by specific media type if requested
                if not media_type or item.get("type") == media_type:
                    results.append(item)
    
    return results


def get_device_playback_state(data: Dict[str, Any], endpoint: str) -> Dict[str, Any]:
    """
    Get the current playback state for a device.
    
    Args:
        data: The data dictionary
        endpoint: The device endpoint
        
    Returns:
        The playback state dictionary
    """
    playback_states = data.get("media_playback_state", {})
    return playback_states.get(endpoint, {"status": "idle"})


def update_device_playback_state(data: Dict[str, Any], endpoint: str, state_updates: Dict[str, Any]) -> None:
    """
    Update the playback state for a device.
    
    Args:
        data: The data dictionary
        endpoint: The device endpoint
        state_updates: The state updates to apply
    """
    if "media_playback_state" not in data:
        data["media_playback_state"] = {}
    
    if endpoint not in data["media_playback_state"]:
        data["media_playback_state"][endpoint] = {}
    
    data["media_playback_state"][endpoint].update(state_updates)


# Import needed for playlist functions
from MediaControlEnv.data import load_playlists


def get_playlist_by_id(data: Dict[str, Any], playlist_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a playlist by its ID.
    
    Args:
        data: The data dictionary
        playlist_id: The playlist ID
        
    Returns:
        The playlist if found, None otherwise
    """
    # Only check top-level playlists
    if "playlists" in data:
        for playlist in data["playlists"]:
            if playlist.get("id") == playlist_id:
                return playlist
    
    return None


def get_user_playlists(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all playlists for a user.
    
    Args:
        data: The data dictionary
        user_id: The user ID (if None, uses current user)
        
    Returns:
        List of user's playlists
    """
    if user_id is None:
        current_user = get_current_user(data)
        if current_user:
            user_id = current_user["user_id"]
        else:
            return []
    
    # Only look for playlists at top level
    playlists = []
    if "playlists" in data:
        playlists = data["playlists"]
    
    # Filter by user
    user_playlists = [p for p in playlists if p.get("user_id") == user_id]
    
    return user_playlists


def create_playlist(data: Dict[str, Any], title: str, user_id: Optional[str] = None) -> str:
    """
    Create a new playlist.
    
    Args:
        data: The data dictionary
        title: The playlist title
        user_id: The user ID (if None, uses current user)
        
    Returns:
        The new playlist ID
    """
    if user_id is None:
        current_user = get_current_user(data)
        if current_user:
            user_id = current_user["user_id"]
        else:
            raise ValueError("No current user set")
    
    # Initialize playlists if needed
    if 'playlists' not in data:
        data['playlists'] = []
    
    # Get all existing playlists
    all_playlists = data['playlists']
    
    # Generate new playlist ID - check all existing playlist IDs
    existing_ids = [p.get("id", "") for p in all_playlists]
    playlist_num = 1
    while f"playlist{playlist_num}" in existing_ids:
        playlist_num += 1
    
    new_playlist_id = f"playlist{playlist_num}"
    
    # Create the playlist
    new_playlist = {
        "id": new_playlist_id,
        "title": title,
        "user_id": user_id,
        "type": "playlist",
        "items": []
    }
    
    # Add to in-memory playlists only at top level
    data['playlists'].append(new_playlist)
    
    return new_playlist_id


def check_device_supports_media_type(device: Dict[str, Any], media_item: Dict[str, Any]) -> bool:
    """
    Check if a device supports playing a specific type of media.
    
    Args:
        device: The device dictionary
        media_item: The media item dictionary
        
    Returns:
        True if the device can play this media type, False otherwise
    """
    media_type = media_item.get("type", "")
    is_audio = media_type in ["song", "album", "playlist"]
    is_video = media_type in ["movie", "tv_show"]
    
    device_categories = device.get("endpoint_categories", [])
    supports_audio = any(cat in ["SPEAKER", "MEDIA_PLAYER", "TV"] for cat in device_categories)
    supports_video = any(cat in ["TV", "MEDIA_PLAYER"] for cat in device_categories)
    
    if is_audio and supports_audio:
        return True
    if is_video and supports_video:
        return True
    
    return False


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to a readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "2:15:30" or "5:45")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"
