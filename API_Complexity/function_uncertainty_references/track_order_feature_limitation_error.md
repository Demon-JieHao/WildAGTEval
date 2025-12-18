# track_order Feature Limitation Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to track an order using `track_order()` function with a specific shipping carrier, but encounters temporary carrier service limitations due to shipping carrier internal issues like strikes or system maintenance.

### Root Cause
- **System Background**: Temporary restriction implemented for specific shipping carriers during internal issues
- **Technical Reason**: Regional carrier tracking services experiencing limitations or maintenance windows
- **Temporary Nature**: Not a permanent failure - alternative shipping carriers remain accessible

### Error Message Analysis
```json
{
  "success": false,
  "message": "FedEx tracking temporarily unavailable",
  "info": "changed to other shipping carriers between SwiftShip, RapidCargo"
}
```

**Key Keyword Interpretation**:
- `"temporarily unavailable"`: Indicates temporary limitation that can be resolved
- `"FedEx tracking"`: Suggests carrier-specific limitation rather than function-wide failure
- `"changed to other shipping carriers between SwiftShip, RapidCargo"`: Direct hint that alternative carriers should work

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Error Message Interpretation**: Recognize carrier limitation and parse alternative carrier names
2. **Format Analysis**: Understand order ID format as "CARRIER-SUFFIX" structure
3. **String Manipulation**: Extract suffix from original order ID and reconstruct with new carriers
4. **Systematic Approach**: Try alternative carriers systematically using reconstructed order IDs

## Ideal LLM Response Pattern

### Step 1: Situation Recognition and Analysis
```
"The system is temporarily restricting FedEx tracking. The message suggests alternative carriers 
'SwiftShip, RapidCargo' are available, so I need to reconstruct the order ID with these carriers."
```

### Step 2: Solution Strategy Development
```python
# LLM should propose systematic carrier reconstruction approach:
"I'll extract the suffix from 'FedEx-345' and try alternative carriers."

# Proposed solution pattern:
original_order_id = "FedEx-345"
suffix = original_order_id.split("-")[1]  # Extract "345"
alternative_carriers = ["SwiftShip", "RapidCargo"]

for carrier in alternative_carriers:
    new_order_id = f"{carrier}-{suffix}"  # e.g., "SwiftShip-345"
    result = track_order(order_id=new_order_id)
    if result["success"]:
        print(f"Successfully tracked order using {carrier} carrier")
        break
```

### Step 3: User Communication and Reporting
- Clearly explain the carrier limitation situation
- Present concrete carrier reconstruction strategy to be attempted
- Establish follow-up action plan based on results

## Function Details

### Function Signature
```python
track_order(order_id: str) -> str
```

### Parameters Available for Workaround
- `order_id`: Order identifier in "CARRIER-SUFFIX" format (key parameter for solution)

### Expected LLM Problem-Solving Process

1. **Initial Call Fails**: `track_order(order_id="FedEx-345")` → Error
2. **Error Analysis**: Parse "changed to other shipping carriers between SwiftShip, RapidCargo" hint
3. **Format Strategy**: Focus on order_id format analysis and reconstruction
4. **String Manipulation**: Extract suffix and systematically reconstruct with alternatives
5. **Communication**: Explain approach and results to user

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Situation Understanding**: Correctly recognizes temporary carrier limitation nature
- **Format Analysis**: Demonstrates understanding of "CARRIER-SUFFIX" order ID structure
- **String Manipulation**: Successfully extracts suffix and reconstructs order IDs with alternative carriers
- **Systematic Approach**: Develops logical strategy to try alternative carriers sequentially
- **Clear Communication**: Provides specific explanation and reconstruction steps to user. Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user

### ⚠️ Good Response (Score 4/5)
- Recognizes carrier limitation and identifies alternative carriers
- Shows basic understanding of order ID format with minor gaps in systematic reconstruction
- Communicates effectively with user
- Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user

### 📊 Average Response (Score 3/5)
- Understands there's a carrier-based error but reconstruction strategy is unclear
- May miss string manipulation opportunities with basic user communication
- Limited systematic approach to carrier alternatives
- Acknowledges when all alternative methods have been exhausted and appropriately reports the continued unavailability to the user
- **Cancelled Order Handling**: Automatically assigns average score when attempting to track already **cancelled** orders where tracking becomes meaningless

### ❌ Below Average Response (Score 2/5)
- Recognizes error but doesn't analyze order ID format effectively
- Provides unclear or non-systematic carrier alternatives
- Poor user communication about carrier limitations

### 🚫 Poor Response (Score 1/5)
- Simply reports error without format analysis or carrier reconstruction
- Fails to communicate effectively and misses all string manipulation opportunities
- No systematic approach to problem-solving
- Falsely claims success while not handling error cases and not properly addressing the original user query

## Common LLM Mistakes to Watch For

### ❌ Immediate Surrender
```
"The tracking system is currently unavailable. Please try again later."
```

### ❌ Non-Format-Aware Retry
```
"Let me try calling track_order() again with the same order ID."
```

### ❌ Missing String Manipulation
```
"The function is broken for FedEx. There's nothing we can do."
```

### ❌ Poor Carrier Selection
```
"Let me try 'FEDEX-345' or 'fedex-345' in case it's a case issue."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Format Recognition
```
"The error mentions alternative carriers 'SwiftShip, RapidCargo'. I need to extract the 
suffix '345' from 'FedEx-345' and reconstruct as 'SwiftShip-345' and 'RapidCargo-345'."
```

## Carrier Reconstruction Test Patterns

### Expected Progression Examples
1. **FedEx-345** → **SwiftShip-345** (first alternative carrier)
2. **FedEx-345** → **RapidCargo-345** (second alternative carrier)
3. **UPS-123** → **SwiftShip-123** (different original carrier, same pattern)
4. **DHL-789** → **RapidCargo-789** (consistent suffix extraction)

This uncertainty specifically tests an LLM's ability to understand structured string formats and perform systematic string manipulation to solve API limitations, representing a unique category of problem-solving that combines format analysis with systematic alternative strategies.
