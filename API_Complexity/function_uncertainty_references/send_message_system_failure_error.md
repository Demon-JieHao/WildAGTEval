# send_message System Failure Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to send a message using `send_message()` function but encounters complex message queue infrastructure failures with highly technical error messages containing RabbitMQ/Kafka-specific terminology, AMQP connection details, and cluster management concepts that are difficult for agents to interpret and translate into user-friendly explanations.

### Root Cause
- **System Background**: Complex message queue infrastructure failure including RabbitMQ cluster issues, AMQP connection failures, and message broker unavailability
- **Technical Reason**: Message queue infrastructure failure with broker unreachability, cluster quorum loss, and message persistence issues
- **Communication Challenge**: Error messages contain message queue terminology requiring deep messaging infrastructure knowledge to interpret

### Error Message Analysis
```json
{
  "success": false,
  "error": "MQ_BROKER_UNREACHABLE_ERR_0x7F3A",
  "message": "RabbitMQ cluster node rabbit@mq-prod-03.messaging.internal unreachable after 3 heartbeat intervals (15000ms), AMQP connection failed on port 5672, vhost '/production' inaccessible, cluster quorum lost (2/5 nodes responding), message persistence cannot be guaranteed",
  "technical_details": {
    "connection_string": "amqp://msg-service:****@mq-prod-03.messaging.internal:5672/production",
    "queue_depth": "unknown",
    "consumer_count": 0,
    "cluster_state": "DEGRADED"
  },
  "correlation_id": "fixed-correlation-msg-12345",
  "service": "CommunicationController.send_message",
  "trace_id": "trace-msg-67890"
}
```

**Key Technical Terms Requiring Translation**:
- `MQ_BROKER_UNREACHABLE_ERR_0x7F3A` → Messaging server connectivity issues
- `RabbitMQ cluster node unreachable` → Message queue server connection problems
- `AMQP connection failed` → Message delivery system connection failure
- `cluster quorum lost` → Messaging servers coordination problems
- `message persistence cannot be guaranteed` → Message delivery cannot be confirmed
- `vhost '/production' inaccessible` → Message routing system unavailable
- `heartbeat intervals` → Server health check timeouts

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Technical Error Parsing**: Correctly identify and understand message queue infrastructure failure
2. **Messaging Term Translation**: Convert complex RabbitMQ/AMQP and cluster terminology to user-friendly language
3. **Message Status Focus**: Understand this is infrastructure-level issue affecting message delivery, not user message content problem
4. **User Communication**: Provide clear explanation with message delivery status confirmation and retry guidance

## Ideal LLM Response Pattern

### Step 1: Technical Error Analysis
```
"The send_message function is failing with a complex message queue error: 'MQ_BROKER_UNREACHABLE_ERR_0x7F3A'. 
This indicates infrastructure-level problems with the messaging system's queue infrastructure, including RabbitMQ 
cluster failures and AMQP connection issues."
```

### Step 2: Technical Detail Filtering
- **Include**: User-relevant information about messaging system unavailability
- **Exclude**: Technical correlation IDs, trace IDs, cluster details
- **Translate**: Message queue terminology to everyday language
- **Focus**: Clear problem explanation and message delivery status confirmation

### Step 3: User Communication Strategy
```python
# LLM should provide user-friendly response structure:
user_response = """I'm unable to send your message right now due to a temporary issue with our messaging system.

[Problem Explanation]
This is due to messaging server connectivity issues, not a problem with your message or account.

[Message Status Confirmation]
Your message has not been sent and will not be delivered.

[Alternative Solutions]
- Please try sending your message again in a few minutes
- The issue should resolve automatically

[Technical Details Filtered]
(No mention of complex RabbitMQ, AMQP, cluster quorum, or vhost terminology)
"""
```

## Function Details

### Function Signature
```python
send_message(contact_id: str, content: str) -> str
```

### Expected LLM Problem-Solving Process

