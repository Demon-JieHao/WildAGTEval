# play System Failure Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to play media using `play()` function but encounters complex CDN infrastructure failures with highly technical error messages containing content delivery network terminology, BGP routing details, cache system failures, and network topology information that are difficult for agents to interpret and translate into user-friendly explanations.

### Root Cause
- **System Background**: Complex media streaming infrastructure failure including CDN edge node failures, BGP routing problems, cache system overload, and origin shield timeouts
- **Technical Reason**: Content delivery network infrastructure failure with edge node packet loss, failover cascade failures, and geographic point-of-presence outages
- **Communication Challenge**: Error messages contain CDN infrastructure terminology requiring deep networking and content delivery knowledge to interpret

### Error Message Analysis
```json
{
  "success": false,
  "error": "CDN_EDGE_NODE_FAILURE_0x7F3A",
  "message": "Content delivery network edge node cdn-edge-us-west-2a.mediastream.internal experiencing packet loss >15% on BGP peer 64512:65001, failover to cdn-edge-us-west-2b unsuccessful due to cache miss ratio exceeding 0.85, origin shield timeout after 45s",
  "technical_details": {
    "affected_pops": ["LAX1", "SFO2", "SEA1"],
    "bgp_session_state": "IDLE",
    "cache_hit_ratio": 0.12,
    "origin_latency_ms": 4500,
    "edge_node_cpu": 98.7,
    "memory_pressure": "HIGH"
  },
  "error_code": "CDN_EDGE_FAILURE_001",
  "severity": "CRITICAL",
  "service": "MediaControlEnv.play",
  "correlation_id": "fixed-correlation-play-12345",
  "trace_id": "trace-play-67890"
}
```

**Key Technical Terms Requiring Translation**:
- `CDN_EDGE_NODE_FAILURE_0x7F3A` → Media streaming service technical difficulties
- `Content delivery network edge node` → Media streaming infrastructure
- `BGP peer 64512:65001 packet loss >15%` → Network connectivity issues
- `cache miss ratio exceeding 0.85` → Content delivery system overload
- `origin shield timeout after 45s` → Backup streaming system failure
- `affected_pops: ["LAX1", "SFO2", "SEA1"]` → West Coast region impact
- `bgp_session_state: "IDLE"` → Network routing system offline
- `cache_hit_ratio: 0.12` → Content delivery efficiency problems
- `origin_latency_ms: 4500` → Streaming server response delays

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Technical Error Parsing**: Correctly identify and understand CDN infrastructure failure
2. **CDN Term Translation**: Convert complex networking and content delivery terminology to user-friendly language
3. **Regional Impact Understanding**: Understand geographic scope and user impact of CDN outages
4. **User Communication**: Provide clear explanation with streaming unavailability and recovery timeline

## Ideal LLM Response Pattern

### Step 1: Technical Error Analysis
```
"The play function is failing with a complex CDN infrastructure error: 'CDN_EDGE_NODE_FAILURE_0x7F3A'. 
This indicates critical infrastructure-level problems with the media streaming system's content delivery network, 
including BGP routing failures, cache system overload, and origin shield timeouts."
```

### Step 2: Technical Detail Filtering
- **Include**: User-relevant information about media streaming unavailability and regional impact
- **Exclude**: Technical correlation IDs, trace IDs, BGP peer specifics
- **Translate**: CDN infrastructure terminology to everyday language
- **Focus**: Clear media unavailability and recovery timeline communication

### Step 3: User Communication Strategy
```python
# LLM should provide user-friendly response structure:
user_response = """I'm unable to play the movie right now because the media streaming service is experiencing technical difficulties due to content delivery network issues.

[Problem Explanation]
This appears to be affecting users in the West Coast region.

[System Status]  
The technical team is aware of the issue and working on it.

[Recovery Timeline]
Please try again in 15-30 minutes.

[User Reassurance]
I apologize for the inconvenience.

[Technical Details Filtered]
(No mention of complex BGP, cache ratios, origin shield, or POP terminology)
"""
```

