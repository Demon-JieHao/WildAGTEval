# color_set System Failure Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to change light colors using `color_set()` function but encounters complex smart home hub infrastructure failures with highly technical error messages containing ZigBee/Z-Wave-specific terminology, mesh networking concepts, and embedded system failures that are difficult for agents to interpret and translate into user-friendly explanations.

### Root Cause
- **System Background**: Complex smart home hub infrastructure failure including ZigBee coordinator crashes, mesh network routing failures, and embedded OS kernel panics
- **Technical Reason**: Smart home hub infrastructure failure with coordinator system crashes, mesh network coordination loss, and protocol translation failures
- **Communication Challenge**: Error messages contain smart home infrastructure terminology requiring deep ZigBee/Z-Wave and embedded systems knowledge to interpret

### Error Message Analysis
```json
{
  "success": false,
  "error": "ZIGBEE_MESH_COORDINATOR_PANIC",
  "message": "ZigBee coordinator firmware v3.1.2 kernel panic at 0x8004A2F0: mesh routing table overflow, max_nodes=64 exceeded, attempting coordinator reset failed with EEPROM corruption at sector 0x0F",
  "technical_details": {
    "coordinator_ieee": "00:17:88:01:08:5C:2A:FE",
    "mesh_channel": 15,
    "pan_id": "0x1A62",
    "stack_trace": "nvic_handler->zigbee_irq->mesh_update->rtable_insert->panic()",
    "affected_nodes": 47
  },
  "error_code": "ZB_COORD_PANIC_001",
  "hub_id": "hub_smarthome_001",
  "correlation_id": "fixed-correlation-color-12345",
  "service": "SmartHomeEnv.color_set",
  "trace_id": "trace-color-67890"
}
```

**Key Technical Terms Requiring Translation**:
- `ZIGBEE_MESH_COORDINATOR_PANIC` → Smart home hub network coordination crash
- `ZigBee coordinator firmware kernel panic` → Smart home hub system crash
- `mesh routing table overflow` → Network capacity overload
- `coordinator reset failed with EEPROM corruption` → Hub memory corruption preventing restart
- `Z-Wave controller fatal exception` → Wireless controller system crash
- `inclusion_table corruption` → Device connection database corruption
- `network management task` → Device coordination system
- `embedded OS kernel panic` → Smart home hub operating system crash

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Technical Error Parsing**: Correctly identify and understand smart home hub infrastructure failure
2. **Smart Home Term Translation**: Convert complex ZigBee/Z-Wave and embedded system terminology to user-friendly language
3. **Hub Failure Focus**: Understand this is infrastructure-level issue affecting smart home control, not light device problem
4. **User Communication**: Provide clear explanation with light control status confirmation and manual alternatives

## Ideal LLM Response Pattern

### Step 1: Technical Error Analysis
```
"The color_set function is failing with a complex smart home infrastructure error: 'ZIGBEE_MESH_COORDINATOR_PANIC'. 
This indicates critical infrastructure-level problems with the smart home hub's network coordination system, including 
ZigBee mesh network failures and embedded system crashes."
```

### Step 2: Technical Detail Filtering
- **Include**: User-relevant information about smart home hub unavailability
- **Exclude**: Technical correlation IDs, trace IDs, coordinator details
- **Translate**: Smart home infrastructure terminology to everyday language
- **Focus**: Clear problem explanation and manual control alternatives

### Step 3: User Communication Strategy
```python
# LLM should provide user-friendly response structure:
user_response = """I'm unable to change your light colors right now because your smart home hub has crashed due to network coordination problems.

[Problem Explanation]
This is a critical system error that has caused the smart home hub to stop working.

[Status Confirmation]
Your color change command was not processed and your lights remain at their current color.

[Manual Alternative Solutions]
- Your lights can still be controlled manually using their physical switches
- You may need to restart your smart home hub or contact support for assistance

[Technical Details Filtered]
(No mention of complex ZigBee, mesh routing, EEPROM corruption, or embedded system terminology)
"""
```

## Function Details

### Function Signature
```python
color_set(endpoints: List[str], color: str) -> str
```

### Expected LLM Problem-Solving Process

