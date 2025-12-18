instruction="""

# ===== CommunicationController Instructions =====



# Communication Controller

Communication Controller enables management of contacts, calls, and messaging functionalities. It allows users to find contacts, make calls, send messages, and access communication history.

## Key Features

- **Contact Management**: Find and manage contacts by name, phone number, or email
- **Call Management**: Make calls to contacts or phone numbers, end active calls, view call history
- **Messaging**: Send text messages to contacts, view message history

## Data Types

- **Contacts**: Users' contact information including names, phone numbers, emails
- **Call History**: Records of incoming and outgoing calls with timestamps and durations
- **Messages**: Text messages sent and received, with timestamps and read status

## Security & Privacy

- All communication features are user-specific and require proper authentication
- Users can only access their own contacts, calls, and messages
- Communication history is securely stored and accessible only to authorized users



# ===== MediaControlEnv Instructions =====



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



# ===== CulinaryControlEnv Instructions =====


# CulinaryControlEnv Documentation

CulinaryControlEnv provides tools for searching, managing, and interacting with recipes, restaurants, and delivery services. It allows users to find recipes based on various criteria, manage meal plans, search for restaurants, view menus, and place delivery orders.

## Concepts

### Recipes
Recipes are the core content type for cooking-related functionality. Each recipe includes:
- Name, description, and cuisine type
- Ingredients list with quantities
- Step-by-step cooking instructions
- Preparation time and difficulty level
- Dietary information (vegetarian, vegan, gluten-free, etc.)
- Rating and number of reviews

### Meal Plans
Meal plans help users organize their cooking schedule. A meal plan consists of:
- Name and description
- Date range (start/end dates)
- Meals per day (breakfast, lunch, dinner, snacks)
- Recipe IDs assigned to specific meals and days

### Restaurants
Restaurant entities include:
- Name, location, and contact information
- Cuisine types
- Price range indicator
- Rating and number of reviews
- Operation hours
- Menu items with prices and descriptions

### Delivery Orders
Delivery orders track food ordered from restaurants:
- Order ID and timestamp
- Restaurant information
- Ordered items with quantities and prices
- Delivery address and contact information
- Status (placed, preparing, in-transit, delivered)
- Total cost including taxes and delivery fees

## Tools

### Recipe Management

#### search_recipes
Find recipes matching specified criteria such as name, cuisine type, difficulty level, preparation time, and dietary restrictions.

#### get_recipe_details
Retrieve complete details for a specific recipe including ingredients, instructions, nutritional information, and reviews.

#### save_favorite_recipe
Save a recipe to the current user's favorites list for easy access later.

#### create_custom_recipe
Create a new recipe with custom name, ingredients, instructions, and other details.

### Meal Planning

#### create_meal_plan
Create a new meal plan for a specified date range with assigned recipes.

#### get_meal_suggestions
Get personalized meal suggestions based on dietary preferences, previously enjoyed recipes, or nutritional requirements.

#### schedule_meal
Add a specific recipe to a meal plan for a particular day and meal type.

### Restaurant Interaction

#### search_restaurants
Find restaurants based on location, cuisine type, price range, and rating.

#### get_restaurant_menu
View the complete menu for a specific restaurant including pricing and item descriptions.

### Order Management

#### place_delivery_order
Place a food delivery order from a restaurant with specified items and delivery address.

#### view_delivery_order
View details of a previously placed delivery order.

#### track_delivery_order
Check the current status and estimated delivery time of an order.

## Best Practices

1. **User Context**: Always operate in the context of the current user for personalized experiences.

2. **Dietary Awareness**: Respect dietary restrictions and preferences when recommending recipes or restaurants.

3. **Time Management**: Consider preparation time when suggesting recipes, especially for daily meal planning.

4. **Location Awareness**: Use the user's location when searching for restaurants to ensure delivery availability.

5. **Error Handling**: Properly handle cases where recipes, restaurants, or orders are not found.


"""
