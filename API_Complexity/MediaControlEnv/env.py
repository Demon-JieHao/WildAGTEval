# Copyright MediaControlEnv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base_env import BaseEnvironment
from common.shared_memory_service import SharedMemoryService
# Import only load_data for backward compatibility if needed
from MediaControlEnv.data import load_data
from MediaControlEnv.tools import ALL_TOOLS
from MediaControlEnv.rules import RULES
from MediaControlEnv.wiki import WIKI
from MediaControlEnv.helpers import get_media_devices, get_user_home_id
from typing import Optional, Dict, Any, List


class MediaControlEnv(BaseEnvironment):
    """
    Media Control Environment for managing media playback across devices.
    """
    
    def __init__(self):
        """
        Initialize the Media Control Environment.
        """
        self.rules = RULES
        self.wiki = WIKI
        super().__init__()  # This will call _load_data and _load_tools
        
    def _initialize_environment_data(self) -> None:
        """Initialize MediaControlEnv-specific data structures"""
        # Initialize media playback state if it doesn't exist
        if "media_playback_state" not in self.data:
            self.data["media_playback_state"] = {}
        
        # Ensure media_database structure exists
        if "media_database" not in self.data:
            self.data["media_database"] = {}
        
        # Ensure playlists exist in the database
        if "playlists" not in self.data["media_database"]:
            self.data["media_database"]["playlists"] = []
    
    def _load_tools(self) -> Dict[str, Any]:
        """Load MediaControlEnv-specific tools"""
        # Convert from list to dict format expected by base class
        tools_dict = {}
        for tool in ALL_TOOLS:
            tool_info = tool.get_info()
            if 'function' in tool_info and 'name' in tool_info['function']:
                tool_name = tool_info['function']['name']
                tools_dict[tool_name] = tool
        return tools_dict
    
    def _save_data(self) -> None:
        """
        Legacy method required by base class.
        In the new design, data is only stored in memory and never saved to disk.
        """
        # Update shared memory instead of saving to disk
        self.memory_service.update_data(self.data)
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all available tools.
        
        Returns:
            List of tool information dictionaries
        """
        return [tool.get_info() for tool in self.tools.values()]
    
    def get_rules(self) -> List[str]:
        """
        Get all rules for the environment.
        
        Returns:
            List of rule strings
        """
        return self.rules
    
    def get_wiki(self) -> str:
        """
        Get the wiki documentation for the environment.
        
        Returns:
            Wiki documentation string
        """
        return self.wiki
    
    def get_media_devices(self) -> List[Dict[str, Any]]:
        """
        Get all devices with media capabilities.
        
        Returns:
            List of devices that support media playback
        """
        return get_media_devices(self.data)
    
    def get_user_playlists(self) -> List[Dict[str, Any]]:
        """
        Get playlists for the current user.
        
        Returns:
            List of user's playlists
        """
        current_user = self.data.get("current_user") or self.data.get("current_user_id")
        if not current_user:
            return []
        
        media_db = self.data.get("media_database", {})
        playlists = media_db.get("playlists", [])
        
        # Filter playlists by user
        user_playlists = [p for p in playlists if p.get("user_id") == current_user]
        return user_playlists
    
    def get_playback_status(self, endpoint: str) -> Dict[str, Any]:
        """
        Get the current playback status for a device.
        
        Args:
            endpoint: The device endpoint
            
        Returns:
            Playback status dictionary
        """
        playback_states = self.data.get("media_playback_state", {})
        return playback_states.get(endpoint, {"status": "idle"})
