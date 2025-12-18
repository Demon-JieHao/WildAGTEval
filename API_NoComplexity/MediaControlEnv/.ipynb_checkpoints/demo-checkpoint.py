#!/usr/bin/env python3
# Copyright MediaControlEnv Demo

"""
Demonstration of MediaControlEnv functionality
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from MediaControlEnv import MediaControlEnv
from SmartHomeEnv import SmartHomeEnv
from common import register_environment, invoke_tool


def demo_basic_playback():
    """Demonstrate basic media playback functionality"""
    print("\n=== Basic Media Playback ===\n")
    
    # Search for media
    print("1. Searching for movies with 'Matrix' in the title...")
    result = invoke_tool("search_media", query="Matrix", media_type="movie")
    data = json.loads(result)
    if data["success"]:
        print(f"   Found {data['count']} results:")
        for item in data["results"]:
            print(f"   - {item['title']} ({item['year']}) - ID: {item['id']}")
    
    # Get media details
    print("\n2. Getting details for 'The Matrix'...")
    result = invoke_tool("get_media_details", media_id="movie1")
    data = json.loads(result)
    if data["success"]:
        details = data["details"]
        print(f"   Title: {details['title']}")
        print(f"   Year: {details['year']}")
        print(f"   Duration: {details['duration_formatted']}")
        print(f"   Genre: {', '.join(details['genre'])}")
        print(f"   Available on: {', '.join(details['services'])}")
    
    # Play media
    print("\n3. Playing 'The Matrix' on Living Room TV...")
    result = invoke_tool("play", endpoints=["4"], media_id="movie1")
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Check playback status
    print("\n4. Checking playback status...")
    result = invoke_tool("get_playback_status", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        status = data["results"][0]
        print(f"   Status: {status['status']}")
        print(f"   Playing: {status['title']}")
        print(f"   Position: {status['position_formatted']} / {status['duration_formatted']}")
        print(f"   Speed: {status['playback_speed']}x")


def demo_playback_control():
    """Demonstrate playback control features"""
    print("\n\n=== Playback Control ===\n")
    
    # Pause playback
    print("1. Pausing playback...")
    result = invoke_tool("pause", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Fast forward
    print("\n2. Fast forwarding 30 seconds...")
    result = invoke_tool("fast_forward", endpoints=["4"], seconds=30)
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Resume playback
    print("\n3. Resuming playback...")
    result = invoke_tool("resume", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Set playback speed
    print("\n4. Setting playback speed to 1.5x...")
    result = invoke_tool("set_playback_speed", endpoints=["4"], speed=1.5)
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Rewind
    print("\n5. Rewinding 10 seconds...")
    result = invoke_tool("rewind", endpoints=["4"], seconds=10)
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")


def demo_playlist_management():
    """Demonstrate playlist functionality"""
    print("\n\n=== Playlist Management ===\n")
    
    # Get existing playlists
    print("1. Getting user playlists...")
    result = invoke_tool("get_playlists")
    data = json.loads(result)
    if data["success"]:
        print(f"   Found {data['count']} playlists:")
        for playlist in data["playlists"]:
            print(f"   - {playlist['title']} (ID: {playlist['id']}) - {playlist['item_count']} items")
    
    # Create new playlist
    print("\n2. Creating a new playlist...")
    result = invoke_tool("create_playlist", title="My Favorites")
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['message']}")
        new_playlist_id = data["playlist_id"]
    
    # Search for music
    print("\n3. Searching for music...")
    result = invoke_tool("search_media", query="", media_type="song", limit=5)
    data = json.loads(result)
    if data["success"]:
        print(f"   Found {data['count']} songs:")
        song_ids = []
        for item in data["results"]:
            print(f"   - {item['title']} by {item['artist']} (ID: {item['id']})")
            song_ids.append(item['id'])
    
    # Add songs to playlist
    if song_ids:
        print("\n4. Adding songs to the new playlist...")
        result = invoke_tool("add_to_playlist", playlist_id=new_playlist_id, media_ids=song_ids[:2])
        data = json.loads(result)
        if data["success"]:
            print(f"   ✓ {data['message']}")


def demo_music_playback():
    """Demonstrate music playback with shuffle"""
    print("\n\n=== Music Playback ===\n")
    
    # Play a playlist
    print("1. Playing playlist on Living Room TV...")
    result = invoke_tool("play", endpoints=["4"], media_id="playlist1")
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Enable shuffle
    print("\n2. Enabling shuffle mode...")
    result = invoke_tool("shuffle", endpoints=["4"], enabled=True)
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Skip to next track
    print("\n3. Skipping to next track...")
    result = invoke_tool("next", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Go to previous track
    print("\n4. Going back to previous track...")
    result = invoke_tool("previous", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Stop playback
    print("\n5. Stopping playback...")
    result = invoke_tool("stop", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")


def demo_integration_with_smarthome():
    """Demonstrate integration with SmartHomeEnv"""
    print("\n\n=== Integration with SmartHomeEnv ===\n")
    print("This demonstrates how MediaControlEnv works with SmartHomeEnv\n")
    
    # Use SmartHomeEnv to turn on TV
    print("1. Using SmartHomeEnv to turn on TV...")
    result = invoke_tool("power_on", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Use MediaControlEnv to play content
    print("\n2. Using MediaControlEnv to play a movie...")
    result = invoke_tool("play", endpoints=["4"], media_id="movie2")
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Use SmartHomeEnv to adjust volume
    print("\n3. Using SmartHomeEnv to set volume to 35%...")
    result = invoke_tool("volume_adjust", endpoints=["4"], volume=35)
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Use MediaControlEnv to pause
    print("\n4. Using MediaControlEnv to pause playback...")
    result = invoke_tool("pause", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")
    
    # Use SmartHomeEnv to turn off TV
    print("\n5. Using SmartHomeEnv to turn off TV...")
    result = invoke_tool("power_off", endpoints=["4"])
    data = json.loads(result)
    if data["success"]:
        print(f"   ✓ {data['results'][0]['message']}")


def main():
    """Run the MediaControlEnv demonstration"""
    print("=== MediaControlEnv Demonstration ===")
    print("Showcasing media control capabilities\n")
    
    # Create and register environments
    print("Setting up environments...")
    media_control = MediaControlEnv()
    smart_home = SmartHomeEnv()
    
    register_environment("MediaControlEnv", media_control)
    register_environment("SmartHomeEnv", smart_home)
    
    # Set current user
    media_control.set_current_user("user1")
    smart_home.set_current_user("user1")
    print("✓ Environments ready")
    
    # Run demonstrations
    demo_basic_playback()
    demo_playback_control()
    demo_playlist_management()
    demo_music_playback()
    demo_integration_with_smarthome()
    
    print("\n\n=== Demo Complete ===")
    print("MediaControlEnv provides comprehensive media control for your smart home!")


if __name__ == "__main__":
    main()
