"""
Configuration settings for LLM Judge system.
"""

import os

# Base directory setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # llm_judge_system/
EVAL_MOCK_API_REAL_DIR = os.path.dirname(BASE_DIR)     # eval_mock_API_Real/

# Path configuration
PATH_CONFIG = {
    'base_dir': BASE_DIR,
    'eval_mock_api_real_dir': EVAL_MOCK_API_REAL_DIR,
    'agent_results_dir': os.path.join(EVAL_MOCK_API_REAL_DIR, 'turn_level_tf_results'),
    'reference_dir': os.path.join(EVAL_MOCK_API_REAL_DIR, 'function_uncertainty_references'),
    'output_dir': os.path.join(EVAL_MOCK_API_REAL_DIR, 'judge_results')
}

# Claude API configuration
CLAUDE_CONFIG = {
    'model': 'us.anthropic.claude-opus-4-20250514-v1:0',  # Use Claude Opus for evaluation
    'temperature': 0.1,  # Low temperature for consistent evaluation
    'max_tokens': 2000,  # Sufficient for detailed JSON evaluation
    'region': 'us-east-1',  # AWS Bedrock region
    'max_retries': 10000
}

# Evaluation configuration
EVALUATION_CONFIG = {
    'enforce_scoring': True,
    'require_evidence': True,
    'min_reasoning_length': 50,
    'output_format': 'json',
    'validate_json_output': True
}

# Batch processing configuration
BATCH_CONFIG = {
    'max_workers': 50,  # Maximum number of parallel processes
    'default_run_id': 0,
    'retry_failed': True,
    'save_intermediate_results': True
}

# File patterns for matching agent and reference files
FILE_PATTERNS = {
    'agent_json_pattern': '*_track_order.json',
    'reference_md_pattern': '*_error.md',
    'supported_functions': ['track_order', 'get_messages'],
    'supported_uncertainty_types': ['feature_limitation_error', 'system_failure_error', 
                                  'informational_notice', 'partially_irrelevant_information']
}

# Logging configuration
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_file': os.path.join(PATH_CONFIG['output_dir'], 'llm_judge.log')
}


def create_output_directories():
    """Create necessary output directories if they don't exist."""
    dirs_to_create = [
        PATH_CONFIG['output_dir'],
        os.path.join(PATH_CONFIG['output_dir'], 'single_evaluations'),
        os.path.join(PATH_CONFIG['output_dir'], 'batch_evaluations'),
        os.path.join(PATH_CONFIG['output_dir'], 'logs')
    ]
    
    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")


def get_config_summary():
    """Print configuration summary for debugging."""
    print("=== LLM Judge System Configuration ===")
    print(f"Base Directory: {PATH_CONFIG['base_dir']}")
    print(f"Eval Mock API Real Directory: {PATH_CONFIG['eval_mock_api_real_dir']}")
    print(f"Agent Results Directory: {PATH_CONFIG['agent_results_dir']}")
    print(f"Reference Directory: {PATH_CONFIG['reference_dir']}")
    print(f"Output Directory: {PATH_CONFIG['output_dir']}")
    print(f"Claude Model: {CLAUDE_CONFIG['model']}")
    print(f"Max Workers: {BATCH_CONFIG['max_workers']}")
    print("=" * 50)


def validate_config():
    """Validate that all required directories exist."""
    required_dirs = [
        PATH_CONFIG['eval_mock_api_real_dir'],
        PATH_CONFIG['agent_results_dir'],
        PATH_CONFIG['reference_dir']
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print("ERROR: Missing required directories:")
        for dir_path in missing_dirs:
            print(f"  - {dir_path}")
        return False
    
    print("Configuration validation passed.")
    return True


if __name__ == "__main__":
    get_config_summary()
    validate_config()
    create_output_directories()