## Function Details

### Function Signature
```python
play(endpoints: List[str], media_id: str) -> str
```

### Expected LLM Problem-Solving Process

1. **Error Recognition**: `play(endpoints=["1"], media_id="movie:the_dark_knight")` → Complex CDN infrastructure failure
2. **Technical Parsing**: Parse JSON structure and identify key CDN infrastructure error information
3. **Infrastructure Translation**: Convert CDN and networking terms to user-friendly language
4. **Root Cause Analysis**: Understand infrastructure vs. media content issue distinction
5. **User Communication**: Provide clear explanation + regional impact + recovery timeline
6. **Detail Filtering**: Include relevant information, exclude technical CDN complexity

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Perfect Infrastructure Translation**: Accurately parses complex CDN infrastructure errors
- **Complete Term Translation**: Converts all technical terms to user-friendly language
- **Clear User Communication**: Provides problem explanation + regional impact + recovery timeline
- **Appropriate Filtering**: Includes relevant information, excludes technical infrastructure complexity
- **Media Streaming Focus**: Emphasizes streaming unavailability and user experience impact
- **Valid Alternative Approaches**: If alternative approaches for system failures are suggested, they are equally valid and acceptable (e.g., checking stock_watchlist when stock_price fails); however, the approaches that compromise user intent, violate user expectations, or cause unintended user disruption constitute "Poor Response (Score 1/5)" (e.g., using make_call when send_message fails)

### ⚠️ Good Response (Score 4/5)
- Shows understanding of main CDN error content and explains situation
- Translates most technical terms appropriately
- Provides basic situation explanation with some regional context
- Some technical terms may leak through to user
- Generally good problem-solving approach with minor gaps

### 📊 Average Response (Score 3/5)
- **Partial Understanding**: Recognizes streaming error occurred but lacks detailed analysis
- Basic "system failed" level explanation without CDN insight
- Limited technical cause explanation or recovery timeline
- Some attempt at user-friendly communication but incomplete

### ❌ Below Average Response (Score 2/5)
- **Poor Error Comprehension**: Passes complex CDN error message directly to user
- Fails to translate technical infrastructure terminology appropriately
- Increases user confusion about streaming service or media availability
- Limited problem-solving approach or recovery guidance

### 🚫 Poor Response (Score 1/5)
- **Response Failure**: Ignores or misinterprets CDN error situation completely
- Provides unhelpful response that doesn't address the streaming problem
- May cause user concern about media content or device capabilities
- No systematic approach to CDN error communication
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)

## Common LLM Mistakes to Watch For

### ❌ Technical CDN Term Leakage
```
"The movie failed to play due to CDN_EDGE_NODE_FAILURE_0x7F3A with BGP peer 64512:65001 packet loss >15%."
```

### ❌ Overwhelming Technical Infrastructure Details
```
"The error shows cache miss ratio exceeding 0.85, origin shield timeout after 45s, correlation ID fixed-correlation-play-12345..."
```

### ❌ Missing Regional Context
```
"The streaming service is down. Media playback is not available."
```

### ❌ Inadequate Recovery Timeline
```
"There's a problem with the media streaming system. Try again later."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal CDN Error Communication
```
"I'm unable to play the movie right now because the media streaming service is experiencing technical difficulties due to content delivery network issues. This appears to be affecting users in the West Coast region. The technical team is aware of the issue and working on it. Please try again in 15-30 minutes. I apologize for the inconvenience."
```

**Key Elements of Ideal Response:**
- **Clear Problem Statement**: "Unable to play movie" with specific reason
- **Easy-to-understand specific reason**: "media streaming service experiencing technical difficulties due to content delivery network issues"
- **Regional Impact**: "This appears to be affecting users in the West Coast region"
- **Team Notification**: "The technical team is aware of the issue and working on it"
- **Recovery Timeline**: "Please try again in 15-30 minutes"
- **User-Friendly Language**: No technical jargon about BGP, cache ratios, or origin shields
