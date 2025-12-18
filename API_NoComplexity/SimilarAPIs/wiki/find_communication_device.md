## Communication Device Finder

This function is designed for finding communication-capable devices across multiple communication modalities. It serves as a comprehensive device discovery tool that identifies all devices supporting any form of electronic communication.

### Key Features

- Locates devices that support a wide range of communication capabilities
- Searches for devices supporting various communication types (voice calls, messaging, video conferencing, intercom)
- Identifies all compatible communication hardware within the user's environment
- Returns detailed information about communication features each device supports
- Provides a unified interface for discovering multi-modal communication devices
- Includes availability status of each discovered device

### Parameters

- **device_types**: Optional filter for specific types of communication devices
- **capabilities**: Optional filter for specific communication capabilities
- **room_id**: Optional room identifier to limit the search to a specific location

### Error Cases

- **No user is currently logged in**: Authentication is required to access device information
- **User information not found**: The system cannot locate device information for the current user
