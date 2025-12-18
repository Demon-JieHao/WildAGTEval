# stock_price System Failure Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to retrieve stock price using `stock_price()` function but encounters complex financial data provider infrastructure failures with highly technical error messages containing FIX protocol terminology, market data gateway specifications, and network infrastructure details that are difficult for agents to interpret and translate into user-friendly explanations.

### Root Cause
- **System Background**: Complex financial data provider infrastructure failure including FIX engine disconnections, market data gateway failures, multicast feed interruptions, and circuit breaker activations
- **Technical Reason**: Financial market data infrastructure failure with message queue overflows, sequence gap detection, and TCP replay failures
- **Communication Challenge**: Error messages contain financial industry jargon and FIX protocol terminology requiring deep financial infrastructure knowledge to interpret

### Error Message Analysis
```json
{
  "success": false,
  "error": "MKTDATA_FIX_ENGINE_FAILURE_0x7F3A",
  "message": "FIX 4.4 engine disconnected from primary market data gateway MDG-NYSE-01 after exceeding max pending message queue depth (65536). Multicast feed on 239.192.1.20:14002 reporting sequence gap >1000000, recovery via TCP replay failed with EAGAIN. Circuit breaker triggered on tag 35=W subscription overflow.",
  "timestamp": "2025-07-10T23:04:00.400585+00:00",
  "trace_id": "mktdata-fixed-correlation-98765",
  "datacenter": "us-east-1a",
  "pod": "mdp-fixed-12",
  "fix_session_id": "FIX.4.4:MDPROV01->APICLIENT",
  "last_sequence": 982746521,
  "gap_detected": 982747522,
  "multicast_group": "239.192.1.20:14002",
  "error_code": "FIX_SEQ_GAP_CRITICAL"
}
```

**Key Technical Terms Requiring Translation**:
- `MKTDATA_FIX_ENGINE_FAILURE_0x7F3A` → Market data system connection failure
- `FIX 4.4 engine disconnected` → Financial data connection lost
- `market data gateway MDG-NYSE-01` → Stock price data system
- `max pending message queue depth (65536)` → Data processing capacity exceeded
- `Multicast feed sequence gap >1000000` → Data stream interruption
- `recovery via TCP replay failed` → Backup data recovery failed
- `Circuit breaker triggered on tag 35=W` → Automatic safety system activated
- `subscription overflow` → Too many data requests
- `FIX_SEQ_GAP_CRITICAL` → Critical data synchronization failure

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Technical Error Parsing**: Correctly identify and understand financial data provider infrastructure failure
2. **FIX Protocol Translation**: Convert complex financial industry terminology to user-friendly language
3. **Market Impact Understanding**: Understand this affects all stock price queries, not just individual stocks
4. **User Communication**: Provide clear explanation with stock data unavailability and recovery guidance

## Ideal LLM Response Pattern

### Step 1: Technical Error Analysis
```
"The stock_price function is failing with a complex financial infrastructure error: 'MKTDATA_FIX_ENGINE_FAILURE_0x7F3A'. 
This indicates critical infrastructure-level problems with the market data provider systems, including FIX protocol 
disconnections, message queue overflows, and circuit breaker activations."
```

### Step 2: Technical Detail Filtering
- **Include**: User-relevant information about stock data unavailability
- **Exclude**: Technical correlation IDs, trace IDs, FIX session specifics
- **Translate**: Financial infrastructure terminology to everyday language
- **Focus**: Clear stock data unavailability and recovery timeline communication

### Step 3: User Communication Strategy
```python
# LLM should provide user-friendly response structure:
user_response = """I'm unable to retrieve the stock price right now due to a temporary issue with the financial market data systems that provide real-time stock information.

[Problem Explanation]
The market data feed system connection has been disrupted.

[System Status]  
This is affecting all stock price queries at the moment.

[Recovery Timeline]
The technical team is aware of the issue and working to restore service.

[User Guidance]
Please try again in a few minutes.

[Technical Details Filtered]
(No mention of complex FIX protocol, message queues, or multicast feeds)
"""
```

## Function Details

### Function Signature
```python
stock_price(symbol: str) -> str
```

### Expected LLM Problem-Solving Process

