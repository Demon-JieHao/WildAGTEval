# Copyright InformationControlEnv

"""
Wiki documentation for InformationControlEnv
"""

WIKI = """
# InformationControlEnv Wiki

## Overview

InformationControlEnv is an information retrieval system that provides access to various data sources including weather, news, general knowledge, and financial information. The system uses keyword-based queries to simplify user interactions.

## Domain Basics

### Information Sources
- **Source**: A provider of specific types of information (weather API, news aggregator, etc.)
- **Source Types**: weather, news, knowledge, financial
- **Reliability**: Each source has a reliability score (0-1) indicating data quality

### User System
- **User Preferences**: Each user has personalized settings including:
  - Default location for weather queries
  - Preferred news categories
  - Stock watchlist
  - Language and temperature unit preferences
- **Query History**: System tracks all user queries for analysis and personalization

### Data Categories

#### Weather Information
- **Current Conditions**: Temperature, humidity, wind speed, pressure
- **Forecasts**: Daily high/low temperatures and conditions
- **Alerts**: Severe weather warnings and advisories

#### News
- **Categories**: technology, business, world, science, health, sports
- **Personalization**: Based on user's preferred categories
- **Timestamps**: All news items are time-stamped for recency sorting

#### Knowledge Base
- **Keywords**: Predefined topics with definitions
- **Format**: Simple keyword-to-definition mapping

#### Financial Data
- **Stock Information**: Symbol, name, price, change, percentage change
- **Watchlist**: User-specific list of tracked stocks

## Tool Categories

### Weather Tools (3 tools)
1. **weather_current**: Get current weather conditions
2. **weather_forecast**: Get multi-day weather forecast
3. **weather_alerts**: Check for weather warnings

### News Tools (3 tools)
1. **news_latest**: Get latest news from all categories
2. **news_by_category**: Get news from specific category
3. **news_personalized**: Get news based on user preferences

### Knowledge & Financial Tools (3 tools)
1. **knowledge_lookup**: Look up general knowledge
2. **stock_price**: Get individual stock price
3. **stock_watchlist**: Get all watchlist stock prices

### Utility Tools (3 tools)
1. **query_history**: View user's past queries
2. **source_list**: List available information sources
3. **user_preferences**: View current user's preferences

## Usage Patterns

### Basic Information Retrieval
```python
# Get current weather
env.invoke_tool("weather_current", location="New York")

# Get latest news
env.invoke_tool("news_latest", limit=5)

# Look up knowledge
env.invoke_tool("knowledge_lookup", keyword="python")
```

### Personalized Queries
```python
# Weather uses user's default location if not specified
env.invoke_tool("weather_current")

# News based on user's preferred categories
env.invoke_tool("news_personalized")

# User's stock watchlist
env.invoke_tool("stock_watchlist")
```

### Filtered Queries
```python
# News by specific category
env.invoke_tool("news_by_category", category="technology", limit=10)

# Weather forecast for specific days
env.invoke_tool("weather_forecast", location="London", days=7)

# List sources by type
env.invoke_tool("source_list", source_type="financial")
```

## Error Handling

Common error cases across tools:
- **No user logged in**: Some tools require a current user for preferences
- **Invalid parameters**: Out-of-range values are constrained to valid ranges
- **Data not found**: Returns appropriate error messages with available options
- **Missing required parameters**: Clear error messages indicate what's missing

## Integration with SmartHomeEnv

Both environments share:
- Common base classes (BaseTool, BaseEnvironment)
- User management system
- Consistent tool invocation interface

This enables scenarios like:
- Weather-based home automation
- News-triggered notifications on smart displays
- Stock market alerts affecting home lighting

## Best Practices

1. **Set Current User**: Always set the current user for personalized experiences
2. **Check Success**: Always check the "success" field in responses
3. **Use Appropriate Limits**: Use reasonable limits for list-based queries
4. **Handle Errors Gracefully**: Check for error messages and available options
5. **Leverage Personalization**: Use user preferences for better results
"""
