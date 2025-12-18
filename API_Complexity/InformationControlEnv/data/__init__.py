# Copyright InformationControlEnv

import os
import sys
from typing import Dict, Any

# Add parent directory to path to import common modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common.shared_memory_service import SharedMemoryService

# Keep for backward compatibility
from common.data_loader import load_common_data

# Get the path to the data directory
DATA_DIR = os.path.dirname(os.path.abspath(__file__))


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
    
    return data


def save_data(data: Dict[str, Any]) -> None:
    """
    Update shared memory data without saving to disk.
    
    Args:
        data: The data dictionary to update
    """
    # Update shared memory (but don't save to disk)
    memory_service = SharedMemoryService.get_instance()
    memory_service.update_data(data)
