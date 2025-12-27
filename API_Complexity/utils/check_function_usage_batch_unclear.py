#!/usr/bin/env python3
"""
Batch function usage checker for all unclear test result directories
Automatically finds and analyzes all directories containing 'unclear' and 'test_results' but not 'reports'
"""

import json
import glob
import os
import sys
from collections import defaultdict
from pathlib import Path

def find_unclear_test_directories(base_path):
    """Find all directories containing 'unclear' and 'test_results' but not 'reports'"""
    base_path = Path(base_path)
    unclear_dirs = []
    
    if not base_path.exists():
        print(f"❌ Base path does not exist: {base_path}")
        return []
    
    # Find all directories
    for item in base_path.iterdir():
        if item.is_dir():
            dir_name = item.name
            # Check if directory contains 'unclear' and 'test_results' but not 'reports'
            # if ('unclear' in dir_name and 
            #     'test_results' in dir_name and 
            #     'reports' not in dir_name):
            #     unclear_dirs.append(item)
            if ('unclear' in dir_name and
                'analysis' not in dir_name ):
                unclear_dirs.append(item)
    
    return sorted(unclear_dirs)

def check_function_usage_in_directory(directory_path):
    """Check function usage in a single directory"""
    # List of target functions to check
    target_functions = [
        'broadcast_alert', 'color_scene_set', 'color_temperature_set',
        'create_calendar_event', 'create_timer', 'device_deactivate',
        'fetch_notification_status', 'find_communication_device',
        'get_calendar_events', 'get_content_details', 'get_device_inventory',
        'hvac_mode_set', 'initiate_call_session', 'place_pickup_order',
        'place_restaurant_order', 'schedule_action', 'search_contact_directory',
        'send_chat_message', 'sync_messages', 'temperature_schedule'
    ]
    
    # Containers for results (including full paths)
    function_usage = defaultdict(list)  # Files where each function is used
    file_results = {}  # Results per file
    
    # Find JSON files in the directory
    json_pattern = os.path.join(directory_path, "*.json")
    json_files = glob.glob(json_pattern)
    
    if len(json_files) == 0:
        return function_usage, file_results, 0
    
    # Process each file
    processed_files = 0
    error_files = 0
    
    for file_path in json_files:
        filename = os.path.basename(file_path)
        file_results[filename] = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # collect all llm_response from query_results
            all_responses = []
            if 'query_results' in data:
                for query_result in data['query_results']:
                    if 'steps' in query_result:
                        for step in query_result['steps']:
                            if 'llm_response' in step:
                                all_responses.append(step['llm_response'])
            
            # check if each function has been invoked
            found_functions = []
            for func in target_functions:
                found = any(func in response for response in all_responses)
                file_results[filename][func] = found
                if found:
                    # full absolute path 저장
                    full_path = os.path.abspath(file_path)
                    function_usage[func].append(full_path)
                    found_functions.append(func)
            
            processed_files += 1
                    
        except Exception as e:
            error_files += 1
    
    return function_usage, file_results, len(json_files)

def generate_detailed_report(function_usage, file_results, total_files, directory_path):
    """Generate detailed report file with unique naming"""
    
    # Create the function_usage_reports directory (ignore if it already exists)
    reports_dir = "function_usage_reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate a unique report filename (convert full path into underscores)
    dir_path_clean = str(directory_path).replace('/', '_').replace('\\', '_')
    if dir_path_clean.startswith('test_with_uncertainties_'):
        dir_path_clean = dir_path_clean[len('test_with_uncertainties_'):]
    
    report_filename = os.path.join(reports_dir, f"function_usage_report_{dir_path_clean}.md")
    
    report_content = []
    report_content.append("# Function Usage Analysis Report")
    report_content.append(f"Analysis Date: {os.popen('date').read().strip()}")
    report_content.append(f"Total Files Analyzed: {total_files}")
    report_content.append(f"Directory: {directory_path}")
    report_content.append("")
    
    # Summary statistics
    report_content.append("## Summary Statistics")
    report_content.append(f"- Functions found: {len(function_usage)}/20")
    report_content.append(f"- Total function occurrences: {sum(len(files) for files in function_usage.values())}")
    report_content.append("")
    
    # Function usage details
    if function_usage:
        report_content.append("## Function Usage Details")
        sorted_functions = sorted(function_usage.items(), key=lambda x: len(x[1]), reverse=True)
        
        for func, files in sorted_functions:
            report_content.append(f"### {func} ({len(files)} files)")
            for file in files:
                report_content.append(f"- {file}")
            report_content.append("")
    
    # Unused functions
    target_functions = [
        'broadcast_alert', 'color_scene_set', 'color_temperature_set',
        'create_calendar_event', 'create_timer', 'device_deactivate',
        'fetch_notification_status', 'find_communication_device',
        'get_calendar_events', 'get_content_details', 'get_device_inventory',
        'hvac_mode_set', 'initiate_call_session', 'place_pickup_order',
        'place_restaurant_order', 'schedule_action', 'search_contact_directory',
        'send_chat_message', 'sync_messages', 'temperature_schedule'
    ]
    
    unused_functions = [func for func in target_functions if func not in function_usage]
    if unused_functions:
        report_content.append("## Functions NOT Found")
        for func in unused_functions:
            report_content.append(f"- {func}")
    
    # Write report to file
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_content))
    
    return report_filename

