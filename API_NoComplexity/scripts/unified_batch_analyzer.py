"""
Unified Batch Analysis Statistics Analyzer
Analyzes unified_batch_summary.txt files from multiple analysis directories and generates comprehensive statistics.

python scripts/unified_batch_analyzer.py --pattern "test_with_uncertainties/TransactionEnv_transformed/*_analysis/"

"""

import argparse
import csv
import glob
import os
import re
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional


def parse_basic_structure(path: str) -> Dict:
    """
    Parse basic path structure.
    
    Args:
        path: Path like test_with_uncertainties/TransactionEnv_transformed/dirname_analysis/
    
    Returns:
        Dict with basic path components
    """
    # Normalize path separators
    path = path.replace('\\', '/')
    parts = path.strip('/').split('/')
    
    if len(parts) < 3:
        return {}
    
    return {
        'env_dir': parts[4] if len(parts) > 1 else '',
        'analysis_dir': parts[5] if len(parts) > 2 else '',
        'full_path': path
    }


def check_turn_level_tf(dirname: str) -> bool:
    """Check if directory name contains turn_level_tf_ prefix."""
    return dirname.startswith('turn_level_tf_')


def check_adhoc_eval(dirname: str) -> bool:
    """Check if directory name contains _AdhocEval_."""
    return '_AdhocEval_' in dirname


def check_complexity_enabled(dirname: str) -> bool:
    """Check if complexity is enabled (no _uncOFF suffix)."""
    return '_uncOFF_' not in dirname


def extract_trg_type(dirname: str) -> str:
    """Extract TRG type from directory name (e.g., s1_unclearTRG -> 'unclear')."""
    import re
    # Look for pattern like s0_unclearTRG, s1_adhocTRG, s2_infonoticeTRG
    match = re.search(r's\d+_(\w+)TRG', dirname)
    if match:
        return match.group(1)  # unclear, adhoc, infonotice, irrelevant, etc.
    return 'None'


def extract_adhoc_type(dirname: str) -> str:
    """Extract adhoc type (adhoc+unclear vs adhoc)."""
    if '_adhoc+unclear_' in dirname:
        return 'adhoc+unclear'
    elif '_adhoc_' in dirname:
        return 'adhoc'
    return 'unknown'


def extract_model_and_details(dirname: str) -> Dict:
    """
    Extract model name and other details from directory name.
    
    Args:
        dirname: Directory name like 'turn_level_tf_ambersontest_adhoc_none_s1_unclearTRG_analysis'
    
    Returns:
        Dict with model, uncertainty_type, seed
    """
    # Remove optional prefixes and suffixes
    cleaned = dirname
    if cleaned.startswith('turn_level_tf_'):
        cleaned = cleaned[len('turn_level_tf_'):]
    if cleaned.endswith('_analysis'):
        cleaned = cleaned[:-len('_analysis')]
    
    # Remove _AdhocEval_ and _uncOFF_ patterns if present
    cleaned = cleaned.replace('_AdhocEval_', '_')
    cleaned = cleaned.replace('_uncOFF_', '_')
    
    # Remove TRG patterns but keep seed (e.g., s1_unclearTRG -> s1)
    # Pattern should match: seed followed by TRG type
    cleaned = re.sub(r'(s\d+)_\w+TRG$', r'\1', cleaned)
    
    # Split by underscores and try to identify parts
    parts = cleaned.split('_')
    
    result = {
        'model': 'unknown',
        'uncertainty_type': 'unknown', 
        'seed': 'unknown'
    }
    
    # Look for seed (s0, s1, s2, etc.)
    seed_idx = -1
    for i, part in enumerate(parts):
        if re.match(r's\d+', part):
            result['seed'] = part
            seed_idx = i
            break
    
    # Find adhoc type position
    adhoc_end_idx = -1
    for j, p in enumerate(parts):
        if p in ['adhoc', 'adhoc+unclear']:
            adhoc_end_idx = j
            break
    
    # Extract uncertainty type (between adhoc and seed)
    if adhoc_end_idx >= 0 and seed_idx > adhoc_end_idx + 1:
        # Join all parts between adhoc type and seed
        uncertainty_parts = parts[adhoc_end_idx + 1:seed_idx]
        result['uncertainty_type'] = '_'.join(uncertainty_parts)
    elif seed_idx > 0 and adhoc_end_idx >= 0:
        # If seed is right after adhoc, no uncertainty type
        if seed_idx == adhoc_end_idx + 1:
            result['uncertainty_type'] = 'none'
        else:
            result['uncertainty_type'] = parts[seed_idx - 1]
    elif seed_idx > 0:
        # Fallback: take the part right before seed
        result['uncertainty_type'] = parts[seed_idx - 1]
    
    # Model should be everything before adhoc
    if adhoc_end_idx > 0:
        result['model'] = '_'.join(parts[:adhoc_end_idx])
    elif len(parts) > 0:
        # Fallback: take first part as model
        result['model'] = parts[0]
    
    return result


