#!/usr/bin/env python3
# Master script to run all API extraction scripts at once INCLUDING SimilarAPIs

import os
import sys
import subprocess
import time
from pathlib import Path

def run_extraction_script(script_name):
    """Run a single extraction script and return success status"""
    try:
        print(f"Running {script_name}...")
        result = subprocess.run(
            [sys.executable, script_name], 
            cwd=os.path.dirname(__file__),
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"✅ {script_name} completed successfully")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {script_name} failed with return code {result.returncode}")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"❌ {script_name} timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ {script_name} failed with exception: {e}")
        return False

def main():
    # Define all extraction scripts to run INCLUDING SimilarAPIs
    extraction_scripts = [
        "extract_smart_home_api.py",
        "extract_info_control_api.py", 
        "extract_media_control_api.py",
        "extract_communication_controller_api.py",
        "extract_culinary_control_api.py",
        "extract_time_notification_api.py",
        "extract_transaction_api.py",
        "extract_similars_api.py",  # Added for SHORT unclear version
    ]
    
    print("🚀 Starting SHORT API extraction for all environments INCLUDING SimilarAPIs...")
    print("=" * 80)
    
    # Check if scripts exist
    script_dir = os.path.dirname(__file__)
    existing_scripts = []
    missing_scripts = []
    
    for script in extraction_scripts:
        script_path = os.path.join(script_dir, script)
        if os.path.exists(script_path):
            existing_scripts.append(script)
        else:
            missing_scripts.append(script)
    
    if missing_scripts:
        print("⚠️  Warning: The following scripts were not found:")
        for script in missing_scripts:
            print(f"   - {script}")
        print()
    
    # Run existing scripts
    successful_runs = 0
    failed_runs = 0
    start_time = time.time()
    
    for script in existing_scripts:
        success = run_extraction_script(script)
        if success:
            successful_runs += 1
        else:
            failed_runs += 1
        print()  # Add spacing between script runs
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("=" * 80)
    print("📊 SHORT API EXTRACTION WITH SIMILARAPIS SUMMARY")
    print("=" * 80)
    print(f"Total scripts found: {len(existing_scripts)}")
    print(f"Successful extractions: {successful_runs}")
    print(f"Failed extractions: {failed_runs}")
    print(f"Missing scripts: {len(missing_scripts)}")
    print(f"Total time: {duration:.2f} seconds")
    
    if successful_runs > 0:
        print(f"\n✅ Successfully extracted APIs from {successful_runs} environment(s)")
        print("📁 Check extracted_api/api_file/ for generated JSON files")
    
    if failed_runs > 0:
        print(f"\n❌ {failed_runs} extraction(s) failed - check error messages above")
        sys.exit(1)
    
    if missing_scripts:
        print(f"\n⚠️  {len(missing_scripts)} script(s) not found - see warnings above")
    
    print("\n🎉 SHORT API extraction with SimilarAPIs completed!")

if __name__ == "__main__":
    main()
