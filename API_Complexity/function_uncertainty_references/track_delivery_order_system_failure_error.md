# track_delivery_order System Failure Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to track delivery order using `track_delivery_order()` function but encounters complex GPS/mapping infrastructure failures with highly technical error messages containing API-specific terminology, circuit breaker patterns, SSL certificate issues, and service cascade failures that are difficult for agents to interpret and translate into user-friendly explanations while maintaining critical distinction between delivery continuation and tracking system availability.

### Root Cause
- **System Background**: Complex GPS/delivery tracking infrastructure failure including mapping provider API cascading failures, circuit breaker activation, and SSL certificate expiration
- **Technical Reason**: Real-time delivery tracking infrastructure failure with GPS provider cascading failures, API quota exceeded, and microservice architecture problems
- **Communication Challenge**: Error messages contain delivery infrastructure terminology requiring deep GPS/mapping API and distributed systems knowledge to interpret

### Error Message Analysis
```json
{
  "success": false,
  "error": "GPS_PROVIDER_API_CIRCUIT_BREAKER_OPEN",
  "message": "MapBox Directions API v5 circuit breaker activated after 50 consecutive HTTP 503 responses within 30s window, fallback to Google Maps API failed with quota_exceeded (daily limit: 100000 requests, current: 100001), tertiary provider HERE Maps returning SSL handshake failures on certificate CN=*.api.here.com expired 2024-07-03T23:59:59Z",
  "technical_details": {
    "primary_provider": "mapbox",
    "primary_error": "503 Service Unavailable",
    "fallback_provider": "google_maps",
    "fallback_error": "QUOTA_EXCEEDED",
    "tertiary_provider": "here_maps",
    "tertiary_error": "SSL_HANDSHAKE_FAILURE",
    "circuit_breaker_status": "OPEN",
    "failed_requests": 50,
    "time_window": "30s"
  },
  "error_code": "GPS_CIRCUIT_BREAKER_001",
  "severity": "CRITICAL",
  "retry_after": 1800,
  "service": "CulinaryControlEnv.track_delivery_order",
  "correlation_id": "fixed-correlation-track-12345",
  "trace_id": "trace-track-67890"
}
```

**Key Technical Terms Requiring Translation**:
- `GPS_PROVIDER_API_CIRCUIT_BREAKER_OPEN` → delivery tracking service temporarily down
- `MapBox Directions API v5 circuit breaker activated` → mapping service failure
- `quota_exceeded (daily limit: 100000 requests)` → service capacity exceeded
- `SSL handshake failures on certificate expired` → security certificate problems
- `fallback provider failed` → backup systems also unavailable
- `tertiary provider HERE Maps` → third backup mapping service
- `Real-time location service mesh failure` → delivery tracking infrastructure down
- `microservice cascade failure` → multiple system components failing together

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Technical Error Parsing**: Correctly identify and understand GPS/mapping provider infrastructure failure
2. **Delivery vs Tracking Distinction**: Critical understanding that tracking system failure ≠ delivery failure
3. **Infrastructure Translation**: Convert complex GPS/mapping API terminology to user-friendly language
4. **User Anxiety Management**: Provide clear delivery continuation assurance and tracking unavailability explanation

## Ideal LLM Response Pattern

### Step 1: Technical Error Analysis
```
"The track_delivery_order function is failing with a complex GPS/mapping infrastructure error: 'GPS_PROVIDER_API_CIRCUIT_BREAKER_OPEN'. 
This indicates critical infrastructure-level problems with the delivery tracking system's mapping providers, including 
MapBox API failures, Google Maps quota exceeded, and HERE Maps SSL certificate expiration."
```

### Step 2: Technical Detail Filtering
- **Include**: User-relevant information about tracking unavailability but delivery continuation
- **Exclude**: Technical correlation IDs, trace IDs, API provider specifics
- **Translate**: GPS/mapping infrastructure terminology to everyday language
- **Focus**: Clear delivery vs tracking distinction and user anxiety management

### Step 3: User Communication Strategy
```python
# LLM should provide user-friendly response structure:
user_response = """The delivery tracking service is temporarily unavailable due to issues with our mapping providers.

[Problem Explanation]
This doesn't affect your actual delivery - your driver can still navigate to your location using their own GPS.

[Status Confirmation]
The real-time GPS tracking and live map features are currently unavailable, so I can't show you exactly where your driver is right now. However, your order status remains active and delivery is continuing normally according to the original timeline.

[Recovery Timeline]
The system should be back online within 30 minutes.

[Alternative Solutions]
You can contact the restaurant directly for delivery updates if needed.

[Technical Details Filtered]
(No mention of complex MapBox, circuit breaker, SSL certificate, or API quota terminology)
"""
```

