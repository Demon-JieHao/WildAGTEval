"""
User context utilities for API benchmark generation.

This module provides functions for loading data and creating
user-specific contexts for API trail generation and validation.
"""

import json
import pprint
from typing import Dict, List, Any


def load_data() -> Dict[str, Any]:
    """
    Load all data files from common/data
    
    Returns:
        Dictionary containing all loaded data from JSON files
    """
    import os
    
    # Try multiple possible paths for common/data
    possible_paths = [
        'common/data/',
        './common/data/',  # When running from project root
        '../../common/data/',  # When running from benchmark/utils
        '../common/data/',  # When running from utils/
        '../../../common/data/',  # When running from subdirectories
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            break
    
    if not data_path:
        raise FileNotFoundError("Could not find common/data directory. Tried paths: " + str(possible_paths))
    
    data = {}
    for filename in ['devices.json', 'groups.json', 'mock_data.json', 
                     'queries.json', 'sources.json', 'users.json']:
        with open(f'{data_path}{filename}', 'r') as f:
            key = filename.replace('.json', '')
            data[key] = json.load(f)
    return data


def create_user_context(data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
    """
    Create a focused context for a specific user, including only relevant information
    for that user to reduce noise in the LLM prompt
    
    Args:
        data: Dictionary containing all loaded data
        user_id: ID of the user to create context for
        
    Returns:
        Dictionary containing user-specific context
        
    Raises:
        ValueError: If user with specified ID is not found
    """
    # Find the specified user
    user = next((u for u in data['users'] if u['user_id'] == user_id), None)
    if not user:
        raise ValueError(f"User {user_id} not found in database")
    
    # Get user's home ID
    home_id = user['home_id']
    
    # Get devices user has access to
    accessible_endpoints = set(user['permissions']['can_control'])
    user_devices = [d for d in data['devices'] 
                   if d['endpoint'] in accessible_endpoints and d['home_id'] == home_id]
    
    # Get groups relevant to this user
    user_groups = [g for g in data['groups'] if g['home_id'] == home_id]
    
    # Get user's query history
    user_queries = [q for q in data['queries'] if q['user_id'] == user_id]
    
    # Get relevant mock data
    # - Weather for user's location
    location_key = user['preferences']['location'].lower().replace(" ", "_")
    user_weather = data['mock_data']['weather'].get(location_key, {})
    
    # - News categories user is interested in
    preferred_categories = user['preferences']['news_categories']
    user_news = {cat: data['mock_data']['news'].get(cat, []) 
                for cat in preferred_categories if cat in data['mock_data']['news']}
    
    # - Stocks in user's watchlist
    stock_watchlist = user['preferences']['stock_watchlist']
    user_stocks = {symbol: data['mock_data']['stocks'].get(symbol, {})
                  for symbol in stock_watchlist if symbol in data['mock_data']['stocks']}
    
    # Build focused context
    context = {
        "user": user,
        "devices": user_devices,
        "groups": user_groups,
        "queries": user_queries,
        "mock_data": {
            "weather": {location_key: user_weather},
            "news": user_news,
            "stocks": user_stocks
        }
    }
    
    # Add summary information to make context clearer
    context["summary"] = {
        "user_name": user["name"],
        "location": user["preferences"]["location"],
        "home_id": home_id,
        "device_count": len(user_devices),
        "accessible_device_types": list(set(d["endpoint_categories"][0] for d in user_devices)),
        "preferred_news_categories": preferred_categories,
        "stock_watchlist": stock_watchlist,
        "spaces": [g["name"] for g in user_groups if g["type"] == "space"],
    }
    
    return context


def test_context_creation():
    """Test function to verify correct context creation for all users"""
    # Load data
    print("Loading data...")
    data = load_data()
    
    # Get all user IDs
    user_ids = [user["user_id"] for user in data["users"]]
    print(f"Found {len(user_ids)} users: {', '.join(user_ids)}")
    
    # Create and test context for each user
    for user_id in user_ids:
        print(f"\n{'='*80}")
        print(f"Testing context creation for user {user_id}")
        print(f"{'='*80}")
        
        try:
            # Create user context
            context = create_user_context(data, user_id)
            
            # Print summary information
            print(f"User: {context['summary']['user_name']} ({user_id})")
            print(f"Location: {context['summary']['location']}")
            print(f"Home ID: {context['summary']['home_id']}")
            print(f"Device count: {context['summary']['device_count']}")
            print(f"Accessible device types: {', '.join(context['summary']['accessible_device_types'])}")
            print(f"News preferences: {', '.join(context['summary']['preferred_news_categories'])}")
            print(f"Stock watchlist: {', '.join(context['summary']['stock_watchlist'])}")
            print(f"Home spaces: {', '.join(context['summary']['spaces'])}")
            
            # Test device permissions
            print("\nVerifying device permissions...")
            user_permissions = set(context['user']['permissions']['can_control'])
            for device in context['devices']:
                assert device['endpoint'] in user_permissions, f"Permission error for device {device['name']}"
                print(f"✓ Device {device['name']} (ID: {device['endpoint']}) - Permission verified")
            
            # Test data consistency
            assert len(context['devices']) == context['summary']['device_count'], "Device count mismatch"
            assert context['user']['name'] == context['summary']['user_name'], "Username mismatch"
            
            print("\nContext creation tests passed!")
            
        except Exception as e:
            print(f"Error creating context for user {user_id}: {e}")

def build_user_context_section(user_context: Dict) -> str:
    """
    Build the user context section of the prompt.
    
    Args:
        user_context: User context dictionary
        
    Returns:
        Formatted user context section
    """
    user = user_context["user"]
    summary = user_context["summary"]
    
    return f"""
    ## User Context
    - User: {summary['user_name']} (ID: {user['user_id']})
    - Location: {summary['location']}
    - Home ID: {summary['home_id']}
    - Devices: {summary['device_count']} devices of types {', '.join(summary['accessible_device_types'])}
    - News preferences: {', '.join(summary['preferred_news_categories'])}
    - Stock watchlist: {', '.join(summary['stock_watchlist'])}
    - Home spaces: {', '.join(summary['spaces'])}
    """

if __name__ == "__main__":
    """
    Main entry point when running this module directly.
    Tests the user context creation functionality.
    
    Usage: python -m utils.user_context
    """
    test_context_creation()
