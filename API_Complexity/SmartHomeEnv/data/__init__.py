# Copyright SmartHomeEnv

import sys
import os
from typing import Any, Dict

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.shared_memory_service import SharedMemoryService

# Keep for backward compatibility
from common.data_loader import load_common_data

FOLDER_PATH = os.path.dirname(__file__)


def load_data() -> Dict[str, Any]:
    """
    Load all data using the shared memory service.
    
    Returns:
        A dictionary containing all data
    """
    # Get shared memory service instance
    memory_service = SharedMemoryService.get_instance()
    
    # Get shared data (loads from disk if not already loaded)
    data = memory_service.get_data()
    
    # Ensure consistency between current_user and current_user_id
    if "current_user" in data and not "current_user_id" in data:
        data["current_user_id"] = data["current_user"]
    elif "current_user_id" in data and not "current_user" in data:
        data["current_user"] = data["current_user_id"]
    
    return data


def save_data(data: Dict[str, Any]) -> None:
    """
    Update shared memory data without saving to disk.
    
    Args:
        data: The data dictionary to update
    """
    # Ensure consistency between current_user and current_user_id
    if "current_user_id" in data:
        data["current_user"] = data["current_user_id"]
    elif "current_user" in data:
        data["current_user_id"] = data["current_user"]
    
    # Update shared memory (but don't save to disk)
    memory_service = SharedMemoryService.get_instance()
    memory_service.update_data(data)
