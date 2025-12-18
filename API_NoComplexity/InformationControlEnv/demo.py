# Copyright InformationControlEnv

import json
from InformationControlEnv import InformationControlEnv


def main():
    """Demonstrate the InformationControlEnv functionality"""
    
    # Create environment instance
    env = InformationControlEnv()
    
    print("=== InformationControlEnv Demo ===\n")
    
    # Set current user
    print("1. Setting current user to 'user1'")
    env.set_current_user("user1")
    print(f"Current user: {env.get_current_user()}\n")
    
    # Get user preferences
    print("2. Getting user preferences")
    result = env.invoke_tool("user_preferences")
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get current weather
    print("3. Getting current weather")
    result = env.invoke_tool("weather_current")
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get weather forecast
    print("4. Getting weather forecast for 3 days")
    result = env.invoke_tool("weather_forecast", days=3)
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get latest news
    print("5. Getting latest news")
    result = env.invoke_tool("news_latest", limit=3)
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get news by category
    print("6. Getting technology news")
    result = env.invoke_tool("news_by_category", category="technology", limit=2)
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get personalized news
    print("7. Getting personalized news")
    result = env.invoke_tool("news_personalized", limit=5)
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Look up knowledge
    print("8. Looking up knowledge about 'python'")
    result = env.invoke_tool("knowledge_lookup", keyword="python")
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get stock price
    print("9. Getting stock price for AAPL")
    result = env.invoke_tool("stock_price", symbol="AAPL")
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get stock watchlist
    print("10. Getting stock watchlist")
    result = env.invoke_tool("stock_watchlist")
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get query history
    print("11. Getting query history")
    result = env.invoke_tool("query_history", limit=5)
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # List available sources
    print("12. Listing available sources")
    result = env.invoke_tool("source_list")
    print(f"Result: {json.dumps(json.loads(result), indent=2)}\n")
    
    # Get all available tools
    print("13. Available tools:")
    tools = env.get_tools()
    for tool in tools:
        if 'function' in tool:
            print(f"   - {tool['function']['name']}: {tool['function']['description']}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()
