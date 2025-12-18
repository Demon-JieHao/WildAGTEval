# Smart Home Data

## Data Files
- `devices.json`: A database of smart home devices with their endpoints, names, categories, supported APIs, and group memberships
- `groups.json`: A database of device groups and spaces
- `user_context.json`: User context information, such as the user's current location

## Data Structure

### Devices
Each device has:
- `endpoint`: Unique identifier for the device
- `name`: Human-readable name of the device
- `alternate_names`: Alternative names for the device
- `endpoint_categories`: Categories the device belongs to (e.g., LIGHT, TV, THERMOSTAT)
- `supported_apis`: APIs that can be called on this device
- `groups`: Groups the device belongs to

### Groups
Each group has:
- `id`: Unique identifier for the group
- `name`: Human-readable name of the group
- `type`: Type of group ("space" for rooms with Echo devices, "device_group" for other groups)
- `has_echo_device`: Whether the group has an Echo device

### User Context
Contains information about the user's current context:
- `current_space`: The space where the user is currently located
