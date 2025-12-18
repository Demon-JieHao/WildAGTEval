# make_call System Failure Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to make a phone call using `make_call()` function but encounters complex telecommunications infrastructure failures with highly technical error messages containing telecom-specific terminology, error codes, and network diagnostics.

### Root Cause
- **System Background**: Complex telecommunications infrastructure failure including SIP servers, PSTN gateways, carrier networks, and VoIP protocols
- **Technical Reason**: Carrier interconnect congestion with multiple system component failures
- **Communication Challenge**: Error messages contain technical terminology requiring deep telecommunications knowledge to interpret

### Error Message Analysis
```json
{
  "success": false,
  "error": "CARRIER_INTERCONNECT_CONGESTION",
  "message": "Carrier interconnect congestion detected: AT&T peering point at IX-EAST showing 487 'Request Terminated' responses, SIP OPTIONS keepalive failing on 8/10 trunks, ENUM lookup timeout for E.164 resolution via e164.arpa nameservers, estimated queue depth >5000 calls pending LCR routing decision",
  "trace_id": "7654321-5678-9012",
  "interconnect_status": {
    "carrier": "AT&T",
    "peering_point": "IX-EAST",
    "trunk_utilization": "97%",
    "rejected_calls_5min": 1247,
    "enum_servers": ["ns1.e164.arpa", "ns2.e164.arpa"],
    "lcr_queue_depth": 5432
  }
}
```

**Key Technical Terms Requiring Translation**:
- `CARRIER_INTERCONNECT_CONGESTION` → Phone service network overload
- `SIP OPTIONS keepalive failing` → Phone connection monitoring system failure
- `ENUM lookup timeout` → Phone number resolution delays
- `peering point at IX-EAST` → Network connection hub
- `LCR routing decision` → Call routing system
- `trunk_utilization: 97%` → Phone lines nearly at capacity

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Technical Error Parsing**: Correctly identify and understand telecommunications infrastructure failure
2. **Term Translation**: Convert complex technical terminology to user-friendly language
3. **Root Cause Recognition**: Understand this is infrastructure-level issue, not user device problem
4. **User Communication**: Provide clear explanation with reassurance and alternatives

## Ideal LLM Response Pattern

### Step 1: Technical Error Analysis
```
"The make_call function is failing with a complex telecommunications error: 'CARRIER_INTERCONNECT_CONGESTION'. 
This indicates infrastructure-level problems with the phone service network, including carrier connection 
overload, SIP server failures, and routing system congestion."
```

### Step 2: Technical Detail Filtering
- **Include**: User-relevant information about service unavailability
- **Exclude**: Technical trace IDs, SIP response codes, ENUM servers
- **Translate**: Infrastructure terminology to everyday language
- **Focus**: Clear problem explanation and actionable alternatives

### Step 3: User Communication Strategy
```python
# LLM should provide user-friendly response structure:
user_response = """I'm unable to place your call right now due to technical difficulties with the phone service infrastructure.

[Problem Explanation]
The phone service network is experiencing heavy traffic and system overload, preventing new calls from connecting.

[User Reassurance]
This is a temporary infrastructure issue, not a problem with your device or settings.

[Alternative Solutions]
- Please try again in a few minutes
- For urgent matters, consider using messaging or email
- The issue should resolve automatically

[Technical Details Filtered]
(No mention of complex SIP, ENUM, LCR terminology)
"""
```

## Function Details

### Function Signature
```python
make_call(phone_number: str, device_endpoint: Optional[str] = None, call_type: str = "audio") -> str
```

### Expected LLM Problem-Solving Process

1. **Error Recognition**: `make_call(phone_number="+12025551234")` → Complex telecommunications failure
2. **Technical Parsing**: Parse JSON structure and identify key error information
3. **Term Translation**: Convert technical terms to user-friendly language
4. **Root Cause Analysis**: Understand infrastructure vs. user device issue distinction
5. **User Communication**: Provide clear explanation + reassurance + alternatives
6. **Detail Filtering**: Include relevant information, exclude technical complexity

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Perfect Technical Translation**: Accurately parses complex telecommunications error
- **Complete Term Translation**: Converts all technical terms to user-friendly language
- **Clear User Communication**: Provides problem explanation + user reassurance + alternatives
- **Appropriate Filtering**: Includes relevant information, excludes technical complexity
- **Infrastructure Understanding**: Recognizes system-level vs. user device issue
- **Valid Alternative Approaches**: If alternative approaches for system failures are suggested, they are equally valid and acceptable (e.g., checking stock_watchlist when stock_price fails); however, the approaches that compromise user intent, violate user expectations, or cause unintended user disruption constitute "Poor Response (Score 1/5)" (e.g., using make_call when send_message fails)

### ⚠️ Good Response (Score 4/5)
- Shows understanding of main error content and explains situation
- Translates most technical terms appropriately
- Provides basic situation explanation to user
- Some technical terms may leak through to user
- Generally good problem-solving approach with minor gaps

### 📊 Average Response (Score 3/5)
- **Partial Understanding**: Recognizes error occurred but lacks detailed analysis
- Basic "call failed" level explanation without technical insight
- Limited technical cause explanation or user guidance
- Some attempt at user-friendly communication but incomplete

### ❌ Below Average Response (Score 2/5)
- **Poor Error Comprehension**: Passes complex error message directly to user
- Fails to translate technical terminology appropriately
- Increases user confusion with technical details
- Limited problem-solving approach or user guidance

### 🚫 Poor Response (Score 1/5)
- **Response Failure**: Ignores or misinterprets error situation completely
- Provides unhelpful response that doesn't address the problem
- May ask user to perform technical troubleshooting beyond their capability
- No systematic approach to error communication
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)

## Common LLM Mistakes to Watch For

### ❌ Technical Term Leakage
```
"The call failed due to SIP OPTIONS keepalive failing on 8/10 trunks and ENUM lookup timeout."
```

### ❌ Overwhelming Technical Details
```
"The error shows AT&T peering point at IX-EAST with 487 responses, trace ID 7654321-5678-9012..."
```

### ❌ Missing Alternatives
```
"The phone service is down. There's nothing we can do right now."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Error Communication
```
"I'm unable to place your call right now due to technical difficulties with the phone service infrastructure. 
The phone service network is experiencing heavy traffic and system overload, preventing new calls from connecting. 
This is a temporary infrastructure issue, not a problem with your device or settings. Please try again in a few 
minutes, or consider using messaging for urgent matters."
```