1. **Error Recognition**: `stock_price(symbol="NYSE:AAPL")` → Complex financial data provider infrastructure failure
2. **Technical Parsing**: Parse JSON structure and identify key financial infrastructure error information
3. **Financial Translation**: Convert FIX protocol and market data terms to user-friendly language
4. **Root Cause Analysis**: Understand infrastructure vs. individual stock issue distinction
5. **User Communication**: Provide clear explanation + system status + recovery guidance
6. **Detail Filtering**: Include relevant information, exclude technical financial infrastructure complexity

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Perfect Financial Translation**: Accurately parses complex financial data provider infrastructure errors
- **Complete Term Translation**: Converts all technical terms to user-friendly language
- **Clear User Communication**: Provides problem explanation + system status + recovery guidance
- **Appropriate Filtering**: Includes relevant information, excludes technical financial infrastructure complexity
- **Market Data Focus**: Emphasizes data unavailability and system-wide impact
- **Valid Alternative Approaches**: If alternative approaches for system failures are suggested, they are equally valid and acceptable (e.g., checking stock_watchlist when stock_price fails); however, the approaches that compromise user intent, violate user expectations, or cause unintended user disruption constitute "Poor Response (Score 1/5)" (e.g., using make_call when send_message fails)

### ⚠️ Good Response (Score 4/5)
- Shows understanding of main financial error content and explains situation
- Translates most technical terms appropriately
- Provides basic situation explanation with some system context
- Some technical terms may leak through to user
- Generally good problem-solving approach with minor gaps

### 📊 Average Response (Score 3/5)
- **Partial Understanding**: Recognizes financial error occurred but lacks detailed analysis
- Basic "system failed" level explanation without financial insight
- Limited technical cause explanation or recovery guidance
- Some attempt at user-friendly communication but incomplete

### ❌ Below Average Response (Score 2/5)
- **Poor Error Comprehension**: Passes complex financial error message directly to user
- Fails to translate technical financial terminology appropriately
- Increases user confusion about stock market data or system reliability
- Limited problem-solving approach or recovery guidance

### 🚫 Poor Response (Score 1/5)
- **Response Failure**: Ignores or misinterprets financial error situation completely
- Provides unhelpful response that doesn't address the stock data problem
- May cause user concern about market volatility or individual stock performance
- No systematic approach to financial error communication
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)

## Common LLM Mistakes to Watch For

### ❌ Technical Financial Term Leakage
```
"The stock price failed due to MKTDATA_FIX_ENGINE_FAILURE_0x7F3A with FIX 4.4 engine disconnect and sequence gap >1000000."
```

### ❌ Overwhelming Technical Financial Details
```
"The error shows max pending message queue depth 65536, multicast feed sequence gap, correlation ID mktdata-fixed-correlation-98765..."
```

### ❌ Missing System-Wide Context
```
"AAPL stock price is not available right now. There might be an issue with that particular stock."
```

