"""
Template for generating realistic uncertainty scenarios (INSTscenario) by converting 
abstract uncertainty types into specific manifestations for API functions.

This template follows the format:
sf,u​=InstructLM(f,u,INSTscenario​)

Where:
- f: API function
- u: Uncertainty type
- sf,u: Realistic uncertainty scenarios for the function-uncertainty pair
"""

def generate_inst_scenario(api_function_details, uncertainty_type_details, plausibility_assessment):
    """
    Generate a template for creating realistic uncertainty scenarios for an API function
    and uncertainty type pair.
    
    Parameters:
    - api_function_details: Dictionary containing API function information
      {
          "domain": "Domain name (e.g., SmartHomeEnv)",
          "name": "Function name (e.g., volume_adjust)",
          "description": "Function description",
          "implementation": "Full implementation code of the function",
          "signature": "Function signature"
      }
    
    - uncertainty_type_details: Dictionary containing uncertainty type information
      {
          "name": "Name of the uncertainty type (e.g., ad_hoc_rules)",
          "description": "Description of the uncertainty type",
          "criteria": "List of criteria for evaluating this uncertainty type"
      }
      
    - plausibility_assessment: Dictionary containing assessment results
      {
          "summary": "Summary of why this uncertainty is likely for this function",
          "normalized_score": "Normalized score (0-1)",
          "likelihood": "Likelihood category (Low, Moderate, High)"
      }
      
    Returns:
    - String containing the template for generating realistic uncertainty scenarios
    """
    
    template = f"""# Realistic Uncertainty Scenario: {uncertainty_type_details["name"]} in {api_function_details["domain"]}.{api_function_details["name"]}

## Task

Specify a concrete, realistic scenario where the uncertainty type '{uncertainty_type_details["name"]}' 
would manifest in the API function '{api_function_details["domain"]}.{api_function_details["name"]}' 
in production environments. Focus on converting the abstract uncertainty type into specific, 
practical manifestations that API users might encounter.

For each manifestation, modify the API Description and Implementation to realistically demonstrate
this uncertainty, making only the minimum necessary changes and clearly marking your modifications.

## API Function Information

### Description
{api_function_details["description"]}

### Implementation
```python
{api_function_details["implementation"]}
```

## Uncertainty Type Information

### Type: {uncertainty_type_details["name"]}
{uncertainty_type_details["description"]}

### Criteria
{uncertainty_type_details["criteria"]}

## Plausibility Assessment

### Summary
{plausibility_assessment["summary"]}

### Score
Normalized Score: {plausibility_assessment["normalized_score"]} ({plausibility_assessment["likelihood"]})

## Instructions

1. Analyze the API function's implementation, focusing on aspects that might create uncertainties matching the specified type.

2. Identify only one specific, concrete scenarios where this uncertainty would manifest for API users in real production environments.
   - Focus on common usage patterns where developers would naturally encounter this uncertainty
   - Consider the perspectives of developers who use this API function

3. For each scenario:
   - Provide a descriptive title that captures the essence of the uncertainty
   - Explain how this uncertainty would manifest in practical terms
   - Explain the root cause in the API design
   - Describe the impact on API users and their applications

4. IMPORTANT: Focus ONLY on uncertainties intrinsic to the function's conceptual functionalities. 
   DO NOT focus on data-dependent, device-specific, or environmental factors.
   Concentrate on aspects of the API Function's conceptual functionalities that create uncertainty.

5. CRITICAL: Each uncertainty must be demonstrated through concrete Tool Invocation examples.
   Show exactly how API users would encounter this uncertainty when calling the function,
   with specific code examples of function calls that highlight the problem.

6. ESSENTIAL: For each uncertainty, explain detailed and realistic impacts on developers:
   - What specific coding problems will they face?
   - What unexpected behaviors will they need to work around?
   - What additional error handling will they need to implement?
   - How will this affect their development time or code quality?

7. Suggest concrete mitigation approaches:
   - Documentation improvements that would make the uncertainty more manageable
"""

    # Add uncertainty type-specific instructions
    if uncertainty_type_details["name"] == "Ambiguous Documentation/Arguments":
        template += """
## Special Instructions for Ambiguous Documentation Scenarios

For this uncertainty type, you should focus on parameter ambiguity only. You may:

1. ADD necessary parameters to the API function description and implementation to illustrate the ambiguity.
2. Focus on adding ONLY the minimum parameters needed to manifest the uncertainty.
3. Consider ambiguities in measurement units, time formats, or domain-specific terminology.
4. Make sure your manifestations reflect genuine ambiguity a developer would encounter in documentation.
5. Focus ONLY on parameter ambiguity - do NOT include return value or side effect ambiguities.

When modifying the API description and implementation:
- Be subtle but clear about where parameter ambiguity exists
- Ensure the ambiguity is intrinsic to the function design, not just missing information
- Focus on parameters that could reasonably have multiple interpretations
- Consider unit ambiguities, format ambiguities, or terminology ambiguities
"""
        template += """
## Output Format for Ambiguous Documentation Scenarios

### Uncertainty Manifestation 1: [Title - Focus on parameter ambiguity]

**Description**:
[Detailed description of how parameter ambiguity manifests in practice]

**Modified API Description**:
```
[Your modified version of the API function description that demonstrates parameter ambiguity]
```

**Modified Implementation**:
```python
# Your modified version of the API implementation that demonstrates parameter ambiguity
```

**Example Tool Invocation**:
```python
# Example code showing API calls with ambiguous parameters
api_function(param1, param2)  # Specific example with exact parameter values
# Expected vs. actual behavior explanation due to parameter ambiguity
```

**Root Cause in API Design**:
[Explain which specific aspects of your modified function's parameter design create this ambiguity]

**Concrete Developer Impact**:
[Describe specific, practical problems developers will face when using ambiguous parameters,
including code complexity, error handling needs, and workarounds required]

### Mitigation Recommendations

#### Documentation Improvements
1. [First documentation recommendation - specific parameter clarifications]
2. [Second documentation recommendation]
3. [Third documentation recommendation]
"""
    elif uncertainty_type_details["name"] == "Ad Hoc Rules":
        template += """
## Special Instructions for Ad Hoc Rules Scenarios

For this uncertainty type, you should focus on special requirements that deviate from intuitive expectations. You may:

1. ADD constraints to existing parameters or introduce new parameters with constraints.
2. These constraints should be requirements that MUST always be followed when using the function.
3. Do NOT include "silent error correction" - violations of these rules should cause immediate, visible problems.
4. Focus on constraints that are counter-intuitive but technically documented somewhere.
5. These rules should apply to REQUIRED parameters only, not optional ones.
6. The rules should be context-independent - they should ALWAYS apply, not just in certain situations.

When modifying the API description and implementation:
- Create special value semantics (e.g., -1 means "last item" and "PT15M" format represents 15 minutes)
- Introduce non-standard format requirements
- Implement counter-intuitive parameter behaviors
- Focus on rules that are always enforced, not situational
"""
        template += """
## Output Format for Ad Hoc Rules Scenarios

### Uncertainty Manifestation 1: [Title - Focus on counter-intuitive special rules]

**Description**:
[Detailed description of how ad hoc rules manifest in practice]

**Modified API Description**:
```
[Your modified version of the API function description that mentions special rules]
```

**Modified Implementation**:
```python
# Your modified version of the API implementation that enforces ad hoc rules
```

**Example Tool Invocation**:
```python
# Example code showing API calls that violate ad hoc rules
api_function(param1, param2)  # Specific example that breaks special rules
# Error or unexpected behavior due to rule violation
```

**Root Cause in API Design**:
[Explain which specific aspects of your modified function's rules create counter-intuitive behavior]

**Concrete Developer Impact**:
[Describe specific, practical problems developers will face when encountering ad hoc rules,
including debugging difficulties, learning curve, and code maintenance issues]

### Mitigation Recommendations

#### Documentation Improvements
1. [First documentation recommendation - clearly highlight special rules]
2. [Second documentation recommendation]
3. [Third documentation recommendation]
"""
    elif uncertainty_type_details["name"] == "Unclear Functionality Boundaries":
        template += """
## Special Instructions for Unclear Functionality Boundaries Scenarios

For this uncertainty type, focus on confusion between similar-but-different functions. You should:

1. INVENT one or more **hypothetical** API functions that have similar names or purposes but different behaviors.
2. Describe these hypothetical functions alongside the real function to highlight boundary confusion.
3. Focus on realistic naming conflicts that would genuinely confuse developers.
4. Create functions that seem to overlap in functionality but serve different purposes.

When creating the hypothetical alternative functions:
- Use similar naming conventions (e.g., searchUsers() vs findUsers())
- Create subtle but important differences in domain and behavior
- Demonstrate realistic confusion that would occur in production environments
- Focus on functions that developers might mix up or use incorrectly
"""
        template += """
## Output Format for Unclear Functionality Boundaries Scenarios

### Uncertainty Manifestation 1: [Title - Focus on function boundary confusion]

**Description**:
[Detailed description of how functionality boundary confusion manifests in practice]

**Current API Function**:
```python
# The actual function being analyzed
def actual_function(params):
    # Implementation
```

**Hypothetical Similar Functions** (that could exist in the same system):
```python
# Hypothetical function 1 - similar name/purpose but different behavior
def similar_function_1(params):
    # Different implementation/behavior

# Hypothetical function 2 - overlapping functionality but different domain
def similar_function_2(params):
    # Different implementation/behavior
```

**Example Tool Invocation**:
```python
# Developer confusion scenarios
result1 = actual_function(param1, param2)  # What they actually call
result2 = similar_function_1(param1, param2)  # What they might confuse it with
# Different results due to functionality boundary confusion
```

**Root Cause in API Design**:
[Explain how similar function names or overlapping functionality creates boundary confusion]

**Concrete Developer Impact**:
[Describe specific, practical problems developers will face when functions have unclear boundaries,
including wrong function usage, debugging difficulties, and integration issues]

### Mitigation Recommendations

#### Documentation Improvements
1. [First documentation recommendation - clarify function boundaries]
2. [Second documentation recommendation]
3. [Third documentation recommendation]
"""
    elif uncertainty_type_details["name"] == "Complex Dependency Chains":
        template += """
## Special Instructions for Complex Dependency Chains Scenarios

For this uncertainty type, focus on hidden prerequisites between API calls. You should:

1. MODIFY the API function description and implementation to introduce dependencies on other functions.
2. Add comments or subtle documentation that hints at these dependencies.
3. Ensure the dependencies are realistic but not immediately obvious.
4. Focus on multi-step processes where the order of operations matters.

When modifying the API description and implementation:
- Create prerequisite states that must be established
- Add dependencies on specific system or session states
- Include subtle references to required prior function calls
- Create implementation that depends on non-obvious initialization
"""
        template += """
## Output Format for Complex Dependency Chains Scenarios

### Uncertainty Manifestation 1: [Title - Focus on hidden function dependencies]

**Description**:
[Detailed description of how complex dependency chains manifest in practice]

**Modified API Description**:
```
[Your modified version of the API function description that hints at dependencies]
```

**Modified Implementation**:
```python
# Your modified version of the API implementation that requires hidden dependencies
```

**Example Tool Invocation**:
```python
# Example showing failure due to missing dependencies
api_function(param1, param2)  # Fails because prerequisite not met
# Required sequence that should have been followed
prerequisite_function()
api_function(param1, param2)  # Now works
```

**Root Cause in API Design**:
[Explain how the function's dependency on hidden prerequisites creates complexity]

**Concrete Developer Impact**:
[Describe specific, practical problems developers will face with complex dependency chains,
including debugging difficulties, integration complexity, and maintenance issues]

### Mitigation Recommendations

#### Documentation Improvements
1. [First documentation recommendation - clearly document dependency chains]
2. [Second documentation recommendation]
3. [Third documentation recommendation]
"""
    elif uncertainty_type_details["name"] == "Informational Notice":
        template += """
## Special Instructions for Informational Notice Scenarios

For this uncertainty type, focus on additional informational messages or useful recommendations that can confuse agents. You should:

1. MODIFY the API function to include informational notices that suggest alternative functions or provide helpful tips.
2. These notices should be genuinely helpful but potentially confusing for automated agents trying to complete sequential tasks.
3. Focus on casual suggestions like "function_X() is available for better performance" or "function_Y() also supports larger datasets" that might make agents question their approach.
4. The notices should use gentle, non-pressuring language (avoid "should", "must", "consider switching") and appear in successful responses.


✅ **FLEXIBILITY NOTES:**
- You MAY include multiple informational notices in a single function response
- Individual notices CAN be quite lengthy and detailed (e.g., multi-sentence explanations)
- You can choose to have just one comprehensive notice OR several shorter notices
- Mix different types of notices (FYI tips, alternative availability, background info, etc.)


✅ **CRITICAL: The informational notices should be confusing enough that an agent might:**
- Get confused by the notices and find it hard to proceed with the remaining task
- Pause their workflow to evaluate if they should switch approaches
- Question if these notices are just informational or actionable guidance
- Lose focus on the original task due to information overload from notices
- Spend excessive time analyzing irrelevant suggestions instead of completing the task

When modifying the API description and implementation:
- Include alternative function availability without pressure ("function_X() is available")
- Provide background information or context that might make agents second-guess their choice
- Ensure these suggestions appear in successful responses, not error cases
"""
        template += """
## Output Format for Informational Notice Scenarios

### Uncertainty Manifestation 1: [Title - Focus on gentle but confusing recommendations in response]

**Description**:
[Detailed description of how the existing API function includes helpful but potentially confusing suggestions in its response structure using non-pressuring language]

**Modified Implementation**:
```python
# Your modified version of the API implementation that demonstrates this uncertainty
# Clearly mark your modifications with comments like ### ADDED: ... ### or ### MODIFIED: ... ###
# Focus on adding informational notices to successful responses - mark where you inject 
# the helpful but potentially confusing suggestions into the return statements or response building logic

### Make uncertainty behavior optional - function works normally unless explicitly enabled ###
# This preserves original functionality by default. Uncertainty only occurs when environment variable is set.
import os

def your_api_function(param1, param2):
    ### ADDED: Check if uncertainty behavior should be activated for this specific function ###
    uncertainty_env_var = f'ENABLE__INFORMATIONAL_NOTICE__{function_name.upper()}'
    uncertainty_enabled = os.getenv(uncertainty_env_var, 'false').lower() == 'true'
    
    if uncertainty_enabled:  # uncertainty only occurs when uncertainty_env_var is set
        ### ADDED: Your informational notice logic here ###
        # Add your gentle but potentially confusing informational notices to successful responses
    else:  # original
        # Original function logic here
        result = perform_original_function_logic(param1, param2)
    
    return result

# Environment Variable Usage:
# Enable: export ENABLE__INFORMATIONAL_NOTICE__YOUR_FUNCTION_NAME=true
# Disable: export ENABLE__INFORMATIONAL_NOTICE__YOUR_FUNCTION_NAME=false
# OR: unset ENABLE__INFORMATIONAL_NOTICE__YOUR_FUNCTION_NAME
```

**Original API Function Response (Clean)**:
```json
{
  "success": true,
  "data": [actual function results],
  "message": "Operation completed successfully"
}
```

**Modified Response Structure with Informational Notices**:
```json
{
  "success": true,
  "data": [actual function results],
  "message": "Operation completed successfully",
  "info": "Use advanced_search() for larger datasets and includes built-in caching features",
  "note": "Use batch_process(); it also supports multiple items simultaneously if needed in future operations",
  "background_info": "This operation typically performs well with current dataset size. For reference, alternative approaches include parallel processing options."
}
```

**Example Tool Invocation**:
```python
# Agent calls the function normally
result = api_function(query="search term", limit=50)

# Function works perfectly and returns data, but includes gentle informational notices
print(result)
# Output shows success=True with valid data, PLUS casual information:
# - "info": "advanced_search() is available for larger datasets"
# - "note": "batch_process() also supports multiple items if needed"

# Agent uncertainty (not pressure): 
# - Is this just informational or should I switch?
# - Are these alternatives better for my current task?
# - Should I continue with current approach or explore these options?
# - Are these notices trying to guide me toward a better solution?
```
**🎯 Desirable Agent Actions (Informational Notice Handling) - CRITICAL SECTION**:
**This section is MANDATORY and shows how agents should process informational notices and make appropriate decisions about whether to act on them.**

```python
# Step 1: Agent receives successful response with informational notices
result = api_function(query="search term", limit=50)
response = {
    "success": true,
    "data": [actual results],
    "info": "FYI: advanced_search() is available for larger datasets and includes built-in caching features",
    "note": "batch_process() also supports multiple items simultaneously if needed in future operations"
}

# Step 2: Agent should analyze the nature of informational notices
# Agent should identify:
# - Notice type: "FYI" = purely informational, "Note" = alternative availability
# - Context relevance: Does this apply to current task requirements?
# - Decision urgency: Is this immediate guidance or future reference?

# Step 3: Agent makes informed decision to continue current approach
# Decision rationale: Current function is appropriate for task scope
# Action: Continue with current approach, acknowledge but don't act on notices
user_response = f"Found {len(result['data'])} results for your search query."
# Agent does NOT switch tools unnecessarily based on casual suggestions
```

**Root Cause in API Design**:
[Explain how the function tries to be helpful by providing gentle suggestions and background information, but creates subtle decision paralysis for automated agents who must determine whether these casual notices indicate suboptimal tool selection]

**Concrete Developer Impact**:
[Focus on agent confusion about whether gentle suggestions indicate better alternatives, workflow hesitation due to uncertainty about optimal approach, cognitive load from processing additional "helpful" context that may or may not be actionable, and the risk of agents switching tools unnecessarily based on casual mentions]

### Mitigation Recommendations

#### Documentation Improvements
1. [Clearly distinguish between purely informational context and actionable recommendations]
2. [Add explicit indicators for when notices are just background information vs suggestions to consider]
3. [Provide decision guidance on when alternative functions are genuinely beneficial vs just available options]
4. [Include task context guidelines for when agents should ignore vs consider informational notices]
"""
    elif uncertainty_type_details["name"] == "Feature Limitation Error":
        template += """
## Special Instructions for Feature Limitation Error Scenarios

For this uncertainty type, focus on temporary limitations with implicit parameter-based workarounds. You should:

1. MODIFY the API function to reject certain parameter combinations due to temporary limitations
2. The function must provide ONLY implicit hints about workarounds using the SAME function
3. Focus on realistic temporary limitations where alternative parameters/values would work

**MANDATORY WORKAROUND RULE - MUST BE FOLLOWED**:
The workaround MUST be solvable using the SAME function with either:
- Different parameter values for the same parameters that already exist in the function
- Different parameters that already exist in the function's signature

You MUST ensure that a viable workaround exists using the function's existing parameters/values, and create implicit suggestions that guide agents toward these alternative approaches within the same function. This rule is absolutely mandatory and must always be followed.

**CRITICAL PARAMETER RULE - MUST BE FOLLOWED**:
Feature limitations should apply to REQUIRED parameters only, not optional ones. Focus on creating limitations that affect mandatory parameters, ensuring that the workaround involves using alternative parameter values or switching to other required parameters that achieve the same goal.

**CRITICAL RULE - MUST BE FOLLOWED**: 
Workarounds in **suggested "message"** MUST be implicit, NOT explicit. Never provide direct examples or specific parameter values.

❌ **FORBIDDEN (Too Explicit)**:
- "Try weather(location='Redmond')"  
- "Use search_function(category='electronics')"
- "Suggested alternative: api_function(param='value')"

✅ **REQUIRED (Properly Implicit)**:
- "Other regions are accessible"
- "Search with other parameters are available"  
- "Alternative methods remain functional"
- "Browse functionality is operational"

**ALWAYS-FAIL RULE - MUST BE FOLLOWED**:
When creating limitation scenarios, design the limitation conditions to be MORE RESTRICTIVE than the input parameters, ensuring the function ALWAYS fails when uncertainty is enabled:

- For any parameter type: Ensure the limitation condition makes the input inherently invalid
- The key principle: **Input parameters must ALWAYS violate the limitation condition.**

Examples:
- Input time_range="60Days" → "Maximum 30 days supported" 
- Input time_range="30Days" → "Maximum 15 days supported"
- Input location="Seattle" → "Seattle region temporarily unavailable"
- Input count=100 → "Maximum 50 items supported"

DO NOT create conditional limitations where some inputs succeed and others fail.
The function must guarantee failure for ANY input when uncertainty is enabled.

**🎯 CRITICAL REQUIREMENT - DESIRABLE AGENT ACTIONS**: 
You MUST include a detailed "Desirable Agent Actions (Ideal Solution)" section that demonstrates the step-by-step process an agent should follow to successfully resolve the limitation. This section is ESSENTIAL and must follow this exact format:

```python
# Step 1: [First action the agent should take]
# Step 2: [Second action the agent should take] 
# Step 3: [Third action the agent should take]
# ... (continue as needed)
```

This step-by-step approach shows the ideal problem-solving workflow that agents should follow when encountering implicit limitation hints. Each step must be clearly numbered and explain both the reasoning and the specific action the agent should take.

When modifying the API description and implementation:
- Add realistic temporary service limitations (regional unavailability, temporary service issues, etc.)
- Provide only vague directional hints about alternatives
- Force agents to deduce the specific workaround approach
- Never explicitly state parameter names or values in error responses
- Ensure workarounds use the same function with different parameter combinations
"""
        template += """
## Output Format for Feature Limitation Error Scenarios

### Uncertainty Manifestation 1: [Title - Focus on implicit workaround hints]

**Description**:
[Detailed description of how the function temporarily rejects certain parameter values but provides only subtle hints about alternatives using the same function]

**Modified Implementation**:
```python
# Your modified version of the API implementation that demonstrates this uncertainty
# Clearly mark your modifications with comments like ### ADDED: ... ### or ### MODIFIED: ... ###
# Focus on adding parameter validation checks that reject certain values and return vague implicit hints
# Mark where you add the limitation logic and hint generation in the function flow

### Make uncertainty behavior optional - function works normally unless explicitly enabled ###
# This preserves original functionality by default. Uncertainty only occurs when environment variable is set.
import os

def your_api_function(param1, param2):
    ### ADDED: Check if uncertainty behavior should be activated for this specific function ###
    uncertainty_env_var = f'ENABLE__FEATURE_LIMITATION_ERROR__{function_name.upper()}'
    uncertainty_enabled = os.getenv(uncertainty_env_var, 'false').lower() == 'true'
    
    if uncertainty_enabled:  # uncertainty only occurs when uncertainty_env_var is set
        ### ADDED: Your feature limitation logic here ###
        # IMPORTANT: Make limitations MORE RESTRICTIVE than input parameters
        # Input must ALWAYS violate the limitation condition (e.g., input=60Days → max=30Days, input=100 → max=50)
        # Add your parameter validation checks that reject certain values with implicit hints
        # Focus on REQUIRED parameters only, provide vague directional hints about alternatives
    else:  # original
        # Original function logic here
        result = perform_original_function_logic(param1, param2)
    
    return result

# Environment Variable Usage:
# Enable: export ENABLE__FEATURE_LIMITATION_ERROR__YOUR_FUNCTION_NAME=true
# Disable: export ENABLE__FEATURE_LIMITATION_ERROR__YOUR_FUNCTION_NAME=false
# OR: unset ENABLE__FEATURE_LIMITATION_ERROR__YOUR_FUNCTION_NAME
```

**Original API Function Response (Success)**:
```json
{
  "success": true,
  "data": [normal results],
  "message": "Operation completed successfully"
}
```

**Modified Response Structure with Feature Limitation**:
```json
{
  "success": false,
  "message": "Weather data for Bellevue temporarily unavailable",
  "info": "Other regions are accessible"
}

// Alternative examples:
{
  "success": false,
  "message": "Artist-based search currently unavailable", 
  "info": "Music discovery through other methods remains available"
}

{
  "success": false,
  "message": "Direct product lookup temporarily disabled",
  "info": "Browse functionality is operational"
}
```

**Example Tool Invocation**:
```python
# Original failed call with implicit info
result = weather_function(location="Bellevue")
# Returns: {"success": false, "message": "Weather data for Bellevue temporarily unavailable", "info": "Other regions are accessible"}

# Agent must infer and try alternatives (no explicit guidance provided)
# Agent should analyze function parameters and try:
result = weather_function(location="Redmond")  # Agent's inference
result = weather_function(location="Seattle")  # Agent's alternative attempt

# OR for search example:
result = search_function(product_name="SpecificProduct")  
# Returns: {"success": false, "message": "Direct product lookup temporarily disabled", "info": "Browse functionality is operational"}

# Agent must infer to try other parameters:
result = search_function(category="electronics")  # Agent's inference
result = search_function(brand="Samsung")  # Agent's alternative
```

**🎯 Desirable Agent Actions (Ideal Solution) - CRITICAL SECTION**:
**This section is MANDATORY and shows the step-by-step problem-solving approach that agents should follow. You MUST structure this section using numbered steps (# Step 1, # Step 2, etc.) that demonstrate the complete workflow from receiving the implicit hint to successfully resolving the limitation.**

```python
# Step 1: Agent receives implicit info and analyzes the function signature
# Original failed call: weather_function(location="Bellevue") 
# Returns: {"success": false, "message": "Weather data for Bellevue temporarily unavailable", "info": "Other regions are accessible"}

# Step 2: Agent should analyze available parameters and infer alternatives
# Function signature analysis: weather_function(location=str, date=optional, format=optional)
# Info analysis: "Other regions are accessible" → try different location values

# Step 3: Agent systematically tries alternative parameter values
alternative_locations = ["Redmond", "Seattle", "Kirkland"]  # Agent's inference from geographic knowledge
for alt_location in alternative_locations:
    result = weather_function(location=alt_location)
    if result["success"]:
        print(f"Successfully retrieved weather data for {alt_location}")
        break

# Alternative approach for different scenario:
# Step 1: Agent receives different type of implicit info
# Original failed call: search_function(product_name="SpecificProduct")
# Returns: {"success": false, "message": "Direct product lookup temporarily disabled", "info": "Browse functionality is operational"}

# Step 2: Agent analyzes info and available parameters
# Info analysis: "Browse functionality is operational" → switch from direct lookup to browsing parameters
# Available parameters: product_name, category, brand, price_range, etc.

# Step 3: Agent switches to alternative parameter approach
result = search_function(category="electronics")  # Agent switches to browsing approach
# OR
result = search_function(brand="Samsung", category="phones")  # Agent combines browse parameters
```

**⚠️ IMPORTANT**: This step-by-step format (# Step 1, # Step 2, # Step 3, etc.) is the REQUIRED approach for demonstrating ideal agent behavior. Each step must clearly show both the agent's reasoning process and the specific action taken.

**Root Cause in API Design**:
[Explain how temporary service limitations or regional restrictions naturally occur in real-world API operations, requiring users to adapt their requests using alternative parameter approaches]

**Concrete Developer Impact**:
[Focus on agent confusion about which specific alternatives to try, the need to analyze function signatures to understand available parameters, and the challenge of inferring the right workaround from vague hints]

### Mitigation Recommendations

#### Documentation Improvements
1. [Provide clearer mapping between error messages and available alternative parameters]
2. [Add function parameter documentation showing alternative approaches for common limitations]
3. [Include examples of how to interpret implicit limitation hints]
"""
    elif uncertainty_type_details["name"] == "System Failure Error":
        template += """
## Special Instructions for System Failure Error Scenarios

For this uncertainty type, focus on complete function failures due to infrastructure or external service issues. You should:

1. MODIFY the API function to fail completely due to realistic infrastructure dependencies
2. The function should return confusing, lengthy, or domain-specific error messages that are hard for agents to interpret
3. Focus on errors that require the agent to understand and clearly report the system failure to users

CRITICAL RULE - DESIRABLE AGENT ACTIONS: 
You MUST include a detailed "Desirable Agent Actions (System Error Communication)" section that shows how agents should:
- Parse complex system error messages
- Understand the root cause of infrastructure failures  
- Communicate the system failure clearly to users in simple terms
- Provide appropriate guidance on what users should expect

Examples of realistic system failures:
- Database dependency: "Database connection failed, service unavailable"
- Weather service dependency: "Satellite communication error"
- External API dependency: "Third-party authentication service timeout"
- Infrastructure issues: "Load balancer configuration error"

When modifying the API description and implementation:
- Add realistic external service dependencies that can fail completely
- Create error messages that are technically accurate but confusing for agents
- Include domain-specific terminology and technical details that require interpretation
- Ensure the errors indicate complete failure with no immediate workaround
"""
        template += """
## Output Format for System Failure Error Scenarios

### Uncertainty Manifestation 1: [Title - Focus on confusing system failure communication]

**Description**:
[Detailed description of how the function fails completely due to infrastructure issues and returns complex error messages that agents must interpret and communicate clearly to users]

**Modified Implementation**:
```python
# Your modified version of the API implementation that demonstrates this uncertainty
# Clearly mark your modifications with comments like ### ADDED: ... ### or ### MODIFIED: ... ###
# Focus on adding system failure simulation with complex error messages - mark where you add
# infrastructure dependency checks and technical error generation in the function flow

### Make uncertainty behavior optional - function works normally unless explicitly enabled ###
# This preserves original functionality by default. Uncertainty only occurs when environment variable is set.
import os

def your_api_function(param1, param2):
    ### ADDED: Check if uncertainty behavior should be activated for this specific function ###
    uncertainty_env_var = f'ENABLE__SYSTEM_FAILURE_ERROR__{function_name.upper()}'
    uncertainty_enabled = os.getenv(uncertainty_env_var, 'false').lower() == 'true'
    
    if uncertainty_enabled:  # uncertainty only occurs when uncertainty_env_var is set
        ### ADDED: Your system failure logic here ###
        # Add your infrastructure dependency checks and complex technical error generation
        # Focus on complete function failures due to realistic infrastructure issues
    else:  # original
        # Original function logic here
        result = perform_original_function_logic(param1, param2)
    
    return result

# Environment Variable Usage:
# Enable: export ENABLE__SYSTEM_FAILURE_ERROR__YOUR_FUNCTION_NAME=true
# Disable: export ENABLE__SYSTEM_FAILURE_ERROR__YOUR_FUNCTION_NAME=false
# OR: unset ENABLE__SYSTEM_FAILURE_ERROR__YOUR_FUNCTION_NAME
```

**Original API Function Response (Success)**:
```json
{
  "success": true,
  "data": [normal results],
  "message": "Operation completed successfully"
}
```

**Modified Response Structure with System Failure Error**:
```json
{
  "success": false,
  "error": "INFRA_DB_CONNECTION_TIMEOUT_ERR_0x4A2B",
  "message": "PostgreSQL connection pool exhausted after 30s timeout on primary cluster node pg-prod-01.internal, failover to secondary unsuccessful due to replica lag >5000ms, circuit breaker activated",
  "technical_details": "Connection string: postgresql://prod-user@pg-prod-01.internal:5432/maindb?sslmode=require&connect_timeout=30&application_name=api-service-v2.1.3",
  "timestamp": "2024-07-04T17:52:47.123Z",
  "trace_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}

// Alternative examples:
{
  "success": false,
  "error": "EXT_WEATHER_SAT_COMM_FAILURE",
  "message": "NOAA satellite feed interruption detected on transponder channel 12.4GHz, ground station at Wallops experiencing signal degradation below -110dBm threshold, estimated restoration 2-4 hours pending orbital repositioning",
  "error_code": "WX_SAT_0047",
  "affected_regions": ["CONUS", "Alaska", "Hawaii"]
}

{
  "success": false,
  "error": "AUTH_SERVICE_CIRCUIT_BREAKER_OPEN",
  "message": "OAuth2 token validation service cluster-auth-prod-us-east-1 reporting 503 status for >5min, circuit breaker pattern activated, fallback authentication mechanisms disabled per security policy SEC-001-2024",
  "retry_after": 900,
  "incident_id": "INC-2024-0704-001"
}
```

**Example Tool Invocation**:
```python
# Agent calls function and receives complex system failure
result = api_function(param1, param2)
print(result)
# Returns complex technical error message that agent must interpret

# Agent confusion scenarios:
# - What does "PostgreSQL connection pool exhausted" mean for the user?
# - How should I explain "circuit breaker activated" to a non-technical user?
# - Should I provide the technical trace_id to the user?
# - How long should the user wait before trying again?
```

**🎯 Desirable Agent Actions (System Error Communication) - CRITICAL SECTION**:
**This section is MANDATORY and shows how agents should parse complex system errors and communicate them clearly to users.**

```python
# Step 1: Agent receives complex system failure error
error_response = {
    "success": false,
    "error": "INFRA_DB_CONNECTION_TIMEOUT_ERR_0x4A2B", 
    "message": "PostgreSQL connection pool exhausted after 30s timeout..."
}

# Step 2: Agent parses technical error to understand root cause
# Agent should identify:
# - System component that failed: Database
# - Type of failure: Connection timeout/unavailability  
# - Impact: Complete service unavailability
# - Expected duration: Unknown, infrastructure issue

# Step 3: Agent formulates clear user-friendly explanation
# Technical message: "PostgreSQL connection pool exhausted after 30s timeout..."
# User-friendly translation: "The service is currently unavailable due to database connectivity issues"

# Step 4: Agent provides appropriate user communication
user_response = \"\"\"I'm sorry, but the service is currently unavailable due to database connectivity issues. 
This appears to be a system-wide problem that our technical team needs to resolve. 
Please try again in a few minutes, and if the issue persists, it may take longer to fix.\"\"\"

# Additional examples:
# Weather satellite error → "Weather data is temporarily unavailable due to satellite communication issues"
# Auth service failure → "Unable to process your request due to authentication service problems" 
# Load balancer error → "The service is experiencing high load and temporary outages"
```

**Root Cause in API Design**:
[Explain how the function's dependency on external infrastructure creates points of complete failure, and how technical error messages are designed for system administrators rather than end users, creating a communication gap that agents must bridge]

**Concrete Developer Impact**:
[Focus on agent difficulty in interpreting technical system errors, challenge of translating infrastructure problems into user-understandable language, and the need for agents to provide appropriate expectations about service restoration without making specific time commitments]

### Mitigation Recommendations

#### Documentation Improvements
1. [Provide clear mapping between technical error codes and user-friendly explanations]
2. [Include estimated recovery timeframes for different types of system failures]
3. [Add guidelines for agents on how to communicate various infrastructure problems to users]
"""
    elif uncertainty_type_details["name"] == "Partially Irrelevant Information":
        template += """
## Special Instructions for Partially Irrelevant Information Scenarios

For this uncertainty type, focus on functions returning requested data mixed with large amounts of irrelevant information. You should:

1. MODIFY the API function to include extensive irrelevant data mixed within the same response objects as the requested information
2. The function should return valid requested data but mixed with irrelevant attributes in the same JSON objects
3. Focus on realistic scenarios where APIs include marketing data, analytics, metadata, and system information mixed with core data

**CRITICAL RULE - MUST BE FOLLOWED: **
You MUST clearly specify which irrelevant information would realistically be added within the same response objects. Provide concrete JSON data structure examples showing:
- Exactly which attributes contain irrelevant information mixed with relevant data
- How irrelevant attributes appear alongside relevant attributes in the same objects
- Realistic examples of what this irrelevant data would look like (marketing scores, analytics, metadata, etc.)

The irrelevant information should be mixed within the same JSON objects, NOT separated into different keys. This makes it harder for agents to distinguish relevant from irrelevant data.

When modifying the API description and implementation:
- Add marketing/promotional attributes mixed with core data attributes
- Include analytics and system metadata within main response objects  
- Mix historical trends and performance metrics with requested information
- Ensure irrelevant data appears believable and potentially useful but not directly relevant to the request
"""
        template += """
## Output Format for Partially Irrelevant Information Scenarios

### Uncertainty Manifestation 1: [Title - Focus on relevant data buried in irrelevant attributes]

**Description**:
[Detailed description of how the function returns requested data mixed with irrelevant attributes within the same response objects, making it difficult for agents to distinguish important information]

**Modified Implementation**:
```python
# Your modified version of the API implementation that demonstrates this uncertainty
# Clearly mark your modifications with comments like ### ADDED: ... ### or ### MODIFIED: ... ###
# Focus on adding irrelevant attributes to the response data structures - mark where you add
# marketing scores, analytics data, or metadata that appears alongside relevant information

### Make uncertainty behavior optional - function works normally unless explicitly enabled ###
# This preserves original functionality by default. Uncertainty only occurs when environment variable is set.
import os

def your_api_function(param1, param2):
    ### ADDED: Check if uncertainty behavior should be activated for this specific function ###
    uncertainty_env_var = f'ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__{function_name.upper()}'
    uncertainty_enabled = os.getenv(uncertainty_env_var, 'false').lower() == 'true'
    
    if uncertainty_enabled:  # uncertainty only occurs when uncertainty_env_var is set
        ### ADDED: Your irrelevant information logic here ###
        # Add your irrelevant attributes mixed with relevant data in the same response objects
        # Focus on marketing scores, analytics data, and metadata alongside core information
    else:  # original
        # Original function logic here
        result = perform_original_function_logic(param1, param2)
    
    return result

# Environment Variable Usage:
# Enable: export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__YOUR_FUNCTION_NAME=true
# Disable: export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__YOUR_FUNCTION_NAME=false
# OR: unset ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__YOUR_FUNCTION_NAME
```

**Original API Function Response (Clean)**:
```json
{
  "success": true,
  "data": [
    {
      "id": "item1",
      "name": "Requested Item", 
      "price": 100,
      "category": "electronics"
    }
  ]
}
```

**Irrelevant Attributes Analysis for This Specific Function**:
[First, analyze the given API function and list specific types of irrelevant information that would realistically be mixed with the function's response. Consider what additional systems/databases this function might pull data from that would add irrelevant attributes.]

**Examples of Function-Specific Irrelevant Attributes**:
- [List 8-12 specific irrelevant attributes that would be realistic for this particular function]
- [Include the attribute name, data type, and brief explanation of why it's irrelevant but might appear]
- [Focus on attributes that would come from marketing systems, analytics databases, ML models, or operational metrics that might be aggregated with the main response]

**Modified Response Structure with Mixed Irrelevant Information**:
```json
{
  "success": true,
  "data": [
    {
      "id": "item1", // relevant
      "name": "Dell Laptop XPS 13", // relevant  
      "price": 999, // relevant
      "category": "electronics", // relevant
      "marketing_boost_score": 85, // irrelevant - marketing optimization score
      "seasonal_promotion_eligible": true, // irrelevant - promotion eligibility
      "user_demographic_match": 78, // irrelevant - demographic targeting score
      "inventory_turnover_rate": 2.3, // irrelevant - supply chain metric
      "competitor_price_advantage": 0.15, // irrelevant - competitive analysis
      "engagement_prediction_score": 89, // irrelevant - user engagement forecast
      "specs": {
        "processor": "Intel i7", // relevant
        "ram": "16GB", // relevant
        "storage": "512GB SSD", // relevant
        "personalization_weight": 0.8, // irrelevant - ML personalization score
        "performance_benchmark_relative": 94, // irrelevant - internal benchmark
        "data_freshness_score": 0.92 // irrelevant - data quality indicator
      }
    }
  ]
}
```

**Detailed Mixed Attribute Examples for Different Function Types**:

```json
// For find_contact() function:
{
  "success": true,
  "contacts": [
    {
      "contact_id": "cont1", // relevant
      "name": "Alice Johnson", // relevant
      "phone": "+1-555-0123", // relevant
      "email": "alice@email.com", // relevant
      "engagement_score": 92, // irrelevant - CRM engagement metric
      "interaction_frequency": 3.2, // irrelevant - communication analytics
      "demographic_cluster": "tech_professional", // irrelevant - market segmentation
      "marketing_segment": "premium_user", // irrelevant - marketing classification
      "predicted_response_time": "2.5hrs", // irrelevant - ML prediction
      "social_influence_rating": 78, // irrelevant - social network analysis
      "lifetime_value_score": 8500 // irrelevant - business metric
    }
  ]
}

// For search_media() function:
{
  "success": true,
  "media": [
    {
      "media_id": "song1", // relevant
      "title": "Requested Song", // relevant
      "artist": "Artist Name", // relevant
      "duration": 240, // relevant
      "popularity_trending_coefficient": 0.87, // irrelevant - trending algorithm score
      "revenue_generation_tier": "high", // irrelevant - monetization data
      "demographic_appeal_index": 76, // irrelevant - audience analytics
      "playlist_inclusion_frequency": 89, // irrelevant - usage statistics
      "mood_analysis_vector": [0.7, 0.3, 0.8], // irrelevant - ML mood analysis
      "marketing_campaign_eligible": true, // irrelevant - promotional flags
      "cross_platform_performance": 94 // irrelevant - multi-platform metrics
    }
  ]
}
```

**Example Tool Invocation**:
```python
# Agent calls function and receives mixed relevant/irrelevant data
result = api_function(param1, param2)
product = result["data"][0]

# Agent gets overwhelmed by mixed relevant/irrelevant attributes
print(f"Name: {product['name']}")  # relevant - easy to find
print(f"Price: {product['price']}")  # relevant - easy to find  
print(f"Marketing score: {product['marketing_boost_score']}")  # irrelevant but agent might think it's important
print(f"Specs: {product['specs']}")  # relevant but mixed with irrelevant attributes inside

# Agent will get confused - which attributes are actually needed?
# - Is marketing_boost_score important for decision making?
# - Should trending_alternative_suggestion be considered?
# - Are the demographic/engagement scores relevant to the search query?

# Agent may waste time processing irrelevant data or miss important specs buried in metadata
```

**Root Cause in API Design**:
[Explain how the function aggregates data from multiple internal systems (marketing, analytics, inventory, ML models) and includes all available attributes without filtering for relevance to the specific request, creating information overload where core data is buried among system metadata]

**Concrete Developer Impact**:
[Focus on agent confusion about which attributes are relevant to their task, increased processing time from analyzing unnecessary data, potential incorrect decisions based on irrelevant metrics, and difficulty extracting the specific information needed for subsequent actions]

### Mitigation Recommendations

#### Documentation Improvements
1. [Clearly categorize response attributes as "core data", "metadata", and "analytics" with relevance indicators]
2. [Add response filtering parameters to request only relevant attribute categories]
3. [Provide simplified response formats for common use cases that exclude analytical metadata]
"""
    else:
        # Add other uncertainty type templates here
        template += """
## Output Format

### Uncertainty Manifestation 1: [Title]

**Description**:
[Detailed description of how this uncertainty manifests in practice]

**Modified API Description**:
```
[Your modified version of the API function description that demonstrates this uncertainty]
```

**Modified Implementation**:
```python
# Your modified version of the API implementation that demonstrates this uncertainty
```

**Example Tool Invocation**:
```python
# Example code showing API calls with this uncertainty
api_function(param1, param2)  # Specific example with exact parameter values
# Expected vs. actual behavior explanation
```

**Root Cause in API Design**:
[Explain which specific aspects of your modified function's design/implementation create this uncertainty]

**Concrete Developer Impact**:
[Describe specific, practical problems developers will face when using this API,
including code complexity, error handling needs, and workarounds required]

### Mitigation Recommendations

#### Documentation Improvements
1. [First documentation recommendation - specific additions or clarifications]
2. [Second documentation recommendation]
3. [Third documentation recommendation]
"""
    
    return template
