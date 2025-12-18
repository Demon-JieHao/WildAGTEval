## Device Deactivation

This function provides a comprehensive device deactivation capability that goes beyond simple power state changes. It's designed for situations requiring full system shutdown of devices with complete process termination.

### Key Features

- Completely deactivates devices in the system
- Cancels all scheduled operations associated with the device
- Terminates all background processes running on the device
- Places devices into configurable power-saving modes
- Supports multiple deactivation modes with varying power/restart time tradeoffs
- Performs a complete system-level shutdown rather than just power state change
- May require longer restart time when reactivated due to full system shutdown

### Deactivation Modes

- **Standard**: Balances power savings with restart time
- **Deep**: Maximizes power savings but increases restart time
- **Temporary**: Optimizes for quick reactivation with minimal power savings

### Parameters

- **endpoints**: List of device endpoint IDs to deactivate
- **deactivation_mode**: Mode of deactivation ("standard", "deep", "temporary")

### Error Cases

- **No devices specified**: The endpoints parameter is empty or not provided
- **Invalid deactivation mode**: The specified mode is not supported
- **Device not found**: The specified endpoint does not exist
- **API not supported**: The device does not support the deactivation API
- **State update failure**: The device state could not be updated
