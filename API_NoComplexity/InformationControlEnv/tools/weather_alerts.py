# Copyright InformationControlEnv

import json
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_user_preferences, get_mock_data_by_key, add_query_to_history
from datetime import datetime


class WeatherAlerts(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], location: str = None) -> str:
        """
        Get weather alerts for a location.
        
        Args:
            data: The data dictionary containing all information
            location: (Optional) Location to get weather alerts for. If not provided, uses user's default location.
            
        Returns:
            A JSON string with weather alerts
        """
        # Get user preferences
        preferences = get_user_preferences(data)
        
        # Determine location
        if not location:
            location = preferences.get("location", "New York")
        
        # Normalize location for mock data lookup
        location_key = location.lower().replace(" ", "_")
        
        # Get mock weather data
        weather_data = get_mock_data_by_key(data, "weather", location_key)
        
        if not weather_data:
            return json.dumps({
                "success": False,
                "message": f"Weather data not available for location: {location}"
            })
        
        alerts = weather_data.get("alerts", [])
        
        # Add query to history
        user = get_current_user(data)
        if user:
            query = {
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "tool": "weather_alerts",
                "parameters": {"location": location},
                "result": "success"
            }
            add_query_to_history(data, query)
        
        return json.dumps({
            "success": True,
            "location": location,
            "alerts": alerts,
            "has_alerts": len(alerts) > 0,
            "alert_count": len(alerts)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "weather_alerts",
                "description": "Get weather alerts and warnings for a location. Includes severe weather warnings, advisories, and watches.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "(Optional) Location to get weather alerts for. If not provided, uses the user's default location from preferences."
                        }
                    }
                },
                "error_cases": [
                    "Location not found: Weather data is not available for the specified location.",
                    "No user preferences: If no location is provided and no user is logged in, defaults to New York."
                ]
            }
        }
