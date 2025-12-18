# Copyright CommunicationController

import json
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from CommunicationController.tool import Tool
from CommunicationController.helpers import (
    find_contact_by_id, find_device_by_endpoint, get_user_home_id, get_active_call
)


class MakeCall(Tool):
    @staticmethod
    def generate_sequential_call_id(data):
        """
        Generate a sequential call ID.
        
        Args:
            data: The global data container
            
        Returns:
            A sequential ID in the form call1, call2, etc.
        """
        # Initialize call_history if it doesn't exist
        if "call_history" not in data:
            data["call_history"] = []
        
        # Extract numeric parts from existing call_id values
        existing_ids = []
        for call in data["call_history"]:
            if "call_id" in call and call["call_id"].startswith("call"):
                try:
                    # Extract numeric part from IDs in 'call1', 'call2' format
                    num = int(call["call_id"].replace("call", ""))
                    existing_ids.append(num)
                except ValueError:
                    # Ignore entries that fail to parse
                    continue
        
        # Start from 1 if no existing IDs, otherwise max + 1
        next_num = 1
        if existing_ids:
            next_num = max(existing_ids) + 1
        
        # Return new ID (simple number without padding)
        return f"call{next_num}"  # e.g., call1, call2
    
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        phone_number: str,
        device_endpoint: Optional[str] = None,
        call_type: str = "audio"
    ) -> str:
        """
        Make a call to a phone number using a specified device.
        
        Args:
            data: The data dictionary containing devices and contacts
            phone_number: Phone number to call (required)
            device_endpoint: Endpoint ID of the device to use for calling
            call_type: Type of call ('audio' or 'video')
            
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
        
        # Check if user already has an active call
        active_call = get_active_call(data, user_id)
        # if active_call:
        #     return json.dumps({
        #         "success": False,
        #         "message": "User already has an active call. End the current call before making a new one."
        #     })
        
        # Phone number is now required by function signature
        
        # Get the user's home ID
        home_id = get_user_home_id(data)
        
        # Check if device_endpoint is provided and valid
        if not device_endpoint:
            # Try to find a suitable device from user preferences
            for user in data.get("users", []):
                if user.get("user_id") == user_id and user.get("communication_info", {}).get("preferred_device"):
                    device_endpoint = user["communication_info"]["preferred_device"]
                    break
            
            # If still no device, find the first available device with make_call API
            if not device_endpoint:
                for device in data.get("devices", []):
                    if (device.get("home_id") == home_id and 
                        "make_call" in device.get("supported_apis", [])):
                        device_endpoint = device.get("endpoint")
                        break
        
        if not device_endpoint:
            return json.dumps({
                "success": False,
                "message": "No suitable device found for making calls"
            })
        
        # Verify the device exists and is available
        device = find_device_by_endpoint(data, device_endpoint, home_id)
        if not device:
            return json.dumps({
                "success": False,
                "message": f"Device with endpoint {device_endpoint} not found or not accessible"
            })
        
        # Check if device is powered on
        if device.get("state", {}).get("power") != "on":
            return json.dumps({
                "success": False,
                "message": f"Device {device.get('name', 'Unknown')} is not powered on"
            })
        
        # Check if device supports the call type
        if call_type == "video" and "video" not in device.get("capabilities", []):
            return json.dumps({
                "success": False,
                "message": f"Device {device.get('name', 'Unknown')} does not support video calls"
            })
            
        # Check if device is currently playing media and pause it
        if "media_playback_state" in data and device_endpoint in data["media_playback_state"]:
            playback_state = data["media_playback_state"][device_endpoint]
            if playback_state.get("status") == "playing":
                # Pause media playback
                data["media_playback_state"][device_endpoint]["status"] = "paused"
        
        # Try to find if this phone number belongs to a contact (for display purposes)
        contact_name = None
        for contact in data.get("contacts", []):
            if contact.get("user_id") == user_id and contact.get("phone_numbers"):
                for phone in contact.get("phone_numbers", []):
                    if phone.get("number") == phone_number:
                        contact_name = contact.get("name")
                        break
                if contact_name:
                    break
        
        # # Generate a unique call ID
        # call_id = f"call_{str(uuid.uuid4())[:8]}"
        # Generate a sequential call ID
        call_id = MakeCall.generate_sequential_call_id(data)
        
        # Create a call record
        timestamp = datetime.utcnow().isoformat() + "Z"
        call_record = {
            "call_id": call_id,
            "user_id": user_id,
            "contact_id": None,
            "phone_number": phone_number,
            "direction": "outgoing",
            "timestamp": timestamp,
            "duration": 0,  # Will be updated when call ends
            "status": "connecting",
            "call_type": call_type,
            "device_endpoint": device_endpoint
        }
        
        # Add to call history
        if "call_history" not in data:
            data["call_history"] = []
        data["call_history"].append(call_record)
        
        # Set as active call
        if "active_calls" not in data:
            data["active_calls"] = {}
        data["active_calls"][user_id] = call_record
        
        # Return success
        return json.dumps({
            "success": True,
            "message": f"Call initiated to {contact_name if contact_name else phone_number} using {device.get('name', 'Unknown device')}",
            "call_id": call_id,
            "call_type": call_type,
            "status": "connecting"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "make_call",
                "description": "Make a call to a phone number using a specified device. This tool initiates a communication session with the specified phone number.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "phone_number": {
                            "type": "string",
                            "description": "Phone number to call."
                        },
                        "device_endpoint": {
                            "type": "string",
                            "description": "Endpoint ID of the device to use for calling. If not specified, a suitable device will be selected automatically."
                        },
                        "call_type": {
                            "type": "string",
                            "enum": ["audio", "video"],
                            "description": "Type of call to make. Default is 'audio'."
                        }
                    },
                    "required": ["phone_number"]
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to make calls.",
                    "User has active call: The user already has an active call that must be ended first.",
                    "No suitable device: No device is available for making calls.",
                    "Device not powered on: The specified device is not powered on.",
                    "Video not supported: The device does not support video calls."
                ]
            }
        }