def extract_metadata_from_path(path: str) -> Optional[Dict[str, str]]:
    """
    Extract metadata from analysis directory path.
    
    Args:
        path: Path like test_with_uncertainties/TransactionEnv_transformed/dirname_analysis/
    
    Returns:
        Dict with metadata or None if parsing fails
    """
    basic = parse_basic_structure(path)
    if not basic or not basic['analysis_dir']:
        return None
    
    dirname = basic['analysis_dir']
    details = extract_model_and_details(dirname)
    
    return {
        'env_dir': basic['env_dir'],
        'has_turn_level_tf': check_turn_level_tf(dirname),
        'has_adhoc_eval': check_adhoc_eval(dirname),
        'has_complexity_enabled': check_complexity_enabled(dirname),
        'trg_type': extract_trg_type(dirname),
        'adhoc_type': extract_adhoc_type(dirname),
        'model_config': details['model'],
        'uncertainty_type': details['uncertainty_type'],
        'seed': details['seed']
    }


def find_analysis_paths(base_pattern: str) -> List[str]:
    """
    Find all paths matching the pattern that contain unified_batch_summary.txt files.
    
    Args:
        base_pattern: Glob pattern like "test_with_uncertainties/TransactionEnv_transformed/*_analysis/"
    
    Returns:
        List of paths containing unified_batch_summary.txt files
    """
    # Find all matching paths
    all_paths = glob.glob(base_pattern, recursive=True)
    
    # Filter to only include paths with unified_batch_summary.txt
    valid_paths = []
    for path in all_paths:
        summary_file = os.path.join(path, 'unified_batch_summary.txt')
        if os.path.exists(summary_file):
            valid_paths.append(path)
    
    return valid_paths


