# Copyright MediaControlEnv

import json
import os
import sys
from typing import Any, Dict, List, Optional

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.shared_memory_service import SharedMemoryService

# Keep for backward compatibility
from common.data_loader import load_common_data

FOLDER_PATH = os.path.dirname(__file__)


def get_common_data_dir() -> str:
    """Get path to common/data directory"""
    return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'common', 'data')


def load_playlists() -> List[Dict[str, Any]]:
    """
    Load all playlists from playlists.json
    
    Returns:
        List of playlist dictionaries
    """
    playlists_file = os.path.join(get_common_data_dir(), 'playlists.json')
    
    if os.path.exists(playlists_file):
        try:
            with open(playlists_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading playlists: {str(e)}")
    
    return []


def load_data() -> Dict[str, Any]:
    """
    Load all data using the shared memory service.
    
    Returns:
        A dictionary containing all data
    """
    # Get shared memory service instance
    memory_service = SharedMemoryService.get_instance()
    
    # Get the shared data (this loads from disk if not already loaded)
    data = memory_service.get_data()
    
    # Ensure media_database structure exists
    if 'media_database' not in data:
        data['media_database'] = {}
    
    # Ensure playlists exist - ONLY in the top level
    if 'playlists' not in data:
        # Try to load playlists from playlists.json if not already in memory
        playlists = load_playlists()
        data['playlists'] = playlists
    
    # Remove any reference in media_database structure to avoid duplicate storage locations
    if 'media_database' in data and 'playlists' in data['media_database']:
        del data['media_database']['playlists']
    
    # Ensure playback state is initialized
    if 'media_playback_state' not in data:
        data['media_playback_state'] = {}
    
    return data


def save_data(data: Dict[str, Any]) -> None:
    """
    Update shared memory data without saving to disk.
    
    Args:
        data: The data dictionary to update
    """
    # Update the shared memory (but don't save to disk)
    memory_service = SharedMemoryService.get_instance()
    memory_service.update_data(data)
