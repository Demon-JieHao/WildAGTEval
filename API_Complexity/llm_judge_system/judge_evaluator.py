"""
Core evaluation logic for LLM Judge system.
Evaluates agent responses against reference markdown criteria using Claude API.
"""

import json
import time
import os
from claude_client import claude_pred
from prompt_templates import build_judge_prompt, validate_agent_json, validate_reference_markdown
from config import PATH_CONFIG, EVALUATION_CONFIG


def evaluate_agent_response(agent_json_path, reference_md_path, client, output_dir, run_id=0):
    """
    Evaluate a single agent response against reference markdown criteria.
    Adapted from generate_scenario() pattern in the notebook.
    
    Args:
        agent_json_path: Path to agent response JSON file
        reference_md_path: Path to reference markdown file
        client: Claude API client
        output_dir: Directory to save evaluation results
        run_id: Run identifier for tracking multiple evaluation runs
    
    Returns:
        Dictionary containing evaluation results
    """
    
    # Extract information from file paths
    agent_filename = os.path.basename(agent_json_path)
    reference_filename = os.path.basename(reference_md_path)
    
    # Create output directory structure
    os.makedirs(output_dir, exist_ok=True)
    
    # Define output file path
    output_filename = f"evaluation_{agent_filename}_{reference_filename}_{run_id}.json"
    output_file = os.path.join(output_dir, output_filename)
    
    # Check if result already exists (optional - can be enabled/disabled)
    if EVALUATION_CONFIG.get('skip_existing', False) and os.path.exists(output_file):
        print(f"Evaluation for {agent_filename} already exists. Skipping.")
        with open(output_file, 'r') as f:
            result = json.load(f)
        return result
    
    print(f"Evaluating: {agent_filename} against {reference_filename}")
    
    try:
        # Read the agent response JSON
        with open(agent_json_path, 'r', encoding='utf-8') as f:
            agent_data = json.load(f)
        
        # Read the reference markdown
        with open(reference_md_path, 'r', encoding='utf-8') as f:
            reference_content = f.read()
        
        # Validate input data
        validate_agent_json(agent_data)
        validate_reference_markdown(reference_content)
        
        # Build the judge prompt
        judge_prompt = build_judge_prompt(
            agent_data, 
            reference_content, 
            os.path.abspath(agent_json_path),
            os.path.abspath(reference_md_path)
        )
        
        # Call Claude API for evaluation
        start_time = time.time()
        
        print(f"Sending evaluation request to Claude...")
        evaluation_raw = claude_pred(client, judge_prompt)
        
        end_time = time.time()
        
        # Parse the JSON response from Claude
        try:
            evaluation_json = json.loads(evaluation_raw)
        except json.JSONDecodeError as e:
            print(f"Error parsing Claude response as JSON: {e}")
            print(f"Raw response: {evaluation_raw[:500]}...")
            # Save raw response for debugging
            evaluation_json = {
                "evaluation_summary": {
                    "agent_response_path": os.path.abspath(agent_json_path),
                    "reference_markdown_path": os.path.abspath(reference_md_path),
                    "function_name": "parse_error",
                    "total_score": "0/5",
                    "overall_performance": "Parse Error"
                },
                "detailed_scores": {},
                "improvement_suggestions": ["Fix JSON parsing error in Claude response"],
                "alignment_assessment": "Unable to assess due to JSON parsing error",
                "raw_claude_response": evaluation_raw,
                "parsing_error": str(e)
            }
        
        # Format final results
        result = {
            "agent_json_path": os.path.abspath(agent_json_path),
            "reference_md_path": os.path.abspath(reference_md_path),
            "agent_filename": agent_filename,
            "reference_filename": reference_filename,
            "evaluation": evaluation_json,
            "execution_time": end_time - start_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "run_id": run_id,
            "claude_model": "us.anthropic.claude-opus-4-20250514-v1:0"
        }
        
        # Save the result
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Evaluation completed in {end_time - start_time:.2f} seconds")
        print(f"Results saved to: {output_file}")
        
        return result
    
    except Exception as e:
        print(f"Error evaluating {agent_json_path}: {str(e)}")
        
        # Create error result
        error_result = {
            "agent_json_path": os.path.abspath(agent_json_path),
            "reference_md_path": os.path.abspath(reference_md_path),
            "agent_filename": agent_filename,
            "reference_filename": reference_filename,
            "evaluation": {
                "evaluation_summary": {
                    "agent_response_path": os.path.abspath(agent_json_path),
                    "reference_markdown_path": os.path.abspath(reference_md_path),
                    "function_name": "error",
                    "total_score": "0/5",
                    "overall_performance": "Evaluation Error"
                },
                "detailed_scores": {},
                "improvement_suggestions": ["Fix evaluation error"],
                "alignment_assessment": "Unable to assess due to evaluation error",
                "error": str(e)
            },
            "execution_time": 0,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "run_id": run_id,
            "status": "error"
        }
        
        # Save error result
        error_output_file = os.path.join(output_dir, f"error_{output_filename}")
        with open(error_output_file, 'w', encoding='utf-8') as f:
            json.dump(error_result, f, indent=2, ensure_ascii=False)
        
        return error_result


def extract_error_type_simple(agent_dir):
    """
    Simple keyword-based error type extraction.
    
    Args:
        agent_dir: Path to agent directory
        
    Returns:
        Error type string or None if not found
        
    Examples:
        test_with_uncertainties/.../feature_limitation.../track_order/ → "feature_limitation"
        test_with_uncertainties/.../system_failure.../get_user_inventory/ → "system_failure"
    """
    if not agent_dir:
        return None
    
    # Simple keyword search
    if 'feature_limitation' in agent_dir:
        return 'feature_limitation'
    elif 'system_failure' in agent_dir:
        return 'system_failure'
    else:
        return None


