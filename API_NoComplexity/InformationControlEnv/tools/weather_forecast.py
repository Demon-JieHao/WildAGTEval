
# Copyright InformationControlEnv

import json
import os
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_user_preferences, get_mock_data_by_key, add_query_to_history
from datetime import datetime


def get_irrelevant_data(category: str, key: str) -> Dict:
    """Load irrelevant data from irrelevant_mock_data.json"""
    try:
        with open('common/data/irrelevant_mock_data.json', 'r') as f:
            irrelevant_data = json.load(f)
        return irrelevant_data.get(category, {}).get(key, {})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}


class WeatherForecast(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], location: str = None, days: int = 3) -> str:
        """
        Get weather forecast for a location.
        
        Args:
            data: The data dictionary containing all information
            location: (Optional) Location to get weather for. If not provided, uses user's default location.
            days: (Optional) Number of days to forecast (default: 3, max: 7)
            
        Returns:
            A JSON string with the weather forecast
        """
        ### ADDED: Check if uncertainty behaviors should be activated ###
        uncertainty_partially_irrelevant_information_enabled = os.getenv('ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__WEATHER_FORECAST', 'false').lower() == 'true'
        uncertainty_feature_limitation_error_enabled = os.getenv('ENABLE__FEATURE_LIMITATION_ERROR__WEATHER_FORECAST', 'false').lower() == 'true'
        
        # Get user preferences
        preferences = get_user_preferences(data)
        
        # Determine location
        if not location:
            location = preferences.get("location", "New York")
        
        ### ADDED: Regional limitation check when uncertainty is enabled ###
        if uncertainty_feature_limitation_error_enabled:
            # Define temporarily unavailable regions (more restrictive than any input)
            return json.dumps({
                "success": False,
                "message": f"Weather data for {location} temporarily unavailable. Other regions are accessible"
            })
        ### END ADDED ###
        
        # Normalize location for mock data lookup
        location_key = location.lower().replace(" ", "_")
        
        # Limit days to reasonable range
        days = max(1, min(7, days))
        
        # Get mock weather data
        weather_data = get_mock_data_by_key(data, "weather", location_key)
        
        if not weather_data:
            return json.dumps({
                "success": False,
                "message": f"Weather data not available for location: {location}"
            })
        
        forecast = weather_data.get("forecast", [])[:days]
        
        # Add query to history
        user = get_current_user(data)
        if user:
            query = {
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "tool": "weather_forecast",
                "parameters": {"location": location, "days": days},
                "result": "success"
            }
            add_query_to_history(data, query)
        
        # Build base response
        response_data = {
            "success": True,
            "location": location,
            "days": days,
            "forecast": forecast
        }
        
        if uncertainty_partially_irrelevant_information_enabled:
            ### ADDED: Include tourism, aviation, and health analytics ###
            irrelevant_data = get_irrelevant_data("weather", location_key)
            if irrelevant_data:
                response_data.update(irrelevant_data)
            
            # Add daily analytics to each forecast day
            daily_analytics = get_irrelevant_data("forecast_daily_analytics", location_key)
            if daily_analytics and len(daily_analytics) > 0:
                for i, forecast_day in enumerate(response_data["forecast"]):
                    if i < len(daily_analytics):
                        # Match by day name for accuracy
                        matching_day_data = None
                        for day_data in daily_analytics:
                            if day_data.get("day") == forecast_day.get("day"):
                                matching_day_data = day_data
                                break
                        
                        if matching_day_data:
                            # Add all irrelevant daily data except the 'day' field
                            for key, value in matching_day_data.items():
                                if key != "day":
                                    forecast_day[key] = value
            ### END ADDED ###
        
        return json.dumps(response_data)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "weather_forecast",
                "description": "Get weather forecast for a location. Provides daily high/low temperatures and conditions for up to 7 days.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "(Optional) Location to get weather for. If not provided, uses the user's default location from preferences."
                        },
                        "days": {
                            "type": "integer",
                            "description": "(Optional) Number of days to forecast (default: 3, max: 7)"
                        }
                    }
                },
                "error_cases": [
                    "Location not found: Weather data is not available for the specified location.",
                    "Invalid days: Days parameter will be constrained to 1-7 range.",
                    "No user preferences: If no location is provided and no user is logged in, defaults to New York."
                ]
            }
        }
