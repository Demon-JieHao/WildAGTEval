# stock_watchlist Feature Limitation Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to retrieve their complete stock watchlist using `stock_watchlist()` function, but encounters watchlist capacity limitations due to non-premium user tier restrictions during high-traffic periods.

### Root Cause
- **System Background**: Temporary restriction implemented for non-premium users to manage system load
- **Technical Reason**: Watchlist size exceeds current user tier capacity limitations
- **Temporary Nature**: Not a permanent failure - premium features would allow expanded capacity

### Error Message Analysis
```json
{
  "success": false,
  "message": "Watchlist exceeds current capacity of 3 symbols",
  "info": "Premium features offer expanded capabilities"
}
```

**Key Keyword Interpretation**:
- `"exceeds current capacity"`: Indicates capacity-based limitation rather than function failure
- `"3 symbols"`: Specific limit number varies dynamically based on actual watchlist size
- `"Premium features offer expanded capabilities"`: Hint about tier-based restrictions and upgrade options

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Error Message Interpretation**: Recognize capacity limitation and premium tier restrictions
2. **Function Discovery**: Identify `stock_price` function as alternative for individual stock queries
3. **Exchange Knowledge**: Understand stock symbol format requirements (NYSE:AAPL, NASDAQ:GOOGL)
4. **Data Integration**: Plan systematic approach to aggregate individual results into watchlist format

## Ideal LLM Response Pattern

### Step 1: Situation Recognition and Analysis
```
"The watchlist function is hitting a capacity limit for non-premium users. Since I can't directly 
adjust the watchlist size, I should use the stock_price function to query each stock individually."
```

### Step 2: Solution Strategy Development
```python
# LLM should propose systematic individual stock approach:
"I'll get each stock's data individually and aggregate them into a watchlist format."

# Proposed solution pattern: 
user_watchlist = ["AAPL", "GOOGL", "MSFT"]  # obtained from `user_preferences()`

# LLM must demonstrate exchange knowledge
stock_queries = [
    "NYSE:AAPL",     # Apple on New York Stock Exchange
    "NASDAQ:GOOGL",  # Google on NASDAQ
    "NASDAQ:MSFT"    # Microsoft on NASDAQ
]

individual_results = []
for exchange_symbol in stock_queries:
    result = stock_price(symbol=exchange_symbol)
    if result["success"]:
        individual_results.append(result["stock"])

# Aggregate into watchlist format
aggregated_watchlist = {
    "success": True,
    "watchlist": user_watchlist,
    "stocks": individual_results,
    "summary": {
        "total_symbols": len(individual_results),
        "total_value": sum([stock["price"] for stock in individual_results]),
        "total_change": sum([stock["change"] for stock in individual_results])
    }
}
```

### Step 3: User Communication and Reporting
- Clearly explain the capacity limitation and premium tier context
- Present technical workaround approach using individual stock queries
- Demonstrate successful data aggregation equivalent to original watchlist function

## Function Details

### Function Signature
```python
stock_watchlist() -> str
```

### Alternative Function for Workaround
```python
stock_price(symbol: str) -> str  # Requires "EXCHANGE:TICKER" format
```

### Expected LLM Problem-Solving Process

1. **Initial Call Fails**: `stock_watchlist()` → Capacity Error
2. **Error Analysis**: Parse "Premium features" hint and understand tier limitation
3. **Function Discovery**: Identify `user_preferences` and `stock_price` as alternative approach
4. **Exchange Knowledge**: Apply correct EXCHANGE:TICKER format for each stock
5. **Systematic Execution**: Query each stock individually with proper formatting
6. **Data Integration**: Aggregate individual results into watchlist structure
7. **Communication**: Explain approach and provide equivalent functionality

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Function Discovery**: Successfully identifies `user_preferences` and `stock_price` as technical workaround
- **Exchange Knowledge**: Demonstrates accurate stock-to-exchange mapping (NYSE:AAPL, NASDAQ:GOOGL, etc.)
- **Technical Independence**: Solves problem without requiring user intervention
- **Data Integration**: Successfully aggregates individual results into watchlist format
- **Systematic Approach**: Plans and executes comprehensive individual stock queries
- **Clear Communication**: Explains limitation and technical solution to user


