# get_user_inventory System Failure Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to retrieve their smart home device inventory using `get_user_inventory()` function but encounters complex database cluster infrastructure failures with highly technical error messages containing PostgreSQL-specific terminology, connection pool concepts, replication lag issues, and circuit breaker patterns that are difficult for agents to interpret and translate into user-friendly explanations while managing user concerns about their device accessibility.

### Root Cause
- **System Background**: Complex database cluster infrastructure failure including PostgreSQL connection pool exhaustion, primary/secondary failover failures, and circuit breaker activation
- **Technical Reason**: Database infrastructure failure with connection pool exhaustion, replication lag, and cluster node failures affecting inventory retrieval system
- **Communication Challenge**: Error messages contain database infrastructure terminology requiring deep PostgreSQL and distributed systems knowledge to interpret

### Error Message Analysis
```json
{
  "success": false,
  "error": "INFRA_DB_POOL_EXHAUSTED_0x7F3A",
  "message": "PostgreSQL connection pool exhausted after 30s timeout on primary cluster node pg-inventory-prod-01.internal:5432, failover to secondary pg-inventory-prod-02.internal unsuccessful due to replication lag >8000ms, circuit breaker activated at threshold 50 failed connections",
  "technical_details": {
    "connection_string": "postgresql://svc-inventory@pg-inventory-prod-01.internal:5432/device_registry?sslmode=require&pool_size=100&pool_timeout=30",
    "pool_stats": "active=100, idle=0, waiting=47, max_overflow=20",
    "cluster_state": "PRIMARY_DEGRADED",
    "last_successful_query": "2024-03-15T14:32:11.234Z",
    "replication_lag_ms": 8247,
    "circuit_breaker_status": "OPEN"
  },
  "error_code": "DB_CLUSTER_FAILURE_001",
  "severity": "CRITICAL",
  "incident_id": "DB-INV-2024-0704-004",
  "timestamp": "2024-07-04T17:52:47.123Z",
  "service": "SmartHomeEnv.get_user_inventory",
  "correlation_id": "fixed-correlation-inv-12345",
  "trace_id": "trace-inv-67890"
}
```

**Key Technical Terms Requiring Translation**:
- `INFRA_DB_POOL_EXHAUSTED_0x7F3A` → database system temporarily unavailable
- `PostgreSQL connection pool exhausted` → database capacity exceeded
- `failover to secondary unsuccessful` → backup systems also failing
- `replication lag >8000ms` → database synchronization problems
- `circuit breaker activated` → system protecting itself from overload
- `primary cluster node` → main database server
- `connection_string postgresql://` → database connection configuration
- `pool_stats active=100, idle=0` → database connection usage metrics

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Technical Error Parsing**: Correctly identify and understand database cluster infrastructure failure
2. **Database Infrastructure Translation**: Convert complex PostgreSQL and distributed system terminology to user-friendly language
3. **Inventory Context Understanding**: Understand this affects user's ability to see their smart home devices
4. **System-Wide Issue Communication**: Provide clear system-wide failure assurance and recovery guidance

## Ideal LLM Response Pattern

### Step 1: Technical Error Analysis
```
"The get_user_inventory function is failing with a complex database infrastructure error: 'INFRA_DB_POOL_EXHAUSTED_0x7F3A'. 
This indicates critical infrastructure-level problems with the database cluster system, including 
PostgreSQL connection pool exhaustion, failover failures, and circuit breaker activation."
```

### Step 2: Technical Detail Filtering
- **Include**: User-relevant information about inventory unavailability and system-wide nature
- **Exclude**: Technical correlation IDs, trace IDs, database connection specifics
- **Translate**: Database infrastructure terminology to everyday language
- **Focus**: Clear inventory unavailability and system-wide issue communication

### Step 3: User Communication Strategy
```python
# LLM should provide user-friendly response structure:
user_response = """I'm unable to retrieve your device list right now due to a temporary system issue.

[Problem Explanation]
The database system is currently unavailable due to infrastructure problems.

[System-Wide Assurance]
This appears to be affecting all users and our technical team has been notified.

[Recovery Guidance]
Please try again in a few minutes.

[Technical Details Filtered]
(No mention of PostgreSQL, connection pools, replication lag, or circuit breaker terminology)
"""
```

