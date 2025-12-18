"""
Batch processing for LLM Judge system.
Handles parallel evaluation of multiple agent responses using multiprocessing.
Adapted from generate_complexity_scenarios_using_inst.ipynb multiprocessing pattern.
"""

import os
import glob
import json
import time
import random
import multiprocessing
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

from claude_client import create_claude_client
from judge_evaluator import evaluate_agent_response, find_matching_reference_file
from config import PATH_CONFIG, BATCH_CONFIG


def evaluate_worker(agent_json_path, reference_md_path, output_dir, run_id):
    """
    Worker function for parallel evaluation.
    Creates its own Claude client to avoid sharing across processes.
    
    Args:
        agent_json_path: Path to agent JSON file
        reference_md_path: Path to reference markdown file  
        output_dir: Output directory for results
        run_id: Run identifier
    
    Returns:
        Tuple of (file_path, result)
    """
    try:
        # Create client for this worker process
        client = create_claude_client()
        if not client:
            raise Exception("Failed to create Claude client in worker process")
        
        # Perform evaluation
        result = evaluate_agent_response(
            agent_json_path, 
            reference_md_path, 
            client, 
            output_dir, 
            run_id
        )
        
        return agent_json_path, result
    
    except Exception as e:
        print(f"Worker error for {agent_json_path}: {str(e)}")
        return agent_json_path, None


def find_agent_files(agent_dir, file_pattern="*_track_order.json"):
    """
    Find all agent JSON files in the specified directory.
    
    Args:
        agent_dir: Directory containing agent response files
        file_pattern: Glob pattern to match agent files
        
    Returns:
        List of agent file paths
    """
    search_pattern = os.path.join(agent_dir, "**", file_pattern) #  "**": finding all files recursively
    agent_files = glob.glob(search_pattern, recursive=True)
    return agent_files


def create_evaluation_pairs(agent_files, reference_dir, agent_dir=None):
    """
    Create pairs of agent files and their matching reference files.
    
    Args:
        agent_files: List of agent JSON file paths
        reference_dir: Directory containing reference markdown files
        agent_dir: Directory containing agent files (for error type extraction)
        
    Returns:
        List of tuples (agent_file, reference_file)
    """
    pairs = []
    unmatched_files = []
    
    for agent_file in agent_files:
        reference_file = find_matching_reference_file(agent_file, reference_dir, agent_dir)
        if reference_file:
            pairs.append((agent_file, reference_file))
        else:
            unmatched_files.append(agent_file)
    
    print(f"Created {len(pairs)} evaluation pairs")
    if unmatched_files:
        print(f"Warning: {len(unmatched_files)} agent files could not be matched to reference files")
        for unmatched in unmatched_files[:5]:  # Show first 5 unmatched files
            print(f"  - {os.path.basename(unmatched)}")
        if len(unmatched_files) > 5:
            print(f"  ... and {len(unmatched_files) - 5} more")
    
    return pairs


def run_parallel_evaluation(evaluation_pairs, output_dir, max_workers=None, max_files=None, run_id=0):
    """
    Run evaluation in parallel using multiprocessing.
    Adapted from run_parallel_generation() in the notebook.
    
    Args:
        evaluation_pairs: List of (agent_file, reference_file) tuples
        output_dir: Output directory for results
        max_workers: Maximum number of worker processes
        max_files: Maximum number of files to process (for testing)
        run_id: Run identifier
        
    Returns:
        List of successful evaluation results
    """
    
    print(f"Starting parallel evaluation with {max_workers or 'auto'} workers...")
    
    if max_files is not None:
        # If max_files is specified, select a random subset
        if len(evaluation_pairs) > max_files:
            evaluation_pairs = random.sample(evaluation_pairs, max_files)
            print(f"Randomly selected {max_files} pairs for processing")
    
    if max_workers is None:
        max_workers = min(BATCH_CONFIG['max_workers'], multiprocessing.cpu_count())
    
    results = []
    total_pairs = len(evaluation_pairs)
    
    print(f"Processing {total_pairs} evaluation pairs with {max_workers} workers...")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_pair = {}
        for agent_file, reference_file in evaluation_pairs:
            future = executor.submit(
                evaluate_worker, 
                agent_file, 
                reference_file, 
                output_dir, 
                run_id
            )
            future_to_pair[future] = (agent_file, reference_file)
        
        # Process results as they complete
        completed = 0
        successful = 0
        failed = 0
        
        for future in tqdm(as_completed(future_to_pair), total=total_pairs, desc="Evaluating"):
            completed += 1
            
            try:
                file_path, result = future.result()
                if result:
                    results.append(result)
                    successful += 1
                else:
                    failed += 1
            except Exception as exc:
                agent_file, reference_file = future_to_pair[future]
                print(f"Evaluation failed for {os.path.basename(agent_file)}: {exc}")
                failed += 1
    
    print(f"\nBatch evaluation completed:")
    print(f"  - Total processed: {completed}")
    print(f"  - Successful: {successful}")
    print(f"  - Failed: {failed}")
    print(f"  - Success rate: {successful/completed*100:.1f}%")
    
    return results


