# Copyright InformationControlEnv

import json
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_user_preferences, get_mock_data_by_key, add_query_to_history, format_news_response
from datetime import datetime


class NewsLatest(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], limit: int = 5) -> str:
        """
        Get the latest news from all categories.
        
        Args:
            data: The data dictionary containing all information
            limit: (Optional) Maximum number of news items to return (default: 5, max: 20)
            
        Returns:
            A JSON string with the latest news
        """
        # Limit to reasonable range
        limit = max(1, min(20, limit))
        
        # Get all news categories
        news_data = data.get("mock_data", {}).get("news", {})
        
        # Collect all news items with their timestamps
        all_news = []
        for category, items in news_data.items():
            for item in items:
                item_with_category = item.copy()
                item_with_category["category"] = category
                all_news.append(item_with_category)
        
        # Sort by timestamp (most recent first)
        all_news.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        
        # Get the latest items
        latest_news = all_news[:limit]
        
        # Add query to history
        user = get_current_user(data)
        if user:
            query = {
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "tool": "news_latest",
                "parameters": {"limit": limit},
                "result": "success"
            }
            add_query_to_history(data, query)
        
        return json.dumps({
            "success": True,
            "count": len(latest_news),
            "news": latest_news,
            "formatted": format_news_response(latest_news)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "news_latest",
                "description": "Get the latest news from all categories. Returns the most recent news items sorted by timestamp.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "(Optional) Maximum number of news items to return (default: 5, max: 20)"
                        }
                    }
                },
                "error_cases": [
                    "Invalid limit: Limit will be constrained to 1-20 range.",
                    "No news available: Returns empty list if no news items are available."
                ]
            }
        }
