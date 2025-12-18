# Copyright SmartHomeEnv

import json
from typing import Any, Dict, List
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class TemperatureSet(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], temperature: int) -> str:
        """
        Set the temperature of one or more thermostat devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to adjust
            temperature: Temperature value to set (in degrees)
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_informational_notice_enabled = os.getenv('ENABLE__INFORMATIONAL_NOTICE__TEMPERATURE_SET', 'false').lower() == 'true'
        
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        if temperature is None:
            return json.dumps({
                "success": False,
                "message": "No temperature specified"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        # Ensure temperature is within reasonable bounds (e.g., 10-32°C or 50-90°F)
        # This is a simplified version - a real implementation would handle different units
        min_temp = 10  # °C
        max_temp = 32  # °C
        
        # Clamp temperature to valid range
        temperature = max(min_temp, min(max_temp, temperature))
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "temperature_set" in device["supported_apis"]:
                # Update the device state directly in the data dictionary
                for i, d in enumerate(data["devices"]):
                    if d["endpoint"] == endpoint and (home_id is None or d["home_id"] == home_id):
                        if "state" not in data["devices"][i]:
                            data["devices"][i]["state"] = {}
                        data["devices"][i]["state"]["temperature"] = temperature
                        success = True
                        break
                else:
                    success = False
                
                if success:
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": True,
                        "message": f"Set {device['name']} temperature to {temperature}°C",
                        "temperature": temperature
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
                    "message": f"Device with endpoint {endpoint} not found or does not support temperature setting"
                })
        
        ### ADDED: Build response with informational notices when uncertainty is enabled ###
        response = {
            "success": any(result["success"] for result in results),
            "results": results
        }
        
        if uncertainty_informational_notice_enabled and response["success"]:
            ### ADDED: Energy efficiency notice ###
            energy_impact = "moderate" if 18 <= temperature <= 24 else "higher"
            response["energy_info"] = f"FYI: Setting temperature to {temperature}°C will have {energy_impact} energy impact. Each degree of heating/cooling adjustment typically affects energy consumption by 3-5%. The optimal comfort range for most users is 20-22°C in winter and 24-26°C in summer."
            
            ### ADDED: Alternative function availability ###
            response["alternatives_available"] = "The schedule_temperature() function is available if you'd like to set different temperatures for different times of day. It includes built-in energy optimization features and can learn from your usage patterns."
            
            ### ADDED: Smart features notice ###
            response["smart_features"] = "Note: The adaptive_comfort_mode() function also adjusts temperature based on occupancy, weather, and learned preferences if that might be useful for your automation needs."
            
            ### ADDED: Zone control information ###
            if len(endpoints) > 1:
                response["zone_info"] = "Since you're controlling multiple thermostats, the zone_temperature_balance() function is available for coordinating temperatures across different areas to optimize comfort and efficiency."
            
            ### ADDED: Seasonal context ###
            import datetime
            month = datetime.datetime.now().month
            if month in [12, 1, 2]:  # Winter months
                response["seasonal_tip"] = "During winter months, the eco_heating_mode() function provides additional energy-saving features while maintaining comfort. It's available if you're interested in reducing heating costs."
            elif month in [6, 7, 8]:  # Summer months
                response["seasonal_tip"] = "During summer months, the smart_cooling_optimizer() function can help reduce cooling costs by pre-cooling during off-peak hours. It's available if that aligns with your needs."
        
        return json.dumps(response)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "temperature_set",
                "description": "Set the temperature of one or more thermostat devices. This tool adjusts the target temperature for thermostats and climate control systems. Temperature values are specified in degrees Celsius and will be automatically constrained to a reasonable range (10-32°C).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to adjust. Each endpoint must correspond to a thermostat device that supports the temperature_set API."
                        },
                        "temperature": {
                            "type": "integer",
                            "description": "Temperature value to set in degrees Celsius. Values will be constrained to the range 10-32°C."
                        }
                    },
                    "required": ["endpoints", "temperature"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "No temperature specified: The temperature parameter is not provided.",
                    "Temperature out of range: The temperature will be automatically constrained to the valid range (10-32°C).",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the temperature_set API.",
                    "State update failure: The device state could not be updated due to a system error."
                ]
            }
        }
