"""
Statistics Analyzer for LLM Judge Results
Analyzes batch_summary files from multiple runs and generates comprehensive statistics.
python llm_judge_system/statistics_analyzer.py --pattern "test_with_uncertainties/TransactionEnv_transformed/turn_level_tf_*_adhoc+unclear_feature_limitation_*/track_order/"
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
import statistics
from typing import Dict, List, Tuple, Optional


def extract_metadata_from_path(path: str) -> Optional[Dict[str, str]]:
    """
    Extract metadata from path pattern:
    test_with_uncertainties/${ENV_DIR}/turn_level_tf_${model_config}_adhoc+unclear_${error_type}_${seed}/${func}/
    
    Returns:
        Dict with keys: env_dir, model_config, error_type, seed, func
    """
    # Normalize path separators
    path = path.replace('\\', '/')
    
    # Pattern to match the expected structure  
    # Updated to correctly parse error_type and seed
    # pattern = r'test_with_uncertainties/([^/]+)/turn_level_tf_([^_]+(?:_[^_]+)*)_adhoc\+unclear_(.+)_(s\d+)/([^/]+)/'
    pattern = r'results/([^/]+)/turn_level_tf_([^_]+(?:_[^_]+)*)_adhoc\+unclear_(.+)_(s\d+)/([^/]+)/'
    
    match = re.search(pattern, path)
    if match:
        return {
            'env_dir': match.group(1),
            'model_config': match.group(2), 
            'error_type': match.group(3),
            'seed': match.group(4),
            'func': match.group(5)
        }
    return None


def find_judge_results_paths(base_pattern: str) -> List[str]:
    """
    Find all paths matching the pattern that contain judge_results directories.
    
    Args:
        base_pattern: Glob pattern like "test_with_uncertainties/*/turn_level_tf_*_adhoc+unclear_*_*/*/"
    
    Returns:
        List of paths containing judge_results directories
    """
    # Find all matching paths
    all_paths = glob.glob(base_pattern, recursive=True)
    
    # Filter to only include paths with judge_results subdirectory
    valid_paths = []
    for path in all_paths:
        judge_results_path = os.path.join(path, 'judge_results')
        if os.path.exists(judge_results_path):
            valid_paths.append(path)
    
    return valid_paths


def collect_batch_summaries(judge_results_path: str) -> List[Dict]:
    """
    Collect all batch_summary_run_*.json files from a judge_results directory.
    
    Args:
        judge_results_path: Path to judge_results directory
    
    Returns:
        List of parsed batch summary dictionaries
    """
    summaries = []
    
    # Look for batch_summary files in run_* subdirectories
    run_pattern = os.path.join(judge_results_path, 'run_*', 'batch_summary_run_*.json')
    summary_files = glob.glob(run_pattern)
    
    # Also look for batch_summary files directly in judge_results
    direct_pattern = os.path.join(judge_results_path, 'batch_summary_run_*.json')
    summary_files.extend(glob.glob(direct_pattern))
    
    for summary_file in summary_files:
        try:
            with open(summary_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                summaries.append(data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not read {summary_file}: {e}")
    
    return summaries


def extract_scores_from_summaries(summaries: List[Dict]) -> List[float]:
    """
    Extract average scores from batch summary data.
    
    Args:
        summaries: List of batch summary dictionaries
    
    Returns:
        List of average scores (floats)
    """
    scores = []
    
    for summary in summaries:
        batch_summary = summary.get('batch_summary', {})
        stats = batch_summary.get('statistics', {})
        avg_score = stats.get('average_score', None)
        
        if avg_score is not None:
            scores.append(float(avg_score))
    
    return scores


def calculate_statistics(scores: List[float]) -> Dict[str, float]:
    """
    Calculate mean, standard deviation, and standard error from scores.
    
    Args:
        scores: List of scores
    
    Returns:
        Dict with 'mean', 'std', 'se', 'count'
    """
    if not scores:
        return {'mean': 0.0, 'std': 0.0, 'se': 0.0, 'count': 0}
    
    mean_val = statistics.mean(scores)
    std_val = statistics.stdev(scores) if len(scores) > 1 else 0.0
    se_val = std_val / (len(scores) ** 0.5) if len(scores) > 0 else 0.0
    
    return {
        'mean': mean_val,
        'std': std_val,
        'se': se_val,
        'count': len(scores)
    }


def analyze_patterns(patterns: List[str]) -> Dict[str, Dict]:
    """
    Analyze multiple patterns and collect statistics.
    
    Args:
        patterns: List of glob patterns to analyze
    
    Returns:
        Dict mapping condition keys to statistics
    """
    results = {}
    
    for pattern in patterns:
        print(f"Analyzing pattern: {pattern}")
        
        # Find paths with judge_results
        paths = find_judge_results_paths(pattern)
        print(f"Found {len(paths)} paths with judge_results")
        
        for path in paths:
            # Extract metadata from path
            metadata = extract_metadata_from_path(path)
            if not metadata:
                print(f"Warning: Could not parse metadata from {path}")
                continue
            
            # Create condition key
            condition_key = f"{metadata['env_dir']}_{metadata['model_config']}_{metadata['error_type']}_{metadata['func']}"
            
            # Collect batch summaries
            judge_results_path = os.path.join(path, 'judge_results')
            summaries = collect_batch_summaries(judge_results_path)
            
            if not summaries:
                print(f"Warning: No batch summaries found in {judge_results_path}")
                continue
            
            # Extract scores and calculate statistics
            scores = extract_scores_from_summaries(summaries)
            if scores:
                stats = calculate_statistics(scores)
                
                # Store results
                if condition_key not in results:
                    results[condition_key] = {
                        'metadata': metadata,
                        'all_scores': [],
                        'summary_files': []
                    }
                
                results[condition_key]['all_scores'].extend(scores)
                results[condition_key]['summary_files'].extend([f"{judge_results_path}/*.json"])
    
    # Calculate final statistics for each condition
    final_results = {}
    for condition_key, data in results.items():
        stats = calculate_statistics(data['all_scores'])
        final_results[condition_key] = {
            'metadata': data['metadata'],
            'statistics': stats,
            'raw_scores': data['all_scores']
        }
    
    return final_results


def aggregate_by_model_error_type(results: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Aggregate results by model-error type combination using Method 1 (File-level pooling).
    
    Args:
        results: Analysis results from analyze_patterns
        
    Returns:
        Dict mapping model-error type keys to aggregated statistics
    """
    aggregated = defaultdict(lambda: {
        'scores': [], 
        'functions': set(), 
        'environments': set(),
        'count_by_condition': 0
    })
    
    for condition_key, data in results.items():
        metadata = data['metadata']
        model = metadata['model_config'] 
        error_type = metadata['error_type']
        
        key = f"{model}_{error_type}"
        aggregated[key]['scores'].extend(data['raw_scores'])
        aggregated[key]['functions'].add(metadata['func'])
        aggregated[key]['environments'].add(metadata['env_dir'])
        aggregated[key]['count_by_condition'] += 1
        aggregated[key]['metadata'] = {
            'model_config': model, 
            'error_type': error_type
        }
    
    # Calculate final statistics for each aggregated condition
    final_aggregated = {}
    for key, data in aggregated.items():
        stats = calculate_statistics(data['scores'])
        final_aggregated[key] = {
            'metadata': data['metadata'],
            'statistics': stats,
            'functions': sorted(list(data['functions'])),
            'environments': sorted(list(data['environments'])),
            'condition_count': data['count_by_condition'],
            'raw_scores': data['scores'],
            'method': 'file_level_pooling'
        }
    
    return final_aggregated


