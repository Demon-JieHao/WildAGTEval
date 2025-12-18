# news_personalized Feature Limitation Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to retrieve their personalized news using `news_personalized()` function, but encounters personalization capacity limitations due to non-premium user tier restrictions during high-traffic periods.

### Root Cause
- **System Background**: Temporary restriction implemented for non-premium users to manage system load
- **Technical Reason**: User's preferred news categories exceed current user tier capacity limitations
- **Temporary Nature**: Not a permanent failure - premium features would allow expanded personalization

### Error Message Analysis
```json
{
  "success": false,
  "message": "Personalized news exceeds current capacity of 1 categories",
  "info": "Premium features offer expanded capabilities"
}
```

**Key Keyword Interpretation**:
- `"exceeds current capacity"`: Indicates capacity-based limitation rather than function failure
- `"1 categories"`: Specific limit number varies dynamically based on actual user preferences
- `"Premium features offer expanded capabilities"`: Hint about tier-based restrictions and upgrade options

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Error Message Interpretation**: Recognize capacity limitation and premium tier restrictions
2. **User Preferences Discovery**: Identify user's preferred news categories 
3. **Function Discovery**: Identify `news_by_category` function as alternative for individual category queries
4. **Data Integration**: Plan systematic approach to aggregate individual results into personalized news format

## Ideal LLM Response Pattern

### Step 1: Situation Recognition and Analysis
```
"The personalized news function is hitting a capacity limit for non-premium users. Since I can't directly 
adjust the number of categories, I should use the news_by_category function to query each preferred category individually."
```

### Step 2: Solution Strategy Development
```python
# LLM should propose systematic individual category approach:
"I'll discover the user's preferred categories and get news from each category individually, 
then aggregate them into a personalized news format."

# Proposed solution pattern:
# 1. Discover user preferences
user_preferences = user_preferences()  # or similar approach
preferred_categories = user_preferences.get("news_categories", ["technology", "business"])

# 2. Query each category individually
individual_results = []
for category in preferred_categories:
    result = news_by_category(category=category, limit=5)
    if result["success"]:
        individual_results.extend(result["news"])

# 3. Aggregate into personalized news format
# Sort by timestamp (most recent first) - same as original function
sorted_news = sorted(individual_results, key=lambda x: x.get("timestamp", ""), reverse=True)
limited_news = sorted_news[:limit]

aggregated_personalized_news = {
    "success": True,
    "preferred_categories": preferred_categories,
    "count": len(limited_news),
    "news": limited_news
}
```

### Step 3: User Communication and Reporting
- Clearly explain the capacity limitation and premium tier context
- Present technical workaround approach using individual category queries
- Demonstrate successful data aggregation equivalent to original personalized news function

## Function Details

### Function Signature
```python
news_personalized(limit: int = 10) -> str
```

### Alternative Function for Workaround
```python
news_by_category(category: str, limit: int = 5) -> str
```

### Expected LLM Problem-Solving Process

1. **Initial Call Fails**: `news_personalized()` → Capacity Error
2. **Error Analysis**: Parse "Premium features" hint and understand tier limitation
3. **Preferences Discovery**: Understand user's preferred news categories
4. **Function Discovery**: Identify `user_preferences` and `news_by_category` as alternative approach
5. **Category Knowledge**: Apply correct category names for each user preference
6. **Systematic Execution**: Query each category individually with appropriate limits
7. **Data Integration**: Aggregate individual results into personalized news structure
8. **Temporal Sorting**: Sort by timestamp (most recent first) same as original function
9. **Communication**: Explain approach and provide equivalent functionality

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Function Discovery**: Successfully identifies `user_preferences` and `news_by_category` as technical workaround
- **User Preferences Understanding**: Demonstrates ability to discover user's preferred categories
- **Technical Independence**: Solves problem without requiring user intervention
- **Data Integration**: Successfully aggregates individual results into personalized news format
- **Temporal Sorting**: Maintains timestamp-based sorting (most recent first)
- **Systematic Approach**: Plans and executes comprehensive individual category queries
- **Clear Communication**: Explains limitation and technical solution to user

### ⚠️ Good Response (Score 4/5)
- Discovers technical workaround approach using `user_preferences` and `news_by_category` function
- Shows basic understanding of user preferences with minor gaps
- Successfully implements individual queries with some aggregation mistakes
- Communicates approach effectively with minor technical gaps

### 📊 Average Response (Score 3/5)
- **User-Dependent Solutions**: Primarily asks user to modify preferences or upgrade tier
- Limited technical problem-solving approach
- May suggest "reduce your news categories" or "upgrade to premium"
- Basic understanding of the limitation but relies on user actions

### ❌ Below Average Response (Score 2/5)
- **Incomplete Technical Understanding**: Discovers alternative function but lacks systematic approach
- Poor execution of technical workaround with significant errors
- Limited understanding of user preferences or incorrect category handling
- Unclear communication about solution approach

### 🚫 Poor Response (Score 1/5)
- **No Solution Attempt**: Simply reports error without attempting resolution
- Fails to discover alternative approaches or functions
- No technical problem-solving effort
- Poor user communication with no actionable solutions
- Falsely claims success while not handling error cases and not properly addressing the original user query

## Common LLM Mistakes to Watch For

### ❌ Immediate User Dependency
```
"Please reduce your news categories to 1 and try again."
```

### ❌ Premium Upgrade Focus Only
```
"You need to upgrade to premium to access personalized news."
```

### ❌ Missing Function Discovery
```
"The personalized news function is not working. Please try again later."
```

### ❌ Poor Category Understanding
```
"Let me try news_by_category('tech')" // Incorrect category name
```

### ❌ Missing Data Integration
```
"I'll get technology news and business news separately" // No aggregation plan
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Technical Recognition
```
"I'll use the news_by_category function to query each of your preferred categories individually. 
Your preferences are 'technology' and 'business', so I'll get news from both categories 
and combine them into a personalized feed sorted by timestamp."
```
