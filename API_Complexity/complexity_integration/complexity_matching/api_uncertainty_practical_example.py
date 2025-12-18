# Example of using the API Uncertainty Assessment Template with a real function

# Import the template function
from api_uncertainty_assessment_template import assess_api_uncertainty

# API FUNCTION DESCRIPTION from SmartHomeEnv.tools.temperature_set
api_function_description = """
Function: temperature_set
Description: Set target temperature on one or more thermostats.

Parameters:
- endpoints: List of device endpoint IDs to set temperature on. Each endpoint must correspond to a thermostat device.
- temperature: Target temperature to set. The value interpretation depends on the thermostat's configuration.

Returns: A JSON string with the result of the operation, including success status for each device and any error messages.

Additional context:
- The function works with smart home thermostats to control temperature settings
- Thermostats may be in different modes (heating, cooling, auto, etc.)
- Different regions may use different temperature scales (Celsius/Fahrenheit)
"""

# UNCERTAINTY TYPE: Ad Hoc Rules
uncertainty_type_name = "Ad Hoc Rules"
uncertainty_type_criteria = """
Criteria:
1. Special Value Semantics Likelihood
   - Definition: The likelihood that the function uses specific numeric or string values that carry special meanings beyond their literal value
   - Assessment Question: How likely is this function to use specific values that have special behaviors not obvious from the value itself?
   - Rating Scale:
     - 0: Values are always interpreted literally with no special cases
     - 1: Few common special values that follow industry conventions
     - 2: Multiple special values with non-obvious behaviors or meanings

2. Non-Standard Format Requirements Likelihood
   - Definition: The likelihood that the function requires data in specific formats that deviate from common industry standards
   - Assessment Question: How likely is this function to require inputs in unusual formats or strict variations of standard formats?
   - Rating Scale:
     - 0: Uses only widely adopted standard formats (e.g., ISO-8601, RFC standards)
     - 1: Mostly standard formats with minor variations
     - 2: Requires specialized formats or significant deviations from standards

3. Counter-Intuitive Parameter Behavior Likelihood
   - Definition: The likelihood that parameters behave in ways that contradict what most developers would reasonably expect
   - Assessment Question: How likely would a developer familiar with similar APIs misunderstand how to use this function's parameters?
   - Rating Scale:
     - 0: Parameters behave exactly as their names and common conventions suggest
     - 1: Some parameters have subtle behaviors that might not be immediately obvious
     - 2: Multiple parameters with behaviors that significantly deviate from conventions

4. Hidden Constraints Likelihood
   - Definition: The likelihood that the function has undocumented or obscurely documented restrictions on how it can be used
   - Assessment Question: How likely is this function to have important limitations that aren't immediately obvious from its general description?
   - Rating Scale:
     - 0: All constraints are straightforward and follow standard patterns
     - 1: Some unique constraints that might not be immediately apparent
     - 2: Multiple significant constraints that developers would likely miss

5. Paid Feature Alternative Likelihood
   - Definition: The likelihood that the function offers limited capabilities in its free version while suggesting workarounds for users who don't have paid access
   - Assessment Question: How likely is this function to have premium features with suggested alternatives for free-tier users?
   - Rating Scale:
     - 0: All capabilities available to all users regardless of payment status
     - 1: Some premium capabilities with simple workarounds for free users
     - 2: Significant premium capabilities requiring complex workarounds for free users
"""

# Use the template function to set up the assessment
assessment_instruction = assess_api_uncertainty(api_function_description, uncertainty_type_name + "\n\n" + uncertainty_type_criteria)

print("====== ASSESSMENT TEMPLATE ======")
print(assessment_instruction)
print("================================")

# EXAMPLE ASSESSMENT OUTPUT
example_assessment = """
# Assessment of Ad Hoc Rules Likelihood

## Individual Criteria Scores

1. Special Value Semantics Likelihood: 1
   - Justification: Temperature control systems often use special values like -1 to indicate "off" or maximum/minimum values to indicate special modes, but these generally follow industry conventions in HVAC controls.

2. Non-Standard Format Requirements Likelihood: 1
   - Justification: While temperature values themselves are standard, thermostats often require specific temperature formats (whole numbers, specific decimal precision) that might vary between devices.

3. Counter-Intuitive Parameter Behavior Likelihood: 2
   - Justification: Thermostat APIs typically have mode-dependent temperature interpretations where the same temperature value may have different effects depending on heating/cooling modes, which is not obvious from the parameter name.

4. Hidden Constraints Likelihood: 2
   - Justification: Thermostats have significant operational constraints like minimum/maximum settable temperatures, minimum differentials between heating/cooling targets, and protection modes that prevent certain temperature settings.

5. Paid Feature Alternative Likelihood: 0
   - Justification: Temperature control is a fundamental thermostat function unlikely to be restricted based on payment tiers in a smart home API.

## Overall Assessment
- Total Score: 6
- Normalized Score: 0.6 (6 / (5 × 2))
- Likelihood: Moderate (0.34-0.66)
- Summary: Temperature setting functions in smart home environments naturally develop ad hoc rules due to the physical constraints of HVAC systems, varied manufacturer implementations, and safety considerations. Real-world thermostats have complex behavioral rules that must be reflected in control APIs, creating a moderate likelihood of non-obvious special behaviors and constraints.
"""

print("\n====== EXAMPLE ASSESSMENT ======")
print(example_assessment)
print("================================")
