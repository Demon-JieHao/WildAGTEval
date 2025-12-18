# Copyright SmartHomeEnv

"""
Uncertainty Manifestation: Temperature Control Function Naming Collision

Description:
Developers working with the SmartHomeEnv API face significant confusion between multiple temperature-
related functions that have similar names but fundamentally different purposes and behaviors. The 
primary `temperature_set` function exists alongside functions like `temperature_adjust` and this 
`temperature_schedule` function that operate on the same devices but with different semantics, 
constraints, and side effects. While `temperature_set` sets immediate absolute temperature values, 
this `temperature_schedule` function creates future temperature settings without changing the current 
temperature. Developers frequently use the wrong function for their intended purpose, leading to 
unexpected behavior in their applications.
"""

import json
import re
from typing import Any, Dict, List, Optional
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


def is_valid_time_format(time_str: str) -> bool:
    """Check if a string is in HH:MM format."""
    if not time_str:
        return False
    return bool(re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", time_str))


class TemperatureSchedule(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "temperature_schedule",
                "description": "Schedule a temperature setting for one or more thermostat devices. This tool creates or modifies temperature schedules without changing the current temperature. Temperature values are specified in degrees Celsius and will be automatically constrained to a reasonable range (10-32°C).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to schedule. Each endpoint must correspond to a thermostat device that supports the temperature_schedule API."
                        },
                        "temperature": {
                            "type": "integer",
                            "description": "Temperature value to set in degrees Celsius. Values will be constrained to the range 10-32°C."
                        },
                        "start_time": {
                            "type": "string",
                            "description": "Time to start the temperature setting (format: \"HH:MM\")."
                        },
                        "end_time": {
                            "type": "string",
                            "description": "Optional time to end the temperature setting (format: \"HH:MM\")."
                        },
                        "days": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Optional list of days to apply the schedule (e.g., [\"Monday\", \"Wednesday\", \"Friday\"])."
                        }
                    },
                    "required": ["endpoints", "temperature", "start_time"]
                }
            }
        }
        
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        endpoints: List[str],
        temperature: int,
        start_time: str,
        end_time: Optional[str] = None,
        days: Optional[List[str]] = None
    ) -> str:
        """
        Schedule a temperature setting for one or more thermostat devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to schedule
            temperature: Temperature value to set in degrees Celsius
            start_time: Time to start the temperature setting (format: "HH:MM")
            end_time: Optional time to end the temperature setting (format: "HH:MM")
            days: Optional list of days to apply the schedule
            
        Returns:
            A JSON string with the result of the operation
        """
        # Validate inputs
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified: The endpoints parameter is empty or not provided"
            })
            
        if temperature is None:
            return json.dumps({
                "success": False,
                "message": "No temperature specified: The temperature parameter is not provided"
            })
            
        if not start_time:
            return json.dumps({
                "success": False,
                "message": "No start time specified: The start_time parameter is not provided"
            })
            
        # Validate time formats
        if not is_valid_time_format(start_time):
            return json.dumps({
                "success": False,
                "message": "Invalid time format: The start_time is not in the correct format (HH:MM)"
            })
            
        if end_time and not is_valid_time_format(end_time):
            return json.dumps({
                "success": False,
                "message": "Invalid time format: The end_time is not in the correct format (HH:MM)"
            })
        
        # Constrain temperature to valid range
        min_temp = 10
        max_temp = 32
        original_temp = temperature
        temperature = max(min_temp, min(max_temp, temperature))
        
        if original_temp != temperature:
            warning_message = f"Temperature out of range: The value {original_temp}°C was constrained to {temperature}°C"
        else:
            warning_message = None
        
        # Validate days if provided
        valid_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if days:
            invalid_days = [day for day in days if day not in valid_days]
            if invalid_days:
                return json.dumps({
                    "success": False,
                    "message": f"Invalid days: The following days are not valid: {', '.join(invalid_days)}"
                })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "temperature_schedule" in device.get("supported_apis", []):
                # Create or update the schedule for this device
                success = False
                for i, d in enumerate(data["devices"]):
                    if d["endpoint"] == endpoint and (home_id is None or d.get("home_id") == home_id):
                        # Initialize schedules if not present
                        if "schedules" not in data["devices"][i]:
                            data["devices"][i]["schedules"] = []
                            
                        # Create the new schedule entry
                        schedule_id = f"temp_{start_time.replace(':', '')}_{temperature}"
                        
                        new_schedule = {
                            "id": schedule_id,
                            "type": "temperature",
                            "temperature": temperature,
                            "start_time": start_time,
                            "days": days if days else valid_days  # Default to all days if not specified
                        }
                        
                        if end_time:
                            new_schedule["end_time"] = end_time
                        
                        # Check if this schedule already exists (by id) and update or append
                        for j, schedule in enumerate(data["devices"][i]["schedules"]):
                            if schedule.get("id") == schedule_id:
                                data["devices"][i]["schedules"][j] = new_schedule
                                break
                        else:
                            data["devices"][i]["schedules"].append(new_schedule)
                            
                        success = True
                        break
                
                if success:
                    results.append({
                        "endpoint": endpoint,
                        "name": device.get("name", endpoint),
                        "success": True,
                        "message": f"Scheduled {device.get('name', endpoint)} to {temperature}°C starting at {start_time}" +
                                  (f" until {end_time}" if end_time else "") +
                                  (f" on {', '.join(days)}" if days else "")
                    })
                else:
                    results.append({
                        "endpoint": endpoint,
                        "success": False,
                        "message": f"Schedule update failure: The device schedule could not be updated due to a system error"
                    })
            else:
                error_message = "Device not found" if not device else "API not supported"
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"{error_message}: Device with endpoint {endpoint} not found or does not support temperature scheduling"
                })
        
        response = {
            "success": any(result["success"] for result in results),
            "results": results
        }
        
        if warning_message:
            response["warning"] = warning_message
            
        return json.dumps(response)
