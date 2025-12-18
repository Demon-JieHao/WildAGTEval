# Copyright Common Data Loader

"""
Common data loader for all environments
"""

import json
import os
from typing import Dict, Any

# Get the path to the common data directory
COMMON_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Shared state for current user across all environments
_shared_state = {
    'current_user': None,
    'current_user_id': None
}

def load_common_data() -> Dict[str, Any]:
    """Load all common data shared by all environments"""
    data = {}
    
    # Load all JSON files from common data directory
    data_files = [
        'users.json',
        'devices.json', 
        'groups.json',
        'mock_data.json',
        'sources.json',
        'queries.json'
    ]
    
    for filename in data_files:
        filepath = os.path.join(COMMON_DATA_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                # Extract the key name from filename (remove .json)
                key = filename.replace('.json', '')
                data[key] = json.load(f)
        else:
            # Initialize with empty list/dict if file doesn't exist
            key = filename.replace('.json', '')
            if key in ['users', 'devices', 'groups', 'sources', 'queries']:
                data[key] = []
            else:
                data[key] = {}
    
    # Use shared state for current_user
    data['current_user'] = _shared_state['current_user']
    data['current_user_id'] = _shared_state['current_user_id']
    
    return data

def save_common_data(data: Dict[str, Any], preserve_files: bool = True) -> None:
    """
    Save all common data - with option to preserve original files
    
    Args:
        data: The data dictionary to save
        preserve_files: If True (default), don't actually write to disk
    """
    # Update shared state
    if 'current_user' in data:
        _shared_state['current_user'] = data['current_user']
    if 'current_user_id' in data:
        _shared_state['current_user_id'] = data['current_user_id']
    
    # Skip file writing if preserve_files is True
    if preserve_files:
        print("INFO: Skipping disk write to preserve original data files")
        return
        
    # Save all data files
    # Except for "current_user" or "current_user_id"
    data_mappings = {
        'users': 'users.json',
        'devices': 'devices.json',
        'groups': 'groups.json',
        'mock_data': 'mock_data.json',
        'sources': 'sources.json',
        'queries': 'queries.json'
     } 
    
    for key, filename in data_mappings.items():
        if key in data:
            filepath = os.path.join(COMMON_DATA_DIR, filename)
            with open(filepath, 'w') as f:
                json.dump(data[key], f, indent=2)

def merge_data(common_data: Dict[str, Any], env_data: Dict[str, Any]) -> Dict[str, Any]:
    """Merge common data with environment-specific data"""
    # Start with a copy of common data
    merged = common_data.copy()
    
    # Add environment-specific data (if any)
    for key, value in env_data.items():
        if key not in merged:
            merged[key] = value
    
    return merged

def get_shared_state() -> Dict[str, Any]:
    """Get the shared state"""
    return _shared_state.copy()

def update_shared_state(updates: Dict[str, Any]) -> None:
    """Update the shared state"""
    _shared_state.update(updates)