def extract_function_name_from_path(agent_dir):
    """
    Extract function name from the last folder in path.
    
    Args:
        agent_dir: Path to agent directory
        
    Returns:
        Function name string
        
    Examples:
        test_with_uncertainties/.../track_order/ → "track_order"
        test_with_uncertainties/.../get_user_inventory/ → "get_user_inventory"
    """
    if not agent_dir:
        return None
    
    # Get the last folder name
    return agent_dir.strip('/').split('/')[-1]


def extract_error_type_from_path(agent_dir):
    """
    Legacy error type extraction for backward compatibility.
    
    Args:
        agent_dir: Path to agent directory
        
    Returns:
        Error type string or None if not found
    """
    if not agent_dir:
        return None
    
    # Normalize path and split into parts
    path_parts = os.path.normpath(agent_dir).split(os.sep)
    
    # Look for error type patterns in path parts
    error_patterns = [
        "feature_limitation_error",
        "system_failure_error", 
        "informational_notice",
        "partially_irrelevant_information"
    ]
    
    for part in path_parts:
        for pattern in error_patterns:
            if pattern in part:
                return pattern
    
    return None


def find_matching_reference_file(agent_json_path, reference_dir, agent_dir=None):
    """
    Find the appropriate reference markdown file for an agent JSON file.
    Supports both new and legacy path formats.
    
    Args:
        agent_json_path: Path to agent JSON file
        reference_dir: Directory containing reference markdown files
        agent_dir: Directory containing agent files (for error type extraction)
    
    Returns:
        Path to matching reference file or None if not found
    """
    
    if not agent_dir:
        print("Warning: No agent_dir provided for reference file matching")
        return None
    
    # Try new simple approach first (for test_with_uncertainties paths)
    if 'test_with_uncertainties' in agent_dir:
        print(f"Using new path format for: {agent_dir}")
        
        # Extract function name from path
        func_name = extract_function_name_from_path(agent_dir)
        
        # Extract error type using simple keyword search
        error_type = extract_error_type_simple(agent_dir)
        
        if func_name and error_type:
            # Construct reference filename
            reference_filename = f"{func_name}_{error_type}_error.md"
            reference_path = os.path.join(reference_dir, reference_filename)
            
            if os.path.exists(reference_path):
                print(f"Matched: {func_name} + {error_type} -> {reference_filename}")
                return reference_path
            else:
                print(f"Warning: Reference file not found: {reference_filename}")
                return None
        else:
            print(f"Warning: Could not extract func_name={func_name} or error_type={error_type} from: {agent_dir}")
            return None
    
    # Fallback to legacy approach for older path formats
    else:
        print(f"Using legacy path format for: {agent_dir}")
        
        agent_filename = os.path.basename(agent_json_path)
        
        # Extract function name from agent filename (legacy method)
        if "track_order" in agent_filename:
            function_name = "track_order"
        elif "get_messages" in agent_filename:
            function_name = "get_messages"
        else:
            print(f"Warning: Could not identify function from filename: {agent_filename}")
            return None
        
        # Extract error type from agent directory path (legacy method)
        error_type = extract_error_type_from_path(agent_dir)
        
        if error_type:
            # Use extracted error type to construct reference filename
            reference_pattern = f"{function_name}_{error_type}.md"
            reference_file = os.path.join(reference_dir, reference_pattern)
            
            if os.path.exists(reference_file):
                print(f"Matched: {agent_filename} -> {reference_pattern} (from path: {agent_dir})")
                return reference_file
            else:
                print(f"Warning: Expected reference file not found: {reference_pattern}")
                return None
        else:
            print(f"Warning: Could not extract error type from path: {agent_dir}")
            return None


def evaluate_single_file_with_auto_matching(agent_json_path, client, output_dir, run_id=0):
    """
    Evaluate a single agent file by automatically finding its matching reference file.
    
    Args:
        agent_json_path: Path to agent JSON file
        client: Claude API client
        output_dir: Directory to save results
        run_id: Run identifier
    
    Returns:
        Evaluation result dictionary
    """
    
    reference_dir = PATH_CONFIG['reference_dir']
    reference_file = find_matching_reference_file(agent_json_path, reference_dir)
    
    if not reference_file:
        print(f"Error: No matching reference file found for {agent_json_path}")
        return None
    
    print(f"Auto-matched: {os.path.basename(agent_json_path)} -> {os.path.basename(reference_file)}")
    
    return evaluate_agent_response(
        agent_json_path, 
        reference_file, 
        client, 
        output_dir, 
        run_id
    )


if __name__ == "__main__":
    # Test single evaluation
    from claude_client import create_claude_client
    
    client = create_claude_client()
    if client:
        # Example test (update paths as needed)
        agent_file = "turn_level_tf_results/featlimit/Conv_user1_TransactionEnv_shopping_batch_scenario4_orders_TurnLevelTF_Turn2_Step0_track_order.json"
        reference_file = "function_uncertainty_references/track_order_feature_limitation_error.md"
        output_dir = "judge_results/test"
        
        if os.path.exists(agent_file) and os.path.exists(reference_file):
            result = evaluate_agent_response(agent_file, reference_file, client, output_dir)
            print("Test evaluation completed successfully!")
        else:
            print("Test files not found. Please check paths.")
    else:
        print("Failed to create Claude client for testing.")