def run_sequential_evaluation(evaluation_pairs, output_dir, max_files=None, run_id=0):
    """
    Run evaluation sequentially (for debugging or when multiprocessing causes issues).
    
    Args:
        evaluation_pairs: List of (agent_file, reference_file) tuples
        output_dir: Output directory for results
        max_files: Maximum number of files to process
        run_id: Run identifier
        
    Returns:
        List of successful evaluation results
    """
    
    print("Running sequential evaluation...")
    
    if max_files is not None and len(evaluation_pairs) > max_files:
        evaluation_pairs = random.sample(evaluation_pairs, max_files)
        print(f"Selected {max_files} pairs for processing")
    
    # Create single client for sequential processing
    client = create_claude_client()
    if not client:
        print("Failed to create Claude client for sequential evaluation")
        return []
    
    results = []
    total_pairs = len(evaluation_pairs)
    
    print(f"Processing {total_pairs} evaluation pairs sequentially...")
    os.makedirs(output_dir, exist_ok=True)
    
    successful = 0
    failed = 0
    
    for i, (agent_file, reference_file) in enumerate(tqdm(evaluation_pairs, desc="Evaluating")):
        try:
            result = evaluate_agent_response(
                agent_file, 
                reference_file, 
                client, 
                output_dir, 
                run_id
            )
            
            if result:
                results.append(result)
                successful += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"Error processing {os.path.basename(agent_file)}: {str(e)}")
            failed += 1
    
    print(f"\nSequential evaluation completed:")
    print(f"  - Total processed: {total_pairs}")
    print(f"  - Successful: {successful}")
    print(f"  - Failed: {failed}")
    print(f"  - Success rate: {successful/total_pairs*100:.1f}%")
    
    return results


def save_batch_summary(results, output_dir, run_id):
    """
    Save a summary of batch evaluation results.
    
    Args:
        results: List of evaluation result dictionaries
        output_dir: Output directory
        run_id: Run identifier
    """
    
    if not results:
        print("No results to summarize")
        return
    
    # Create summary data
    summary_data = []
    total_scores = []
    
    for result in results:
        evaluation = result.get("evaluation", {})
        evaluation_summary = evaluation.get("evaluation_summary", {})
        
        summary_record = {
            "agent_filename": result.get("agent_filename", "unknown"),
            "reference_filename": result.get("reference_filename", "unknown"),
            "function_name": evaluation_summary.get("function_name", "unknown"),
            "total_score": evaluation_summary.get("total_score", "0/5"),
            "overall_performance": evaluation_summary.get("overall_performance", "unknown"),
            "execution_time": result.get("execution_time", 0),
            "timestamp": result.get("timestamp", "unknown")
        }
        
        summary_data.append(summary_record)
        
        # Extract numeric score for statistics
        score_str = evaluation_summary.get("total_score", "0/5")
        try:
            score_num = float(score_str.split("/")[0])
            total_scores.append(score_num)
        except:
            total_scores.append(0)
    
    # Calculate statistics
    if total_scores:
        avg_score = sum(total_scores) / len(total_scores)
        min_score = min(total_scores)
        max_score = max(total_scores)
    else:
        avg_score = min_score = max_score = 0
    
    # Create summary report
    summary_report = {
        "batch_summary": {
            "run_id": run_id,
            "total_evaluations": len(results),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "statistics": {
                "average_score": round(avg_score, 2),
                "min_score": min_score,
                "max_score": max_score,
                "total_execution_time": sum(r.get("execution_time", 0) for r in results)
            }
        },
        "individual_results": summary_data
    }
    
    # Save summary
    summary_file = os.path.join(output_dir, f"batch_summary_run_{run_id}.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary_report, f, indent=2, ensure_ascii=False)
    
    print(f"Batch summary saved to: {summary_file}")
    print(f"Average score: {avg_score:.2f}/5")
    print(f"Score range: {min_score} - {max_score}")


if __name__ == "__main__":
    # Test batch processing
    print("Testing batch evaluation...")
    
    # Configuration
    agent_dir = PATH_CONFIG['agent_results_dir']
    reference_dir = PATH_CONFIG['reference_dir']
    output_dir = os.path.join(PATH_CONFIG['output_dir'], 'batch_test')
    
    # Find files and create pairs
    agent_files = find_agent_files(agent_dir)
    evaluation_pairs = create_evaluation_pairs(agent_files, reference_dir)
    
    if evaluation_pairs:
        # Run parallel evaluation (limited for testing)
        results = run_parallel_evaluation(
            evaluation_pairs, 
            output_dir, 
            max_workers=2, 
            max_files=2,  # Limit for testing
            run_id=0
        )
        
        # Save summary
        save_batch_summary(results, output_dir, 0)
        
        print("Batch evaluation test completed successfully!")
    else:
        print("No evaluation pairs found for testing.")
