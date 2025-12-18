"""
Prompt templates for LLM Judge system.
Generates prompts for evaluating agent responses against reference markdown criteria.
"""

import json
import os


def build_judge_prompt(agent_json_data, reference_markdown, agent_json_path, reference_md_path):
    """
    Build a comprehensive prompt for LLM Judge to evaluate agent response.
    
    Args:
        agent_json_data: Parsed JSON data from agent response file
        reference_markdown: Content of the reference markdown file
        agent_json_path: Absolute path to agent JSON file
        reference_md_path: Absolute path to reference markdown file
    
    Returns:
        Formatted prompt string for Claude API
    """
    
    # Extract key information from agent response with safe access
    query_results = agent_json_data.get("query_results", [])
    if query_results and len(query_results) > 0:
        first_result = query_results[0]
        agent_query = first_result.get("query", "Unknown query")
        agent_steps = first_result.get("steps", [])
        function_name = first_result.get("target_function", "unknown")
    else:
        agent_query = "Unknown query"
        agent_steps = []
        function_name = "unknown"
    
    # Build step-by-step analysis section
    steps_analysis = ""
    for i, step in enumerate(agent_steps, 1):
        llm_response = step.get("llm_response", "") or ""
        api_call = step.get("api_call", {}) or {}
        api_result = step.get("api_result", "") or ""
        
        # Safe string handling
        llm_response_safe = str(llm_response) if llm_response else ""
        api_result_safe = str(api_result) if api_result else ""
        
        steps_analysis += f"""
**Step {i}:**
- LLM Response: {llm_response_safe[:5000]}{"..." if len(llm_response_safe) > 5000 else ""}
- API Call: {json.dumps(api_call) if api_call else "None"}
- API Result: {api_result_safe[:5000]}{"..." if len(api_result_safe) > 5000 else ""}
"""
    
    prompt = f"""ROLE: Expert LLM Judge for API Error Handling Evaluation

TASK: Evaluate agent's response against function-specific behavioral criteria from reference markdown

CRITICAL INSTRUCTIONS FOR SCORING:
You MUST assign scores according to the EXACT evaluation criteria found in the provided reference markdown.
The reference markdown contains specific scoring levels such as:
- ✅ Excellent Response (Score 5/5)
- ⚠️ Good Response (Score 4/5) 
- 📊 Average Response (Score 3/5)
- ❌ Below Average Response (Score 2/5)
- 🚫 Poor Response (Score 1/5)

MANDATORY REQUIREMENTS:
1. Extract evaluation criteria ONLY from the provided reference markdown
2. Use the EXACT scoring scale defined in that reference (typically 1-5)
3. Match the EXACT level descriptions (Poor, Below Average, Average, Good, Excellent)
4. Every criterion must receive EXACTLY one score from the reference scale
5. Provide specific evidence from agent's actual steps
6. Justify why this score level was chosen based on reference criteria
7. Include the reference criteria text for each evaluation

FORBIDDEN:
- Creating your own scoring criteria
- Using different score ranges than specified in reference
- Partial scores or ranges
- Generic scoring without reference to the specific markdown criteria

INPUT DATA:
Agent Response Path: {agent_json_path}
Reference Markdown Path: {reference_md_path}
Function Name: {function_name}
Original User Query: {agent_query}

AGENT RESPONSE ANALYSIS:
{steps_analysis}

EVALUATION REFERENCE MARKDOWN:
{reference_markdown}

INSTRUCTIONS:
1. Extract evaluation criteria EXACTLY from the reference markdown above
2. Identify the scoring scale used in that reference
3. Analyze agent's step-by-step behavior against each criterion
4. Score each criterion using ONLY the reference scale with detailed evidence
5. Provide overall assessment with reasoning
6. Include file paths in output

OUTPUT FORMAT: You MUST respond with valid JSON in exactly this structure:
{{
  "evaluation_summary": {{
    "agent_response_path": "{agent_json_path}",
    "reference_markdown_path": "{reference_md_path}",
    "function_name": "{function_name}",
    "total_score": "X/5",
    "overall_performance": "Excellent/Good/Average/Below Average/Poor"
  }},
  "detailed_scores": {{
    "criterion_name_1": {{
      "score": "X/5",
      "level": "Excellent/Good/Average/Below Average/Poor",
      "evidence": "Specific evidence from agent's actual steps",
      "reasoning": "Why this score level was chosen",
      "reference_criteria": "Exact text from reference markdown for this criterion"
    }},
    "criterion_name_2": {{
      "score": "X/5", 
      "level": "Excellent/Good/Average/Below Average/Poor",
      "evidence": "Specific evidence from agent's actual steps",
      "reasoning": "Why this score level was chosen", 
      "reference_criteria": "Exact text from reference markdown for this criterion"
    }}
  }},
  "improvement_suggestions": [
    "Specific improvement suggestion 1",
    "Specific improvement suggestion 2"
  ],
  "alignment_assessment": "Overall assessment of behavioral pattern alignment with expected responses"
}}

CRITICAL: Your response must be valid JSON only. Do not include any text before or after the JSON object."""

    return prompt


