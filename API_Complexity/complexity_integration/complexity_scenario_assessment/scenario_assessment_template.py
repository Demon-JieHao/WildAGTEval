#!/usr/bin/env python3
"""
Generate assessment templates for uncertainty scenarios.
"""

def generate_assessment_template(api_function_details, uncertainty_type_details, 
                               uncertainty_type_instructions, scenario_content, 
                               output_format_instructions=None, run_ids=None):
    """
    Generate an assessment template for a specific scenario.
    
    Parameters:
    - api_function_details: Dictionary containing API function information
    - uncertainty_type_details: Dictionary containing uncertainty type information
    - uncertainty_type_instructions: String containing specific instructions for this uncertainty type
    - scenario_content: String containing the scenario content
    - output_format_instructions: Optional string containing output format instructions
    - run_ids: Optional list of run IDs included in the scenario content
    
    Returns:
    - String containing the assessment template
    """
    
    # Extract domain, function name, and uncertainty type
    domain = api_function_details.get("domain", "Unknown")
    function = api_function_details.get("name", "Unknown")
    uncertainty_type = uncertainty_type_details.get("name", "Unknown")
    
    # Format run ID if available
    runs_info = ""
    if run_ids:
        runs_info = f"\n\n**Included Run:** {run_ids}"
    
    # Format criteria for better readability if available
    criteria = ""
    if uncertainty_type_details.get("criteria"):
        criteria_text = uncertainty_type_details.get("criteria").replace("#", "").strip()
        criteria_items = [item.strip() for item in criteria_text.split('\n') if item.strip()]
        if criteria_items:
            criteria = "\n\n### Criteria"
            for i, item in enumerate(criteria_items, 1):
                criteria += f"\n{i}. {item}"
    
        # Generate the template
    template = f"""# Scenario Assessment: {domain}.{function} - {uncertainty_type}

## Assessment Task Overview

This template provides a structured framework for evaluating a **Specified Uncertainty Manifestation Scenario**. 

The goal is to assess how effectively the scenario demonstrates the "{uncertainty_type}" uncertainty type within the context of the {domain}.{function} API. This assessment considers:

1. How realistically the scenario represents challenges developers would face in production environments
2. How faithfully it implements the specific characteristics of the "{uncertainty_type}" uncertainty type
3. How efficiently and elegantly the uncertainty is manifested in the API design

The assessment draws from multiple sources:
- API function specification and implementation details
- Formal uncertainty type definitions and criteria
- Specialized instructions for creating "{uncertainty_type}" scenarios
- The actual scenario content describing how the uncertainty manifests

## API Function Information

**Domain:** {domain}
**Function:** {function}
**Description:** {api_function_details.get("description", "N/A")}

**Implementation:**
```python
{api_function_details.get("implementation", "Implementation not available.")}
```

## Uncertainty Type Information

### Type: {uncertainty_type}
{uncertainty_type_details.get("description", "N/A")}{criteria}

## Uncertainty Type Specific Instructions

{uncertainty_type_instructions}

## Scenario Content{runs_info}

{scenario_content}

## Assessment Instructions

This assessment evaluates the uncertainty scenario across three equally weighted dimensions (33.33% each). For each dimension, carefully review the scenario against the specific criteria below, assign a score from 1-10 based on the rubric, and provide a clear rationale with specific examples from the scenario.

### 1. Real-world Resonance

**What this measures**: How realistic, plausible, and authentic the scenario is for developers in actual production environments

**Evaluation Criteria**:
- To what degree does the scenario represent a realistic manifestation of the uncertainty type in a production environment?
- How well does the scenario reflect genuine challenges developers would face when using this API?
- Does the scenario present a confusing situation that would authentically impact developer productivity?
- Is the manifestation specific to the function's domain and purpose rather than generic?

***Scoring Rubric** (10-point scale):
- **1**: Completely unrealistic scenario with no connection to actual development practices
- **2**: Highly implausible scenario that contradicts common development workflows
- **3**: Unrealistic scenario that would rarely if ever occur in practice
- **4**: Low plausibility scenario with minimal potential to cause confusion
- **5**: Somewhat plausible scenario but unlikely to cause significant confusion
- **6**: Moderately realistic scenario with some potential to confuse developers
- **7**: Realistic scenario that could reasonably cause developer confusion
- **8**: Highly realistic scenario that would naturally cause confusion
- **9**: Very authentic scenario representing a common developer challenge
- **10**: Exceptionally authentic scenario representing a severe, widespread developer challenge

### 2. Uncertainty-Type Conformance

**What this measures**: How closely the scenario follows the specific requirements and characteristics of the uncertainty type

**Evaluation Criteria**:
- How closely does the scenario follow the specific instructions for its uncertainty type as defined in ## Uncertainty Type Specific Instructions?
- Does the scenario focus exclusively on the correct aspects of uncertainty (e.g., input arguments for ambiguous documentation)?
- Has the scenario avoided prohibited patterns (e.g., using existing API functions for unclear functionality boundaries)?
- Does the scenario implement the key requirements for its uncertainty type (e.g., permanent rules for ad hoc rules)?

**Scoring Rubric** (10-point scale):
- **1**: Completely ignores or contradicts uncertainty type instructions
- **2**: Fundamentally misinterprets the uncertainty type purpose
- **3**: Significant deviations from uncertainty type requirements
- **4**: Partially follows instructions but contains major deviations
- **5**: Generally follows primary instructions with several inconsistencies
- **6**: Implements basic requirements with minor inconsistencies
- **7**: Generally follows instructions with few inconsistencies
- **8**: Closely adheres to instructions with minimal deviations
- **9**: Excellent implementation that faithfully captures the uncertainty type
- **10**: Exemplary implementation perfectly capturing the uncertainty type's essence


### 3. Implementation Efficiency

**What this measures**: How efficiently and clearly the scenario implements the uncertainty with minimal and focused changes

**Evaluation Criteria**:
- Are the modifications to the API function's **Implementation:** in ## API Function Information minimal and focused?
- How easy is it to understand the implementation changes and their connection to the uncertainty?
- Are the changes grounded in the original description/implementation, adding only what's necessary?
- For scenarios with similar API functions (unclear boundaries), are the hypothetical functions well-designed and clearly explained?

**Scoring Rubric** (10-point scale):
- **1**: Completely unrelated modifications with no connection to the original implementation
- **2**: Excessive, confusing modifications that obscure the original function's purpose
- **3**: Major changes that greatly complicate the implementation unnecessarily
- **4**: Overly complex changes that are difficult to understand
- **5**: Modifications with unnecessary complexity and several unclear elements
- **6**: Reasonable modifications with some unnecessary complexity or unclear elements
- **7**: Mostly focused changes with minor unnecessary elements
- **8**: Clear, focused changes that effectively demonstrate the uncertainty
- **9**: Very elegant implementation with minimal, precise changes
- **10**: Exceptionally elegant, minimal changes that perfectly illustrate the uncertainty

## OUTPUT FORMAT

Complete all sections below with your detailed assessment.

### Dimension Scores

| Dimension | Score (1-10) | Weight | Weighted Score |
|-----------|--------------|--------|---------------|
| Real-world Resonance | [SCORE] | 33.33% | [WEIGHTED] |
| Uncertainty-Type Conformance | [SCORE] | 33.33% | [WEIGHTED] |
| Implementation Efficiency | [SCORE] | 33.33% | [WEIGHTED] |
| **TOTAL** | | | **[TOTAL]** |

### Score Classification

**Classification:** [Poor / Acceptable / Good / Excellent]  
**Total Score:** [TOTAL]

**Interpretation Scale**:
- **1.0-3.0**: Poor - Significant revision needed
- **3.1-5.0**: Acceptable - Usable with improvements
- **5.1-8.0**: Good - Effective scenario with minor refinements possible
- **8.1-10.0**: Excellent - Exemplary scenario requiring no changes

### Primary Strengths
1. [First major strength]
2. [Second major strength]

### Primary Weaknesses
1. [First major weakness]
2. [Second major weakness]

### Improvement Recommendations
[Provide 2-3 specific, actionable recommendations if the score is below 8.0. Focus on concrete changes that would improve the scenario's effectiveness]

## Final Determination

This scenario [EFFECTIVELY/PARTIALLY/FAILS TO] demonstrates the **[UNCERTAINTY_TYPE]** uncertainty type in the **[DOMAIN].[FUNCTION]** API. 

[1-2 sentence conclusion about whether this scenario should be used as an example of this uncertainty type, potentially with the suggested improvements]
"""
    
    return template

# Test the function if called directly
if __name__ == "__main__":
    # Create a simple test with dummy data
    api_function_details = {
        "domain": "TestDomain",
        "name": "test_function",
        "description": "A test function description"
    }
    
    uncertainty_type_details = {
        "name": "test_uncertainty",
        "description": "A test uncertainty description"
    }
    
    uncertainty_type_instructions = "Test instructions for this uncertainty type."
    
    scenario_content = "This is a test scenario content."
    
    template = generate_assessment_template(
        api_function_details,
        uncertainty_type_details,
        uncertainty_type_instructions,
        scenario_content
    )
    
    print(template)
