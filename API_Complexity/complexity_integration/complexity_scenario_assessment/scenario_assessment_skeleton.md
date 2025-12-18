# INSTRUCTION for assessing uncertainty scenarios

## Concise Skeleton
1. TASK: Evaluate scenario effectiveness for demonstrating API uncertainty
2. API: [Domain].[Function]
3. UNCERTAINTY: [Type]
4. DIMENSIONS (33.33% each):
   4.1. REAL-WORLD RESONANCE: Score [1-5] - [Brief justification]
   4.2. TYPE CONFORMANCE: Score [1-5] - [Brief justification]
   4.3. IMPLEMENTATION EFFICIENCY: Score [1-5] - [Brief justification]
5. OVERALL: [Total] - [Poor/Acceptable/Good/Excellent]
6. STRENGTHS: 1. [First] 2. [Second]
7. WEAKNESSES: 1. [First] 2. [Second]
8. RECOMMENDATIONS: [Brief actionable improvements]
9. DETERMINATION: [EFFECTIVELY/PARTIALLY/FAILS TO] demonstrates uncertainty

## Detailed Skeleton

## 1. ASSESSMENT TASK OVERVIEW
   - Evaluate how effectively the scenario demonstrates the uncertainty type
   - Assess 3 equally weighted dimensions (33.33% each):
     * Real-world Resonance
     * Uncertainty-Type Conformance
     * Implementation Efficiency
   - Score each dimension on a 1-5 scale with detailed rationale

## 2. API FUNCTION INFORMATION
   - Domain: [Function's domain, e.g., SmartHomeEnv]
   - Function: [Function name, e.g., temperature_set]
   - Description: [Original function description]
   - Implementation: [Original function implementation code]

## 3. UNCERTAINTY TYPE INFORMATION
   - Type: [Uncertainty type name, e.g., ambiguous_documentation]
   - Description: [General description of this uncertainty type]
   - Criteria: [List of criteria for evaluating this uncertainty type]

## 4. UNCERTAINTY TYPE SPECIFIC INSTRUCTIONS
   - [Specialized instructions for creating scenarios of this uncertainty type]
   - [Guidelines specific to this uncertainty category]

## 5. SCENARIO CONTENT
   - [The specific uncertainty scenario to be assessed]
   - [Includes modified API description and implementation]

## 6. ASSESSMENT INSTRUCTIONS
   ### 6.1 Real-world Resonance
   - What this measures: Realism and authenticity for developers in production
   - Evaluation criteria:
     * Realistic manifestation in production environments
     * Reflection of genuine developer challenges
     * Confusion impact on developer productivity
     * Specificity to function's domain and purpose
   - Scoring rubric: 1-5 scale (1: Unrealistic, 5: Exceptionally authentic)

   ### 6.2 Uncertainty-Type Conformance
   - What this measures: Adherence to uncertainty type requirements
   - Evaluation criteria:
     * Follows specific instructions for uncertainty type
     * Focuses on correct aspects of uncertainty
     * Avoids prohibited patterns
     * Implements key requirements for uncertainty type
   - Scoring rubric: 1-5 scale (1: Misinterprets instructions, 5: Exemplary implementation)

   ### 6.3 Implementation Efficiency
   - What this measures: Efficient, clear implementation with minimal changes
   - Evaluation criteria:
     * Modifications minimal and focused
     * Easy to understand changes and connection to uncertainty
     * Changes grounded in original implementation
     * Well-designed hypothetical functions (for boundaries)
   - Scoring rubric: 1-5 scale (1: Excessive modifications, 5: Exceptionally elegant changes)

## 7. OUTPUT FORMAT
   ### Dimension Scores
   | Dimension | Score (1-5) | Weight | Weighted Score |
   |-----------|-------------|--------|---------------|
   | Real-world Resonance | [SCORE] | 33.33% | [WEIGHTED] |
   | Uncertainty-Type Conformance | [SCORE] | 33.33% | [WEIGHTED] |
   | Implementation Efficiency | [SCORE] | 33.33% | [WEIGHTED] |
   | **TOTAL** | | | **[TOTAL]** |

   ### Score Classification
   **Classification:** [Poor / Acceptable / Good / Excellent]  
   **Total Score:** [TOTAL]

   **Interpretation Scale**:
   - **1.0-2.0**: Poor - Significant revision needed
   - **2.1-3.0**: Acceptable - Usable with improvements
   - **3.1-4.0**: Good - Effective scenario with minor refinements
   - **4.1-5.0**: Excellent - Exemplary scenario requiring no changes

   ### Primary Strengths
   1. [First major strength]
   2. [Second major strength]

   ### Primary Weaknesses
   1. [First major weakness]
   2. [Second major weakness]

   ### Improvement Recommendations
   [2-3 specific, actionable recommendations for scores below 4.0]

   ### Final Determination
   This scenario [EFFECTIVELY/PARTIALLY/FAILS TO] demonstrates the uncertainty type in the API.
   [1-2 sentence conclusion about whether this scenario should be used]
