# Copyright InformationControlEnv

from typing import Any, Dict, List, Optional


def get_current_user(data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get the current user from the data"""
    current_user_id = data.get("current_user")
    if not current_user_id:
        return None
    
    for user in data.get("users", []):
        if user["user_id"] == current_user_id:
            return user
    
    return None


def get_user_preferences(data: Dict[str, Any]) -> Dict[str, Any]:
    """Get the current user's preferences"""
    user = get_current_user(data)
    if user:
        return user.get("preferences", {})
    return {}


def find_source_by_id(data: Dict[str, Any], source_id: str) -> Optional[Dict[str, Any]]:
    """Find a source by its ID"""
    for source in data.get("sources", []):
        if source["source_id"] == source_id:
            return source
    return None


def find_source_by_name(data: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    """Find a source by its name"""
    name_lower = name.lower()
    for source in data.get("sources", []):
        if source["name"].lower() == name_lower:
            return source
    return None


def get_sources_by_type(data: Dict[str, Any], source_type: str) -> List[Dict[str, Any]]:
    """Get all sources of a specific type"""
    sources = []
    for source in data.get("sources", []):
        if source["type"] == source_type:
            sources.append(source)
    return sources


def get_mock_data_by_key(data: Dict[str, Any], category: str, key: str) -> Optional[Any]:
    """Get mock data by category and key"""
    mock_data = data.get("mock_data", {})
    category_data = mock_data.get(category, {})
    return category_data.get(key)


def add_query_to_history(data: Dict[str, Any], query: Dict[str, Any]) -> None:
    """Add a query to the user's query history"""
    if "queries" not in data:
        data["queries"] = []
    data["queries"].append(query)
    
    # Keep only the last 100 queries
    if len(data["queries"]) > 100:
        data["queries"] = data["queries"][-100:]


def get_user_query_history(data: Dict[str, Any], user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Get a user's query history"""
    queries = []
    for query in reversed(data.get("queries", [])):
        if query.get("user_id") == user_id:
            queries.append(query)
            if len(queries) >= limit:
                break
    return queries


def format_weather_response(weather_data: Dict[str, Any]) -> str:
    """Format weather data into a readable response"""
    if not weather_data:
        return "No weather data available"
    
    temp = weather_data.get("temperature", "N/A")
    condition = weather_data.get("condition", "N/A")
    humidity = weather_data.get("humidity", "N/A")
    wind_speed = weather_data.get("wind_speed", "N/A")
    
    return f"Temperature: {temp}°C, Condition: {condition}, Humidity: {humidity}%, Wind: {wind_speed} km/h"


def format_news_response(news_items: List[Dict[str, Any]]) -> str:
    """Format news items into a readable response"""
    if not news_items:
        return "No news items available"
    
    formatted_items = []
    for item in news_items[:5]:  # Limit to 5 items
        title = item.get("title", "No title")
        source = item.get("source", "Unknown source")
        formatted_items.append(f"• {title} ({source})")
    
    return "\n".join(formatted_items)


def format_stock_response(stock_data: Dict[str, Any]) -> str:
    """Format stock data into a readable response"""
    if not stock_data:
        return "No stock data available"
    
    symbol = stock_data.get("symbol", "N/A")
    price = stock_data.get("price", "N/A")
    change = stock_data.get("change", "N/A")
    change_percent = stock_data.get("change_percent", "N/A")
    
    return f"{symbol}: ${price} ({change} / {change_percent}%)"
