# Copyright TimeNotificationEnv

"""
Uncertainty Manifestation: Confusion Between Notification Retrieval and Notification Status Functions

Description:
Developers would be confused between the `get_notifications` function and this `fetch_notification_status` 
function that exists in the same notification ecosystem. While both functions retrieve notification-related 
data, they serve fundamentally different purposes. `get_notifications` returns the actual notification objects 
with their content, while this `fetch_notification_status` function provides metadata about notification 
delivery status, read receipts, and user interaction metrics. The similar naming and overlapping parameter 
sets create significant confusion about which function to use when developers need specific notification-related 
information.
"""

import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from SmartHomeEnv.tool import Tool


def get_notification_status_data(data: Dict[str, Any], notification_ids: Optional[List[str]] = None, 
                                start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
    """
    Get status data for notifications from the data dictionary.
    
    Args:
        data: The data dictionary containing notifications
        notification_ids: Optional list of specific notification IDs to check
        start_date: Optional filter for notifications after this date (ISO format)
        end_date: Optional filter for notifications before this date (ISO format)
        
    Returns:
        A list of notification status objects
    """
    # Get current user's notification statuses
    current_user = data.get("current_user", {})
    user_id = current_user.get("id")
    
    if not user_id:
        return []
    
    # Get all notification statuses for the user
    all_statuses = []
    
    # In a real system, notification statuses would likely be stored in a separate collection
    # Here we'll derive them from the notifications collection with some status metadata
    notifications = data.get("notifications", [])
    for notification in notifications:
        # Only include notifications for this user
        if notification.get("user_id") != user_id:
            continue
            
        # If specific IDs were provided, only include those
        if notification_ids and notification.get("id") not in notification_ids:
            continue
            
        # Apply date filters if provided
        if start_date or end_date:
            created_at = notification.get("created_at")
            if not created_at:
                continue
                
            try:
                notification_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                
                if start_date:
                    start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
                    if notification_date < start:
                        continue
                        
                if end_date:
                    end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
                    if notification_date > end:
                        continue
            except ValueError:
                # Skip if dates can't be parsed
                continue
        
        # Create status object with delivery and interaction metrics
        status = {
            "notification_id": notification.get("id"),
            "title": notification.get("title"),
            "source": notification.get("source"),
            "type": notification.get("type"),
            "created_at": notification.get("created_at"),
            "delivered": True,  # Most notifications are delivered
            "delivered_at": notification.get("created_at"),  # Simplified - normally would be later
            "read": notification.get("read", False),
            "read_at": notification.get("read_at"),
            "clicked": notification.get("clicked", False),
            "clicked_at": notification.get("clicked_at"),
            "dismissed": notification.get("dismissed", False),
            "dismissed_at": notification.get("dismissed_at")
        }
        
        all_statuses.append(status)
        
    # Sort by created_at (most recent first)
    all_statuses.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    return all_statuses


def validate_date_format(date_str: Optional[str]) -> bool:
    """Validate ISO date format."""
    if not date_str:
        return True
        
    try:
        datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


class FetchNotificationStatus(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "fetch_notification_status",
                "description": "Fetch delivery status and interaction metrics for notifications sent to users. Returns aggregated metrics and detailed status information for each notification.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "notification_ids": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Optional list of specific notification IDs to check. If not provided, checks all notifications."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of notification statuses to return. Defaults to 20."
                        },
                        "source": {
                            "type": "string",
                            "description": "Optional filter to show status only for notifications from a specific source/environment."
                        },
                        "type": {
                            "type": "string",
                            "description": "Optional filter to show status only for notifications of a specific type (e.g., system, reminder, alert)."
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Optional filter for notifications sent after this date (ISO format)."
                        },
                        "end_date": {
                            "type": "string",
                            "description": "Optional filter for notifications sent before this date (ISO format)."
                        }
                    }
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any],
              notification_ids: Optional[List[str]] = None,
              limit: Optional[int] = 20,
              source: Optional[str] = None,
              type: Optional[str] = None,
              start_date: Optional[str] = None,
              end_date: Optional[str] = None) -> str:
        """
        Fetch delivery status and interaction metrics for notifications.
        
        Args:
            data: The data dictionary
            notification_ids: Optional list of specific notification IDs to check
            limit: Maximum number of notification statuses to return (default: 20)
            source: Optional filter by notification source (environment name)
            type: Optional filter by notification type
            start_date: Optional filter for notifications after this date (ISO format)
            end_date: Optional filter for notifications before this date (ISO format)
            
        Returns:
            A JSON string with notification status metrics
        """
        # Check if user is logged in
        current_user = data.get("current_user", {})
        if not current_user or not current_user.get("id"):
            return json.dumps({
                "success": False,
                "message": "No user logged in: No user is currently logged in to retrieve notification status."
            })
        
        # Validate date formats if provided
        if (start_date and not validate_date_format(start_date)) or (end_date and not validate_date_format(end_date)):
            return json.dumps({
                "success": False,
                "message": "Invalid date format: The provided date strings are not in valid ISO format."
            })
        
        # Get notification status data
        status_data = get_notification_status_data(data, notification_ids, start_date, end_date)
        
        # Apply additional filters
        if source:
            status_data = [s for s in status_data if s.get("source") == source]
        
        if type:
            status_data = [s for s in status_data if s.get("type") == type]
        
        # Apply limit after filtering
        if limit is not None and limit > 0 and len(status_data) > limit:
            status_data = status_data[:limit]
        
        # Calculate aggregate metrics
        total_sent = len(status_data)
        total_delivered = sum(1 for s in status_data if s.get("delivered"))
        total_read = sum(1 for s in status_data if s.get("read"))
        total_clicked = sum(1 for s in status_data if s.get("clicked"))
        total_dismissed = sum(1 for s in status_data if s.get("dismissed"))
        
        # Avoid division by zero
        delivery_rate = total_delivered / total_sent if total_sent > 0 else 0
        read_rate = total_read / total_delivered if total_delivered > 0 else 0
        click_rate = total_clicked / total_read if total_read > 0 else 0
        dismissal_rate = total_dismissed / total_delivered if total_delivered > 0 else 0
        
        # Build response with metrics and status details
        return json.dumps({
            "success": True,
            "message": f"Retrieved status for {total_sent} notifications",
            "metrics": {
                "total_sent": total_sent,
                "total_delivered": total_delivered,
                "total_read": total_read,
                "total_clicked": total_clicked,
                "total_dismissed": total_dismissed,
                "delivery_rate": delivery_rate,
                "read_rate": read_rate,
                "click_rate": click_rate,
                "dismissal_rate": dismissal_rate
            },
            "status_details": status_data
        })