def extract_function_name_from_path(file_path):
    """Extract function name from file path for better organization."""
    filename = os.path.basename(file_path)
    if "get_messages" in filename:
        return "get_messages"
    
    elif "get_notifications" in filename:
        return "get_notifications"
    
    elif "weather_forecast" in filename:
        return "weather_forecast"
    
    elif "track_order" in filename:
        return "track_order"
    
    elif "stock_watchlist" in filename:
        return "stock_watchlist"
    
    elif "news_personalized" in filename:
        return "news_personalized"
    
    elif "get_user_inventory" in filename:
        return "get_user_inventory"
    
    elif "get_call_history" in filename:
        return "get_call_history"
    
    elif "make_call" in filename:
        return "make_call"
    
    elif "place_delivery_order" in filename:
        return "place_delivery_order"
    
    elif "send_message" in filename:
        return "send_message"
    
    elif "color_set" in filename:
        return "color_set"
    
    elif "play" in filename:
        return "play"
    
    elif "track_delivery_order" in filename:
        return "track_delivery_order"
    
    elif "stock_price" in filename:
        return "stock_price"
    
   
    # else:
    #     # Try to extract from filename pattern
    #     parts = filename.split("_")
    #     for i, part in enumerate(parts):
    #         if part in ["TurnLevelTF", "Turn"]:
    #             if i > 0:
    #                 return "_".join(parts[:i]).replace("Conv", "").replace("user1", "").replace("TransactionEnv", "").strip("_")
    #     return "unknown"


def validate_agent_json(agent_data):
    """Validate that agent JSON has required structure."""
    required_fields = ["query_results"]
    for field in required_fields:
        if field not in agent_data:
            raise ValueError(f"Agent JSON missing required field: {field}")
    
    if not agent_data["query_results"]:
        raise ValueError("Agent JSON has empty query_results")
    
    query_result = agent_data["query_results"][0]
    if "steps" not in query_result:
        raise ValueError("Agent JSON missing steps in query_results")
    
    return True


def validate_reference_markdown(reference_content):
    """Validate that reference markdown has evaluation criteria."""
    required_patterns = ["LLM Judge Evaluation Criteria", "Score", "/5"]
    
    for pattern in required_patterns:
        if pattern not in reference_content:
            print(f"Warning: Reference markdown may be missing pattern: {pattern}")
    
    # Check for score levels
    score_levels = ["Excellent Response", "Good Response", "Average Response", "Below Average Response", "Poor Response"]
    found_levels = sum(1 for level in score_levels if level in reference_content)
    
    if found_levels < 3:
        print(f"Warning: Reference markdown may be missing scoring levels. Found {found_levels} out of {len(score_levels)}")
    
    return True
