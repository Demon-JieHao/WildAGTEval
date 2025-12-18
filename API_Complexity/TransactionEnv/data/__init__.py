# Copyright TransactionEnv data module

import os
import json
from typing import Dict, Any

def load_data() -> Dict[str, Any]:
    """
    Load TransactionEnv-specific data from JSON files.
    This is for backward compatibility only.
    
    Returns:
        Dictionary containing the data
    """
    data = {}
    
    # Get the data directory path
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'common', 'data')
    
    # Load products
    try:
        products_path = os.path.join(data_dir, 'products.json')
        if os.path.exists(products_path):
            with open(products_path, 'r') as f:
                data['products'] = json.load(f)
        else:
            data['products'] = []
    except Exception as e:
        print(f"Error loading products data: {str(e)}")
        data['products'] = []
    
    # Load shopping carts
    try:
        shopping_carts_path = os.path.join(data_dir, 'shopping_carts.json')
        if os.path.exists(shopping_carts_path):
            with open(shopping_carts_path, 'r') as f:
                data['shopping_carts'] = json.load(f)
        else:
            data['shopping_carts'] = {}
    except Exception as e:
        print(f"Error loading shopping carts data: {str(e)}")
        data['shopping_carts'] = {}
    
    # Load orders
    try:
        orders_path = os.path.join(data_dir, 'orders.json')
        if os.path.exists(orders_path):
            with open(orders_path, 'r') as f:
                data['orders'] = json.load(f)
        else:
            data['orders'] = []
    except Exception as e:
        print(f"Error loading orders data: {str(e)}")
        data['orders'] = []
    
    return data


def save_data(data: Dict[str, Any]) -> None:
    """
    Save TransactionEnv-specific data to JSON files.
    This function is not used in the current implementation as data is only stored in memory.
    
    Args:
        data: Dictionary containing the data to save
    """
    # This is a placeholder to maintain API compatibility.
    # In the current implementation, data is never written back to disk.
    pass
