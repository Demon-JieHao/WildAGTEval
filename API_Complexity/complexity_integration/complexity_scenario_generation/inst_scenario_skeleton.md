# INSTRUCTION for creating realistic uncertainty scenarios (INSTscenario)

## Concise Skeleton
1. TASK: Generate realistic API uncertainty scenarios
2. API FUNCTION: [Domain].[Name] - [Brief description]
3. UNCERTAINTY TYPE: [Type] - [Brief description]
4. PLAUSIBILITY: [Score] ([Likelihood]) - [Brief justification]
5. INSTRUCTIONS: Create scenarios with minimum changes showing uncertainty
6. OUTPUT FORMAT:
   6.1 MANIFESTATION: [Title]
   6.2 DESCRIPTION: [How uncertainty manifests]
   6.3 MODIFIED API: [Changed description]
   6.4 MODIFIED CODE: [Implementation showing uncertainty]
   6.5 EXAMPLE: [Usage showing confusion]

## Detailed Skeleton

## 1. TASK
   - Generate concrete, realistic scenarios where specified uncertainty type manifests in API function
   - Convert abstract uncertainty type into specific, practical manifestations for API users
   - Modify API Description and Implementation with minimum necessary changes

## 2. API FUNCTION INFORMATION
   - Description: [Original function description]
   - Implementation: [Original function implementation code]
   - Domain: [Function's domain, e.g., SmartHomeEnv]
   - Name: [Function name, e.g., temperature_set]

## 3. UNCERTAINTY TYPE INFORMATION
   - Type: [Uncertainty type name, e.g., ambiguous_documentation]
   - Description: [General description of this uncertainty type]
   - Criteria: [List of criteria for evaluating this uncertainty type]

## 4. PLAUSIBILITY ASSESSMENT
   - Summary: [Why this uncertainty is likely for this function]
   - Score: [Normalized score (0-1)]
   - Likelihood: [Low, Moderate, High]

## 5. INSTRUCTIONS
   1. Analyze API implementation focusing on potential uncertainty aspects
   2. Identify specific concrete scenarios where uncertainty manifests in production
   3. Focus on common usage patterns where developers naturally encounter this uncertainty
   4. For each scenario:
      - Provide descriptive title
      - Explain manifestation in practical terms
      - Explain root cause in API design
      - Describe impact on API users and applications

## 6. SPECIAL INSTRUCTIONS
   **For Ambiguous Documentation:**
   - Focus on parameter ambiguity, not return values or side effects
   - Add necessary parameters to illustrate ambiguity
   - Consider ambiguities in units, formats, or terminology
   - Ensure uncertainties reflect realistic documentation issues

   **For Ad Hoc Rules:**
   - Focus on special requirements that deviate from expectations
   - Add constraints to existing parameters
   - Ensure rules must be followed (violations cause visible problems)
   - Focus on counter-intuitive but technically documented constraints

   **For Unclear Functionality Boundaries:**
   - Focus on similar functions with different behaviors
   - Create hypothetical functions with similar names/signatures
   - Ensure functions seem related but handle edge cases differently
   - Functions should have overlapping but distinct functionality

## 7. OUTPUT FORMAT
   ### Uncertainty Manifestation 1: [Title]
   
   **Description**:
   [Detailed description of how uncertainty manifests in practice]

   **Modified API Description**:
   ```
   [Modified API function description demonstrating the uncertainty]
   ```

   **Modified Implementation**:
   ```python
   # Modified implementation with clearly marked changes
   # Highlight uncertainty with comments like "### Modified for uncertainty ###"
   ```

   **Example Tool Invocation**:
   ```python
   # Example showing developer confusion or errors due to uncertainty
   api_function(param1, param2)  # With specific values
