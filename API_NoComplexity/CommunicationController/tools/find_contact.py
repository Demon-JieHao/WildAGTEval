# Copyright CommunicationController

import json
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool
from CommunicationController.helpers import (
    find_contact_by_name, find_contact_by_phone, find_contact_by_email
)


class FindContact(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], query: str, search_type: str = "name", limit: int = 5) -> str:
        """
        Find contacts based on search criteria.
        
        Args:
            data: The data dictionary containing contacts
            query: The search term
            search_type: Type of search ('name', 'phone', 'email')
            limit: Maximum number of contacts to return
            
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
        
        # Perform search based on search_type
        if search_type == "name":
            contacts = find_contact_by_name(data, query, user_id)
        elif search_type == "phone":
            contacts = find_contact_by_phone(data, query, user_id)
        elif search_type == "email":
            contacts = find_contact_by_email(data, query, user_id)
        else:
            return json.dumps({
                "success": False,
                "message": f"Invalid search_type: {search_type}. Must be 'name', 'phone', or 'email'."
            })
        
        # Apply limit
        if limit > 0:
            contacts = contacts[:limit]
        
        # Return results
        if contacts:
            return json.dumps({
                "success": True,
                "message": f"Found {len(contacts)} contact(s)",
                "contacts": contacts
            })
        else:
            return json.dumps({
                "success": True,
                "message": f"No contacts found for query: '{query}'",
                "contacts": []
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_contact",
                "description": "Find contacts by name, phone number, or email. This tool searches through the user's contacts and returns matching entries based on the specified search criteria.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search term to find contacts (name, phone number, or email)."
                        },
                        "search_type": {
                            "type": "string",
                            "enum": ["name", "phone", "email"],
                            "description": "Type of search to perform. Default is 'name'."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of contacts to return. Default is 5.",
                            "minimum": 1
                        }
                    },
                    "required": ["query"]
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to access contacts.",
                    "Invalid search_type: The specified search type is not 'name', 'phone', or 'email'.",
                    "No contacts found: No contacts match the provided search query."
                ]
            }
        }
