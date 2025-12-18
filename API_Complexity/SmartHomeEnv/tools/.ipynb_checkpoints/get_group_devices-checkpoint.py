# Copyright SmartHomeEnv

import json
from typing import Any, Dict
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import find_group_by_id, find_group_by_name, get_devices_in_group


class GetGroupDevices(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], group_id: str = None, group_name: str = None) -> str:
        """
        Get all devices in a group.
        
        Args:
            data: The data dictionary containing devices and groups
            group_id: (Optional) The ID of the group
            group_name: (Optional) The name of the group
            
        Returns:
            A JSON string with the result of the operation
        """
        if not group_id and not group_name:
            return json.dumps({
                "success": False,
                "message": "No group ID or name specified"
            })
        
        # Find the group
        group = None
        if group_id:
            group = find_group_by_id(data, group_id)
        elif group_name:
            group = find_group_by_name(data, group_name)
        
        if not group:
            return json.dumps({
                "success": False,
                "message": f"Group not found"
            })
        
        # Get devices in the group
        devices = get_devices_in_group(data, group["id"])
        
        return json.dumps({
            "success": True,
            "group": group,
            "devices": devices
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_group_devices",
                "description": "Get all devices in a group. This tool retrieves all devices that belong to a specific group, identified either by group ID or group name. Groups can be spaces (rooms) or functional collections of devices (e.g., all lights).",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "group_id": {
                            "type": "string",
                            "description": "(Optional) The ID of the group. Either group_id or group_name must be provided."
                        },
                        "group_name": {
                            "type": "string",
                            "description": "(Optional) The name of the group. Either group_id or group_name must be provided."
                        }
                    }
                },
                "error_cases": [
                    "No group ID or name specified: Neither the group_id nor group_name parameter is provided.",
                    "Group not found: The specified group ID or name does not exist in the system.",
                    "No current user: No user is currently set in the system, so the home context cannot be determined.",
                    "Empty group: The group exists but contains no devices (not an error, but returns an empty list)."
                ]
            }
        }
