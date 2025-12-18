# Copyright ContentManagementEnv

"""
Uncertainty Manifestation: Confusion Between `get_media_details` and `get_content_details` APIs

Description:
Developers frequently confuse the `get_media_details` function with this hypothetical 
`get_content_details` function that exists in a related content management system within 
the same ecosystem. While both retrieve metadata about digital content, they serve 
fundamentally different purposes and return different data structures. `get_media_details` 
is designed for retrievable playable media (songs, videos, etc.) with playback-related metadata, 
while `get_content_details` is designed for content management with publishing, rights management, 
and distribution metadata. The similar naming and overlapping domain create significant 
confusion about which API to use in different contexts.
"""

import json
from typing import Any, Dict, Optional
from MediaControlEnv.tool import Tool  # Using MediaControlEnv's Tool class as ContentManagementEnv doesn't exist


def find_content_by_id(data: Dict[str, Any], content_id: str) -> Dict[str, Any]:
    """Find content in the content management system by ID."""
    content_items = data.get("content_items", {})
    return content_items.get(content_id, None)


class GetContentDetails(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_content_details",
                "description": "Get detailed information about a specific content item including publication status, rights management information, distribution channels, and type-specific metadata for content management purposes.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "content_id": {
                            "type": "string",
                            "description": "ID of the content item to get details for"
                        }
                    },
                    "required": ["content_id"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], content_id: str) -> str:
        """
        Get detailed information about a specific content item in the content management system.
        
        Args:
            data: The data dictionary containing content database
            content_id: ID of the content item
            
        Returns:
            A JSON string with the content details
        """
        if not content_id:
            return json.dumps({
                "success": False,
                "message": "No content ID: The content_id parameter is empty or not provided"
            })
        
        # Find the content item
        content_item = find_content_by_id(data, content_id)
        
        if content_item:
            # Format the details with focus on content management data
            details = {
                "id": content_item.get("id"),
                "title": content_item.get("title"),
                "type": content_item.get("type"),
                "status": content_item.get("status", "draft"),
                "created_date": content_item.get("created_date", ""),
                "modified_date": content_item.get("modified_date", ""),
                "publish_date": content_item.get("publish_date", ""),
                "expiry_date": content_item.get("expiry_date", ""),
                "owner": content_item.get("owner", ""),
                "rights_info": content_item.get("rights_info", {}),
                "distribution_channels": content_item.get("distribution_channels", []),
                "tags": content_item.get("tags", [])
            }
            
            # Add type-specific fields
            if content_item.get("type") == "article":
                details["author"] = content_item.get("author", "")
                details["word_count"] = content_item.get("word_count", 0)
                details["category"] = content_item.get("category", "")
            elif content_item.get("type") == "image":
                details["photographer"] = content_item.get("photographer", "")
                details["dimensions"] = content_item.get("dimensions", {})
                details["format"] = content_item.get("format", "")
            elif content_item.get("type") == "video_asset":
                details["producer"] = content_item.get("producer", "")
                details["duration"] = content_item.get("duration", 0)
                details["resolution"] = content_item.get("resolution", "")
            elif content_item.get("type") == "audio_asset":
                details["producer"] = content_item.get("producer", "")
                details["duration"] = content_item.get("duration", 0)
                details["bitrate"] = content_item.get("bitrate", 0)
            
            return json.dumps({
                "success": True,
                "details": details,
                "message": f"Found content details for '{content_item.get('title')}'"
            })
        else:
            return json.dumps({
                "success": False,
                "message": f"Content not found: The specified content ID '{content_id}' does not exist in the content management system"
            })
