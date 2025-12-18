# Copyright Shared Memory Service

import json
import os
import threading
from typing import Dict, Any, List, Optional, Callable
import weakref

class SharedMemoryService:
    """
    A singleton service that provides in-memory data sharing across environments.
    This service loads data from disk once but never writes back to it,
    ensuring each session starts with the same initial state.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of SharedMemoryService
        Note: This singleton pattern only works within the same process.
        Different processes will have their own separate instances."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = SharedMemoryService()
            return cls._instance
    
    def __init__(self):
        self.data = {}
        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        self.observers = weakref.WeakSet()  # Use WeakSet to avoid memory leaks
        self.initialized = False
    
    def initialize_data(self):
        """Initialize data from disk files (only done once per session)"""
        if not self.initialized:
            self._load_initial_data()
            self.initialized = True
    
    def _load_initial_data(self):
        """Load initial data from disk (without modifying files)"""
        # First clear any existing data to ensure clean slate
        self.data.clear()
        
        # Define the mapping between data keys and file names
        data_files = {
            # 1 Smart Home Env data files
            'users': 'users.json',
            'devices': 'devices.json', 
            'groups': 'groups.json',
            # 2 Information Control Env data files
            'mock_data': 'mock_data.json',
            'sources': 'sources.json',
            'queries': 'queries.json',
            # 3 Media Env data files
            'media_database': 'media_database.json',
            'playlists': 'playlists.json',
            # 4 Transaction data files
            'products': 'products.json',
            'orders': 'orders.json',
            'shopping_carts': 'shopping_carts.json',
            # 5 CulinaryControlEnv data files
            'recipes': 'recipes.json',
            'restaurants': 'restaurants.json',
            'favorite_recipes': 'favorite_recipes.json',
            'favorite_restaurants': 'favorite_restaurants.json',
            'meal_plans': 'meal_plans.json',
            'delivery_orders': 'delivery_orders.json',
            # 6 CommunicationController data files
            'contacts': 'contacts.json',
            'call_history': 'call_history.json',
            'message_history': 'message_history.json',
            # 7 TimeNotificationEnv data files
            'alarms': 'alarms.json',
            'reminders': 'reminders.json',
            'notifications': 'notifications.json'
        }
        
        # Load each data file
        for key, filename in data_files.items():
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        file_content = f.read()
                        # Parse the content and create a completely new object
                        parsed_data = json.loads(file_content)
                        self.data[key] = parsed_data
                except Exception as e:
                    print(f"Error loading {filepath}: {str(e)}")
                    # Initialize with empty structure if error
                    if key in ['users', 'devices', 'groups', 'sources', 'queries', 'playlists']:
                        self.data[key] = []
                    else:
                        self.data[key] = {}
            else:
                # Initialize with empty structure if file doesn't exist
                if key in ['users', 'devices', 'groups', 'sources', 'queries', 'playlists']:
                    self.data[key] = []
                else:
                    self.data[key] = {}
        
        # Initialize runtime-specific data structures
        if 'media_playback_state' not in self.data:
            self.data['media_playback_state'] = {}
        
        # Initialize user session info
        self.data['current_user'] = None
        self.data['current_user_id'] = None
    
    def register_observer(self, observer):
        """Register an observer to be notified of data changes"""
        self.observers.add(observer)
    
    def unregister_observer(self, observer):
        """Unregister an observer"""
        self.observers.discard(observer)
    
    def notify_observers(self, updated_keys=None):
        """Notify all observers of data changes"""
        for observer in self.observers:
            if hasattr(observer, 'on_data_updated'):
                try:
                    observer.on_data_updated(updated_keys)
                except Exception as e:
                    print(f"Error notifying observer {observer}: {str(e)}")
    
    def get_data(self):
        """Get reference to the shared data (allows direct modification)"""
        if not self.initialized:
            self.initialize_data()
        return self.data
    
    def update_data(self, updates):
        """Update data with the provided updates (in-memory only)"""
        if not self.initialized:
            self.initialize_data()
            
        updated_keys = []
        
        # Only update data that's actually been changed
        # This is important to avoid unnecessary updates
        for key, value in updates.items():
            if key in self.data and id(self.data[key]) != id(value):
                self.data[key] = value
                updated_keys.append(key)
        
        if updated_keys:
            self.notify_observers(updated_keys)
    
    def reset_data(self):
        """Reset data to initial state (for session restart)"""
        print("Resetting shared memory data to initial state...")
        
        # Save reference to observers
        current_observers = self.observers
        
        # Mark as uninitialized so it will reload from disk
        self.initialized = False
        
        # Create a completely new data dictionary
        old_data = self.data
        self.data = {}
        
        # Load fresh data from disk
        self.initialize_data()
        
        # Important: notify observers with a special flag to update their references
        for observer in current_observers:
            if hasattr(observer, 'on_data_reset'):
                try:
                    observer.on_data_reset(self.data)
                except Exception as e:
                    print(f"Error notifying observer {observer} of reset: {str(e)}")
        
        # Regular notification
        self.notify_observers()
        
        print(f"Reset complete. Device 10 power state: {self.data.get('devices', [{}])[9].get('state', {}).get('power', 'unknown')}")

    def get_current_user(self) -> Optional[str]:
        """Get the current user ID"""
        if not self.initialized:
            self.initialize_data()
        return self.data.get("current_user")
    
    def set_current_user(self, user_id: str) -> bool:
        """Set the current user across all environments"""
        if not self.initialized:
            self.initialize_data()
            
        for user in self.data.get("users", []):
            if user["user_id"] == user_id:
                self.data["current_user"] = user_id
                self.data["current_user_id"] = user_id
                self.notify_observers(["current_user", "current_user_id"])
                return True
        return False
