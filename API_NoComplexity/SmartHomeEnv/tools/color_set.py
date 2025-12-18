# Copyright SmartHomeEnv

import json
from typing import Any, Dict, List
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class ColorSet(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], color: str) -> str:
        """
        Set the color of one or more light devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to adjust
            color: Color name or hex value to set
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        if not color:
            return json.dumps({
                "success": False,
                "message": "No color specified"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        # Common color names mapping (in a real implementation, this would be more extensive)
        color_map = {
            "red": "#FF0000",
            "green": "#00FF00",
            "blue": "#0000FF",
            "yellow": "#FFFF00",
            "orange": "#FFA500",
            "purple": "#800080",
            "pink": "#FFC0CB",
            "white": "#FFFFFF",
            "black": "#000000",
            "gray": "#808080",
            "brown": "#A52A2A",
            "aqua": "#00FFFF",
            "navy": "#000080",
            "teal": "#008080",
            "olive": "#808000",
            "lime": "#00FF00",
            "maroon": "#800000",
            "silver": "#C0C0C0",
        }
        
        # Convert color name to hex if it's a known color
        color_value = color_map.get(color.lower(), color)
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "color_set" in device["supported_apis"]:
                # Update the device state directly in the data dictionary
                for i, d in enumerate(data["devices"]):
                    if d["endpoint"] == endpoint and (home_id is None or d["home_id"] == home_id):
                        if "state" not in data["devices"][i]:
                            data["devices"][i]["state"] = {}
                        data["devices"][i]["state"]["color"] = color_value
                        success = True
                        break
                else:
                    success = False
                
                if success:
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": True,
                        "message": f"Set {device['name']} color to {color}",
                        "color": color_value
                    })
                else:
                    results.append({
                        "endpoint": endpoint,
                        "success": False,
                        "message": f"Failed to update state for device with endpoint {endpoint}"
                    })
            else:
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"Device with endpoint {endpoint} not found or does not support color setting"
                })
        
        return json.dumps({
            "success": any(result["success"] for result in results),
            "results": results
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "color_set",
                "description": "Set the color of one or more light devices. This tool changes the color of smart lights that support color adjustment. Colors can be specified using common color names (red, blue, green, etc.), temperature descriptions (warm, cool), or hex color values (#RRGGBB).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to adjust. Each endpoint must correspond to a light device that supports the color_set API."
                        },
                        "color": {
                            "type": "string",
                            "description": "Color name (e.g., 'red', 'blue', 'warm', 'cool'). Supported color names include: red, green, blue, yellow, orange, purple, pink, white, black, gray, brown, aqua, navy, teal, olive, lime, maroon, and silver"
                        }
                    },
                    "required": ["endpoints", "color"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "No color specified: The color parameter is empty or not provided.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the color_set API (not all lights support color adjustment).",
                    "State update failure: The device state could not be updated due to a system error."
                ]
            }
        }
