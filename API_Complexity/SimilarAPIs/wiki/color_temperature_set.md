## Color Temperature Setting

Color temperature setting is designed specifically for adjusting the white light spectrum of lighting devices. This function allows precise control over the warmth or coolness of white light, measured in Kelvin units.

### Key Features

- Adjusts lights along the white light spectrum from warm to cool
- Controls the temperature appearance rather than the hue of light
- Can be specified using either technical Kelvin values or human-readable descriptive terms
- Optimized for managing white light characteristics in compatible devices
- Provides fine-grained control over the "feel" of lighting environments

### Temperature Options

- **Warm (2700K)**: Yellowish, cozy lighting similar to traditional incandescent bulbs
- **Neutral (4000K)**: Balanced white light for general use
- **Cool (5000K)**: Crisp white light with slightly blue tint
- **Daylight (6500K)**: Bluish white light mimicking natural daylight

### Parameters

- **endpoints**: List of device endpoint IDs to adjust
- **temperature**: Color temperature as a Kelvin value (2000-6500) or descriptive string ('warm', 'neutral', 'cool', 'daylight')

### Error Cases

- **No devices specified**: The endpoints parameter is empty or not provided
- **No temperature specified**: The temperature parameter is empty or not provided
- **Invalid temperature**: The specified temperature is outside the valid range (2000-6500K)
- **Device not found**: The specified endpoint does not exist in the user's home
- **API not supported**: The device does not support color temperature adjustment
- **State update failure**: The device state could not be updated