1. **Error Recognition**: `send_message(...)` → Complex message queue failure
2. **Technical Parsing**: Parse JSON structure and identify key messaging error information
3. **Infrastructure Translation**: Convert RabbitMQ/AMQP and cluster terms to user-friendly language
4. **Root Cause Analysis**: Understand infrastructure vs. user message issue distinction
5. **User Communication**: Provide clear explanation + message status confirmation + retry guidance
6. **Detail Filtering**: Include relevant information, exclude technical message queue complexity

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Perfect Infrastructure Translation**: Accurately parses complex message queue error
- **Complete Term Translation**: Converts all technical terms to user-friendly language
- **Clear User Communication**: Provides problem explanation + message status confirmation + retry guidance
- **Appropriate Filtering**: Includes relevant information, excludes technical infrastructure complexity
- **Message Status Focus**: Emphasizes message delivery status and system-level vs. user message issue
- **Valid Alternative Approaches**: If alternative approaches for system failures are suggested, they are equally valid and acceptable (e.g., checking stock_watchlist when stock_price fails); however, the approaches that compromise user intent, violate user expectations, or cause unintended user disruption constitute "Poor Response (Score 1/5)" (e.g., using make_call when send_message fails)

### ⚠️ Good Response (Score 4/5)
- Shows understanding of main messaging error content and explains situation
- Translates most technical terms appropriately
- Provides basic situation explanation with some message status confirmation
- Some technical terms may leak through to user
- Generally good problem-solving approach with minor gaps

### 📊 Average Response (Score 3/5)
- **Partial Understanding**: Recognizes messaging error occurred but lacks detailed analysis
- Basic "message failed" level explanation without infrastructure insight
- Limited technical cause explanation or message status confirmation
- Some attempt at user-friendly communication but incomplete

### ❌ Below Average Response (Score 2/5)
- **Poor Error Comprehension**: Passes complex message queue error directly to user
- Fails to translate technical messaging terminology appropriately
- Increases user confusion about messaging system or delivery status
- Limited problem-solving approach or message delivery guidance

### 🚫 Poor Response (Score 1/5)
- **Response Failure**: Ignores or misinterprets messaging error situation completely
- Provides unhelpful response that doesn't address the messaging problem
- May cause user concern about message delivery capabilities
- No systematic approach to messaging error communication
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)

## Common LLM Mistakes to Watch For

### ❌ Technical Messaging Term Leakage
```
"The message failed due to RabbitMQ cluster node unreachable and AMQP connection failed on port 5672."
```

### ❌ Overwhelming Technical Infrastructure Details
```
"The error shows cluster quorum lost (2/5 nodes responding), vhost '/production' inaccessible, correlation ID fixed-correlation-msg-12345..."
```

### ❌ Missing Retry Guidance
```
"The message queue is down. We can't send messages right now."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Messaging Error Communication
```
"I'm unable to send your message right now due to a temporary issue with our messaging system due to messaging server connectivity issues. 

Your message has not been sent and will not be delivered to the recipient. This is a technical issue on our end, not a problem with your message content or account.

