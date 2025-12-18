"""
Utility functions for LLM Judge system.
"""

import os
import json
import time
from datetime import datetime


def format_timestamp(timestamp=None):
    """Format timestamp for consistent display."""
    if timestamp is None:
        timestamp = time.time()
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def safe_json_load(file_path):
    """Safely load JSON file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {str(e)}")
        return None
    except Exception as e:
        print(f"Error: Failed to read {file_path}: {str(e)}")
        return None


def safe_file_read(file_path):
    """Safely read text file with error handling."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        return None
    except Exception as e:
        print(f"Error: Failed to read {file_path}: {str(e)}")
        return None


def extract_score_from_string(score_str):
    """Extract numeric score from score string like '3/5'."""
    try:
        if '/' in score_str:
            numerator, denominator = score_str.split('/')
            return float(numerator), float(denominator)
        else:
            return float(score_str), 5.0  # Default denominator
    except (ValueError, AttributeError):
        return 0.0, 5.0


def calculate_average_score(results):
    """Calculate average score from evaluation results."""
    scores = []
    
    for result in results:
        evaluation = result.get("evaluation", {})
        summary = evaluation.get("evaluation_summary", {})
        score_str = summary.get("total_score", "0/5")
        
        numerator, _ = extract_score_from_string(score_str)
        scores.append(numerator)
    
    return sum(scores) / len(scores) if scores else 0.0


def print_evaluation_summary(result):
    """Print a formatted summary of an evaluation result."""
    if not result:
        print("No evaluation result to display")
        return
    
    evaluation = result.get("evaluation", {})
    summary = evaluation.get("evaluation_summary", {})
    
    print("=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Agent File: {os.path.basename(result.get('agent_filename', 'unknown'))}")
    print(f"Reference File: {os.path.basename(result.get('reference_filename', 'unknown'))}")
    print(f"Function: {summary.get('function_name', 'unknown')}")
    print(f"Total Score: {summary.get('total_score', 'unknown')}")
    print(f"Performance: {summary.get('overall_performance', 'unknown')}")
    print(f"Execution Time: {result.get('execution_time', 0):.2f} seconds")
    
    # Print detailed scores if available
    detailed_scores = evaluation.get("detailed_scores", {})
    if detailed_scores:
        print("\nDETAILED SCORES:")
        print("-" * 40)
        for criterion, details in detailed_scores.items():
            score = details.get("score", "unknown")
            level = details.get("level", "unknown")
            print(f"{criterion}: {score} ({level})")
    
    # Print improvement suggestions
    suggestions = evaluation.get("improvement_suggestions", [])
    if suggestions:
        print("\nIMPROVEMENT SUGGESTIONS:")
        print("-" * 40)
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")
    
    print("=" * 60)


def validate_evaluation_result(result):
    """Validate that an evaluation result has the expected structure."""
    required_fields = ["evaluation", "agent_json_path", "reference_md_path"]
    
    for field in required_fields:
        if field not in result:
            return False, f"Missing required field: {field}"
    
    evaluation = result.get("evaluation", {})
    if "evaluation_summary" not in evaluation:
        return False, "Missing evaluation_summary in evaluation"
    
    summary = evaluation.get("evaluation_summary", {})
    required_summary_fields = ["function_name", "total_score", "overall_performance"]
    
    for field in required_summary_fields:
        if field not in summary:
            return False, f"Missing required summary field: {field}"
    
    return True, "Validation passed"


def create_directory_if_not_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
        return True
    return False


def count_files_in_directory(directory, pattern="*"):
    """Count files matching pattern in directory."""
    import glob
    
    if not os.path.exists(directory):
        return 0
    
    search_pattern = os.path.join(directory, "**", pattern)
    files = glob.glob(search_pattern, recursive=True)
    return len(files)


def get_file_size_mb(file_path):
    """Get file size in MB."""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except OSError:
        return 0.0


def cleanup_old_results(results_dir, days_old=7):
    """Clean up evaluation results older than specified days."""
    import time
    
    if not os.path.exists(results_dir):
        return 0
    
    current_time = time.time()
    cutoff_time = current_time - (days_old * 24 * 60 * 60)
    
    cleaned_count = 0
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.getmtime(file_path) < cutoff_time:
                    os.remove(file_path)
                    cleaned_count += 1
            except OSError:
                pass
    
    return cleaned_count


if __name__ == "__main__":
    # Test utility functions
    print("Testing utility functions...")
    
    # Test timestamp formatting
    print(f"Current timestamp: {format_timestamp()}")
    
    # Test score extraction
    test_scores = ["3/5", "4.5/5", "2/5", "invalid"]
    for score in test_scores:
        num, denom = extract_score_from_string(score)
        print(f"Score '{score}' -> {num}/{denom}")
    
    print("Utility functions test completed!")
