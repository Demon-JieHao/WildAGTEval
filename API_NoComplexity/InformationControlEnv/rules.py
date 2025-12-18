# Copyright InformationControlEnv

"""
Rules for InformationControlEnv
"""

RULES = [
    # Query Processing Rules
    "All user queries must be keyword-based - complex natural language queries should be simplified to keywords",
    "Query parameters must be validated before processing - invalid values should be constrained to valid ranges",
    "All queries must be logged to the query history for the current user",
    
    # User Context Rules
    "A current user must be set for personalized queries to work properly",
    "User preferences should be used as defaults when specific parameters are not provided",
    "User location preference is used for weather queries when no location is specified",
    "User's preferred news categories are used for personalized news feeds",
    "User's stock watchlist determines which stocks are tracked",
    
    # Data Source Rules
    "Information sources have reliability scores that indicate data quality",
    "Sources are categorized by type: weather, news, knowledge, financial",
    "Each source supports specific query types as defined in its configuration",
    
    # Weather Information Rules
    "Weather locations must be normalized (lowercase, underscores for spaces)",
    "Weather forecasts are limited to a maximum of 7 days",
    "Temperature units follow user preferences (celsius/fahrenheit)",
    "Weather alerts are location-specific and may be empty",
    
    # News Rules
    "News items must include timestamps for proper sorting",
    "News categories are predefined: technology, business, world, science, health, sports",
    "Latest news is sorted by timestamp in descending order (most recent first)",
    "News limits are constrained between 1 and 20 items per query",
    
    # Knowledge Base Rules
    "Knowledge lookups require exact keyword matches (case-insensitive)",
    "Keywords with spaces should use underscores in the lookup",
    "Available keywords are returned when a lookup fails",
    
    # Financial Data Rules
    "Stock symbols must be uppercase for lookups",
    "Stock prices include current price, change, and percentage change",
    "Watchlist calculations include total value and total change summaries",
    "Invalid stock symbols are silently skipped in watchlist queries",
    
    # Query History Rules
    "Query history is stored per user and includes timestamp, tool, parameters, and result",
    "Query history is limited to the last 100 queries per user",
    "History queries can retrieve up to 50 recent queries at once",
    
    # Error Handling Rules
    "All tools must return a JSON response with a 'success' field",
    "Failed operations must include a descriptive 'message' field",
    "Tools should provide available options when invalid parameters are given",
    "Missing required parameters must result in clear error messages",
    
    # Integration Rules
    "Tools must inherit from the BaseTool class",
    "All tools must implement invoke() and get_info() methods",
    "Tool names must be unique across the environment",
    "Tools should be stateless - all state is maintained in the data dictionary"
]
