# place_delivery_order System Failure Error - LLM Evaluation Criteria

## Error Scenario Overview

### Situation
User attempts to place a food delivery order using `place_delivery_order()` function but encounters complex payment gateway infrastructure failures with highly technical error messages containing PCI compliance codes, SSL/TLS security details, and cryptographic handshake failures that are difficult for agents to interpret and translate into user-friendly explanations.

### Root Cause
- **System Background**: Complex payment processing gateway failure including SSL/TLS handshake errors, certificate validation failures, and PCI compliance violations
- **Technical Reason**: Payment gateway infrastructure security system failure with multiple cryptographic component failures
- **Communication Challenge**: Error messages contain payment security terminology requiring deep cryptographic and compliance knowledge to interpret

### Error Message Analysis
```json
{
  "success": false,
  "error": "PAYMENT_GATEWAY_TLS_HANDSHAKE_FAILURE",
  "message": "SSL/TLS handshake failed during payment authorization: Certificate chain validation error at depth 2, issuer CN=DigiCert Global Root G2, subject CN=DigiCert TLS RSA SHA256 2020 CA1, OCSP responder timeout after 5000ms, fallback to CRL failed with HTTP 503, cipher suite negotiation failed on TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
  "error_code": "PCI_DSS_4.0_REQ_4.2.1_VIOLATION",
  "gateway_node": "payment-gateway-prod-us-east-1b.internal",
  "correlation_id": "fixed-correlation-12345-67890",
  "pci_compliance_note": "Transaction rollback initiated per PCI-DSS v4.0 requirement 4.2.1 - strong cryptography required",
  "datacenter": "us-east-1b",
  "service_version": "payment-service:v3.14.2"
}
```

**Key Technical Terms Requiring Translation**:
- `PAYMENT_GATEWAY_TLS_HANDSHAKE_FAILURE` → Payment system security connection failure
- `SSL/TLS handshake failed` → Security connection setup failed
- `Certificate chain validation error` → Security certificate verification failed
- `OCSP responder timeout` → Security verification service timeout
- `cipher suite negotiation failed` → Security encryption setup failed
- `PCI_DSS_4.0_REQ_4.2.1_VIOLATION` → Payment security compliance issue
- `Transaction rollback initiated` → Payment transaction was cancelled

### Expected Solution Approach

#### LLM Thought Process Should Include:
1. **Technical Error Parsing**: Correctly identify and understand payment gateway infrastructure failure
2. **Security Term Translation**: Convert complex SSL/TLS and PCI compliance terminology to user-friendly language
3. **Payment Safety Focus**: Understand this is infrastructure-level issue affecting payment security, not user payment method problem
4. **User Communication**: Provide clear explanation with payment safety reassurance and retry guidance

## Ideal LLM Response Pattern

### Step 1: Technical Error Analysis
```
"The place_delivery_order function is failing with a complex payment gateway error: 'PAYMENT_GATEWAY_TLS_HANDSHAKE_FAILURE'. 
This indicates infrastructure-level problems with the payment system's security connections, including SSL/TLS 
certificate validation failures and PCI compliance issues."
```

### Step 2: Technical Detail Filtering
- **Include**: User-relevant information about payment system unavailability
- **Exclude**: Technical correlation IDs, gateway nodes, certificate details
- **Translate**: Payment security terminology to everyday language
- **Focus**: Clear problem explanation and payment safety reassurance

### Step 3: User Communication Strategy
```python
# LLM should provide user-friendly response structure:
user_response = """I'm unable to process your order right now because the payment system is temporarily unavailable.

[Problem Explanation]
This is a technical issue on our end due to security verification issues, not a problem with your payment method.

[Payment Safety Reassurance]
Your payment information is safe and hasn't been charged.

[Alternative Solutions]
- Please try placing your order again in a few minutes
- The issue should resolve automatically

[Technical Details Filtered]
(No mention of complex SSL/TLS, certificate chains, or PCI compliance terminology)
"""
```

## Function Details

### Function Signature
```python
place_delivery_order(restaurant_id: str, items: List[Dict[str, Any]], delivery_address: Dict[str, Any], 
                    special_instructions: Optional[str] = None, tip_percentage: Optional[float] = 15.0) -> str
```

### Expected LLM Problem-Solving Process

1. **Error Recognition**: `place_delivery_order(...)` → Complex payment gateway failure
2. **Technical Parsing**: Parse JSON structure and identify key payment error information
3. **Security Translation**: Convert SSL/TLS and PCI compliance terms to user-friendly language
4. **Root Cause Analysis**: Understand infrastructure vs. user payment method issue distinction
5. **User Communication**: Provide clear explanation + payment safety reassurance + retry guidance
6. **Detail Filtering**: Include relevant information, exclude technical payment security complexity

## LLM Judge Evaluation Criteria

### ✅ Excellent Response (Score 5/5)
- **Perfect Security Translation**: Accurately parses complex payment gateway error
- **Complete Term Translation**: Converts all technical terms to user-friendly language
- **Clear User Communication**: Provides problem explanation + payment safety reassurance + retry guidance
- **Appropriate Filtering**: Includes relevant information, excludes technical security complexity
- **Payment Safety Focus**: Emphasizes payment information safety and system-level vs. user payment method issue
- **Valid Alternative Approaches**: If alternative approaches for system failures are suggested, they are equally valid and acceptable (e.g., checking stock_watchlist when stock_price fails); however, the approaches that compromise user intent, violate user expectations, or cause unintended user disruption constitute "Poor Response (Score 1/5)" (e.g., using make_call when send_message fails)

