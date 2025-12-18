# Copyright SmartHomeEnv

"""
Uncertainty Manifestation: Mode Control Confusion Between Thermostats and HVAC Systems

Description:
Developers would be confused between the `mode_set` function for thermostats and this function 
`hvac_mode_set` that appears similar but controls the broader HVAC system with different capabilities 
and behaviors. While `mode_set` controls individual thermostat devices with simple modes like "heat" 
and "cool", this `hvac_mode_set` function controls the central HVAC system with more complex modes 
like "zoned", "circulation", and "dehumidify". This creates confusion because both functions appear 
to control temperature settings but operate at different levels of the home climate system with 
different available modes and behaviors.
"""

import json
from typing import Any, Dict, Optional, List
from SmartHomeEnv.tool import Tool


def get_user_home_id(data: Dict[str, Any]) -> str:
    """Get the current user's home ID."""
    current_user = data.get("current_user", {})
    return current_user.get("home_id")


def find_hvac_system_by_id(data: Dict[str, Any], system_id: str) -> Dict[str, Any]:
    """Find an HVAC system by ID."""
    for system in data.get("hvac_systems", []):
        if system.get("system_id") == system_id:
            return system
    return None


class HVACModeSet(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "hvac_mode_set",
                "description": "Set the operating mode of a central HVAC system. This tool changes how the entire home climate system operates, controlling air handlers, compressors, and zone controllers. Available modes include standard (normal operation), zoned (different settings per zone), circulation (fan only), dehumidify (moisture removal without cooling), and off (system disabled).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "system_id": {
                            "type": "string",
                            "description": "ID of the central HVAC system to control."
                        },
                        "hvac_mode": {
                            "type": "string",
                            "enum": ["standard", "zoned", "circulation", "dehumidify", "off"],
                            "description": "Mode to set for the HVAC system operation."
                        },
                        "zone_settings": {
                            "type": "object",
                            "description": "Optional settings for specific zones when in 'zoned' mode."
                        }
                    },
                    "required": ["system_id", "hvac_mode"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], system_id: str, hvac_mode: str, 
              zone_settings: Optional[Dict[str, Any]] = None) -> str:
        """
        Set the operating mode of the central HVAC system.
        
        Args:
            data: The data dictionary containing HVAC systems
            system_id: ID of the central HVAC system to control
            hvac_mode: Mode to set (e.g., "zoned", "circulation", "dehumidify", "standard", "off")
            zone_settings: Optional settings for specific zones when in "zoned" mode
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if not system_id:
            return json.dumps({
                "success": False,
                "message": "No system ID specified: The system_id parameter is empty or not provided"
            })
            
        if not hvac_mode:
            return json.dumps({
                "success": False,
                "message": "No mode specified: The hvac_mode parameter is empty or not provided"
            })
            
        # Validate mode
        valid_modes = ["standard", "zoned", "circulation", "dehumidify", "off"]
        if hvac_mode not in valid_modes:
            return json.dumps({
                "success": False,
                "message": f"Invalid mode: The specified mode '{hvac_mode}' is not one of the valid options: {', '.join(valid_modes)}"
            })
            
        # Find the HVAC system
        system = find_hvac_system_by_id(data, system_id)
        if not system:
            return json.dumps({
                "success": False,
                "message": f"System not found: The specified system_id '{system_id}' does not exist"
            })
            
        # If setting to zoned mode, validate zone settings
        if hvac_mode == "zoned" and (not zone_settings or not isinstance(zone_settings, dict)):
            return json.dumps({
                "success": False,
                "message": "Zone configuration error: When setting to 'zoned' mode, zone_settings must be provided"
            })
            
        if hvac_mode == "zoned" and zone_settings:
            # Make sure all specified zones exist in the system
            system_zones = system.get("zones", [])
            for zone_id in zone_settings.keys():
                if zone_id not in [z.get("zone_id") for z in system_zones]:
                    return json.dumps({
                        "success": False,
                        "message": f"Zone configuration error: Zone '{zone_id}' does not exist in this HVAC system"
                    })
        
        # Update the system mode
        for i, sys in enumerate(data.get("hvac_systems", [])):
            if sys.get("system_id") == system_id:
                data["hvac_systems"][i]["mode"] = hvac_mode
                # If zoned mode, update zone settings
                if hvac_mode == "zoned" and zone_settings:
                    data["hvac_systems"][i]["zone_settings"] = zone_settings
                break
        
        # Return success response with details
        result = {
            "success": True,
            "message": f"HVAC system '{system.get('name', system_id)}' set to '{hvac_mode}' mode"
        }
        
        # Add zone information if in zoned mode
        if hvac_mode == "zoned" and zone_settings:
            result["zone_settings"] = zone_settings
            
        return json.dumps(result)
