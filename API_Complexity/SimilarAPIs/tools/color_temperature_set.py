# Copyright SmartHomeEnv

"""
Uncertainty Manifestation: Confusion Between Light Color Control Functions

Description:
Developers working with the SmartHome API face significant confusion between multiple 
similarly-named functions that control different aspects of light appearance. The `color_set` 
function overlaps conceptually with other hypothetical lighting control functions like `light_color_set`, 
`color_scene_set`, and this `color_temperature_set` function. Each function manipulates light 
appearance but with subtly different behaviors, capabilities, and limitations. Developers struggle 
to determine which function to use for specific lighting scenarios, especially when dealing with 
devices that support multiple color-related features.
"""

import json
from typing import Any, Dict, List, Union
from SmartHomeEnv.tool import Tool


def get_user_home_id(data: Dict[str, Any]) -> str:
    """Get the current user's home ID."""
    current_user = data.get("current_user", {})
    return current_user.get("home_id")


def find_device_by_endpoint(data: Dict[str, Any], endpoint: str, home_id: str = None) -> Dict[str, Any]:
    """Find a device by endpoint ID, optionally filtered by home ID."""
    devices = data.get("devices", [])
    for device in devices:
        if device["endpoint"] == endpoint and (home_id is None or device.get("home_id") == home_id):
            return device
    return None


# Convert descriptive temperature to Kelvin value
def get_kelvin_value(temp_descriptor: str) -> int:
    """Convert descriptive temperature term to Kelvin value."""
    temp_map = {
        "warm": 2700,
        "neutral": 4000,
        "cool": 5000,
        "daylight": 6500
    }
    return temp_map.get(temp_descriptor.lower(), 4000)  # Default to neutral if not recognized


class ColorTemperatureSet(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function", 
            "function": {
                "name": "color_temperature_set",
                "description": "Set the color temperature of one or more light devices. This tool adjusts lights along the white light spectrum from warm (yellowish) to cool (bluish) white, specified either in Kelvin or using descriptive terms.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to adjust. Each endpoint must correspond to a light device that supports color temperature adjustment."
                        },
                        "temperature": {
                            "type": "string",
                            "description": "Color temperature as a numeric Kelvin value (2000-6500) or descriptive string ('warm', 'neutral', 'cool', 'daylight')."
                        }
                    },
                    "required": ["endpoints", "temperature"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], temperature: Union[int, str]) -> str:
        """
        Set the color temperature of one or more light devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to adjust
            temperature: Color temperature in Kelvin (2000-6500) or descriptive string
                        ("warm", "neutral", "cool", "daylight")
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified: The endpoints parameter is empty or not provided"
            })
        
        if temperature is None:
            return json.dumps({
                "success": False,
                "message": "No temperature specified: The temperature parameter is empty or not provided"
            })
        
        # Convert temperature to numeric Kelvin value if it's a descriptive string
        temp_kelvin = temperature
        temp_descriptor = None
        
        if isinstance(temperature, str):
            if temperature.isdigit():
                temp_kelvin = int(temperature)
            else:
                temp_descriptor = temperature.lower()
                temp_kelvin = get_kelvin_value(temp_descriptor)
        
        # Validate kelvin range
        if temp_kelvin < 2000 or temp_kelvin > 6500:
            return json.dumps({
                "success": False,
                "message": f"Invalid temperature: The specified temperature ({temperature}) is outside the valid range (2000-6500K)"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            
            if not device:
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"Device not found: The specified endpoint {endpoint} does not exist in the current user's home"
                })
                continue
            
            # Check if the device supports color temperature adjustment
            if "color_temperature_set" not in device.get("supported_apis", []):
                results.append({
                    "endpoint": endpoint,
                    "name": device.get("name", endpoint),
                    "success": False,
                    "message": f"API not supported: The device {device.get('name', endpoint)} does not support the color_temperature_set API"
                })
                continue
            
            # Update device state
            success = False
            for i, d in enumerate(data["devices"]):
                if d["endpoint"] == endpoint and (home_id is None or d.get("home_id") == home_id):
                    if "state" not in data["devices"][i]:
                        data["devices"][i]["state"] = {}
                    
                    # Store both the numeric and descriptive values if available
                    data["devices"][i]["state"]["color_temperature_kelvin"] = temp_kelvin
                    if temp_descriptor:
                        data["devices"][i]["state"]["color_temperature_descriptor"] = temp_descriptor
                    
                    success = True
                    break
            
            if success:
                temp_display = f"{temp_kelvin}K"
                if temp_descriptor:
                    temp_display = f"{temp_descriptor} ({temp_kelvin}K)"
                    
                results.append({
                    "endpoint": endpoint,
                    "name": device.get("name", endpoint),
                    "success": True,
                    "message": f"Set {device.get('name', endpoint)} color temperature to {temp_display}",
                    "temperature": {
                        "kelvin": temp_kelvin,
                        "descriptor": temp_descriptor
                    }
                })
            else:
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"State update failure: The device state could not be updated due to a system error"
                })
        
        return json.dumps({
            "success": any(result["success"] for result in results),
            "results": results
        })