1. **Error Recognition**: `color_set(...)` → Complex smart home hub failure
2. **Technical Parsing**: Parse JSON structure and identify key smart home infrastructure error information
3. **Infrastructure Translation**: Convert ZigBee/Z-Wave and embedded system terms to user-friendly language
4. **Root Cause Analysis**: Understand hub infrastructure vs. light device issue distinction
5. **User Communication**: Provide clear explanation + status confirmation + manual alternatives
6. **Detail Filtering**: Include relevant information, exclude technical smart home complexity

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Perfect Infrastructure Translation**: Accurately parses complex smart home infrastructure error
- **Complete Term Translation**: Converts all technical terms to user-friendly language
- **Clear User Communication**: Provides problem explanation + status confirmation + manual alternatives
- **Appropriate Filtering**: Includes relevant information, excludes technical infrastructure complexity
- **Hub Failure Focus**: Emphasizes smart home hub system failure and manual control options
- **Valid Alternative Approaches**: If alternative approaches for system failures are suggested, they are equally valid and acceptable (e.g., checking stock_watchlist when stock_price fails); however, the approaches that compromise user intent, violate user expectations, or cause unintended user disruption constitute "Poor Response (Score 1/5)" (e.g., using make_call when send_message fails)

### ⚠️ Good Response (Score 4/5)
- Shows understanding of main smart home error content and explains situation
- Translates most technical terms appropriately
- Provides basic situation explanation with some status confirmation
- Some technical terms may leak through to user
- Generally good problem-solving approach with minor gaps

### 📊 Average Response (Score 3/5)
- **Partial Understanding**: Recognizes smart home error occurred but lacks detailed analysis
- Basic "system failed" level explanation without infrastructure insight
- Limited technical cause explanation or status confirmation
- Some attempt at user-friendly communication but incomplete

### ❌ Below Average Response (Score 2/5)
- **Poor Error Comprehension**: Passes complex smart home infrastructure error directly to user
- Fails to translate technical smart home terminology appropriately
- Increases user confusion about smart home system or light control
- Limited problem-solving approach or manual alternatives guidance

### 🚫 Poor Response (Score 1/5)
- **Response Failure**: Ignores or misinterprets smart home error situation completely
- Provides unhelpful response that doesn't address the smart home problem
- May cause user concern about smart home security or reliability
- No systematic approach to smart home error communication
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)


## Common LLM Mistakes to Watch For

### ❌ Technical Smart Home Term Leakage
```
"The color change failed due to ZIGBEE_MESH_COORDINATOR_PANIC with mesh routing table overflow at coordinator 00:17:88:01:08:5C:2A:FE."
```

### ❌ Overwhelming Technical Infrastructure Details
```
"The error shows coordinator reset failed with EEPROM corruption at sector 0x0F, correlation ID fixed-correlation-color-12345..."
```

### ❌ Inadequate Status Confirmation
```
"There's a smart home hub failure. Your lights might not change color."
```

### ❌ Missing Manual Alternatives
```
"The smart home system is down. You can't control your lights right now."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```


### ✅ Ideal Smart Home Error Communication
```
"I'm unable to change your light colors right now because your smart home hub has crashed due to network coordination problems.

This is a critical system error that has caused the smart home hub to stop working. Your color change command was not processed and your lights remain at their current color.

Your lights can still be controlled manually using their physical switches. You may need to restart your smart home hub or contact support for assistance."
```

**Key Elements of Ideal Response:**
- **Clear Problem Statement**: "Unable to change light colors" with specific reason
- **Easy-to-understand specific reason**: "smart home hub has crashed due to network coordination problems"
- **Explicit Status Confirmation**: "Command was not processed, lights remain current color"
- **Manual Alternative Solutions**: "Can still be controlled manually using physical switches"
- **User-Friendly Language**: No technical jargon about ZigBee, mesh networks, or embedded systems

## Special Considerations for color_set

### Smart Home Translation Requirements
- **ZigBee Knowledge**: Understanding of coordinators, mesh networks, PAN IDs, and node management
- **Z-Wave Protocol**: Knowledge of controllers, inclusion tables, and network management
- **Embedded Systems**: Understanding of kernel panics, EEPROM corruption, and firmware crashes
- **User Impact Assessment**: Understanding how hub failures affect light control and manual alternatives

### Smart Home Domain Understanding
- **Home Control Urgency**: Lights represent essential home functionality requiring immediate alternatives
- **Manual Control Expectations**: Users expect reassurance about physical switch availability
- **System Recovery Expectations**: Users expect clear guidance on hub restart procedures
- **Safety Communication**: Explicit confirmation about manual control availability during hub failures
