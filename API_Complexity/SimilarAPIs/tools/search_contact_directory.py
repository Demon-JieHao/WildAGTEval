# Copyright CommunicationController

"""
Uncertainty Manifestation: Confusion Between Directory Search Functions

Description:
Developers face significant confusion between contact search functions that have similar names
but different scopes and behaviors. While 'find_contact' searches personal contacts,
this 'search_contact_directory' function searches the organization-wide directory including
external partners and employees across departments. The similar naming and overlapping parameter sets
create a situation where developers frequently use the wrong function for their intended purpose,
leading to unexpected behaviors like missing contacts or returning too many irrelevant results.
"""

import json
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool


def has_directory_access(data: Dict[str, Any]) -> bool:
    """Check if the current user has access to the organization directory."""
    user_id = data.get("current_user")
    if not user_id:
        return False
    
    # Find the user in the users list
    users = data.get("users", [])
    user = next((u for u in users if u.get("user_id") == user_id), None)
    if not user:
        return False
    
    # Check if user has directory access permissions
    return user.get("permissions", {}).get("directory_access", False)


def search_organization_directory(
    data: Dict[str, Any],
    query: str,
    search_type: str = "name",
    department: Optional[str] = None,
    include_external: bool = True
) -> List[Dict[str, Any]]:
    """Search the organization directory based on criteria."""
    directory = data.get("organization_directory", {}).get("entries", [])
    if not directory:
        return []
    
    # Filter by department if specified
    if department:
        directory = [entry for entry in directory if entry.get("department") == department]
    
    # Filter external contacts if specified
    if not include_external:
        directory = [entry for entry in directory if not entry.get("is_external", False)]
    
    # Search based on the specified search type
    results = []
    query_lower = query.lower()
    
    for entry in directory:
        match = False
        
        if search_type == "name":
            # Search in full name, first name, and last name
            name = entry.get("name", "").lower()
            first_name = entry.get("first_name", "").lower()
            last_name = entry.get("last_name", "").lower()
            match = (
                query_lower in name or 
                query_lower in first_name or 
                query_lower in last_name
            )
        elif search_type == "phone":
            phone = entry.get("phone", "").replace(" ", "").replace("-", "")
            query_clean = query.replace(" ", "").replace("-", "")
            match = query_clean in phone
        elif search_type == "email":
            email = entry.get("email", "").lower()
            match = query_lower in email
        elif search_type == "position":
            position = entry.get("position", "").lower()
            match = query_lower in position
        elif search_type == "department":
            dept = entry.get("department", "").lower()
            match = query_lower in dept
        
        if match:
            results.append(entry)
    
    return results


class SearchContactDirectory(Tool):
    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_contact_directory",
                "description": "Search the organization-wide contact directory. This tool allows searching across all employees and external contacts in the organization directory based on various criteria.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search term to look for in the directory."
                        },
                        "search_type": {
                            "type": "string",
                            "enum": ["name", "phone", "email", "position", "department"],
                            "description": "What field to search in. Default is 'name'."
                        },
                        "department": {
                            "type": "string",
                            "description": "Optional filter to limit results to a specific department."
                        },
                        "include_external": {
                            "type": "boolean",
                            "description": "Whether to include external partners in results. Default is true."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of contacts to return. Default is 20."
                        }
                    },
                    "required": ["query"]
                }
            }
        }
        
    @staticmethod
    def invoke(data: Dict[str, Any], query: str, search_type: str = "name", department: str = None, 
              include_external: bool = True, limit: int = 20) -> str:
        """
        Search the organization-wide contact directory.
        
        Args:
            data: The data dictionary containing directory information
            query: The search term
            search_type: Type of search ('name', 'phone', 'email', 'position', 'department')
            department: Filter results to a specific department
            include_external: Whether to include external partners in results
            limit: Maximum number of contacts to return
            
        Returns:
            A JSON string with the result of the operation
        """
        # Authentication check - requires organization access
        if not has_directory_access(data):
            return json.dumps({
                "success": False,
                "message": "User does not have access to the organization directory"
            })
        
        # Validate search type
        valid_search_types = ["name", "phone", "email", "position", "department"]
        if search_type not in valid_search_types:
            return json.dumps({
                "success": False,
                "message": f"Invalid search_type: {search_type}. Must be one of {', '.join(valid_search_types)}"
            })
        
        # Perform directory search
        directory_results = search_organization_directory(
            data, query, search_type, department, include_external
        )
        
        # Apply limit
        if limit > 0 and len(directory_results) > limit:
            directory_results = directory_results[:limit]
        
        # Return results
        if directory_results:
            return json.dumps({
                "success": True,
                "message": f"Found {len(directory_results)} directory entries",
                "directory_entries": directory_results
            })
        else:
            return json.dumps({
                "success": True,
                "message": f"No directory entries found for query: '{query}'",
                "directory_entries": []
            })
