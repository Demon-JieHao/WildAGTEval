# Copyright InformationControlEnv

import json
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_user_query_history
from datetime import datetime


class QueryHistory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], limit: int = 10) -> str:
        """
        Get user's query history.
        
        Args:
            data: The data dictionary containing all information
            limit: (Optional) Maximum number of queries to return (default: 10, max: 50)
            
        Returns:
            A JSON string with the query history
        """
        # Get current user
        user = get_current_user(data)
        if not user:
            return json.dumps({
                "success": False,
                "message": "No user logged in"
            })
        
        # Limit to reasonable range
        limit = max(1, min(50, limit))
        
        # Get query history
        history = get_user_query_history(data, user["user_id"], limit)
        
        # Format history for display
        formatted_history = []
        for query in history:
            formatted_history.append({
                "timestamp": query.get("timestamp"),
                "tool": query.get("tool"),
                "parameters": query.get("parameters"),
                "result": query.get("result")
            })
        
        return json.dumps({
            "success": True,
            "user_id": user["user_id"],
            "count": len(formatted_history),
            "history": formatted_history
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "query_history",
                "description": "Get user's query history. Shows recent information queries made by the current user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "(Optional) Maximum number of queries to return (default: 10, max: 50)"
                        }
                    }
                },
                "error_cases": [
                    "No user logged in: Returns error if no current user is set.",
                    "Invalid limit: Limit will be constrained to 1-50 range.",
                    "No history: Returns empty list if user has no query history."
                ]
            }
        }
