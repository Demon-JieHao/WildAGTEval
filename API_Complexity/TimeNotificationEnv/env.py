# Copyright TimeNotificationEnv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base_env import BaseEnvironment
from common.shared_memory_service import SharedMemoryService
from TimeNotificationEnv.tools import ALL_TOOLS
from TimeNotificationEnv.rules import RULES
from TimeNotificationEnv.wiki import WIKI
from TimeNotificationEnv.helpers import (
    get_user_alarms, get_user_reminders, get_user_notifications,
    find_alarm_by_id, find_reminder_by_id, find_notification_by_id
)
from typing import Optional, Dict, Any, List


class TimeNotificationEnv(BaseEnvironment):
    """
    Time Notification Environment for managing alarms, reminders, and notifications.
    """
    
    def __init__(self):
        """
        Initialize the Time Notification Environment.
        """
        self.rules = RULES
        self.wiki = WIKI
        super().__init__()  # This will call _initialize_environment_data and _load_tools
        
    def _initialize_environment_data(self) -> None:
        """Initialize TimeNotificationEnv-specific data structures"""
        # Initialize alarms data if it doesn't exist
        if "alarms" not in self.data:
            self.data["alarms"] = []
        
        # Initialize reminders data if it doesn't exist
        if "reminders" not in self.data:
            self.data["reminders"] = []
        
        # Initialize notifications data if it doesn't exist
        if "notifications" not in self.data:
            self.data["notifications"] = []
        
        # Initialize user notification preferences if needed
        for user in self.data.get("users", []):
            if "notification_preferences" not in user:
                user["notification_preferences"] = {
                    "do_not_disturb": False,
                    "notification_sounds": True,
                    "preferred_device_endpoint": None
                }
    
    def _load_tools(self) -> Dict[str, Any]:
        """Load TimeNotificationEnv-specific tools"""
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
        # Don't save to disk, just update memory service
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
    
    def get_user_alarms(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all alarms for a specific user.
        
        Args:
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            List of alarm dictionaries for the user
        """
        return get_user_alarms(self.data, user_id)
    
    def get_user_reminders(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all reminders for a specific user.
        
        Args:
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            List of reminder dictionaries for the user
        """
        return get_user_reminders(self.data, user_id)
    
    def get_user_notifications(
        self,
        user_id: Optional[str] = None,
        limit: Optional[int] = None,
        include_read: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Get notifications for a specific user.
        
        Args:
            user_id: The ID of the user (if None, uses current user)
            limit: Maximum number of notifications to return
            include_read: Whether to include read notifications
            
        Returns:
            List of notification dictionaries for the user
        """
        return get_user_notifications(self.data, user_id, limit, include_read)
    
    def find_alarm(self, alarm_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Find an alarm by its ID.
        
        Args:
            alarm_id: The ID of the alarm to find
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            The alarm dictionary if found, None otherwise
        """
        return find_alarm_by_id(self.data, alarm_id, user_id)
    
    def find_reminder(self, reminder_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Find a reminder by its ID.
        
        Args:
            reminder_id: The ID of the reminder to find
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            The reminder dictionary if found, None otherwise
        """
        return find_reminder_by_id(self.data, reminder_id, user_id)
    
    def find_notification(self, notification_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Find a notification by its ID.
        
        Args:
            notification_id: The ID of the notification to find
            user_id: The ID of the user (if None, uses current user)
            
        Returns:
            The notification dictionary if found, None otherwise
        """
        return find_notification_by_id(self.data, notification_id, user_id)