def main():
    # Base directory
    # base_path = "test_with_uncertainties/TransactionEnv" # "test_with_uncertainties"
    # base_path = "test_with_uncertainties/TransactionEnv_transformed" # "test_with_uncertainties"
    base_path = "/home/code/test_with_uncertainties/Combined_transformed" # "test_with_uncertainties"
    
    if not os.path.exists(base_path):
        print(f"❌ Base directory does not exist: {base_path}")
        sys.exit(1)
    
    print("🚀 Starting Batch Function Usage Analysis for UNCLEAR directories")
    print("=" * 80)
    
    # Find all unclear test directories
    unclear_dirs = find_unclear_test_directories(base_path)
    
    if not unclear_dirs:
        print(f"❌ No unclear test result directories found in {base_path}")
        sys.exit(1)
    
    print(f"🔍 Found {len(unclear_dirs)} unclear test result directories:")
    for dir_path in unclear_dirs:
        print(f"   - {dir_path}")
    print()
    
    # Process each directory
    overall_results = {}
    
    for dir_path in unclear_dirs:
        print(f"📂 Processing: {dir_path}")
        
        function_usage, file_results, total_files = check_function_usage_in_directory(dir_path)
        
        print(f"   📊 Files: {total_files}")
        
        if function_usage:
            found_functions = list(function_usage.keys())
            total_occurrences = sum(len(files) for files in function_usage.values())
            print(f"   ✅ Functions found: {len(found_functions)} ({total_occurrences} total occurrences)")
            
            # Show top 3 functions
            sorted_functions = sorted(function_usage.items(), key=lambda x: len(x[1]), reverse=True)
            for func, files in sorted_functions[:3]:
                print(f"      - {func}: {len(files)} files")
            if len(sorted_functions) > 3:
                print(f"      - ... and {len(sorted_functions)-3} more functions")
        else:
            print(f"   ❌ No target functions found")
        
        # Generate report
        report_filename = generate_detailed_report(function_usage, file_results, total_files, dir_path)
        print(f"   📄 Report: {report_filename}")
        
        # Store results for summary
        overall_results[str(dir_path)] = {
            'total_files': total_files,
            'functions_found': len(function_usage),
            'total_occurrences': sum(len(files) for files in function_usage.values()),
            'top_functions': sorted(function_usage.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        }
        
        print()
    
    # Generate overall summary
    print("=" * 80)
    print("📈 Overall Summary:")
    print("-" * 50)
    
    total_dirs = len(unclear_dirs)
    dirs_with_functions = sum(1 for result in overall_results.values() if result['functions_found'] > 0)
    total_files_processed = sum(result['total_files'] for result in overall_results.values())
    total_function_occurrences = sum(result['total_occurrences'] for result in overall_results.values())
    
    print(f"📁 Directories processed: {total_dirs}")
    print(f"📊 Total files processed: {total_files_processed}")
    print(f"✅ Directories with functions found: {dirs_with_functions}/{total_dirs}")
    print(f"🔧 Total function occurrences: {total_function_occurrences}")
    print()
    
    # Show top performing directories
    if dirs_with_functions > 0:
        print("🏆 Top directories by function occurrences:")
        sorted_dirs = sorted(overall_results.items(), 
                           key=lambda x: x[1]['total_occurrences'], 
                           reverse=True)
        
        for i, (dir_name, result) in enumerate(sorted_dirs[:5]):
            if result['functions_found'] > 0:
                dir_short = os.path.basename(dir_name)
                print(f"   {i+1}. {dir_short}: {result['total_occurrences']} occurrences ({result['functions_found']} functions)")
    
    # All functions found across all directories
    all_functions_found = set()
    for result in overall_results.values():
        for func, _ in result['top_functions']:
            all_functions_found.add(func)
    
    if all_functions_found:
        print(f"\n🎯 Unique functions found across all directories: {len(all_functions_found)}")
        for func in sorted(all_functions_found):
            print(f"   - {func}")
    
    print("\n✨ Analysis completed!")
    print(f"📄 Individual reports generated for each directory")

def parse_experiment_info(filename):
    """Parse experiment information from filename"""
    info = {
        'model': 'unknown',
        'think_type': 'unknown',
        'complexity': 'unknown',
        'seed': 'unknown',
        'experiment_type': 'unknown'
    }
    
    # Remove prefix and suffix
    name = filename.replace('function_usage_report_', '').replace('.md', '')
    
    # Extract model
    if 'claude37' in name:
        info['model'] = 'claude-3.5-sonnet'
    elif 'claude40' in name:
        info['model'] = 'claude-4-sonnet'
    elif 'qwen3_32b' in name:
        info['model'] = 'qwen-32b'
    elif 'claude3_5' in name:
        info['model'] = 'claude-3.5'
    
    # Extract think type
    if 'no_think' in name:
        info['think_type'] = 'no_think'
    elif 'fullthink' in name:
        info['think_type'] = 'fullthink'
    elif 'think' in name:
        info['think_type'] = 'think'
    
    # Extract complexity
    if 'adhoc+unclear' in name:
        if 'partially_irrelevant' in name:
            info['complexity'] = 'adhoc+unclear+partially_irrelevant'
        elif 'system_failure' in name:
            info['complexity'] = 'adhoc+unclear+system_failure'
        elif 'feature_limitation' in name:
            info['complexity'] = 'adhoc+unclear+feature_limitation'
        else:
            info['complexity'] = 'adhoc+unclear'
    elif 'adhoc' in name:
        info['complexity'] = 'adhoc'
    elif 'unclear' in name:
        info['complexity'] = 'unclear'
    
    # Extract seed
    import re
    seed_match = re.search(r'_s(\d+)', name)
    if seed_match:
        info['seed'] = f"s{seed_match.group(1)}"
    
    # Extract experiment type
    if 'turn_level_tf' in name:
        info['experiment_type'] = 'turn_level_teacher_forcing'
    elif 'Combined_transformed' in name:
        info['experiment_type'] = 'combined_transformed'
    elif 'Complex_natural' in name:
        info['experiment_type'] = 'complex_natural'
    elif 'TransactionEnv' in name:
        info['experiment_type'] = 'transaction'
    else:
        info['experiment_type'] = 'other'
    
    return info

def scan_function_reports():
    """Scan all function usage reports for function patterns"""
    target_functions = [
        'broadcast_alert', 'color_scene_set', 'color_temperature_set',
        'create_calendar_event', 'create_timer', 'device_deactivate',
        'fetch_notification_status', 'find_communication_device',
        'get_calendar_events', 'get_content_details', 'get_device_inventory',
        'hvac_mode_set', 'initiate_call_session', 'place_pickup_order',
        'place_restaurant_order', 'schedule_action', 'search_contact_directory',
        'send_chat_message', 'sync_messages', 'temperature_schedule'
    ]
    
    reports_dir = "function_usage_reports"
    if not os.path.exists(reports_dir):
        print(f"❌ Reports directory does not exist: {reports_dir}")
        return {}, {}
    
    # Function usage tracking
    function_usage = defaultdict(list)  # function -> list of report files
    report_details = {}  # report_file -> {functions_found, experiment_info}
    
    # Get all .md files
    md_files = glob.glob(os.path.join(reports_dir, "*.md"))
    
    if not md_files:
        print(f"❌ No .md files found in {reports_dir}")
        return {}, {}
    
    print(f"📊 Scanning {len(md_files)} report files...")
    
    for md_file in md_files:
        filename = os.path.basename(md_file)
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find functions using "### {function}" pattern
            found_functions = []
            for func in target_functions:
                pattern = f"### {func}"
                if pattern in content:
                    found_functions.append(func)
                    function_usage[func].append(filename)
            
            # Parse experiment info
            exp_info = parse_experiment_info(filename)
            
            # Store report details
            report_details[filename] = {
                'functions_found': found_functions,
                'experiment_info': exp_info
            }
            
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
    
    return function_usage, report_details

def generate_summary_report(function_usage, report_details):
    """Generate comprehensive summary report"""
    from datetime import datetime
    
    target_functions = [
        'broadcast_alert', 'color_scene_set', 'color_temperature_set',
        'create_calendar_event', 'create_timer', 'device_deactivate',
        'fetch_notification_status', 'find_communication_device',
        'get_calendar_events', 'get_content_details', 'get_device_inventory',
        'hvac_mode_set', 'initiate_call_session', 'place_pickup_order',
        'place_restaurant_order', 'schedule_action', 'search_contact_directory',
        'send_chat_message', 'sync_messages', 'temperature_schedule'
    ]
    
    # Generate summary
    summary_content = []
    summary_content.append("# Function Usage Summary Across All Reports")
    summary_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    summary_content.append("")
    
    # Overall statistics
    total_reports = len(report_details)
    functions_found = len(function_usage)
    total_occurrences = sum(len(files) for files in function_usage.values())
    
    summary_content.append("## Overall Statistics")
    summary_content.append(f"- Total Reports Analyzed: {total_reports}")
    summary_content.append(f"- Functions Found: {functions_found}/20")
    summary_content.append(f"- Total Function Occurrences: {total_occurrences}")
    summary_content.append("")
    
    # Function-wise analysis
    if function_usage:
        summary_content.append("## Function Usage Analysis")
        summary_content.append("")
        
        # Sort functions by usage count
        sorted_functions = sorted(function_usage.items(), key=lambda x: len(x[1]), reverse=True)
        
        for func, files in sorted_functions:
            summary_content.append(f"### {func}")
            summary_content.append(f"- **Usage Count**: {len(files)} reports")
            summary_content.append(f"- **Found in**:")
            
            # Group by experiment type
            exp_groups = defaultdict(list)
            for filename in files:
                if filename in report_details:
                    exp_type = report_details[filename]['experiment_info']['experiment_type']
                    exp_groups[exp_type].append(filename)
            
            for exp_type, filenames in exp_groups.items():
                summary_content.append(f"  - **{exp_type}**: {len(filenames)} reports")
                for filename in filenames[:3]:  # Show first 3
                    summary_content.append(f"    - {filename}")
                if len(filenames) > 3:
                    summary_content.append(f"    - ... and {len(filenames)-3} more")
            
            summary_content.append("")
    
    # Experiment-wise analysis
    summary_content.append("## Experiment-wise Analysis")
    summary_content.append("")
    
    # By model
    model_stats = defaultdict(set)
    for filename, details in report_details.items():
        model = details['experiment_info']['model']
        for func in details['functions_found']:
            model_stats[model].add(func)
    
    summary_content.append("### By Model")
    for model, functions in sorted(model_stats.items()):
        summary_content.append(f"- **{model}**: {len(functions)} unique functions")
        if functions:
            func_list = sorted(list(functions))
            summary_content.append(f"  - Functions: {', '.join(func_list[:5])}")
            if len(func_list) > 5:
                summary_content.append(f"  - ... and {len(func_list)-5} more")
    summary_content.append("")
    
    # By complexity
    complexity_stats = defaultdict(set)
    for filename, details in report_details.items():
        complexity = details['experiment_info']['complexity']
        for func in details['functions_found']:
            complexity_stats[complexity].add(func)
    
    summary_content.append("### By Complexity Type")
    for complexity, functions in sorted(complexity_stats.items()):
        summary_content.append(f"- **{complexity}**: {len(functions)} unique functions")
        if functions:
            func_list = sorted(list(functions))
            summary_content.append(f"  - Functions: {', '.join(func_list[:5])}")
            if len(func_list) > 5:
                summary_content.append(f"  - ... and {len(func_list)-5} more")
    summary_content.append("")
    
    # Functions not found
    unused_functions = [func for func in target_functions if func not in function_usage]
    if unused_functions:
        summary_content.append("## Functions NOT Found in Any Report")
        for func in unused_functions:
            summary_content.append(f"- {func}")
        summary_content.append("")
    
    # Most/Least common functions
    if function_usage:
        summary_content.append("## Function Popularity Ranking")
        summary_content.append("")
        
        summary_content.append("### Most Common Functions")
        for i, (func, files) in enumerate(sorted_functions[:5]):
            summary_content.append(f"{i+1}. **{func}**: {len(files)} reports")
        
        summary_content.append("")
        summary_content.append("### Least Common Functions (but found)")
        for i, (func, files) in enumerate(sorted_functions[-5:]):
            summary_content.append(f"{i+1}. **{func}**: {len(files)} reports")
    
    # Write summary file
    summary_filename = "function_usage_reports/SUMMARY.md"
    with open(summary_filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_content))
    
    return summary_filename

def generate_function_summary():
    """Main function to generate function usage summary from existing reports"""
    print("🚀 Starting Function Usage Summary Generation")
    print("=" * 60)
    
    # Scan all reports
    function_usage, report_details = scan_function_reports()
    
    if not function_usage and not report_details:
        print("❌ No data found to summarize")
        return
    
    print(f"📊 Summary Stats:")
    print(f"   - Reports analyzed: {len(report_details)}")
    print(f"   - Functions found: {len(function_usage)}/20")
    print(f"   - Total occurrences: {sum(len(files) for files in function_usage.values())}")
    print()
    
    # Generate summary report
    summary_file = generate_summary_report(function_usage, report_details)
    
    print(f"✅ Summary report generated: {summary_file}")
    print()
    
    # Show top functions
    if function_usage:
        print("🏆 Top 5 Functions:")
        sorted_functions = sorted(function_usage.items(), key=lambda x: len(x[1]), reverse=True)
        for i, (func, files) in enumerate(sorted_functions[:5]):
            print(f"   {i+1}. {func}: {len(files)} reports")
    
    print("\n✨ Function usage summary completed!")

if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--summary":
        generate_function_summary()
    else:
        main()
