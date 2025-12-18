# Copyright SmartHomeEnv

"""
Uncertainty Manifestation: Confusion Between "get_user_inventory" and "get_device_inventory"

Description:
Developers frequently confuse `get_user_inventory()` with this similarly named but functionally 
different API `get_device_inventory()`. While `get_user_inventory()` returns a high-level overview 
of devices and groups associated with a user's home (with limited device details), this 
`get_device_inventory()` function provides comprehensive details about the specific capabilities, 
firmware versions, and hardware specifications of individual devices. This confusion leads developers 
to use `get_user_inventory()` when they need detailed device specifications, only to discover the 
data they need is missing, or conversely, to use the more resource-intensive `get_device_inventory()` 
when they only need basic device identification.
"""

import json
from typing import Any, Dict, Optional
from SmartHomeEnv.tool import Tool


def get_current_user(data: Dict[str, Any]) -> Dict[str, Any]:
    """Get the current user information."""
    user_id = data.get("current_user")
    if not user_id:
        return None
    
    for user in data.get("users", []):
        if user.get("user_id") == user_id:
            return user
    
    return None


class GetDeviceInventory(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function", 
            "function": {
                "name": "get_device_inventory",
                "description": "Get current stock levels and inventory information for smart home devices. This tool retrieves stock quantities, reorder points, supplier information, and stock location details for device inventory management. It's particularly useful for tracking device availability, managing stock levels, and planning procurement.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_id": {
                            "type": "string",
                            "description": "(Optional) The specific device ID to get stock information for. If provided, returns stock details for just this device model."
                        },
                        "warehouse_id": {
                            "type": "string", 
                            "description": "(Optional) The warehouse ID to get all device stock levels for. If provided without device_id, returns stock information for all devices in the warehouse."
                        }
                    }
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], device_id: Optional[str] = None, warehouse_id: Optional[str] = None) -> str:
        """
        Get detailed technical inventory of device specifications and capabilities.
        
        Args:
            data: The data dictionary
            device_id: (Optional) The specific device ID to get stock information for
            warehouse_id: (Optional) The warehouse ID to get all device stock levels for
            
        Returns:
            A JSON string with comprehensive device specifications
        """
        # If neither device_id nor warehouse_id provided, use current user's warehouse
        if device_id is None and warehouse_id is None:
            user = get_current_user(data)
            if not user:
                return json.dumps({
                    "success": False,
                    "message": "No current user set and no warehouse_id provided"
                })
            warehouse_id = user.get("warehouse_id")
        
        # Get detailed device specifications
        device_specs = []
        for device in data.get("devices", []):
            # Filter by device_id if provided
            if device_id and device.get("device_id") != device_id:
                continue
            # Filter by warehouse_id if provided and no device_id specified  
            if device_id is None and warehouse_id and device.get("warehouse_id") != warehouse_id:
                continue
                
            # Include comprehensive technical specifications
            device_specs.append({
                "device_id": device.get("device_id"),
                "endpoint": device.get("endpoint"),
                "name": device.get("name"),
                "model": device.get("model"),
                "manufacturer": device.get("manufacturer"),
                "firmware_version": device.get("firmware_version"),
                "hardware_version": device.get("hardware_version"),
                "capabilities": device.get("capabilities", []),
                "supported_protocols": device.get("supported_protocols", []),
                "connection_type": device.get("connection_type"),
                "power_source": device.get("power_source"),
                "last_updated": device.get("last_updated"),
                "technical_specs": device.get("technical_specs", {}),
                "endpoint_categories": device.get("endpoint_categories", []),
                "supported_apis": device.get("supported_apis", []),
                "state": device.get("state", {})
            })
        
        # Handle the case when no matching devices are found
        if not device_specs:
            if device_id:
                return json.dumps({
                    "success": False,
                    "message": f"Device not found: The specified device_id '{device_id}' does not exist in the system"
                })
            elif warehouse_id:
                # Check if warehouse exists
                warehouses = data.get("warehouses", [])
                if not any(w.get("warehouse_id") == warehouse_id for w in warehouses):
                    return json.dumps({
                        "success": False,
                        "message": f"Warehouse not found: The specified warehouse_id '{warehouse_id}' does not exist in the system"
                    })
                return json.dumps({
                    "success": True,
                    "message": "No devices found in the specified warehouse",
                    "device_count": 0,
                    "devices": []
                })
        
        return json.dumps({
            "success": True,
            "device_count": len(device_specs),
            "devices": device_specs
        })
