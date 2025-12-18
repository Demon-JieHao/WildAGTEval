## Color Scene Setting

Color scene setting is designed specifically for applying coordinated lighting effects to entire rooms. This function handles the application of predefined scenes to all compatible lights in a specified room.

### Key Features

- Applies predefined lighting scenes to an entire room at once
- Creates coordinated lighting environments across multiple devices
- Each scene controls multiple lighting parameters simultaneously (color, brightness, temperature)
- Designed for room-wide ambiance rather than individual light control
- Supports specialized scenes for different activities and moods

### Supported Scenes

- **Movie**: Dim blue lighting optimized for movie watching
- **Relax**: Warm amber glow at medium brightness for relaxation
- **Energize**: Bright daylight temperature lighting to increase alertness
- **Reading**: Moderately bright warm white lighting for comfortable reading
- **Nightlight**: Very dim red lighting for minimal disruption at night
- **Party**: Bright cycling colors for festive environments
- **Focus**: Bright cool white lighting to enhance concentration

### Parameters

- **room_id**: Room identifier where the scene should be applied
- **scene_name**: Name of the predefined scene to apply

### Error Cases

- **No room specified**: The room_id parameter is empty or not provided
- **No scene specified**: The scene_name parameter is empty or not provided
- **Room not found**: The specified room does not exist in the current user's home
- **Scene not found**: The specified scene name is not recognized
- **No compatible devices**: The room has no lights that support color scenes
- **State update failure**: No devices could be updated with the scene
