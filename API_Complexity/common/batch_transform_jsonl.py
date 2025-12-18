#!/usr/bin/env python3
"""Batch script that performs JSONL conversion for files per environment."""

import os
import glob
import subprocess
import argparse
from pathlib import Path


def find_exec_files(base_dir):
    """Find and return a list of *_exec.py files."""
    pattern = os.path.join(base_dir, "*_exec.py")
    exec_files = glob.glob(pattern)
    return sorted(exec_files)


def get_corresponding_files(exec_file, env_name):
    """Return the paths of the mapping file and JSONL files corresponding to an exec file."""
    base_name = os.path.basename(exec_file).replace("_exec.py", "")
    dir_name = os.path.dirname(exec_file)
    
    # Corresponding files
    jsonl_file = os.path.join(dir_name, f"{base_name}.jsonl")
    
    # Path of the transformed directory (dynamically created based on environment name)
    transformed_dir = dir_name.replace(f"/{env_name}", f"/{env_name}_transformed")
    mapping_file = os.path.join(transformed_dir, f"{base_name}_exec_mapping.json")
    output_jsonl = os.path.join(transformed_dir, f"{base_name}.jsonl")
    
    return jsonl_file, mapping_file, output_jsonl


def check_file_exists(file_path):
    """Check whether a file exists."""
    return os.path.exists(file_path)


def run_transform_command(mapping_file, input_jsonl, output_jsonl):
    """Execute the JSONL transform command."""
    cmd = [
        "python", "common/transform_jsonl_script.py",
        "--mapping", mapping_file,
        "--input", input_jsonl,
        "--output", output_jsonl
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def main():
    """Main batch-processing entry point."""
    parser = argparse.ArgumentParser(description='Batch transform JSONL files')
    parser.add_argument('env_name', help='Environment name (e.g., TransactionEnv, MediaControlEnv)')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of files to process (for testing)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed without actually doing it')
    
    args = parser.parse_args()
    
    # Get environment name
    env_name = args.env_name
    
    print(f"🔄 Starting batch JSONL transformation for environment: {env_name}...")
    
    # Find exec files under the environment-specific directory
    base_dir = f"atomic_conversation_units/success_conversations/{env_name}"
    
    # Check if the input directory exists
    if not os.path.exists(base_dir):
        print(f"❌ Could not find input directory: {base_dir}")
        print("💡 Available environments:")
        success_dir = "atomic_conversation_units/success_conversations"
        if os.path.exists(success_dir):
            for item in os.listdir(success_dir):
                item_path = os.path.join(success_dir, item)
                if os.path.isdir(item_path) and not item.endswith("_transformed"):
                    print(f"   - {item}")
        return 1
    
    exec_files = find_exec_files(base_dir)
    
    print(f"📂 Input directory: {base_dir}")
    print(f"🔍 Found {len(exec_files)} exec file(s).")
    
    if args.limit:
        exec_files = exec_files[:args.limit]
        print(f"🔢 Processing limit: only {args.limit} file(s) will be processed.")
    
    # Process each file
    processed = 0
    skipped = 0
    failed = 0
    
    for i, exec_file in enumerate(exec_files, 1):
        print(f"\n{'='*60}")
        print(f"Processing ({i}/{len(exec_files)}): {os.path.basename(exec_file)}")
        print(f"{'='*60}")
        
        # Get paths of corresponding files
        jsonl_file, mapping_file, output_jsonl = get_corresponding_files(exec_file, env_name)
        
        print(f"📄 JSONL file: {jsonl_file}")
        print(f"🗂️  Mapping file: {mapping_file}")
        print(f"📤 Output file: {output_jsonl}")
        
        # Check that all required files exist
        if not check_file_exists(jsonl_file):
            print(f"❌ JSONL file not found: {jsonl_file}")
            skipped += 1
            continue
        
        if not check_file_exists(mapping_file):
            print(f"❌ Mapping file not found: {mapping_file}")
            skipped += 1
            continue
        
        print(f"✅ All required files are present.")
        
        if args.dry_run:
            print(f"🔍 [DRY RUN] The following transform command would be executed:")
            print(f"    python common/transform_jsonl_script.py \\")
            print(f"      --mapping {mapping_file} \\")
            print(f"      --input {jsonl_file} \\")
            print(f"      --output {output_jsonl}")
            processed += 1
            continue
        
        # Run the actual transform
        print(f"🔄 Starting transform...")
        success, stdout, stderr = run_transform_command(mapping_file, jsonl_file, output_jsonl)
        
        if success:
            print(f"✅ Transform succeeded!")
            if stdout:
                # Print only the last few lines (to avoid overly long output)
                lines = stdout.strip().split('\n')
                for line in lines[-5:]:
                    print(f"    {line}")
            processed += 1
        else:
            print(f"❌ Transform failed!")
            if stderr:
                print(f"    Error: {stderr}")
            failed += 1
    
    # Print final summary
    print(f"\n{'='*60}")
    print(f"Batch processing complete!")
    print(f"{'='*60}")
    print(f"✅ Succeeded: {processed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total targets: {len(exec_files)}")
    
    if args.dry_run:
        print(f"\n💡 To actually run the transforms, remove the --dry-run option.")


if __name__ == "__main__":
    main()