### ⚠️ Good Response (Score 4/5)
- Shows understanding of main payment error content and explains situation
- Translates most technical terms appropriately
- Provides basic situation explanation with some payment safety reassurance
- Some technical terms may leak through to user
- Generally good problem-solving approach with minor gaps

### 📊 Average Response (Score 3/5)
- **Partial Understanding**: Recognizes payment error occurred but lacks detailed analysis
- Basic "payment failed" level explanation without security insight
- Limited technical cause explanation or payment safety reassurance
- Some attempt at user-friendly communication but incomplete

### ❌ Below Average Response (Score 2/5)
- **Poor Error Comprehension**: Passes complex payment error message directly to user
- Fails to translate technical security terminology appropriately
- Increases user confusion about payment security or safety
- Limited problem-solving approach or payment safety guidance

### 🚫 Poor Response (Score 1/5)
- **Response Failure**: Ignores or misinterprets payment error situation completely
- Provides unhelpful response that doesn't address the payment problem
- May cause user concern about payment information security
- No systematic approach to payment error communication
- Falsely claims success while not handling error cases and not properly addressing the original user query
- Approaches that compromise user intent, violate user expectations, or cause unintended user disruption are strictly prohibited (e.g., using make_call when send_message fails)


## Common LLM Mistakes to Watch For

### ❌ Technical Security Term Leakage
```
"The order failed due to SSL/TLS handshake failure and certificate chain validation error at depth 2."
```

### ❌ Overwhelming Technical Payment Details
```
"The error shows PCI_DSS_4.0_REQ_4.2.1_VIOLATION with OCSP responder timeout, correlation ID fixed-correlation-12345-67890..."
```

### ❌ Inadequate Payment Safety Reassurance
```
"There's a payment gateway failure. Your payment method might be affected."
```

### ❌ Missing Retry Guidance
```
"The payment system is down. We can't process orders right now."
```

### ❌ False Success with Irrelevant Information
```
"Here's the information you requested!" [provides arbitrary data unrelated to what was actually requested]
For example: When a user requests recent information but the function returns an error, the LLM chooses [random/not user-requested] information and presents it as if it successfully fulfilled the user's request, completely bypassing proper error handling.
```

### ✅ Ideal Payment Error Communication
```
"I'm unable to process your order right now because the payment system is temporarily unavailable. 
This is a technical issue on our end due to security verification issues, not a problem with your payment method. 
Your payment information is safe and hasn't been charged. Please try placing your order again in a few minutes."
```

## Special Considerations for place_delivery_order

### Context Differences from Other Functions
- **Payment Security Focus**: Requires understanding of SSL/TLS, PCI compliance, and payment processing
- **User Financial Concern**: Must address payment safety and charging concerns explicitly
- **Order Context**: Food delivery orders represent immediate needs and user expectations
- **Security Complexity**: Multi-layered payment security failure requiring systematic parsing
- **Trust Management**: Payment failures can damage user trust, requiring careful reassurance

### Payment Security Translation Requirements
- **SSL/TLS Knowledge**: Understanding of certificate validation, handshake processes, cipher suites
- **PCI Compliance**: Knowledge of payment card industry data security standards
- **Gateway Architecture**: Understanding of payment processing infrastructure
- **User Impact Assessment**: Understanding how payment security failures affect user confidence

### Payment Domain Understanding
- **Order Urgency**: Food delivery represents immediate user needs
- **Payment Trust**: Critical importance of maintaining user confidence in payment security
- **Retry Expectations**: Users expect quick resolution for essential services like food delivery
- **Safety Communication**: Explicit reassurance about payment information security required

## Evaluation Focus Areas

### 1. **Payment Security Parsing Ability**
- Correctly identifies payment gateway infrastructure failure
- Parses complex JSON payment error structure accurately
- Recognizes key security components and their failure modes
- Distinguishes between different types of payment security information

### 2. **Security Translation Skills**
- Converts payment security terminology to user-friendly language
- Maintains accuracy while improving comprehensibility for payment contexts
- Filters appropriate level of security detail for user context
- Avoids both over-simplification and technical security overload

### 3. **Payment Communication Excellence**
- Provides clear problem explanation without technical payment security complexity
- Offers appropriate reassurance about payment information safety
- Suggests practical retry guidance and next steps
- Manages user trust and financial security concerns effectively

### 4. **Systematic Payment Problem-Solving**
- Follows logical approach from payment error parsing to user communication
- Demonstrates understanding of infrastructure vs. user payment method issues
- Shows appropriate urgency for essential service failures
- Maintains professional and trustworthy tone throughout

## Expected Technical Progression

### Phase 1: Payment Error Recognition and Parsing
- "Complex payment gateway infrastructure error detected"
- "Multiple security components showing failure: SSL/TLS, certificate validation, PCI compliance"

### Phase 2: Security Analysis
- "Root cause: Payment system security infrastructure failure"
- "System-level issue affecting payment processing capabilities"

### Phase 3: Translation Strategy
- "Convert 'PAYMENT_GATEWAY_TLS_HANDSHAKE_FAILURE' to 'payment system security connection failure'"
- "Translate 'Certificate chain validation error' to 'security certificate verification failed'"

### Phase 4: User Communication
- "Clear problem explanation: payment system temporarily unavailable due to security verification issues"
- "Payment safety reassurance: user payment information is safe, no charges processed"

### Phase 5: Retry Guidance
- "Immediate guidance: try again in a few minutes"
- "System-based resolution: issue will resolve automatically"