def aggregate_by_model_error_type_method2(results: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Aggregate results by model-error type combination using Method 2 (Function-level averaging).
    
    Args:
        results: Analysis results from analyze_patterns
        
    Returns:
        Dict mapping model-error type keys to aggregated statistics
    """
    aggregated = defaultdict(lambda: {
        'function_means': [], 
        'functions': set(), 
        'environments': set(),
        'count_by_condition': 0,
        'all_scores': []
    })
    
    for condition_key, data in results.items():
        metadata = data['metadata']
        model = metadata['model_config'] 
        error_type = metadata['error_type']
        
        key = f"{model}_{error_type}"
        
        # Calculate mean for this specific condition (model-error-function-env combination)
        condition_mean = data['statistics']['mean']
        aggregated[key]['function_means'].append(condition_mean)
        aggregated[key]['functions'].add(metadata['func'])
        aggregated[key]['environments'].add(metadata['env_dir'])
        aggregated[key]['count_by_condition'] += 1
        aggregated[key]['all_scores'].extend(data['raw_scores'])  # Keep all scores for reference
        aggregated[key]['metadata'] = {
            'model_config': model, 
            'error_type': error_type
        }
    
    # Calculate final statistics for each aggregated condition using function means
    final_aggregated = {}
    for key, data in aggregated.items():
        stats = calculate_statistics(data['function_means'])
        final_aggregated[key] = {
            'metadata': data['metadata'],
            'statistics': stats,
            'functions': sorted(list(data['functions'])),
            'environments': sorted(list(data['environments'])),
            'condition_count': data['count_by_condition'],
            'raw_scores': data['all_scores'],  # All individual scores
            'function_means': data['function_means'],  # Function-level means used for aggregation
            'method': 'function_level_averaging'
        }
    
    return final_aggregated


def print_results_table(results: Dict[str, Dict]):
    """
    Print results in a formatted table with both detailed and aggregated views (Method 1 and Method 2).
    
    Args:
        results: Analysis results from analyze_patterns
    """
    if not results:
        print("No results to display.")
        return
    
    # Print detailed results first
    print("\n" + "="*140)
    print("DETAILED RESULTS (Individual Conditions)")
    print("="*140)
    
    # Table header
    header = f"{'Environment':<15} {'Model':<30} {'Function':<18} {'Error Type':<20} {'Mean±SE':<12} {'Count':<8}"
    print(header)
    print("-" * 140)
    
    # Sort results by environment, then function, then error type
    sorted_items = sorted(results.items(), key=lambda x: (
        x[1]['metadata']['env_dir'],
        x[1]['metadata']['func'], 
        x[1]['metadata']['error_type'],
        x[1]['metadata']['model_config']
    ))
    
    for condition_key, data in sorted_items:
        metadata = data['metadata']
        stats = data['statistics']
        
        env_display = metadata['env_dir'][:14]
        model_display = metadata['model_config'][:29]
        func_display = metadata['func'][:17]
        error_display = metadata['error_type'][:19]
        
        mean_se = f"{stats['mean']:.2f}±{stats['se']:.3f}"
        count = stats['count']
        
        row = f"{env_display:<15} {model_display:<30} {func_display:<18} {error_display:<20} {mean_se:<12} {count:<8}"
        print(row)
    
    print("="*140)
    
    # Print aggregated results - Method 1 (File-level pooling)
    aggregated_results_method1 = aggregate_by_model_error_type(results)
    
    print("\n" + "="*120)
    print("AGGREGATE RESULTS - Method 1 (File-level pooling)")
    print("="*120)
    
    # Aggregate table header
    agg_header = f"{'Model':<30} {'Error Type':<20} {'Mean±SE':<12} {'Count':<8} {'Conditions':<10} {'Functions':<30}"
    print(agg_header)
    print("-" * 120)
    
    # Sort aggregated results by model, then error type
    sorted_agg_items_method1 = sorted(aggregated_results_method1.items(), key=lambda x: (
        x[1]['metadata']['model_config'],
        x[1]['metadata']['error_type']
    ))
    
    for agg_key, agg_data in sorted_agg_items_method1:
        metadata = agg_data['metadata']
        stats = agg_data['statistics']
        
        model_display = metadata['model_config'][:29]
        error_display = metadata['error_type'][:19]
        mean_se = f"{stats['mean']:.2f}±{stats['se']:.3f}"
        count = stats['count']
        conditions = agg_data['condition_count']
        functions_str = ', '.join(agg_data['functions'][:2])  # Show first 2 functions
        if len(agg_data['functions']) > 2:
            functions_str += f", +{len(agg_data['functions'])-2}"
        functions_display = functions_str[:29]
        
        agg_row = f"{model_display:<30} {error_display:<20} {mean_se:<12} {count:<8} {conditions:<10} {functions_display:<30}"
        print(agg_row)
    
    print("="*120)
    
    # Print aggregated results - Method 2 (Function-level averaging)
    aggregated_results_method2 = aggregate_by_model_error_type_method2(results)
    
    print("\n" + "="*120)
    print("AGGREGATE RESULTS - Method 2 (Function-level averaging)")
    print("="*120)
    
    # Aggregate table header (same as method 1)
    print(agg_header)
    print("-" * 120)
    
    # Sort aggregated results by model, then error type
    sorted_agg_items_method2 = sorted(aggregated_results_method2.items(), key=lambda x: (
        x[1]['metadata']['model_config'],
        x[1]['metadata']['error_type']
    ))
    
    for agg_key, agg_data in sorted_agg_items_method2:
        metadata = agg_data['metadata']
        stats = agg_data['statistics']
        
        model_display = metadata['model_config'][:29]
        error_display = metadata['error_type'][:19]
        mean_se = f"{stats['mean']:.2f}±{stats['se']:.3f}"
        count = len(agg_data['function_means'])  # Number of function conditions averaged
        conditions = agg_data['condition_count']
        functions_str = ', '.join(agg_data['functions'][:2])  # Show first 2 functions
        if len(agg_data['functions']) > 2:
            functions_str += f", +{len(agg_data['functions'])-2}"
        functions_display = functions_str[:29]
        
        agg_row = f"{model_display:<30} {error_display:<20} {mean_se:<12} {count:<8} {conditions:<10} {functions_display:<30}"
        print(agg_row)
    
    print("="*120)
    
    # Summary statistics for both methods
    all_means = [data['statistics']['mean'] for data in results.values()]
    agg_means_method1 = [data['statistics']['mean'] for data in aggregated_results_method1.values()]
    agg_means_method2 = [data['statistics']['mean'] for data in aggregated_results_method2.values()]
    
    if all_means:
        overall_mean = statistics.mean(all_means)
        overall_std = statistics.stdev(all_means) if len(all_means) > 1 else 0.0
        
        agg_mean_method1 = statistics.mean(agg_means_method1) if agg_means_method1 else 0.0
        agg_std_method1 = statistics.stdev(agg_means_method1) if len(agg_means_method1) > 1 else 0.0
        
        agg_mean_method2 = statistics.mean(agg_means_method2) if agg_means_method2 else 0.0
        agg_std_method2 = statistics.stdev(agg_means_method2) if len(agg_means_method2) > 1 else 0.0
        
        print("\n" + "="*120)
        print("OVERALL STATISTICS")
        print("="*120)
        
        # Create formatted statistics table
        stats_header = f"{'Metric':<35} {'Detailed':<12} {'Method1':<12} {'Method2':<12}"
        print(stats_header)
        print("-" * 120)
        
        # Total conditions row
        total_row = f"{'Total Conditions':<35} {len(results):<12} {len(aggregated_results_method1):<12} {len(aggregated_results_method2):<12}"
        print(total_row)
        
        # Overall mean row
        mean_row = f"{'Overall Mean':<35} {overall_mean:.3f}".ljust(47) + f"{agg_mean_method1:.3f}".ljust(12) + f"{agg_mean_method2:.3f}"
        print(mean_row)
        
        # Overall std row
        std_row = f"{'Overall Std':<35} {overall_std:.3f}".ljust(47) + f"{agg_std_method1:.3f}".ljust(12) + f"{agg_std_method2:.3f}"
        print(std_row)
        
        # Min mean row
        if agg_means_method1 and agg_means_method2:
            min_row = f"{'Min Mean':<35} {min(all_means):.3f}".ljust(47) + f"{min(agg_means_method1):.3f}".ljust(12) + f"{min(agg_means_method2):.3f}"
            print(min_row)
            
            # Max mean row
            max_row = f"{'Max Mean':<35} {max(all_means):.3f}".ljust(47) + f"{max(agg_means_method1):.3f}".ljust(12) + f"{max(agg_means_method2):.3f}"
            print(max_row)
        
        print("="*120)
    
    print("\n")


def save_csv_results(results: Dict[str, Dict], output_file: str):
    """
    Save results to unified CSV file with detailed and both aggregated methods using section dividers.
    """
    # Ensure reports directory exists
    reports_dir = os.path.dirname(output_file)
    if reports_dir and not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Create unified filename
    base_name = output_file.replace('.csv', '')
    unified_file = f"{base_name}_unified.csv"
    
    # Get aggregated results for both methods
    aggregated_results_method1 = aggregate_by_model_error_type(results)
    aggregated_results_method2 = aggregate_by_model_error_type_method2(results)
    
    with open(unified_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Section 1: Detailed Results
        writer.writerow(['=== DETAILED RESULTS ==='])
        writer.writerow(['Environment', 'Model', 'Function', 'Error_Type', 'Seed', 'Mean±SE', 'Count'])
        
        # Sort detailed results
        sorted_items = sorted(results.items(), key=lambda x: (
            x[1]['metadata']['env_dir'],
            x[1]['metadata']['func'], 
            x[1]['metadata']['error_type'],
            x[1]['metadata']['model_config']
        ))
        
        for condition_key, data in sorted_items:
            metadata = data['metadata']
            stats = data['statistics']
            mean_se = f"{stats['mean']:.2f}±{stats['se']:.3f}"
            
            writer.writerow([
                metadata['env_dir'],
                metadata['model_config'],
                metadata['func'],
                metadata['error_type'],
                metadata['seed'],
                mean_se,
                stats['count']
            ])
        
        # Empty row for separation
        writer.writerow([])
        
        # Section 2: Aggregate Method 1 (File-level pooling)
        writer.writerow(['=== AGGREGATE METHOD 1 (File-level pooling) ==='])
        writer.writerow(['Model', 'Error_Type', 'Mean±SE', 'Count', 'Conditions', 'Functions'])
        
        sorted_agg_items_method1 = sorted(aggregated_results_method1.items(), key=lambda x: (
            x[1]['metadata']['model_config'],
            x[1]['metadata']['error_type']
        ))
        
        for agg_key, agg_data in sorted_agg_items_method1:
            metadata = agg_data['metadata']
            stats = agg_data['statistics']
            mean_se = f"{stats['mean']:.2f}±{stats['se']:.3f}"
            functions_str = '; '.join(agg_data['functions'])
            
            writer.writerow([
                metadata['model_config'],
                metadata['error_type'],
                mean_se,
                stats['count'],
                agg_data['condition_count'],
                functions_str
            ])
        
        # Empty row for separation
        writer.writerow([])
        
        # Section 3: Aggregate Method 2 (Function-level averaging)  
        writer.writerow(['=== AGGREGATE METHOD 2 (Function-level averaging) ==='])
        writer.writerow(['Model', 'Error_Type', 'Mean±SE', 'Count', 'Conditions', 'Functions'])
        
        sorted_agg_items_method2 = sorted(aggregated_results_method2.items(), key=lambda x: (
            x[1]['metadata']['model_config'],
            x[1]['metadata']['error_type']
        ))
        
        for agg_key, agg_data in sorted_agg_items_method2:
            metadata = agg_data['metadata']
            stats = agg_data['statistics']
            mean_se = f"{stats['mean']:.2f}±{stats['se']:.3f}"
            functions_str = '; '.join(agg_data['functions'])
            
            writer.writerow([
                metadata['model_config'],
                metadata['error_type'],
                mean_se,
                len(agg_data['function_means']),  # Number of function conditions averaged
                agg_data['condition_count'],
                functions_str
            ])
        
        # Empty row for separation
        writer.writerow([])
        
        # Section 4: Overall Statistics
        writer.writerow(['=== OVERALL STATISTICS ==='])
        writer.writerow(['Metric', 'Detailed_Results', 'Method1_File_Pooling', 'Method2_Function_Averaging'])
        
        # Calculate statistics for all methods
        all_means = [data['statistics']['mean'] for data in results.values()]
        agg_means_method1 = [data['statistics']['mean'] for data in aggregated_results_method1.values()]
        agg_means_method2 = [data['statistics']['mean'] for data in aggregated_results_method2.values()]
        
        if all_means:
            overall_mean = statistics.mean(all_means)
            overall_std = statistics.stdev(all_means) if len(all_means) > 1 else 0.0
            
            agg_mean_method1 = statistics.mean(agg_means_method1) if agg_means_method1 else 0.0
            agg_std_method1 = statistics.stdev(agg_means_method1) if len(agg_means_method1) > 1 else 0.0
            
            agg_mean_method2 = statistics.mean(agg_means_method2) if agg_means_method2 else 0.0
            agg_std_method2 = statistics.stdev(agg_means_method2) if len(agg_means_method2) > 1 else 0.0
            
            # Write statistics rows
            writer.writerow(['Total_Conditions', len(results), len(aggregated_results_method1), len(aggregated_results_method2)])
            writer.writerow(['Overall_Mean', f"{overall_mean:.3f}", f"{agg_mean_method1:.3f}", f"{agg_mean_method2:.3f}"])
            writer.writerow(['Overall_Std', f"{overall_std:.3f}", f"{agg_std_method1:.3f}", f"{agg_std_method2:.3f}"])
            writer.writerow(['Min_Mean', f"{min(all_means):.3f}", f"{min(agg_means_method1):.3f}" if agg_means_method1 else "0.000", f"{min(agg_means_method2):.3f}" if agg_means_method2 else "0.000"])
            writer.writerow(['Max_Mean', f"{max(all_means):.3f}", f"{max(agg_means_method1):.3f}" if agg_means_method1 else "0.000", f"{max(agg_means_method2):.3f}" if agg_means_method2 else "0.000"])
    
    print(f"Unified CSV results saved to: {unified_file}")


def save_detailed_results(results: Dict[str, Dict], output_file: str):
    """
    Save detailed results to JSON file with both detailed and aggregated results.
    """
    # Ensure reports directory exists
    reports_dir = os.path.dirname(output_file)
    if reports_dir and not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Generate formatted table string
    table_summary = generate_table_string(results)
    
    # Get aggregated results
    aggregated_results = aggregate_by_model_error_type(results)
    
    # Convert to serializable format with table summary
    output_data = {
        'table_summary': table_summary,
        'detailed_results': {},
        'aggregated_results': {}
    }
    
    # Add detailed results
    for key, data in results.items():
        output_data['detailed_results'][key] = {
            'metadata': data['metadata'],
            'statistics': data['statistics'],
            'raw_scores': data['raw_scores']
        }
    
    # Add aggregated results
    for key, data in aggregated_results.items():
        output_data['aggregated_results'][key] = {
            'metadata': data['metadata'],
            'statistics': data['statistics'],
            'functions': data['functions'],
            'environments': data['environments'],
            'condition_count': data['condition_count'],
            'raw_scores': data['raw_scores']
        }
    
    # Add overall statistics
    all_means = [data['statistics']['mean'] for data in results.values()]
    agg_means = [data['statistics']['mean'] for data in aggregated_results.values()]
    
    if all_means:
        overall_mean = statistics.mean(all_means)
        overall_std = statistics.stdev(all_means) if len(all_means) > 1 else 0.0
        agg_mean = statistics.mean(agg_means) if agg_means else 0.0
        agg_std = statistics.stdev(agg_means) if len(agg_means) > 1 else 0.0
        
        output_data['overall_statistics'] = {
            'detailed': {
                'total_conditions': len(results),
                'overall_mean': overall_mean,
                'overall_std': overall_std,
                'min_mean': min(all_means),
                'max_mean': max(all_means)
            },
            'aggregated': {
                'total_model_error_combinations': len(aggregated_results),
                'aggregate_mean': agg_mean,
                'aggregate_std': agg_std,
                'min_aggregate_mean': min(agg_means) if agg_means else 0.0,
                'max_aggregate_mean': max(agg_means) if agg_means else 0.0
            }
        }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Results with both detailed and aggregated data saved to: {output_file}")


def generate_table_string(results: Dict[str, Dict]) -> str:
    """
    Generate formatted table string from results.
    """
    if not results:
        return "No results to display."
    
    lines = []
    lines.append("=" * 140)
    lines.append("LLM JUDGE STATISTICS SUMMARY")
    lines.append("=" * 140)
    
    # Table header
    header = f"{'Environment':<15} {'Model':<30} {'Function':<18} {'Error Type':<20} {'Mean±SE':<12} {'Count':<8}"
    lines.append(header)
    lines.append("-" * 140)
    
    # Sort results by environment, then function, then error type
    sorted_items = sorted(results.items(), key=lambda x: (
        x[1]['metadata']['env_dir'],
        x[1]['metadata']['func'], 
        x[1]['metadata']['error_type'],
        x[1]['metadata']['model_config']
    ))
    
    for condition_key, data in sorted_items:
        metadata = data['metadata']
        stats = data['statistics']
        
        env_display = metadata['env_dir'][:14]
        model_display = metadata['model_config'][:29]
        func_display = metadata['func'][:17]
        error_display = metadata['error_type'][:19]
        
        mean_se = f"{stats['mean']:.2f}±{stats['se']:.3f}"
        count = stats['count']
        
        row = f"{env_display:<15} {model_display:<30} {func_display:<18} {error_display:<20} {mean_se:<12} {count:<8}"
        lines.append(row)
    
    lines.append("=" * 140)
    
    # Summary statistics
    all_means = [data['statistics']['mean'] for data in results.values()]
    if all_means:
        overall_mean = statistics.mean(all_means)
        overall_std = statistics.stdev(all_means) if len(all_means) > 1 else 0.0
        lines.append("")
        lines.append("OVERALL STATISTICS:")
        lines.append(f"Total Conditions: {len(results)}")
        lines.append(f"Overall Mean: {overall_mean:.3f}")
        lines.append(f"Overall Std: {overall_std:.3f}")
        lines.append(f"Min Mean: {min(all_means):.3f}")
        lines.append(f"Max Mean: {max(all_means):.3f}")
    
    return "\n".join(lines)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze LLM Judge batch summary statistics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all results for a specific environment
  python statistics_analyzer.py --pattern "test_with_uncertainties/TransactionEnv/turn_level_tf_*_adhoc+unclear_*_*/*/"
  
  # Analyze specific function across all conditions
  python statistics_analyzer.py --pattern "test_with_uncertainties/*/turn_level_tf_*_adhoc+unclear_*_*/track_order/"
  
  # Analyze multiple patterns
  python statistics_analyzer.py --patterns \\
    "test_with_uncertainties/*/turn_level_tf_*_adhoc+unclear_feature_limitation_*/*/" \\
    "test_with_uncertainties/*/turn_level_tf_*_adhoc+unclear_system_failure_*/*/"
  
  # Save detailed results
  python statistics_analyzer.py --pattern "test_with_uncertainties/*/*/" --output results.json
        """
    )
    
    parser.add_argument('--pattern', type=str,
                       help='Single glob pattern to analyze')
    parser.add_argument('--patterns', nargs='+',
                       help='Multiple glob patterns to analyze')
    parser.add_argument('--output', type=str,
                       help='Output file for detailed JSON results')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Determine patterns to analyze
    if args.patterns:
        patterns = args.patterns
    elif args.pattern:
        patterns = [args.pattern]
    else:
        # Default pattern
        patterns = ["test_with_uncertainties/*/turn_level_tf_*_adhoc+unclear_*_*/*/"]
        print("No pattern specified, using default pattern for all conditions")
    
    # Analyze patterns
    results = analyze_patterns(patterns)
    
    # Print results table
    print_results_table(results)
    
    # Save detailed results if requested
    if args.output:
        # Determine file format based on extension
        if args.output.endswith('.csv'):
            save_csv_results(results, args.output)
        else:
            # Default to JSON for backward compatibility
            save_detailed_results(results, args.output)
    else:
        # Generate default CSV file in reports directory
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_csv_file = f"reports/llm_judge_statistics_{timestamp}.csv"
        save_csv_results(results, default_csv_file)
    
    if args.verbose:
        print(f"\nProcessed {len(results)} conditions:")
        for key in sorted(results.keys()):
            print(f"  - {key}")


if __name__ == "__main__":
    main()
