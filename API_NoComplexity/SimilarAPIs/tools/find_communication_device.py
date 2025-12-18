# Copyright CommunicationController

"""
Uncertainty Manifestation: Confusion Between `find_call_device` and `find_communication_device`

Description:
Developers face significant confusion between two similarly named functions that handle communication 
but with fundamentally different purposes and behaviors. The `CommunicationController.find_call_device` 
function is designed for finding devices that support making calls (voice communication), while this 
hypothetical `find_communication_device` function is designed for finding devices supporting any form 
of communication (calls, messaging, video conferencing, intercom functionality, etc.). The similar naming 
and overlapping parameter sets create a situation where developers frequently use the wrong function 
for their intended purpose, leading to unexpected behaviors and integration issues.
"""

import json
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool


def find_device_by_endpoint(data: Dict[str, Any], endpoint: str, home_id: str = None) -> Dict[str, Any]:
    """Find a device by endpoint ID, optionally filtered by home ID."""
    devices = data.get("devices", [])
    for device in devices:
        if device["endpoint"] == endpoint and (home_id is None or device.get("home_id") == home_id):
            return device
    return None


def find_all_communication_devices(data: Dict[str, Any], user_id: str) -> List[Dict[str, Any]]:
    """Find all devices that support any communication features."""
    # Get user's home ID
    user = next((u for u in data.get("users", []) if u.get("user_id") == user_id), None)
    if not user:
        return []
    
    home_id = user.get("home_id")
    
    # Get devices in user's home
    all_devices = data.get("devices", [])
    home_devices = [d for d in all_devices if d.get("home_id") == home_id]
    
    # Filter for devices with any communication capability
    communication_apis = ["make_call", "send_message", "receive_message", "intercom"]
    comm_devices = []
    
    for device in home_devices:
        supported_apis = device.get("supported_apis", [])
        if any(api in supported_apis for api in communication_apis):
            comm_devices.append(device)
    
    return comm_devices


class FindCommunicationDevice(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_communication_device",
                "description": "Find devices that support any communication features including messaging, calls, video, intercom functionality, etc. This tool searches for devices that can be used for any type of communication.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_name": {
                            "type": "string",
                            "description": "Optional name or partial name to search for. If not provided, returns all communication devices."
                        },
                        "endpoint": {
                            "type": "string",
                            "description": "Optional specific endpoint ID to find a particular device."
                        },
                        "communication_type": {
                            "type": "string",
                            "description": "Optional filter by communication type ('call', 'message', 'intercom', etc.)"
                        }
                    }
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], device_name: Optional[str] = None, endpoint: Optional[str] = None, 
              communication_type: Optional[str] = None) -> str:
        """
        Find devices that support any communication features (calls, messaging, intercom, etc.).
        
        Args:
            data: The data dictionary containing devices
            device_name: Optional name (or partial name) to search for
            endpoint: Optional specific endpoint ID to find
            communication_type: Optional filter by communication type ('call', 'message', 'intercom', etc.)
            
        Returns:
            A JSON string with the result of the operation
        """
        # Get the current user's ID
        user_id = data.get("current_user")
        if not user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in"
            })
        
        # If endpoint is provided, look for that specific device
        if endpoint:
            # Get the user's home ID
            user = next((u for u in data.get("users", []) if u.get("user_id") == user_id), None)
            if not user:
                return json.dumps({
                    "success": False,
                    "message": "User information not found"
                })
            
            home_id = user.get("home_id")
            device = find_device_by_endpoint(data, endpoint, home_id)
            
            if not device:
                return json.dumps({
                    "success": False,
                    "message": f"Device with endpoint {endpoint} not found or not accessible"
                })
            
            # Check if the device supports ANY communication features
            communication_apis = ["make_call", "send_message", "receive_message", "intercom"]
            supported_comms = [api for api in communication_apis if api in device.get("supported_apis", [])]
            
            if not supported_comms:
                return json.dumps({
                    "success": False,
                    "message": f"Device {device.get('name')} does not support any communication features"
                })
            
            # Filter by communication type if specified
            if communication_type:
                comm_type_map = {
                    "call": "make_call",
                    "message": ["send_message", "receive_message"],
                    "intercom": "intercom"
                }
                required_apis = comm_type_map.get(communication_type)
                
                if not required_apis:
                    return json.dumps({
                        "success": False,
                        "message": f"Invalid communication type: {communication_type}"
                    })
                    
                if isinstance(required_apis, list):
                    has_required = any(api in device.get("supported_apis", []) for api in required_apis)
                else:
                    has_required = required_apis in device.get("supported_apis", [])
                    
                if not has_required:
                    return json.dumps({
                        "success": False,
                        "message": f"Device {device.get('name')} does not support {communication_type} features"
                    })
            
            return json.dumps({
                "success": True,
                "message": f"Found communication device: {device.get('name')}",
                "device": device,
                "supported_communication": supported_comms
            })
        
        # Get all communication devices (any type)
        all_comm_devices = find_all_communication_devices(data, user_id)
        
        # Filter by communication type if specified
        if communication_type:
            comm_type_map = {
                "call": "make_call",
                "message": ["send_message", "receive_message"],
                "intercom": "intercom"
            }
            required_apis = comm_type_map.get(communication_type)
            
            if not required_apis:
                return json.dumps({
                    "success": False,
                    "message": f"Invalid communication type: {communication_type}"
                })
                
            if isinstance(required_apis, list):
                all_comm_devices = [
                    device for device in all_comm_devices
                    if any(api in device.get("supported_apis", []) for api in required_apis)
                ]
            else:
                all_comm_devices = [
                    device for device in all_comm_devices
                    if required_apis in device.get("supported_apis", [])
                ]
        
        # Filter by name if provided
        if device_name:
            device_name_lower = device_name.lower()
            all_comm_devices = [
                device for device in all_comm_devices
                if device_name_lower in device.get("name", "").lower()
            ]
        
        # Return the devices
        if not all_comm_devices:
            message = "No communication devices found"
            if device_name:
                message += f" matching '{device_name}'"
            if communication_type:
                message += f" supporting {communication_type}"
            
            return json.dumps({
                "success": True,
                "message": message,
                "devices": []
            })
        
        # Return result
        return json.dumps({
            "success": True,
            "message": f"Found {len(all_comm_devices)} communication device(s)",
            "devices": all_comm_devices
        })