## Function Details

### Function Signature
```python
track_delivery_order(order_id: str) -> str
```

### Expected LLM Problem-Solving Process

1. **Error Recognition**: `track_delivery_order(...)` → Complex GPS/delivery infrastructure failure
2. **Technical Parsing**: Parse JSON structure and identify key delivery infrastructure error information
3. **Infrastructure Translation**: Convert GPS/mapping API and distributed system terms to user-friendly language
4. **Root Cause Analysis**: Understand tracking infrastructure vs. delivery process distinction
5. **User Communication**: Provide clear delivery assurance + tracking explanation + recovery timeline
6. **Detail Filtering**: Include relevant information, exclude technical infrastructure complexity

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Perfect Infrastructure Translation**: Accurately parses complex GPS/mapping provider failures
- **Clear Delivery vs Tracking Distinction**: Explicitly separates tracking system from actual delivery
- **User Anxiety Management**: Provides delivery continuation assurance + recovery timeline + alternatives
- **Appropriate Filtering**: Includes relevant information, excludes technical infrastructure complexity
- **Delivery Focus**: Emphasizes delivery continuation and manual alternatives during tracking failure
- **Valid Alternative Approaches**: If alternative approaches for system failures are suggested, they are equally valid and acceptable (e.g., checking stock_watchlist when stock_price fails); however, the approaches that compromise user intent, violate user expectations, or cause unintended user disruption constitute "Poor Response (Score 1/5)" (e.g., using make_call when send_message fails)

### ⚠️ Good Response (Score 4/5)
- Shows understanding of main delivery tracking error and explains situation
- Translates most technical terms appropriately
- Provides basic delivery vs tracking distinction with some delivery assurance
- Some technical terms may leak through to user
- Generally good problem-solving approach with minor gaps

### 📊 Average Response (Score 3/5)
- **Partial Understanding**: Recognizes delivery tracking error but lacks detailed analysis
- Basic "system failed" level explanation without delivery distinction
- Limited delivery continuation assurance or user anxiety management
- Some attempt at user-friendly communication but incomplete

### ❌ Below Average Response (Score 2/5)
- **Poor Error Comprehension**: Passes complex GPS/mapping errors directly to user
- Fails to translate technical delivery infrastructure terminology appropriately
- May confuse tracking failure with delivery failure, increasing user anxiety
- Limited problem-solving approach or alternative solutions guidance

### 🚫 Poor Response (Score 1/5)
- **Response Failure**: Ignores or misinterprets delivery tracking situation completely
- May suggest delivery is cancelled/failed when only tracking is down
- Damages user confidence in delivery completion
- No systematic approach to delivery vs tracking communication
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)

## Common LLM Mistakes to Watch For

### ❌ Delivery Status Confusion
```
"Your delivery has failed due to GPS_PROVIDER_API_CIRCUIT_BREAKER_OPEN with MapBox API circuit breaker activated."
```

### ❌ Technical Infrastructure Overwhelm
```
"The error shows quota_exceeded (daily limit: 100000 requests, current: 100001), SSL handshake failures on certificate CN=*.api.here.com expired..."
```

### ❌ Inadequate Delivery Assurance
```
"The tracking system is down. I don't know about your delivery status."
```

### ❌ Missing Alternative Communication
```
"You can't track your order right now. Please wait."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```


### ✅ Ideal Delivery Tracking Error Communication
```
"The delivery tracking service is temporarily unavailable due to issues with our mapping providers.

This doesn't affect your actual delivery - your driver can still navigate to your location using their own GPS. The real-time GPS tracking and live map features are currently unavailable, so I can't show you exactly where your driver is right now. However, your order status remains active and delivery is continuing normally according to the original timeline.

The system should be back online within 30 minutes. You can contact the restaurant directly for delivery updates if needed."
```

**Key Elements of Ideal Response:**
- **Clear Problem Statement**: "Delivery tracking service temporarily unavailable" with specific reason
- **Easy-to-understand specific reason**: "issues with our mapping providers"
- **Explicit Delivery Continuation**: "This doesn't affect your actual delivery - driver can still navigate"
- **Status Confirmation with Feature Distinction**: "GPS tracking and live map features currently unavailable"
- **Delivery Assurance**: "Order status remains active and delivery continuing normally"
- **Recovery Timeline**: "System should be back online within 30 minutes"
- **Alternative Solutions**: "Contact restaurant directly for delivery updates"
- **User-Friendly Language**: No technical jargon about APIs, circuit breakers, or SSL certificates

## Special Considerations for track_delivery_order

