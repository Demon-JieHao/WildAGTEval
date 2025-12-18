# Copyright InformationControlEnv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base_env import BaseEnvironment
from common.shared_memory_service import SharedMemoryService
# Import only for backward compatibility if needed
from InformationControlEnv.data import load_data
from InformationControlEnv.tools import get_all_tools
from InformationControlEnv.rules import RULES
from InformationControlEnv.wiki import WIKI


class InformationControlEnv(BaseEnvironment):
    """Information Control Environment for querying various information sources"""
    
    def __init__(self):
        """Initialize the Information Control Environment."""
        self.rules = RULES
        self.wiki = WIKI
        super().__init__()  # This will call _load_data and _load_tools
    
    def _initialize_environment_data(self):
        """Initialize InformationControlEnv-specific data structures"""
        # Ensure we have necessary data structures
        # Most data is already loaded by shared memory service
        pass
    
    def _load_tools(self):
        """Load InformationControlEnv-specific tools"""
        return get_all_tools()
    
    def _save_data(self):
        """
        Legacy method required by base class.
        In the new design, data is only stored in memory and never saved to disk.
        """
        # Update shared memory instead of saving to disk
        self.memory_service.update_data(self.data)
    
    def get_sources(self):
        """Get all available information sources"""
        return self.data.get("sources", [])
    
    def get_user_preferences(self):
        """Get the current user's preferences"""
        current_user_id = self.get_current_user()
        if not current_user_id:
            return {}
        
        for user in self.data.get("users", []):
            if user["user_id"] == current_user_id:
                return user.get("preferences", {})
        
        return {}
    
    def get_rules(self):
        """Get all rules for the environment."""
        return self.rules
    
    def get_wiki(self):
        """Get the wiki documentation for the environment."""
        return self.wiki
