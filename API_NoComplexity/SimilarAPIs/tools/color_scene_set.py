# Copyright SmartHomeEnv

"""
Uncertainty Manifestation: Confusion Between Light Color Control Functions

Description:
Developers working with the SmartHome API face significant confusion between multiple 
similarly-named functions that control different aspects of light appearance. The `color_set` 
function overlaps conceptually with other hypothetical lighting control functions like `light_color_set`, 
`color_temperature_set`, and this `color_scene_set` function. Each function manipulates light 
appearance but with subtly different behaviors, capabilities, and limitations. Developers struggle 
to determine which function to use for specific lighting scenarios, especially when dealing with 
devices that support multiple color-related features.
"""

import json
from typing import Any, Dict
from SmartHomeEnv.tool import Tool


def get_user_home_id(data: Dict[str, Any]) -> str:
    """Get the current user's home ID."""
    current_user = data.get("current_user", {})
    return current_user.get("home_id")


class ColorSceneSet(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "color_scene_set",
                "description": "Apply a predefined color scene to all compatible lights in a room. This tool changes multiple lights to create coordinated lighting effects based on predefined scenes like 'Movie', 'Relax', or 'Energize'.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "room_id": {
                            "type": "string",
                            "description": "Room identifier where the scene should be applied."
                        },
                        "scene_name": {
                            "type": "string",
                            "description": "Name of the predefined scene to apply. Supported scenes include: Movie, Relax, Energize, Reading, Nightlight, Party, and Focus."
                        }
                    },
                    "required": ["room_id", "scene_name"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], room_id: str, scene_name: str) -> str:
        """
        Apply a predefined color scene to all compatible lights in a room.
        
        Args:
            data: The data dictionary containing devices
            room_id: The room identifier
            scene_name: Name of the predefined scene (e.g., "Movie", "Relax", "Energize")
            
        Returns:
            A JSON string with the result of the operation
        """
        if not room_id:
            return json.dumps({
                "success": False,
                "message": "No room specified: The room_id parameter is empty or not provided"
            })
        
        if not scene_name:
            return json.dumps({
                "success": False,
                "message": "No scene specified: The scene_name parameter is empty or not provided"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        # Find the room
        rooms = data.get("rooms", {})
        room = rooms.get(room_id)
        
        if not room or room.get("home_id") != home_id:
            return json.dumps({
                "success": False,
                "message": f"Room not found: The specified room does not exist in the current user's home"
            })
        
        # Validate scene name
        valid_scenes = ["Movie", "Relax", "Energize", "Reading", "Nightlight", "Party", "Focus"]
        scene_name_lower = scene_name.lower()
        valid_scene = False
        
        for valid_scene_name in valid_scenes:
            if valid_scene_name.lower() == scene_name_lower:
                # Use the properly capitalized version
                scene_name = valid_scene_name
                valid_scene = True
                break
                
        if not valid_scene:
            return json.dumps({
                "success": False,
                "message": f"Scene not found: The specified scene name '{scene_name}' is not recognized. Valid scenes: {', '.join(valid_scenes)}"
            })
            
        # Find all compatible light devices in the room
        devices = data.get("devices", [])
        compatible_devices = []
        
        for device in devices:
            if (device.get("home_id") == home_id and 
                device.get("room_id") == room_id and 
                "color_scene_set" in device.get("supported_apis", [])):
                compatible_devices.append(device)
        
        if not compatible_devices:
            return json.dumps({
                "success": False,
                "message": f"No compatible devices: The room has no lights that support color scenes"
            })
        
        # Apply the scene to all compatible devices
        scene_configs = {
            "Movie": {"color": "blue", "brightness": 20, "color_temperature": 2700},
            "Relax": {"color": "amber", "brightness": 40, "color_temperature": 2200},
            "Energize": {"color": "daylight", "brightness": 100, "color_temperature": 6500},
            "Reading": {"color": "warm_white", "brightness": 80, "color_temperature": 3500},
            "Nightlight": {"color": "red", "brightness": 5, "color_temperature": 1800},
            "Party": {"color": "multi", "brightness": 90, "effects": "color_cycle"},
            "Focus": {"color": "cool_white", "brightness": 100, "color_temperature": 5000}
        }
        
        scene_config = scene_configs.get(scene_name)
        
        # Update all compatible devices with the scene configuration
        updated_devices = []
        failed_devices = []
        
        for device in compatible_devices:
            endpoint = device.get("endpoint")
            
            # Update device state
            success = False
            for i, d in enumerate(data["devices"]):
                if d["endpoint"] == endpoint:
                    if "state" not in data["devices"][i]:
                        data["devices"][i]["state"] = {}
                    
                    # Apply scene configuration
                    data["devices"][i]["state"]["active_scene"] = scene_name
                    
                    # Apply specific scene settings
                    if "color" in scene_config:
                        data["devices"][i]["state"]["color"] = scene_config["color"]
                    
                    if "brightness" in scene_config:
                        data["devices"][i]["state"]["brightness"] = scene_config["brightness"]
                    
                    if "color_temperature" in scene_config:
                        data["devices"][i]["state"]["color_temperature_kelvin"] = scene_config["color_temperature"]
                    
                    if "effects" in scene_config:
                        data["devices"][i]["state"]["effects"] = scene_config["effects"]
                    
                    success = True
                    break
            
            if success:
                updated_devices.append({
                    "endpoint": endpoint,
                    "name": device.get("name", endpoint),
                    "success": True
                })
            else:
                failed_devices.append({
                    "endpoint": endpoint,
                    "name": device.get("name", endpoint),
                    "success": False
                })
        
        if updated_devices:
            return json.dumps({
                "success": True,
                "message": f"Applied '{scene_name}' scene to {len(updated_devices)} devices in {room.get('name', room_id)}",
                "room": {
                    "id": room_id,
                    "name": room.get("name", "")
                },
                "scene": scene_name,
                "updated_devices": updated_devices,
                "failed_devices": failed_devices
            })
        else:
            return json.dumps({
                "success": False,
                "message": f"State update failure: No devices could be updated with the {scene_name} scene"
            })