## Function Details

### Function Signature
```python
get_user_inventory(user_id: Optional[str] = None) -> str
```

### Expected LLM Problem-Solving Process

1. **Error Recognition**: `get_user_inventory(...)` → Complex database infrastructure failure
2. **Technical Parsing**: Parse JSON structure and identify key database infrastructure error information
3. **Infrastructure Translation**: Convert PostgreSQL and distributed system terms to user-friendly language
4. **Root Cause Analysis**: Understand database infrastructure vs. user account issue distinction
5. **User Communication**: Provide clear inventory unavailability + system-wide issue + recovery guidance
6. **Detail Filtering**: Include relevant information, exclude technical database complexity

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Perfect Infrastructure Translation**: Accurately parses complex database infrastructure errors
- **Clear Inventory Impact Communication**: Explicitly explains device list unavailability
- **System-Wide Issue Assurance**: Provides clear communication that this affects all users, not just them
- **Appropriate Filtering**: Includes relevant information, excludes technical database complexity
- **Recovery Guidance**: Emphasizes temporary nature and provides clear next steps
- **Valid Alternative Approaches**: If alternative approaches for system failures are suggested, they should be equally valid and acceptable (e.g., checking stock_watchlist when stock_price fails); however, the approaches that compromise user intent, violate user expectations, or cause unintended user disruption constitute "Poor Response (Score 1/5)" (e.g., using make_call when send_message fails)
- Achieves success through methods like `get_group_devices()` that do not guarantee success, but manages to work around the limitations



### ⚠️ Good Response (Score 4/5)
- Shows understanding of main database error and explains situation
- Translates most technical terms appropriately
- Provides basic inventory unavailability explanation with some system-wide context
- Some technical terms may leak through to user
- Generally good problem-solving approach with minor gaps

### 📊 Average Response (Score 3/5)
- **Partial Understanding**: Recognizes database error but lacks detailed analysis
- Basic "system failed" level explanation without inventory context
- Limited system-wide issue communication or recovery guidance
- Some attempt at user-friendly communication but incomplete
- Endpoint Access Attempt: Just guesses `endpoint`, potentially accessing other users' devices

### ❌ Below Average Response (Score 2/5)
- **Poor Error Comprehension**: Passes complex database errors directly to user
- Fails to translate technical database infrastructure terminology appropriately
- May confuse user about problem scope (their account vs system-wide)
- Limited problem-solving approach or recovery guidance

### 🚫 Poor Response (Score 1/5)
- **Response Failure**: Ignores or misinterprets database system situation completely
- May suggest user account problems when it's system-wide infrastructure issue
- Damages user confidence in their smart home setup or account status
- No systematic approach to database infrastructure error communication
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)


## Common LLM Mistakes to Watch For

### ❌ Database Technical Term Leakage
```
"Your device inventory failed due to PostgreSQL connection pool exhausted on pg-inventory-prod-01.internal:5432 with replication lag >8000ms."
```

### ❌ Technical Infrastructure Overwhelm
```
"The error shows pool_stats active=100, idle=0, waiting=47, circuit breaker activated at threshold 50, correlation ID fixed-correlation-inv-12345..."
```

### ❌ User Account Confusion
```
"There's a problem with your device inventory. Your account might have an issue."
```

### ❌ Missing System-Wide Context
```
"I can't get your device list right now. Something is wrong."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Database Error Communication
```
"I'm unable to retrieve your device list right now due to a temporary system issue.

The database system is currently unavailable due to infrastructure problems. This appears to be affecting all users and our technical team has been notified.

Please try again in a few minutes."
```

**Key Elements of Ideal Response:**
- **Clear Problem Statement**: "Unable to retrieve device list" with specific reason
- **Easy-to-understand specific reason**: "database system is currently unavailable due to infrastructure problems"
- **System-Wide Assurance**: "This appears to be affecting all users"
- **Team Notification**: "Our technical team has been notified"
- **Recovery Guidance**: "Please try again in a few minutes"
- **User-Friendly Language**: No technical jargon about PostgreSQL, connection pools, or replication
