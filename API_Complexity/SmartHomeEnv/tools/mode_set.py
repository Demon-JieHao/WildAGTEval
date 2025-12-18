# Copyright SmartHomeEnv

import json
from typing import Any, Dict, List
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class ModeSet(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], mode: str) -> str:
        """
        Set the mode of one or more thermostat devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to adjust
            mode: Mode to set (e.g., "heat", "cool", "auto", "off")
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        if not mode:
            return json.dumps({
                "success": False,
                "message": "No mode specified"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        # Valid thermostat modes
        valid_modes = ["heat", "cool", "auto", "off", "eco"]
        
        # Check if the mode is valid
        if mode.lower() not in valid_modes:
            return json.dumps({
                "success": False,
                "message": f"Invalid mode: {mode}. Valid modes are: {', '.join(valid_modes)}"
            })
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "mode_set" in device["supported_apis"]:
                # Update the device state directly in the data dictionary
                for i, d in enumerate(data["devices"]):
                    if d["endpoint"] == endpoint and (home_id is None or d["home_id"] == home_id):
                        if "state" not in data["devices"][i]:
                            data["devices"][i]["state"] = {}
                        data["devices"][i]["state"]["mode"] = mode.lower()
                        success = True
                        break
                else:
                    success = False
                
                if success:
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": True,
                        "message": f"Set {device['name']} mode to {mode}",
                        "mode": mode.lower()
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
                    "message": f"Device with endpoint {endpoint} not found or does not support mode setting"
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
                "name": "mode_set",
                "description": "Set the mode of one or more thermostat devices. This tool changes the operating mode of thermostats and climate control systems. Available modes include heat (heating only), cool (cooling only), auto (automatic heating and cooling), off (system disabled), and eco (energy-saving mode).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to adjust. Each endpoint must correspond to a thermostat device that supports the mode_set API."
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["heat", "cool", "auto", "off", "eco"],
                            "description": "Mode to set (e.g., 'heat', 'cool', 'auto', 'off', 'eco'). The mode determines how the thermostat operates."
                        }
                    },
                    "required": ["endpoints", "mode"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "No mode specified: The mode parameter is empty or not provided.",
                    "Invalid mode: The specified mode is not one of the valid options (heat, cool, auto, off, eco).",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the mode_set API.",
                    "State update failure: The device state could not be updated due to a system error."
                ]
            }
        }
