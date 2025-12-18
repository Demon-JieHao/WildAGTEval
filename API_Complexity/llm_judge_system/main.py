"""
Main CLI interface for LLM Judge system.
Provides command-line access to single and batch evaluation capabilities.
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from claude_client import create_claude_client
from judge_evaluator import evaluate_agent_response, evaluate_single_file_with_auto_matching
from batch_judge import (
    find_agent_files, 
    create_evaluation_pairs, 
    run_parallel_evaluation, 
    run_sequential_evaluation,
    save_batch_summary
)
from config import PATH_CONFIG, BATCH_CONFIG, get_config_summary, validate_config, create_output_directories


def single_evaluation_mode(args):
    """Handle single file evaluation."""
    print("=== Single Evaluation Mode ===")
    
    # Validate input files
    if not os.path.exists(args.agent_json):
        print(f"Error: Agent JSON file not found: {args.agent_json}")
        return False
    
    if args.reference_md and not os.path.exists(args.reference_md):
        print(f"Error: Reference markdown file not found: {args.reference_md}")
        return False
    
    # Create Claude client
    print("Creating Claude client...")
    client = create_claude_client()
    if not client:
        print("Failed to create Claude client. Please check your credentials.")
        return False
    
    # Prepare output directory
    output_dir = os.path.dirname(args.output) if args.output else PATH_CONFIG['output_dir']
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        if args.reference_md:
            # Manual reference file specified
            print(f"Evaluating: {args.agent_json}")
            print(f"Reference: {args.reference_md}")
            
            result = evaluate_agent_response(
                args.agent_json,
                args.reference_md,
                client,
                output_dir,
                args.run_id
            )
        else:
            # Auto-match reference file
            print(f"Auto-matching reference file for: {args.agent_json}")
            
            result = evaluate_single_file_with_auto_matching(
                args.agent_json,
                client,
                output_dir,
                args.run_id
            )
        
        if result:
            print("Single evaluation completed successfully!")
            
            # Print summary
            evaluation = result.get("evaluation", {})
            summary = evaluation.get("evaluation_summary", {})
            print(f"Function: {summary.get('function_name', 'unknown')}")
            print(f"Total Score: {summary.get('total_score', 'unknown')}")
            print(f"Performance: {summary.get('overall_performance', 'unknown')}")
            print(f"Execution Time: {result.get('execution_time', 0):.2f} seconds")
            
            return True
        else:
            print("Single evaluation failed!")
            return False
            
    except Exception as e:
        print(f"Error during single evaluation: {str(e)}")
        return False


def batch_evaluation_mode(args):
    """Handle batch evaluation mode."""
    print("=== Batch Evaluation Mode ===")
    
    # Validate directories
    if not os.path.exists(args.agent_dir):
        print(f"Error: Agent directory not found: {args.agent_dir}")
        return False
    
    reference_dir = args.reference_dir or PATH_CONFIG['reference_dir']
    if not os.path.exists(reference_dir):
        print(f"Error: Reference directory not found: {reference_dir}")
        return False
    
    # Find agent files
    print(f"Scanning for agent files in: {args.agent_dir}")
    agent_files = find_agent_files(args.agent_dir, args.file_pattern)
    
    if not agent_files:
        print("No agent files found matching the pattern!")
        return False
    
    # Create evaluation pairs
    print("Creating evaluation pairs...")
    evaluation_pairs = create_evaluation_pairs(agent_files, reference_dir, args.agent_dir)
    
    if not evaluation_pairs:
        print("No valid evaluation pairs found!")
        return False
    
    # Prepare output directory
    output_dir = args.output_dir or os.path.join(PATH_CONFIG['output_dir'], f'batch_run_{args.run_id}')
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Output directory: {output_dir}")
    
    # Run evaluation
    start_time = time.time()
    
    try:
        if args.sequential:
            print("Running sequential evaluation...")
            results = run_sequential_evaluation(
                evaluation_pairs,
                output_dir,
                args.max_files,
                args.run_id
            )
        else:
            print("Running parallel evaluation...")
            results = run_parallel_evaluation(
                evaluation_pairs,
                output_dir,
                args.max_workers,
                args.max_files,
                args.run_id
            )
        
        end_time = time.time()
        
        # Save batch summary
        print("Generating batch summary...")
        save_batch_summary(results, output_dir, args.run_id)
        
        # Print final statistics
        print(f"\n=== Batch Evaluation Summary ===")
        print(f"Total evaluation pairs: {len(evaluation_pairs)}")
        print(f"Successful evaluations: {len(results)}")
        print(f"Total execution time: {end_time - start_time:.2f} seconds")
        print(f"Average time per evaluation: {(end_time - start_time) / len(evaluation_pairs):.2f} seconds")
        print(f"Results saved to: {output_dir}")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"Error during batch evaluation: {str(e)}")
        return False


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LLM Judge System - Evaluate agent responses against reference criteria",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single evaluation with auto-matching
  python main.py --agent_json path/to/agent.json --output results.json
  
  # Single evaluation with manual reference
  python main.py --agent_json path/to/agent.json --reference_md path/to/reference.md
  
  # Batch evaluation
  python main.py --batch --agent_dir path/to/agents/ --output_dir path/to/results/
  
  # Batch evaluation with limits
  python main.py --batch --agent_dir path/to/agents/ --max_files 10 --max_workers 4
        """
    )
    
    # Mode selection
    parser.add_argument('--batch', action='store_true',
                       help='Run in batch evaluation mode')
    
    # Single evaluation arguments
    parser.add_argument('--agent_json', type=str,
                       help='Path to agent response JSON file (single mode)')
    parser.add_argument('--reference_md', type=str,
                       help='Path to reference markdown file (optional, auto-match if not provided)')
    parser.add_argument('--output', type=str,
                       help='Output file path (single mode)')
    
    # Batch evaluation arguments
    parser.add_argument('--agent_dir', type=str,
                       help='Directory containing agent response files (batch mode)')
    parser.add_argument('--reference_dir', type=str,
                       help='Directory containing reference markdown files (batch mode)')
    parser.add_argument('--output_dir', type=str,
                       help='Output directory for batch results (batch mode)')
    
    # Processing options
    parser.add_argument('--file_pattern', type=str, default='*_track_order.json',
                       help='File pattern to match agent files (default: *_track_order.json)')
    parser.add_argument('--max_files', type=int,
                       help='Maximum number of files to process (for testing)')
    parser.add_argument('--max_workers', type=int, default=BATCH_CONFIG['max_workers'],
                       help=f'Maximum number of parallel workers (default: {BATCH_CONFIG["max_workers"]})')
    parser.add_argument('--sequential', action='store_true',
                       help='Run evaluations sequentially instead of in parallel')
    
    # General options
    parser.add_argument('--run_id', type=int, default=0,
                       help='Run identifier for tracking multiple runs (default: 0)')
    parser.add_argument('--config', action='store_true',
                       help='Show configuration and exit')
    parser.add_argument('--setup', action='store_true',
                       help='Create output directories and exit')
    
    args = parser.parse_args()
    print(args)
    
    # Handle special modes
    if args.config:
        get_config_summary()
        return 0
    
    if args.setup:
        create_output_directories()
        return 0
    
    # Validate configuration
    print("Validating configuration...")
    if not validate_config():
        print("Configuration validation failed!")
        return 1
    
    # Create output directories
    create_output_directories()
    
    # Determine mode and run
    if args.batch:
        # Batch evaluation mode
        if not args.agent_dir:
            print("Error: --agent_dir is required for batch mode")
            return 1
        
        success = batch_evaluation_mode(args)
        
    else:
        # Single evaluation mode
        if not args.agent_json:
            print("Error: --agent_json is required for single evaluation mode")
            return 1
        
        success = single_evaluation_mode(args)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
