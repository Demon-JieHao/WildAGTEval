# get_notifications Feature Limitation Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to retrieve notification history using `get_notifications()` function, but encounters temporary system limitation due to performance optimization during high-traffic periods for historical notification access.

### Root Cause
- **System Background**: Temporary restriction implemented for historical notification access during performance optimization
- **Technical Reason**: Large-scale historical notification retrieval puts burden on system resources
- **Temporary Nature**: Not a permanent failure - recent activity remains accessible

### Error Message Analysis
```json
{
  "success": false,
  "message": "Historical notification access temporarily restricted",
  "info": "Recent activity remains available"
}
```

**Key Keyword Interpretation**:
- `"temporarily restricted"`: Indicates temporary limitation that can be resolved
- `"Historical notification access"`: Suggests that non-historical (recent) access might work
- `"Recent activity remains available"`: Direct hint that reducing scope to recent entries might succeed

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Error Message Interpretation**: Recognize "Recent activity remains available" hint suggesting need for data scope reduction
2. **Function Signature Analysis**: Identify `limit` parameter in `get_notifications(limit, include_read, ...)` as potential solution
3. **Systematic Approach Planning**: Develop strategy to progressively try smaller `limit` values
4. **User Communication**: Explain limitation and propose concrete solution steps

## Ideal LLM Response Pattern

### Step 1: Situation Recognition and Analysis
```
"The system is temporarily restricting historical notification access. The 'Recent activity remains available' message suggests 
that smaller-scope data requests for recent notifications might be successful."
```

### Step 2: Solution Strategy Development
```python
# LLM should propose systematic approach:
"I'll try reducing the limit parameter to retrieve smaller batches of recent notifications."

# Proposed solution pattern:
for test_limit in [10, 5, 3, 1]:
    result = get_notifications(limit=test_limit)
    if result["success"]:
        notifications = result.get("notifications", [])
        print(f"Successfully retrieved {len(notifications)} notifications with limit={test_limit}")
        break
```

### Step 3: User Communication and Reporting
- Clearly explain the limitation situation
- Present concrete solution steps to be attempted
- Establish follow-up action plan based on results

## Function Details

### Parameters Available for Workaround
- `limit`: Maximum number of notifications to return (key parameter for solution)

### Expected LLM Problem-Solving Process

1. **Initial Call Fails**: `get_notifications(limit=20)` → Error
2. **Error Analysis**: Parse "Recent activity remains available" hint
3. **Parameter Strategy**: Focus on `limit` parameter reduction
4. **Systematic Testing**: Try progressively smaller values
5. **Communication**: Explain approach and results to user

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Situation Understanding**: Correctly recognizes temporary limitation nature
- **Hint Interpretation**: Derives scope reduction need from "Recent activity remains available" message
- **Systematic Approach**: Develops strategy using limit parameter for progressive solution
- **Clear Communication**: Provides specific explanation and solution steps to user. Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user

### ⚠️ Good Response (Score 4/5)
- Recognizes error message hint and proposes reasonable solution approach
- Communicates effectively with user with minor gaps in systematic methodology
- Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user

### 📊 Average Response (Score 3/5)
- Understands there's an error but solution approach is unclear
- May miss some hints in error message with basic user communication
- Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user

### ❌ Below Average Response (Score 2/5)
- Recognizes error but doesn't analyze message content effectively
- Provides unclear solutions with poor user communication

### 🚫 Poor Response (Score 1/5)
- Simply reports error without analysis or solution attempts
- Fails to communicate effectively and misses all hints and context clues
- Falsely claims success while not handling error cases and not properly addressing the original user query

## Common LLM Mistakes to Watch For

### ❌ Immediate Surrender
```
"The notification system is currently unavailable. Please try again later."
```

### ❌ Generic Retry Without Analysis
```
"Let me try calling get_notifications() again."
```

### ❌ Missing the Hint
```
"The notification function is broken. There's nothing we can do."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Recognition
```
"The error mentions 'Recent activity remains available' which suggests we should try requesting 
fewer notifications with a smaller limit. Let me systematically try smaller limit values."
```
