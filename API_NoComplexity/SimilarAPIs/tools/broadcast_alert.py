# Copyright AlertSystemEnv

"""
Uncertainty Manifestation: Notification Creation vs. Alert Broadcasting Confusion

Description:
Developers would be confused between `TimeNotificationEnv.create_notification` and this 
`AlertSystemEnv.broadcast_alert` function. Both functions appear to serve similar purposes (sending 
important messages to users), but they operate in fundamentally different domains with different 
behaviors, persistence models, and delivery mechanisms. The naming similarity creates confusion about 
which function to use for time-sensitive communications, especially since both accept similar 
parameters like title, message, and priority.
"""

import json
from typing import Any, Dict, List, Optional
from SmartHomeEnv.tool import Tool


class BroadcastAlert(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "broadcast_alert",
                "description": "Broadcast an urgent alert to multiple users across various communication channels simultaneously. Designed for time-sensitive announcements that require immediate attention and potentially user acknowledgment.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the alert."
                        },
                        "message": {
                            "type": "string",
                            "description": "The detailed alert message content."
                        },
                        "severity": {
                            "type": "string",
                            "enum": ["minor", "standard", "critical", "emergency"],
                            "description": "Severity level of the alert, affecting delivery urgency and visual presentation."
                        },
                        "target_groups": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of user group IDs to target with the alert. If not provided, broadcasts to all users."
                        },
                        "expiration": {
                            "type": "integer",
                            "description": "Time in seconds until the alert expires and is no longer shown to users. Default is 3600 (1 hour)."
                        },
                        "action_url": {
                            "type": "string",
                            "description": "Optional URL that users can click to take action related to the alert."
                        },
                        "broadcast_channels": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["app", "email", "sms", "push"]
                            },
                            "description": "Communication channels to use for alert delivery. Default is all available channels."
                        },
                        "require_acknowledgment": {
                            "type": "boolean",
                            "description": "Whether users must acknowledge the alert before it can be dismissed."
                        }
                    },
                    "required": ["title", "message"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any],
              title: str,
              message: str,
              severity: str = "standard",
              target_groups: Optional[List[str]] = None,
              expiration: int = 3600,
              action_url: Optional[str] = None,
              broadcast_channels: Optional[List[str]] = None,
              require_acknowledgment: bool = False) -> str:
        """
        Broadcast an alert to multiple users across various communication channels.
        
        Args:
            data: The data dictionary
            title: The title of the alert
            message: The alert message content
            severity: Alert severity level (minor, standard, critical, emergency)
            target_groups: List of user groups to target (defaults to all users)
            expiration: Time in seconds until the alert expires (default 1 hour)
            action_url: Optional URL for users to take action on the alert
            broadcast_channels: Communication channels to use for delivery
            require_acknowledgment: Whether users must acknowledge the alert
            
        Returns:
            A JSON string with the broadcast results and tracking information
        """
        # Validate input parameters
        valid_severities = ["minor", "standard", "critical", "emergency"]
        valid_channels = ["app", "email", "sms", "push"]
        
        if severity not in valid_severities:
            return json.dumps({
                "success": False,
                "message": f"Invalid severity: Severity must be one of: {', '.join(valid_severities)}."
            })
        
        # Set default channels if not provided
        if broadcast_channels is None:
            broadcast_channels = ["app", "email", "sms"]
        else:
            # Validate channels
            invalid_channels = [channel for channel in broadcast_channels if channel not in valid_channels]
            if invalid_channels:
                return json.dumps({
                    "success": False,
                    "message": f"Invalid broadcast channels: {', '.join(invalid_channels)}. Specified channels must be supported types."
                })
                
        # Process target groups
        all_users = []
        user_groups = data.get("user_groups", {})
        
        if target_groups is None:
            # Target all users
            all_users = data.get("users", [])
        else:
            # Collect users from specified groups
            for group_id in target_groups:
                if group_id in user_groups:
                    group_users = user_groups[group_id].get("members", [])
                    all_users.extend(group_users)
            
            # Remove duplicates
            all_users = list(set(all_users))
            
        if not all_users:
            return json.dumps({
                "success": False,
                "message": "No valid targets: No users found in the specified target groups."
            })
            
        # Generate a broadcast ID
        import uuid
        import time
        broadcast_id = f"alert_{int(time.time())}_{str(uuid.uuid4())[:8]}"
        
        # Initialize delivery stats
        delivery_stats = {
            "total_users": len(all_users),
            "channels": {}
        }
        
        for channel in broadcast_channels:
            delivery_stats["channels"][channel] = {
                "sent": 0,
                "pending": len(all_users),
                "failed": 0
            }
        
        # In a real implementation, this would actually send messages through various channels
        # Here we'll simulate successful delivery to most users with some failures
        for channel in broadcast_channels:
            # Simulate delivery rates
            if channel == "app":
                # 95% success for app notifications
                success_rate = 0.95
            elif channel == "email":
                # 90% success for emails
                success_rate = 0.90
            elif channel == "sms":
                # 85% success for SMS
                success_rate = 0.85
            else:  # push
                # 80% success for push notifications
                success_rate = 0.80
                
            # Update simulated statistics
            sent_count = int(len(all_users) * success_rate)
            failed_count = len(all_users) - sent_count
            
            delivery_stats["channels"][channel]["sent"] = sent_count
            delivery_stats["channels"][channel]["pending"] = 0
            delivery_stats["channels"][channel]["failed"] = failed_count
        
        # Store the alert in the system
        if "alerts" not in data:
            data["alerts"] = []
            
        alert_data = {
            "id": broadcast_id,
            "title": title,
            "message": message,
            "severity": severity,
            "created_at": int(time.time()),
            "expires_at": int(time.time()) + expiration,
            "target_groups": target_groups,
            "action_url": action_url,
            "broadcast_channels": broadcast_channels,
            "require_acknowledgment": require_acknowledgment,
            "delivery_stats": delivery_stats,
            "acknowledged_by": []
        }
        
        data["alerts"].append(alert_data)
        
        return json.dumps({
            "success": True,
            "message": f"Alert broadcast initiated to {len(all_users)} users across {len(broadcast_channels)} channels",
            "broadcast_id": broadcast_id,
            "delivery_stats": delivery_stats,
            "expiration": alert_data["expires_at"]
        })
