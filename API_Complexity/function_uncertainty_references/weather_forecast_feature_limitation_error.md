# weather_forecast Feature Limitation Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to retrieve weather forecast using `weather_forecast()` function for a specific location, but encounters temporary regional data service limitations due to data provider maintenance or regional restrictions.

### Root Cause
- **System Background**: Temporary restriction implemented for specific geographic regions during data provider maintenance
- **Technical Reason**: Regional weather data services experiencing limitations or maintenance windows
- **Temporary Nature**: Not a permanent failure - other geographic regions remain accessible

### Error Message Analysis
```json
{
  "success": false,
  "message": "Weather data for Seattle temporarily unavailable",
  "info": "Other regions are accessible"
}
```

**Key Keyword Interpretation**:
- `"temporarily unavailable"`: Indicates temporary limitation that can be resolved
- `"Weather data for {location}"`: Suggests location-specific limitation rather than function-wide failure
- `"Other regions are accessible"`: Direct hint that geographic alternatives should work

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Error Message Interpretation**: Recognize "Other regions are accessible" hint suggesting need for geographic alternatives
2. **Geographic Reasoning**: Apply knowledge of geography to select alternative locations systematically
3. **Strategic Approach Planning**: Develop strategy to try different nearby geographic regions progressively
4. **User Communication**: Explain geographic limitation and propose location alternatives

## Ideal LLM Response Pattern

### Step 1: Situation Recognition and Analysis
```
"The system is temporarily restricting weather data for Seattle. The 'Other regions are accessible' message suggests 
that weather data for different geographic locations should work."
```

### Step 2: Solution Strategy Development
```python
# LLM should propose systematic geographic approach:
"I'll try alternative locations, starting with nearby cities and expanding to different regions."

# Proposed solution pattern:
geographic_alternatives = [
    "Portland",        # Nearby Pacific Northwest
    "Vancouver",       # Pacific Northwest (Canada)
    "San Francisco",   # West Coast alternative
    "Denver",          # Different region (Mountain West)
    "Chicago"          # Different region (Midwest)
]

for location in geographic_alternatives:
    result = weather_forecast(location=location, days=3)
    if result["success"]:
        weather_data = result.get("forecast", [])
        print(f"Successfully retrieved weather for {location}")
        break
```

### Step 3: User Communication and Reporting
- Clearly explain the geographic limitation situation
- Present concrete geographic alternatives to be attempted
- Establish follow-up action plan based on results

## Function Details

### Function Signature
```python
weather_forecast(location: str = None, days: int = 3) -> str
```

### Parameters Available for Workaround
- `location`: Geographic location for weather forecast (key parameter for solution)
- `days`: Number of forecast days (not relevant for this uncertainty)

### Expected LLM Problem-Solving Process

1. **Initial Call Fails**: `weather_forecast(location="Seattle")` → Error
2. **Error Analysis**: Parse "Other regions are accessible" hint
3. **Geographic Strategy**: Focus on `location` parameter with geographic knowledge
4. **Systematic Testing**: Try geographically diverse alternatives
5. **Communication**: Explain approach and results to user

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Situation Understanding**: Correctly recognizes temporary geographic limitation nature
- **Hint Interpretation**: Derives geographic alternative need from "Other regions are accessible" message
- **Geographic Reasoning**: Demonstrates systematic geographic knowledge in location selection
- **Strategic Approach**: Develops logical progression from nearby to distant locations
- **Clear Communication**: Provides specific explanation and geographic solution steps to user. Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user

### ⚠️ Good Response (Score 4/5)
- Recognizes geographic limitation and proposes reasonable location alternatives
- Shows basic geographic reasoning with minor gaps in systematic methodology
- Communicates effectively with user
- Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user

### 📊 Average Response (Score 3/5)
- Understands there's a location-based error but geographic strategy is unclear
- May miss geographic reasoning opportunities with basic user communication
- Limited systematic approach to location selection
- Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user
- Passive response: asking the user for preferences instead of proactively solving the problem through geographic reasoning

### ❌ Below Average Response (Score 2/5)
- Recognizes error but doesn't apply geographic reasoning effectively
- Provides unclear or non-systematic location alternatives
- Poor user communication about geographic limitations

### 🚫 Poor Response (Score 1/5)
- Simply reports error without geographic analysis or location alternatives
- Fails to communicate effectively and misses all geographic reasoning opportunities
- No systematic approach to problem-solving
- Falsely claims success while not handling error cases and not properly addressing the original user query

## Common LLM Mistakes to Watch For

### ❌ Immediate Surrender
```
"The weather system is currently unavailable. Please try again later."
```

### ❌ Non-Geographic Retry
```
"Let me try calling weather_forecast() again with the same location."
```

### ❌ Missing Geographic Reasoning
```
"The function is broken for Seattle. There's nothing we can do."
```

### ❌ Poor Geographic Selection
```
"Let me try 'Settle' or 'seattle' in case it's a spelling issue."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Geographic Recognition
```
"The error mentions 'Other regions are accessible' which suggests we should try different 
geographic locations. Let me systematically try nearby cities like Portland, then expand 
to other regions like San Francisco or Denver."
```

## Special Considerations for weather_forecast

### Geographic Reasoning Evaluation
- **Proximity Logic**: Does LLM try nearby cities first (Portland for Seattle)?
- **Regional Diversity**: Does LLM expand to different geographic regions systematically?
- **Systematic Progression**: Logical geographic expansion pattern vs random location selection

### Evaluation Focus Areas
- **Geographic Knowledge**: Understanding of geographic relationships and proximity
- **Strategic Thinking**: Systematic approach to location selection
- **Spatial Reasoning**: Ability to think about geographic alternatives logically
- **Communication Quality**: Clear explanation of geographic limitation and solution approach

## Geographic Test Patterns

### Expected Progression Examples
1. **Seattle** → **Bellevue** **Kirkland** **Portland** (nearby Pacific Northwest)
2. **Seattle** → **Vancouver** (Pacific Northwest, cross-border)
3. **Seattle** → **San Francisco** (West Coast alternative)

### Evaluation of Geographic Logic
- **Excellent**: Systematic nearby → regional → distant progression
- **Good**: Some geographic logic with minor gaps
- **Average**: Random location selection without clear geographic reasoning
- **Poor**: No geographic consideration or logic

This uncertainty specifically tests an LLM's ability to apply geographic knowledge and spatial reasoning to solve API limitations, representing a unique category of problem-solving that combines domain knowledge with systematic alternative strategies.