def extract_success_rate_from_summary(file_path: str) -> Optional[float]:
    """
    Extract success rate from unified_batch_summary.txt file.
    
    Args:
        file_path: Path to unified_batch_summary.txt file
    
    Returns:
        Success rate as float or None if not found
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Look for "Success Rate: XX.X%" pattern
        match = re.search(r'Success Rate:\s*([\d.]+)%', content)
        if match:
            return float(match.group(1))
    except (FileNotFoundError, ValueError) as e:
        print(f"Warning: Could not read success rate from {file_path}: {e}")
    
    return None


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
        
        # Find paths with unified_batch_summary.txt
        paths = find_analysis_paths(pattern)
        print(f"Found {len(paths)} paths with unified_batch_summary.txt")
        
        for path in paths:
            # Extract metadata from path
            metadata = extract_metadata_from_path(path)
            if not metadata:
                print(f"Warning: Could not parse metadata from {path}")
                continue
            
            # Create condition key
            condition_key = f"{metadata['env_dir']}_{metadata['model_config']}_{metadata['adhoc_type']}_{metadata['uncertainty_type']}"
            if metadata['has_turn_level_tf']:
                condition_key = f"TF_{condition_key}"
            if metadata['has_adhoc_eval']:
                condition_key = f"{condition_key}_AdhocEval"
            if not metadata['has_complexity_enabled']:
                condition_key = f"{condition_key}_uncOFF"
            if metadata['trg_type'] != 'None':
                condition_key = f"{condition_key}_{metadata['trg_type']}TRG"
            
            # Read success rate from unified_batch_summary.txt
            summary_file = os.path.join(path, 'unified_batch_summary.txt')
            success_rate = extract_success_rate_from_summary(summary_file)
            
            if success_rate is None:
                print(f"Warning: No success rate found in {summary_file}")
                continue
            
            # Store results
            if condition_key not in results:
                results[condition_key] = {
                    'metadata': metadata,
                    'all_scores': [],
                    'summary_files': []
                }
            
            results[condition_key]['all_scores'].append(success_rate)
            results[condition_key]['summary_files'].append(summary_file)
    
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


def print_results_table(results: Dict[str, Dict]):
    """
    Print results in a formatted table.
    
    Args:
        results: Analysis results from analyze_patterns
    """
    if not results:
        print("No results to display.")
        return
    
    print("\n" + "="*160)
    print("UNIFIED BATCH ANALYSIS STATISTICS SUMMARY")
    print("="*160)
    
    # Table header
    header = f"{'Environment':<20} {'Model':<25} {'TF':<5} {'AE':<5} {'Adhoc Type':<15} {'Uncertainty':<20} {'CompEnabled':<12} {'TRGType':<10} {'Mean±SE':<12} {'Count':<8}"
    print(header)
    print("-" * 182)
    
    # Sort results by environment, then TF, then model, then AE, then adhoc type, then uncertainty, then complexity, then TRG
    sorted_items = sorted(results.items(), key=lambda x: (
        x[1]['metadata']['env_dir'],
        x[1]['metadata']['has_turn_level_tf'],
        x[1]['metadata']['model_config'],
        x[1]['metadata']['has_adhoc_eval'],
        x[1]['metadata']['adhoc_type'],
        x[1]['metadata']['uncertainty_type'],
        x[1]['metadata']['has_complexity_enabled'],
        x[1]['metadata']['trg_type']
    ))
    
    for condition_key, data in sorted_items:
        metadata = data['metadata']
        stats = data['statistics']
        
        env_display = metadata['env_dir'][:19]
        model_display = metadata['model_config'][:24]
        tf_display = "Yes" if metadata['has_turn_level_tf'] else "No"
        ae_display = "Yes" if metadata['has_adhoc_eval'] else "No"
        adhoc_display = metadata['adhoc_type'][:14]
        uncertainty_display = metadata['uncertainty_type'][:19]
        comp_display = "ON" if metadata['has_complexity_enabled'] else "OFF"
        trg_display = metadata['trg_type'][:9]
        
        mean_se = f"{stats['mean']:.2f}±{stats['se']:.3f}"
        count = stats['count']
        
        row = f"{env_display:<20} {model_display:<25} {tf_display:<5} {ae_display:<5} {adhoc_display:<15} {uncertainty_display:<20} {comp_display:<12} {trg_display:<10} {mean_se:<12} {count:<8}"
        print(row)
    
    print("="*160)
    
    # Summary statistics
    all_means = [data['statistics']['mean'] for data in results.values()]
    if all_means:
        overall_mean = statistics.mean(all_means)
        overall_std = statistics.stdev(all_means) if len(all_means) > 1 else 0.0
        print(f"\nOVERALL STATISTICS:")
        print(f"Total Conditions: {len(results)}")
        print(f"Overall Mean: {overall_mean:.3f}")
        print(f"Overall Std: {overall_std:.3f}")
        print(f"Min Mean: {min(all_means):.3f}")
        print(f"Max Mean: {max(all_means):.3f}")
    
    print("\n")


def save_csv_results(results: Dict[str, Dict], output_file: str):
    """
    Save results to CSV file for better readability.
    """
    # Ensure reports directory exists
    reports_dir = os.path.dirname(output_file)
    if reports_dir and not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Sort results by environment, then TF, then model, then AE, then adhoc type, then uncertainty, then complexity, then TRG
    sorted_items = sorted(results.items(), key=lambda x: (
        x[1]['metadata']['env_dir'],
        x[1]['metadata']['has_turn_level_tf'],
        x[1]['metadata']['model_config'],
        x[1]['metadata']['has_adhoc_eval'],
        x[1]['metadata']['adhoc_type'],
        x[1]['metadata']['uncertainty_type'],
        x[1]['metadata']['has_complexity_enabled'],
        x[1]['metadata']['trg_type']
    ))
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Environment', 'Model', 'Turn_Level_TF', 'AdhocEval', 'Adhoc_Type',
            'Uncertainty_Type', 'Complexity_Enabled', 'TRG_Type', 'Mean', 'Std', 'SE', 'Count', 'Raw_Scores'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for condition_key, data in sorted_items:
            metadata = data['metadata']
            stats = data['statistics']
            raw_scores_str = ','.join([str(score) for score in data['raw_scores']])
            
            writer.writerow({
                'Environment': metadata['env_dir'],
                'Model': metadata['model_config'],
                'Turn_Level_TF': metadata['has_turn_level_tf'],
                'AdhocEval': metadata['has_adhoc_eval'],
                'Adhoc_Type': metadata['adhoc_type'],
                'Uncertainty_Type': metadata['uncertainty_type'],
                'Complexity_Enabled': metadata['has_complexity_enabled'],
                'TRG_Type': metadata['trg_type'],
                'Mean': f"{stats['mean']:.4f}",
                'Std': f"{stats['std']:.4f}",
                'SE': f"{stats['se']:.4f}",
                'Count': stats['count'],
                'Raw_Scores': raw_scores_str
            })
    
    print(f"CSV results saved to: {output_file}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze Unified Batch Summary statistics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all results for TransactionEnv_transformed
  python unified_batch_analyzer.py --pattern "test_with_uncertainties/TransactionEnv_transformed/*_analysis/"
  
  # Analyze specific model results
  python unified_batch_analyzer.py --pattern "test_with_uncertainties/TransactionEnv_transformed/*claude37_think*_analysis/"
  
  # Save results to specific CSV file
  python unified_batch_analyzer.py --pattern "test_with_uncertainties/TransactionEnv_transformed/*_analysis/" --output reports/my_results.csv
        """
    )
    
    parser.add_argument('--pattern', type=str,
                       help='Single glob pattern to analyze')
    parser.add_argument('--patterns', nargs='+',
                       help='Multiple glob patterns to analyze')
    parser.add_argument('--output', type=str,
                       help='Output CSV file path')
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
        patterns = ["test_with_uncertainties/TransactionEnv_transformed/*_analysis/"]
        print("No pattern specified, using default pattern for all TransactionEnv_transformed analysis")
    
    # Analyze patterns
    results = analyze_patterns(patterns)
    
    # Print results table
    print_results_table(results)
    
    # Save CSV results
    if args.output:
        save_csv_results(results, args.output)
    else:
        # Generate default CSV file in reports directory
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_csv_file = f"reports/unified_batch_analysis_{timestamp}.csv"
        save_csv_results(results, default_csv_file)
    
    if args.verbose:
        print(f"\nProcessed {len(results)} conditions:")
        for key in sorted(results.keys()):
            print(f"  - {key}")


if __name__ == "__main__":
    main()
