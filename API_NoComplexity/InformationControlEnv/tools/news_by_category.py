# Copyright InformationControlEnv

import json
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_user_preferences, get_mock_data_by_key, add_query_to_history, format_news_response
from datetime import datetime


class NewsByCategory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], category: str, limit: int = 5) -> str:
        """
        Get news from a specific category.
        
        Args:
            data: The data dictionary containing all information
            category: News category (technology, business, world, science, health, sports)
            limit: (Optional) Maximum number of news items to return (default: 5, max: 20)
            
        Returns:
            A JSON string with news from the specified category
        """
        # Limit to reasonable range
        limit = max(1, min(20, limit))
        
        # Normalize category
        category_lower = category.lower()
        
        # Get news for the category
        news_items = get_mock_data_by_key(data, "news", category_lower)
        
        if news_items is None:
            # Get available categories
            news_data = data.get("mock_data", {}).get("news", {})
            available_categories = list(news_data.keys())
            
            return json.dumps({
                "success": False,
                "message": f"Category '{category}' not found",
                "available_categories": available_categories
            })
        
        # Limit the results
        limited_news = news_items[:limit]
        
        # Add category to each item
        for item in limited_news:
            item["category"] = category_lower
        
        # Add query to history
        user = get_current_user(data)
        if user:
            query = {
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "tool": "news_by_category",
                "parameters": {"category": category, "limit": limit},
                "result": "success"
            }
            add_query_to_history(data, query)
        
        return json.dumps({
            "success": True,
            "category": category,
            "count": len(limited_news),
            "news": limited_news,
            "formatted": format_news_response(limited_news)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "news_by_category",
                "description": "Get news from a specific category. Available categories include technology, business, world, science, health, and sports.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "News category to retrieve (technology, business, world, science, health, sports)"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "(Optional) Maximum number of news items to return (default: 5, max: 20)"
                        }
                    },
                    "required": ["category"]
                },
                "error_cases": [
                    "Invalid category: Returns error with list of available categories.",
                    "Invalid limit: Limit will be constrained to 1-20 range.",
                    "No news in category: Returns empty list if no news items are available in the category."
                ]
            }
        }
