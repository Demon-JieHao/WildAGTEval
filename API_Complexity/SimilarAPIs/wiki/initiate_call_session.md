## Call Session Management

This function is designed for establishing sophisticated multi-party communication sessions in a cloud communication platform. It creates structured communication environments with advanced collaboration features.

### Key Features

- Creates formal communication sessions with persistent connection management
- Supports multiple concurrent participants in a single call session
- Offers advanced session features including recording and screen sharing
- Generates unique session identifiers and join URLs for participants
- Provides differentiated session types for various collaboration needs
- Supports virtual backgrounds for enhanced visual presentation
- Maintains session state and participant tracking

### Session Types

- **Standard**: Basic communication session between participants
- **Conference**: Enhanced session with moderation features and larger participant capacity
- **Webinar**: Presentation-oriented session with dedicated presenter and audience roles

### Parameters

- **recipient_id**: ID of the recipient to call (user ID)
- **phone_number**: Phone number to call (alternative to recipient_id)
- **session_type**: Type of session ('standard', 'conference', 'webinar')
- **with_recording**: Whether to record the call session
- **virtual_background**: Optional background image URL for video calls

### Error Cases

- **No user logged in**: No user is currently logged in to create sessions
- **Invalid session type**: The specified session type is not supported
- **Recording not permitted**: The user does not have permission to record calls
- **Session limit reached**: The user has reached their maximum concurrent sessions
- **Invalid recipient**: The specified recipient ID does not exist in the system
