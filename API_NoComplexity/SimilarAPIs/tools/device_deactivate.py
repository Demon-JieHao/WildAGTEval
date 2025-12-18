# Copyright SmartHomeEnv

"""
Uncertainty Manifestation: Confusion between `power_off` and `device_deactivate` functions

Description:
Developers would be confused between the `power_off` function and this `device_deactivate` function. 
While both appear to "turn off" devices, they have fundamentally different behaviors and purposes. 
`power_off` simply changes the power state while preserving device settings, whereas this 
`device_deactivate` function completely deactivates a device in the system, including stopping all 
background processes, canceling scheduled operations, and potentially putting the device in a deep 
power-saving mode that requires a longer restart time. This distinction is critical but not obvious 
from the function names alone, leading developers to use the wrong function for their intended purpose.
"""

import json
from typing import Any, Dict, List
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


def cancel_scheduled_operations(data: Dict[str, Any], endpoint: str) -> None:
    """Cancel any scheduled operations for the specified device."""
    if "scheduled_operations" in data:
        data["scheduled_operations"] = [
            op for op in data.get("scheduled_operations", []) 
            if op.get("target_endpoint") != endpoint
        ]


def stop_background_processes(data: Dict[str, Any], endpoint: str) -> None:
    """Stop background processes for the specified device."""
    if "background_processes" in data:
        processes = data.get("background_processes", {})
        if endpoint in processes:
            processes[endpoint] = []


class DeviceDeactivate(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "device_deactivate",
                "description": "Deactivate one or more devices, putting them in a low-power state and stopping all processes. This tool completely deactivates devices, canceling any scheduled operations, stopping background processes, and putting devices in a specified power-saving mode. When a device is deactivated, it may require a longer startup time when reactivated compared to simply turning it back on after using power_off.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "endpoints": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of device endpoint IDs to deactivate. Each endpoint must correspond to a device that supports the device_deactivate API."
                        },
                        "deactivation_mode": {
                            "type": "string",
                            "enum": ["standard", "deep", "temporary"],
                            "description": "Mode of deactivation: 'standard' (default) balances power savings with restart time, 'deep' maximizes power savings but increases restart time, 'temporary' optimizes for quick reactivation.",
                            "default": "standard"
                        }
                    },
                    "required": ["endpoints"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], endpoints: List[str], deactivation_mode: str = "standard") -> str:
        """
        Deactivate one or more devices, putting them in a low-power state and stopping all processes.
        
        Args:
            data: The data dictionary containing devices
            endpoints: List of device endpoint IDs to deactivate
            deactivation_mode: Mode of deactivation ("standard", "deep", "temporary")
            
        Returns:
            A JSON string with the result of the operation
        """
        if not endpoints:
            return json.dumps({
                "success": False,
                "message": "No devices specified: The endpoints parameter is empty or not provided"
            })
        
        # Validate deactivation mode
        valid_modes = ["standard", "deep", "temporary"]
        if deactivation_mode not in valid_modes:
            return json.dumps({
                "success": False,
                "message": f"Invalid deactivation mode: The mode '{deactivation_mode}' is not supported"
            })
        
        # Get the current user's home ID
        home_id = get_user_home_id(data)
        
        results = []
        for endpoint in endpoints:
            device = find_device_by_endpoint(data, endpoint, home_id)
            if device and "device_deactivate" in device.get("supported_apis", []):
                # Cancel any scheduled operations for this device
                cancel_scheduled_operations(data, endpoint)
                
                # Stop background processes
                stop_background_processes(data, endpoint)
                
                # Update the device state
                success = False
                for i, d in enumerate(data.get("devices", [])):
                    if d["endpoint"] == endpoint and (home_id is None or d.get("home_id") == home_id):
                        if "state" not in data["devices"][i]:
                            data["devices"][i]["state"] = {}
                        data["devices"][i]["state"]["power"] = "off"
                        data["devices"][i]["state"]["active"] = False
                        data["devices"][i]["state"]["deactivation_mode"] = deactivation_mode
                        success = True
                        break
                
                if success:
                    results.append({
                        "endpoint": endpoint,
                        "name": device.get("name", endpoint),
                        "success": True,
                        "message": f"Deactivated {device.get('name', endpoint)} in {deactivation_mode} mode"
                    })
                else:
                    results.append({
                        "endpoint": endpoint,
                        "success": False,
                        "message": f"State update failure: The device state could not be updated due to a system error"
                    })
            else:
                error_message = "Device not found" if not device else "API not supported"
                results.append({
                    "endpoint": endpoint,
                    "success": False,
                    "message": f"{error_message}: Device with endpoint {endpoint} not found or does not support deactivation"
                })
        
        return json.dumps({
            "success": any(result["success"] for result in results),
            "results": results
        })