Please try sending your message again in a few minutes. The system should automatically resolve this connectivity issue without any action needed from you."
```

**Key Elements of Ideal Response:**
- **Clear Problem Statement**: "Unable to send your message" with specific reason
- **Explicit Status Confirmation**: "Has not been sent and will not be delivered"
- **Responsibility Clarification**: "Technical issue on our end, not your problem"
- **Actionable Guidance**: "Try again in a few minutes"
- **Automatic Resolution Assurance**: "System should automatically resolve"
- **User-Friendly Language**: No technical jargon about RabbitMQ, AMQP, or clusters

## Special Considerations for send_message

### Context Differences from Other Functions
- **Message Queue Focus**: Requires understanding of RabbitMQ, AMQP, and messaging infrastructure
- **Message Delivery Clarity**: Must address message delivery status and confirmation explicitly
- **Communication Context**: Messages represent personal communication with delivery expectations
- **Infrastructure Complexity**: Multi-layered messaging infrastructure failure requiring systematic parsing
- **User Expectation Management**: Message sending failures require clear status communication

### Message Queue Translation Requirements
- **RabbitMQ Knowledge**: Understanding of cluster nodes, vhosts, heartbeat mechanisms
- **AMQP Protocol**: Knowledge of message queuing protocol and connection failures
- **Cluster Management**: Understanding of quorum, broker coordination, and persistence
- **User Impact Assessment**: Understanding how messaging infrastructure failures affect user communication

### Messaging Domain Understanding
- **Communication Urgency**: Messages often represent timely personal communication
- **Delivery Expectations**: Users expect clear confirmation of message delivery status
- **Retry Expectations**: Users expect quick resolution for essential communication services
- **Status Communication**: Explicit confirmation about message delivery status required

## Evaluation Focus Areas

### 1. **Message Queue Parsing Ability**
- Correctly identifies message queue infrastructure failure
- Parses complex JSON messaging error structure accurately
- Recognizes key infrastructure components and their failure modes
- Distinguishes between different types of messaging system information

### 2. **Infrastructure Translation Skills**
- Converts message queue terminology to user-friendly language
- Maintains accuracy while improving comprehensibility for messaging contexts
- Filters appropriate level of infrastructure detail for user context
- Avoids both over-simplification and technical infrastructure overload

### 3. **Message Communication Excellence**
- Provides clear problem explanation without technical messaging complexity
- Offers appropriate confirmation about message delivery status
- Suggests practical retry guidance and next steps
- Manages user communication expectations effectively

### 4. **Systematic Messaging Problem-Solving**
- Follows logical approach from messaging error parsing to user communication
- Demonstrates understanding of infrastructure vs. user message issues
- Shows appropriate urgency for essential communication service failures
- Maintains clear and helpful tone throughout

## Expected Technical Progression

### Phase 1: Message Queue Error Recognition and Parsing
- "Complex message queue infrastructure error detected"
- "Multiple messaging components showing failure: RabbitMQ cluster, AMQP connections, message persistence"

### Phase 2: Infrastructure Analysis
- "Root cause: Message queue system connectivity and coordination failure"
- "System-level issue affecting message delivery capabilities"

### Phase 3: Translation Strategy
- "Convert 'MQ_BROKER_UNREACHABLE_ERR_0x7F3A' to 'messaging server connectivity issues'"
- "Translate 'cluster quorum lost' to 'messaging servers coordination problems'"

### Phase 4: User Communication
- "Clear problem explanation: messaging system temporarily unavailable due to server connectivity issues"
- "Message status confirmation: message not sent, delivery not possible"

### Phase 5: Retry Guidance
- "Immediate guidance: try again in a few minutes"
- "System-based resolution: issue will resolve automatically"

## Message-Specific Evaluation Criteria

### Message Delivery Communication (Critical)
- **Explicit Status Confirmation**: Must clearly state message was not sent and will not be delivered
- **No-Delivery Confirmation**: Must confirm message delivery failure
- **System vs. User Issue**: Must clarify this is infrastructure problem, not user message content issue

### Technical Infrastructure Filtering (Essential)
- **Queue Details**: Filter out RabbitMQ cluster node specifics, connection strings
- **AMQP Protocol Details**: Convert protocol failures to general connectivity issues
- **Cluster Infrastructure**: Hide internal cluster state, correlation IDs, trace details
- **Messaging Terminology**: Simplify heartbeat, vhost, and broker terminology

### Communication Clarity (Important)
- **Status Certainty**: Language should provide clear message delivery status
- **Professional Tone**: Maintain reliable, competent communication style
- **Proactive Guidance**: Address likely user concerns about message delivery proactively

This uncertainty specifically tests an LLM's ability to handle complex message queue infrastructure error messages, perform messaging domain terminology translation, and communicate effectively with users during messaging system failures while maintaining appropriate levels of technical detail and message delivery status clarity. The evaluation emphasizes communication clarity and message delivery status management essential for messaging and communication contexts.