### ⚠️ Good Response (Score 4/5)
- Discovers technical workaround approach using `user_preferences` and `stock_price` function
- Shows basic exchange knowledge with minor mapping errors
- Successfully implements individual queries with some format mistakes
- Communicates approach effectively with minor gaps

### 📊 Average Response (Score 3/5)
- **User-Dependent Solutions**: Primarily asks user to modify settings or upgrade tier
- Limited technical problem-solving approach
- May suggest "reduce watchlist to 3 stocks" or "upgrade to premium"
- Basic understanding of the limitation but relies on user actions

### ❌ Below Average Response (Score 2/5)
- **Incomplete Technical Understanding**: Discovers alternative function but lacks systematic approach
- Poor execution of technical workaround with significant errors
- Limited exchange knowledge or incorrect symbol formatting
- Unclear communication about solution approach

### 🚫 Poor Response (Score 1/5)
- **No Solution Attempt**: Simply reports error without attempting resolution
- Fails to discover alternative approaches or functions
- No technical problem-solving effort
- Poor user communication with no actionable solutions
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)

## Common LLM Mistakes to Watch For

### ❌ Immediate User Dependency
```
"Please reduce your watchlist to 3 stocks and try again."
```

### ❌ Premium Upgrade Focus Only
```
"You need to upgrade to premium to access your full watchlist."
```

### ❌ Missing Function Discovery
```
"The watchlist function is not working. Please try again later."
```

### ❌ Poor Exchange Knowledge
```
"Let me try stock_price('AAPL')" // Missing exchange prefix
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Technical Recognition
```
"I'll use the stock_price function to query each stock individually. I need to use the 
correct exchange format: NYSE:AAPL for Apple, NASDAQ:GOOGL for Google, etc."
```

## Special Considerations for stock_watchlist

### Context Differences from Other Functions
- **No Parameters**: Function has no direct parameters to adjust, requiring alternative approach
- **Multi-Function Strategy**: Requires using different function (stock_price) as workaround
- **Domain Knowledge**: Requires understanding of stock exchanges and ticker symbols
- **Data Restructuring**: Must reconstruct watchlist format from individual queries

### Exchange Knowledge Evaluation
- **Core Stocks**: AAPL→NYSE, GOOGL→NASDAQ, MSFT→NASDAQ, TSLA→NASDAQ, AMZN→NASDAQ
- **Format Understanding**: Must use "EXCHANGE:TICKER" format, not just ticker symbols
- **Systematic Coverage**: Should query all stocks in user's watchlist, not just subset

### Technical Independence Assessment
- **Excellent**: Complete technical solution without user dependency
- **Good**: Mostly technical with minor user interaction needs
- **Average**: Balanced mix of technical and user-dependent approaches
- **Poor**: Primarily relies on user actions rather than technical solutions

## Evaluation Focus Areas

### 1. **Function Relationship Understanding**
- Recognition that `stock_watchlist` and `stock_price` serve related purposes
- Understanding that individual queries can substitute for batch queries
- Knowledge of when to use alternative functions

### 2. **Financial Domain Knowledge**
- Stock exchange system understanding (NYSE vs NASDAQ)
- Ticker symbol format requirements
- Portfolio aggregation concepts (total value, total change)

### 3. **System Architecture Thinking**
- Recognition of tier-based limitations in SaaS systems
- Understanding of premium vs free feature restrictions
- Ability to work within system constraints rather than around them

### 4. **Data Integration Skills**
- Combining multiple individual responses into unified format
- Maintaining data structure consistency with original function
- Calculating aggregate statistics (totals, summaries)
