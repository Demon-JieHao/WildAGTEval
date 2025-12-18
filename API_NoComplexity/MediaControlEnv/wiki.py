# Copyright MediaControlEnv

WIKI = """
# MediaControlEnv Wiki

## Overview

MediaControlEnv is a media control environment that manages playback across various devices. It integrates seamlessly with SmartHomeEnv to provide comprehensive media control capabilities for smart TVs, speakers, and other media-enabled devices.

## Key Concepts

### Media Types
- **Movies**: Full-length films with metadata like year, genre, and streaming services
- **TV Shows**: Series with seasons and episodes
- **Music**: Songs and albums with artist information
- **Playlists**: User-created collections of media items

### Device Categories
- **TV**: Devices that support both audio and video playback
- **SPEAKER**: Audio-only playback devices
- **MEDIA_PLAYER**: Devices that can play various media types

### Playback States
- **idle**: No media is currently loaded
- **playing**: Media is actively playing
- **paused**: Media is temporarily stopped
- **stopped**: Media playback has ended

## Integration with SmartHomeEnv

MediaControlEnv works together with SmartHomeEnv:
1. SmartHomeEnv handles basic device control (power, volume)
2. MediaControlEnv handles media-specific operations (play, pause, playlists)

Example workflow:
```
1. Use SmartHomeEnv to turn on TV: power_on(endpoints=["4"])
2. Use MediaControlEnv to play content: play(endpoints=["4"], media_id="movie1")
3. Use SmartHomeEnv to adjust volume: volume_adjust(endpoints=["4"], volume=40)
4. Use MediaControlEnv to pause: pause(endpoints=["4"])
```

## Available Tools

### Basic Playback Control
- **play**: Start playing media on devices
- **pause**: Temporarily stop playback
- **resume**: Continue paused playback
- **stop**: Completely stop playback

### Navigation
- **next**: Skip to next item in queue/playlist
- **previous**: Go to previous item
- **fast_forward**: Skip forward in current media
- **rewind**: Skip backward in current media

### Advanced Controls
- **set_playback_speed**: Adjust playback speed (0.5x-2x)
- **shuffle**: Toggle random playback order
- **loop**: Set repeat mode (off/one/all)

### Content Management
- **search_media**: Find media by title, type, or genre
- **search_by_artist**: Find music content by artist name
- **get_media_details**: Get detailed information about media
- **get_playback_status**: Check what's currently playing

### Playlist Operations
- **create_playlist**: Create a new playlist
- **add_to_playlist**: Add media to existing playlist
- **get_playlists**: List user's playlists

### Queue Management
- **add_to_queue**: Add media to playback queue
- **get_queue**: View current playback queue

## Media Database

The system includes a pre-populated media database with:
- Popular movies from various genres
- TV shows with multiple seasons
- Music tracks and albums
- User-created playlists

Each media item includes:
- Unique ID for reference
- Title and type
- Duration information
- Available streaming services
- Genre classifications

## Device Compatibility

Not all devices support all media types:
- TVs can play both video and audio content
- Speakers can only play audio content
- Media players typically support all content types

The system automatically checks compatibility before playback.

## Streaming Services

Media items are tagged with available streaming services:
- Video: Netflix, HBO Max, Amazon Prime Video
- Audio: Spotify, Apple Music, Amazon Music

## Error Handling

Common error scenarios:
- Device doesn't support the media type
- Media not found in database
- No active playback to control
- Playlist ownership restrictions
- Device offline or unavailable

## Best Practices

1. Always check device capabilities before attempting playback
2. Use search_media to find content before playing
3. Save frequently used content to playlists
4. Check playback status before issuing control commands
5. Consider device location when setting up multi-room audio

## Example Scenarios

### Movie Night
```
1. Turn on TV (SmartHomeEnv)
2. Search for movie by title
3. Play selected movie
4. Adjust volume as needed (SmartHomeEnv)
5. Pause for breaks
6. Resume when ready
```

### Music Throughout the House
```
1. Turn on multiple speakers (SmartHomeEnv)
2. Create or select a playlist
3. Play playlist on all speakers
4. Control playback from any room
5. Adjust individual speaker volumes (SmartHomeEnv)
```

### Binge Watching
```
1. Search for TV show
2. Play from specific season/episode
3. Use next to go to next episode
4. Show automatically continues through season
5. Track progress across sessions
```

## Technical Details

- Playback state is maintained per device
- Position tracking enables resume functionality
- Queue system allows pre-loading next items
- Playlists are user-specific
- Media database can be extended with new content

## Future Enhancements

Potential additions to the system:
- Voice control integration
- Recommendation engine
- Parental controls
- Download for offline playback
- Social sharing features
- Advanced search filters
- Custom media metadata
"""