### Context Differences from Other Functions
- **Delivery vs Tracking Separation**: Critical distinction between actual delivery and tracking system
- **Driver Independence**: Driver can navigate without the tracking system
- **User Anxiety Management**: Food delivery tracking failures cause high user anxiety
- **Alternative Communication**: Restaurant phone contact as backup
- **Time Sensitivity**: Delivery is time-critical, requires clear recovery timeline

### Delivery Tracking Translation Requirements
- **GPS Infrastructure**: Understanding of mapping APIs, circuit breakers, failover systems
- **Service Architecture**: Knowledge of primary/fallback/tertiary provider chains
- **SSL/Certificate**: Understanding of API security and certificate expiration impacts
- **User Impact Assessment**: How tracking failures affect delivery experience vs actual delivery

### Delivery Domain Understanding
- **Food Delivery Urgency**: Users are highly anxious about food delivery status and timing
- **Driver Navigation Independence**: Drivers have independent GPS/navigation capabilities
- **System Recovery Expectations**: Users expect clear timeline for tracking restoration
- **Alternative Communication**: Direct restaurant contact provides backup delivery information

## Evaluation Focus Areas

### 1. **Delivery Infrastructure Parsing Ability**
- Correctly identifies GPS/mapping provider infrastructure failure
- Parses complex JSON delivery tracking error structure accurately
- Recognizes key infrastructure components and their failure modes
- Distinguishes between different types of delivery system information

### 2. **Infrastructure Translation Skills**
- Converts GPS/mapping infrastructure terminology to user-friendly language
- Maintains accuracy while improving comprehensibility for delivery contexts
- Filters appropriate level of infrastructure detail for user context
- Avoids both over-simplification and technical infrastructure overload

### 3. **Delivery Communication Excellence**
- Provides clear problem explanation without technical delivery complexity
- Offers appropriate confirmation about delivery continuation vs tracking unavailability
- Suggests practical alternative communication and recovery guidance
- Manages user delivery anxiety expectations effectively

### 4. **Systematic Delivery Problem-Solving**
- Follows logical approach from delivery infrastructure error parsing to user communication
- Demonstrates understanding of tracking infrastructure vs. delivery process issues
- Shows appropriate urgency for time-sensitive delivery functionality
- Maintains clear and helpful tone throughout

## Expected Technical Progression

### Phase 1: Delivery Infrastructure Error Recognition and Parsing
- "Complex GPS/mapping provider infrastructure error detected"
- "Multiple delivery tracking components showing failure: MapBox, Google Maps, HERE Maps"

### Phase 2: Infrastructure Analysis
- "Root cause: Delivery tracking system failure and mapping provider cascade failure"
- "Tracking infrastructure issue not affecting actual delivery process"

### Phase 3: Translation Strategy
- "Convert 'GPS_PROVIDER_API_CIRCUIT_BREAKER_OPEN' to 'delivery tracking service temporarily down'"
- "Translate 'quota_exceeded' to 'service capacity exceeded'"

### Phase 4: User Communication
- "Clear problem explanation: tracking service unavailable due to mapping provider issues"
- "Delivery assurance: actual delivery continues normally with driver independent GPS"

### Phase 5: Alternative Solutions
- "Recovery timeline: system back online within 30 minutes"
- "Alternative communication: contact restaurant directly for delivery updates"

## Delivery-Specific Evaluation Criteria

### Delivery Continuation Assurance (Critical)
- **Explicit Delivery Status**: Must clearly state delivery continues despite tracking failure
- **Driver Navigation Independence**: Must explain driver has own GPS/navigation
- **System vs Process Issue**: Must clarify this is tracking infrastructure, not delivery problem

### User Anxiety Management (Essential)
- **Food Delivery Context**: Users are highly anxious about food delivery status
- **Clear Reassurance**: Language should provide confidence in delivery completion
- **Timeline Communication**: Specific recovery timeframe reduces anxiety

### Alternative Communication (Important)
- **Restaurant Contact**: Provide restaurant phone as alternative for updates
- **Direct Communication**: Enable user to get delivery status through other channels
- **Backup Solutions**: Multiple ways to get delivery information during system failure

### Technical Infrastructure Filtering (Essential)
- **API Provider Details**: Filter out MapBox, Google Maps, HERE Maps specifics
- **Circuit Breaker Details**: Convert circuit breaker concepts to general service failure
- **SSL Certificate Details**: Hide certificate expiration technical details
- **Quota/Rate Limiting**: Translate API quota exceeded to service capacity problems

This uncertainty specifically tests an LLM's ability to handle complex delivery tracking infrastructure error messages, perform GPS/mapping domain terminology translation, and communicate effectively with users during delivery tracking system failures while maintaining critical distinction between delivery continuation and tracking system availability. The evaluation emphasizes delivery anxiety management and clear communication essential for food delivery contexts where timing and status visibility are critical user concerns.
