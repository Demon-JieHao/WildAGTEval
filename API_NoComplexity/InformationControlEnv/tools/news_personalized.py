# Copyright InformationControlEnv

import json
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_user_preferences, get_mock_data_by_key, add_query_to_history, format_news_response
from datetime import datetime


class NewsPersonalized(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], limit: int = 10) -> str:
        """
        Get personalized news based on user preferences.
        
        Args:
            data: The data dictionary containing all information
            limit: (Optional) Maximum number of news items to return (default: 10, max: 20)
            
        Returns:
            A JSON string with personalized news
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_feature_limitation_error_enabled = os.getenv('ENABLE__FEATURE_LIMITATION_ERROR__NEWS_PERSONALIZED', 'false').lower() == 'true'
        
        # Get user preferences
        preferences = get_user_preferences(data)
        preferred_categories = preferences.get("news_categories", ["technology", "business"])
        
        ### ADDED: Personalization limitation check - always more restrictive ###
        if uncertainty_feature_limitation_error_enabled:
            # Determine dynamic limit based on preferences complexity
            if len(preferred_categories) > 5:
                max_allowed_categories = 2
            elif len(preferred_categories) > 2:
                max_allowed_categories = 1
            else:
                max_allowed_categories = 0  # Even basic preferences can fail
            
            if len(preferred_categories) > max_allowed_categories:
                return json.dumps({
                    "success": False,
                    "message": f"Personalized news exceeds current capacity of {max_allowed_categories} categories",
                    "info": "Premium features offer expanded capabilities"
                })
        ### END ADDED ###
        
        # Limit to reasonable range
        limit = max(1, min(20, limit))
        
        # Collect news from preferred categories
        personalized_news = []
        news_data = data.get("mock_data", {}).get("news", {})
        
        for category in preferred_categories:
            if category in news_data:
                items = news_data[category]
                for item in items:
                    item_with_category = item.copy()
                    item_with_category["category"] = category
                    personalized_news.append(item_with_category)
        
        # Sort by timestamp (most recent first)
        personalized_news.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Limit the results
        limited_news = personalized_news[:limit]
        
        # Add query to history
        user = get_current_user(data)
        if user:
            query = {
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "tool": "news_personalized",
                "parameters": {"limit": limit},
                "result": "success"
            }
            add_query_to_history(data, query)
        
        return json.dumps({
            "success": True,
            "preferred_categories": preferred_categories,
            "count": len(limited_news),
            "news": limited_news,
            "formatted": format_news_response(limited_news)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "news_personalized",
                "description": "Get personalized news based on user preferences. Returns news from the user's preferred categories sorted by recency.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "(Optional) Maximum number of news items to return (default: 10, max: 20)"
                        }
                    }
                },
                "error_cases": [
                    "No user preferences: If no user is logged in, defaults to technology and business categories.",
                    "Invalid limit: Limit will be constrained to 1-20 range.",
                    "No news available: Returns empty list if no news items are available in preferred categories."
                ]
            }
        }