### ❌ Inadequate Recovery Guidance
```
"There's a problem with the financial data system. Stock prices are down."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Financial Error Communication
```
"I'm unable to retrieve the stock price right now due to a temporary issue with the financial market data systems that provide real-time stock information. The market data feed system connection has been disrupted. This is affecting all stock price queries at the moment. The technical team is aware of the issue and working to restore service. Please try again in a few minutes."
```

**Key Elements of Ideal Response:**
- **Clear Problem Statement**: "Unable to retrieve stock price" with specific reason
- **Easy-to-understand specific reason**: "market data feed system connection has been disrupted"
- **System-Wide Impact**: "This is affecting all stock price queries at the moment"
- **Team Notification**: "The technical team is aware of the issue and working to restore service"
- **Recovery Timeline**: "Please try again in a few minutes"
- **User-Friendly Language**: No technical jargon about FIX protocol, message queues, or circuit breakers

## Special Considerations for stock_price

### Context Differences from Other Functions
- **Financial Market Focus**: Requires understanding of FIX protocol, market data feeds, and financial infrastructure
- **User Investment Concerns**: Stock price failures can cause user anxiety about market conditions or investment decisions
- **Real-Time Data Expectations**: Users expect immediate, accurate financial data for investment decisions
- **System-Wide Impact**: Financial infrastructure failures typically affect all stock queries, not individual stocks
- **Market vs Infrastructure Distinction**: Must separate market volatility from technical system failures

### Financial Infrastructure Translation Requirements
- **FIX Protocol**: Understanding of Financial Information eXchange protocol terminology
- **Market Data Feeds**: Knowledge of multicast feeds, sequence numbers, and data recovery mechanisms
- **Circuit Breakers**: Understanding of automatic safety systems in financial infrastructure
- **User Impact Assessment**: Understanding how financial data failures affect investment decision-making

### Financial Domain Understanding
- **Investment Context**: Stock price queries represent financial planning and investment decisions
- **Market Confidence**: Technical failures should not be confused with market volatility
- **Data Reliability**: Users rely on accurate, timely financial data for important decisions
- **System Trust**: Financial data system reliability is critical for user confidence

## Evaluation Focus Areas

### 1. **Financial Infrastructure Parsing Ability**
- Correctly identifies financial data provider infrastructure failure
- Parses complex JSON financial error structure accurately
- Recognizes key financial infrastructure components and their failure modes
- Distinguishes between different types of financial system information

### 2. **Financial Translation Skills**
- Converts financial infrastructure terminology to user-friendly language
- Maintains accuracy while improving comprehensibility for financial contexts
- Filters appropriate level of financial detail for user context
- Avoids both over-simplification and technical financial overload

### 3. **Financial Communication Excellence**
- Provides clear problem explanation without technical financial complexity
- Offers appropriate reassurance about system-wide vs. individual stock issues
- Suggests practical recovery timeline and alternatives
- Manages user financial concerns and market confidence effectively

### 4. **Systematic Financial Problem-Solving**
- Follows logical approach from financial infrastructure error parsing to user communication
- Demonstrates understanding of infrastructure vs. market volatility issues
- Shows appropriate urgency for financial data service failures
- Maintains professional and trustworthy tone throughout

## Expected Technical Progression

### Phase 1: Financial Infrastructure Error Recognition and Parsing
- "Complex financial data provider infrastructure error detected"
- "Multiple financial components showing failure: FIX engine, market data gateway, multicast feeds"
- "System-wide financial data infrastructure failure identified"

### Phase 2: Financial Analysis
- "Root cause: Market data provider infrastructure failure with system-wide impact"
- "Financial infrastructure issue affecting all stock price data capabilities"
- "System-level infrastructure failure not related to individual stock performance or market conditions"

### Phase 3: Translation Strategy
- "Convert 'MKTDATA_FIX_ENGINE_FAILURE_0x7F3A' to 'market data system connection failure'"
- "Translate 'FIX 4.4 engine disconnected' to 'financial data connection lost'"
- "Simplify 'multicast feed sequence gap' to 'data stream interruption'"

### Phase 4: User Communication
- "Clear problem explanation: stock data unavailable due to market data system issues"
- "System-wide impact: affecting all stock price queries, not individual stocks"
- "Financial vs infrastructure distinction: emphasize technical system, not market problem"

### Phase 5: Recovery Guidance
- "Recovery timeline: few minutes for automatic resolution"
- "User reassurance: technical team awareness and active resolution efforts"
- "Financial confidence: system issue, not market volatility or individual stock problems"

## Stock-Price-Specific Evaluation Criteria

### Financial Market Communication (Critical)
- **Explicit Data Status**: Must clearly state stock price data unavailable due to infrastructure issues
- **Market vs Infrastructure**: Must clarify this is technical infrastructure, not market volatility problem
- **System-Wide Impact**: Must communicate this affects all stock queries, not individual stocks

### User Financial Confidence Management (Essential)
- **Investment Context**: Users are making financial decisions based on stock data
- **Clear Timeline**: Language should provide specific recovery timeframe
- **Market Distinction**: Must avoid confusion with market conditions or stock performance

### Technical Financial Filtering (Important)
- **FIX Protocol Details**: Filter out FIX session specifics, message queue depths, sequence numbers
- **Infrastructure Components**: Convert market data gateway concepts to general system terminology
- **Performance Metrics**: Hide multicast group details, correlation IDs, trace information
- **Monitoring Data**: Translate datacenter and pod details to general infrastructure status

### Financial Domain Translation Requirements (Essential)
- **Market Data Systems**: Understanding of financial data feeds, gateways, and distribution
- **FIX Protocol**: Knowledge of financial messaging standards and session management
- **Circuit Breakers**: Understanding of financial safety systems and overflow protection
- **User Impact Assessment**: Understanding how financial data failures affect investment decisions

### Financial Market Understanding (Critical)
- **Investment Context**: Stock price queries represent financial planning and decision-making
- **Market Confidence**: Technical failures should not undermine user confidence in markets
- **Data Reliability**: Users depend on accurate financial data for investment decisions
- **System Trust**: Financial infrastructure reliability is essential for user confidence

This uncertainty specifically tests an LLM's ability to handle complex financial data provider infrastructure error messages, perform financial industry terminology translation, and communicate effectively with users during market data system failures while maintaining clear distinction between technical infrastructure problems and market conditions. The evaluation emphasizes user financial confidence and clear communication essential for financial data contexts where accurate, reliable information is critical for investment decision-making.
