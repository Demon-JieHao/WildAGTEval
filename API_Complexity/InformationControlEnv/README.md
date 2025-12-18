# InformationControlEnv

An Information Control Environment API that provides access to various information sources including weather, news, general knowledge, and financial data.

## Overview

InformationControlEnv is designed to simulate an information retrieval system with about 20 tools that can query different types of data sources. It follows the same architecture as SmartHomeEnv and uses a common base class system for easy integration.

## Features

### Weather Information
- **weather_current**: Get current weather conditions for a location
- **weather_forecast**: Get weather forecast for up to 7 days
- **weather_alerts**: Get weather alerts and warnings

### News
- **news_latest**: Get the latest news from all categories
- **news_by_category**: Get news from specific categories (technology, business, world, science, health, sports)
- **news_personalized**: Get personalized news based on user preferences

### Knowledge & Facts
- **knowledge_lookup**: Look up general knowledge about keywords

### Financial Data
- **stock_price**: Get current stock price for a symbol
- **stock_watchlist**: Get stock prices for user's watchlist

### Utility Tools
- **query_history**: View user's query history
- **source_list**: List available information sources
- **user_preferences**: Get current user's preferences

## Usage

```python
from InformationControlEnv import InformationControlEnv

# Create environment instance
env = InformationControlEnv()

# Set current user
env.set_current_user("user1")

# Get current weather
result = env.invoke_tool("weather_current", location="New York")

# Get latest news
result = env.invoke_tool("news_latest", limit=5)

# Look up knowledge
result = env.invoke_tool("knowledge_lookup", keyword="python")

# Get stock price
result = env.invoke_tool("stock_price", symbol="AAPL")
```

## Data Structure

The environment uses JSON files to store:
- **users.json**: User profiles and preferences
- **sources.json**: Available information sources
- **queries.json**: Query history
- **mock_data.json**: Mock data for weather, news, knowledge, and stocks

## Integration with SmartHomeEnv

Both InformationControlEnv and SmartHomeEnv inherit from common base classes:
- `BaseTool`: Common interface for all tools
- `BaseEnvironment`: Common environment functionality

This allows for potential future integration where both environments can work together.

## Demo

Run the demo to see all features in action:

```bash
python InformationControlEnv/demo.py
