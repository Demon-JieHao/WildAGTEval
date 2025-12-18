# Copyright SmartHomeEnv

import json
from typing import Any, Dict, List
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_device_by_endpoint, get_user_home_id


class ChannelChange(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], channel: int) -> str:
        """
        Change the channel on one or more TV devices.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to adjust
            channel: Channel number to change to
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified"
            })
        
        if channel is None:
            return json.dumps({
                "success": False,
                "message": "No channel specified"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        # Ensure channel is a positive integer
        if not isinstance(channel, int) or channel <= 0:
            return json.dumps({
                "success": False,
                "message": "Channel must be a positive integer"
            })
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "channel_change" in device["supported_apis"]:
                # Update the device state directly in the data dictionary
                for i, d in enumerate(data["devices"]):
                    if d["endpoint"] == endpoint and (home_id is None or d["home_id"] == home_id):
                        if "state" not in data["devices"][i]:
                            data["devices"][i]["state"] = {}
                        data["devices"][i]["state"]["channel"] = channel
                        success = True
                        break
                else:
                    success = False
                
                if success:
                    results.append({
                        "endpoint": endpoint,
                        "name": device["name"],
                        "success": True,
                        "message": f"Changed {device['name']} to channel {channel}",
                        "channel": channel
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
                    "message": f"Device with endpoint {endpoint} not found or does not support channel changing"
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
                "name": "channel_change",
                "description": "Change the channel on one or more TV devices. This tool switches the current channel on televisions and other media devices that support channel selection. The channel is specified as a positive integer representing the channel number.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to adjust. Each endpoint must correspond to a TV device that supports the channel_change API."
                        },
                        "channel": {
                            "type": "integer",
                            "description": "Channel number to change to. Must be a positive integer."
                        }
                    },
                    "required": ["endpoints", "channel"]
                },
                "error_cases": [
                    "No devices specified: The endpoints parameter is empty or not provided.",
                    "No channel specified: The channel parameter is not provided.",
                    "Invalid channel: The channel must be a positive integer.",
                    "Device not found: One or more specified endpoints do not exist in the current user's home.",
                    "API not supported: One or more devices do not support the channel_change API.",
                    "State update failure: The device state could not be updated due to a system error.",
                    "Channel not available: The specified channel may not be available on the device (though this is not checked in the current implementation)."
                ]
            }
        }
