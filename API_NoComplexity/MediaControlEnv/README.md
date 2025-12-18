# MediaControlEnv

Media Control Environment for managing media playback across devices in a smart home ecosystem.

## Overview

MediaControlEnv provides comprehensive media control capabilities for smart TVs, speakers, and other media-enabled devices. It integrates seamlessly with SmartHomeEnv to create a complete smart home media experience.

## Key Features

- **Media Playback Control**: Play, pause, resume, stop media across devices
- **Navigation**: Skip tracks, fast forward, rewind
- **Content Discovery**: Search media library, get details about content
- **Playlist Management**: Create and manage user-specific playlists
- **Advanced Controls**: Playback speed adjustment, shuffle mode
- **Multi-device Support**: Control media on multiple devices simultaneously

## Available Tools

### Basic Playback (4 tools)
- `play` - Start playing media on devices
- `pause` - Pause current playback
- `resume` - Resume paused playback
- `stop` - Stop playback completely

### Navigation (4 tools)
- `next` - Skip to next track/episode
- `previous` - Go to previous track/episode
- `fast_forward` - Skip forward (default 30 seconds)
- `rewind` - Skip backward (default 10 seconds)

### Content Management (3 tools)
- `search_media` - Search for media by title
- `get_media_details` - Get detailed information about media
- `get_playback_status` - Check current playback status

### Playlist Operations (3 tools)
- `create_playlist` - Create a new playlist
- `add_to_playlist` - Add media to playlist
- `get_playlists` - List user playlists

### Advanced Features (2 tools)
- `set_playback_speed` - Adjust playback speed (0.5x-2x)
- `shuffle` - Toggle shuffle mode

## Integration with SmartHomeEnv

MediaControlEnv works together with SmartHomeEnv:
- SmartHomeEnv handles device power and volume control
- MediaControlEnv handles media-specific operations

### Example Workflow
```python
# 1. Turn on TV using SmartHomeEnv
invoke_tool("power_on", endpoints=["4"])

# 2. Search for content using MediaControlEnv
invoke_tool("search_media", query="Matrix", media_type="movie")

# 3. Play the movie
invoke_tool("play", endpoints=["4"], media_id="movie1")

# 4. Adjust volume using SmartHomeEnv
invoke_tool("volume_adjust", endpoints=["4"], volume=40)

# 5. Pause when needed using MediaControlEnv
invoke_tool("pause", endpoints=["4"])
```

## Media Database

The environment includes a pre-populated media database with:
- Movies (The Matrix, Inception, etc.)
- TV Shows (Stranger Things, Game of Thrones, etc.)
- Music (songs and albums)
- User playlists

## Device Compatibility

Media devices must have appropriate capabilities:
- **TVs**: Support both video and audio content
- **Speakers**: Support only audio content
- **Media Players**: Typically support all content types

The system automatically checks device compatibility before playback.

## Usage

```python
from MediaControlEnv import MediaControlEnv

# Create environment
env = MediaControlEnv()

# Set current user
env.set_current_user("user1")

# Search for media
result = env.invoke_tool("search_media", query="Matrix")

# Play on device
result = env.invoke_tool("play", endpoints=["4"], media_id="movie1")

# Check playback status
result = env.invoke_tool("get_playback_status", endpoints=["4"])
```

## Error Handling

The environment handles common error scenarios:
- Device not found or offline
- Incompatible media type for device
- No active playback for control operations
- Playlist ownership restrictions
- Invalid parameter values

## Rules

See `rules.py` for the complete list of operational rules that guide the environment's behavior.

## Wiki

For detailed documentation, see `wiki.md`.
