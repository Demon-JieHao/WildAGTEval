#!/usr/bin/env python3
"""
Data Sampler Script - Random sampling with backup and restore functionality

This script performs random sampling of 300 files from file sets in Combined directory.
Each file set consists of: *_exec.py, *_exec_mapping.json, *.jsonl

Usage:
    python scripts/data_sampler.py                    # Sample data (default)
    python scripts/data_sampler.py --action sample    # Sample data 
    python scripts/data_sampler.py --action restore   # Restore from backup
    python scripts/data_sampler.py --help            # Show help
"""

import os
import sys
import shutil
import random
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Set, Dict, Tuple


class DataSampler:
    def __init__(self, target_dir: str = "atomic_conversation_units/success_conversations/Combined", 
                 reports_dir: str = "reports", seed: int = 42, sample_size: int = 300):
        self.target_dir = Path(target_dir)
        self.reports_dir = Path(reports_dir)
        self.seed = seed
        self.sample_size = sample_size
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create reports directory if it doesn't exist
        self.reports_dir.mkdir(exist_ok=True)
        
        print(f"🎲 Data Sampler Script")
        print(f"📁 Target: {self.target_dir}")
        print(f"📊 Seed: {self.seed}, Sample Size: {self.sample_size}")
        print(f"📋 Reports: {self.reports_dir}")
        
    def find_file_sets(self) -> List[str]:
        """Find all file sets by identifying *_exec.py files and extracting base names."""
        if not self.target_dir.exists():
            raise FileNotFoundError(f"Target directory not found: {self.target_dir}")
        
        exec_files = sorted(self.target_dir.glob("*_exec.py"))
        base_names = []
        
        for exec_file in exec_files:
            # Extract base name by removing '_exec.py'
            base_name = exec_file.stem.replace('_exec', '')
            base_names.append(base_name)
        
        print(f"🔍 Found {len(base_names)} file sets")
        return base_names
    
    def verify_file_set(self, base_name: str) -> Tuple[bool, List[str]]:
        """Verify that all three files in a set exist."""
        required_files = [
            f"{base_name}_exec.py",
            # f"{base_name}_exec_mapping.json", 
            f"{base_name}.jsonl"
        ]
        
        existing_files = []
        for file_name in required_files:
            file_path = self.target_dir / file_name
            if file_path.exists():
                existing_files.append(file_name)
        
        is_complete = len(existing_files) == 2
        return is_complete, existing_files
    
    def create_backup(self) -> Path:
        """Create a backup of the entire target directory."""
        backup_name = f"Combined_backup_{self.timestamp}"
        backup_path = self.target_dir.parent / backup_name
        
        print(f"💾 Creating backup: {backup_name}")
        shutil.copytree(self.target_dir, backup_path)
        
        # Save backup info
        backup_info = {
            "backup_path": str(backup_path),
            "original_path": str(self.target_dir),
            "timestamp": self.timestamp,
            "created_at": datetime.now().isoformat()
        }
        
        backup_info_path = self.reports_dir / "backup_info.json"
        with open(backup_info_path, 'w') as f:
            json.dump(backup_info, f, indent=2)
        
        print(f"✅ Backup created: {backup_path}")
        return backup_path
    
    def sample_file_sets(self, base_names: List[str]) -> List[str]:
        """Randomly sample specified number of file sets with fixed seed."""
        total_sets = len(base_names)
        sample_size = min(self.sample_size, total_sets)
        
        print(f"🎯 Selecting {sample_size} sets from {total_sets}")
        
        # Set seed and sample
        random.seed(self.seed)
        selected_sets = random.sample(base_names, sample_size)
        
        return sorted(selected_sets)  # Sort for consistent output
    
    def save_sampling_results(self, selected_sets: List[str], all_sets: List[str]):
        """Save sampling results and metadata to files."""
        # Save selected samples
        selected_file = self.reports_dir / "selected_samples.txt"
        with open(selected_file, 'w') as f:
            for base_name in selected_sets:
                f.write(f"{base_name}\n")
        
        # Save sampling metadata
        sampling_info = {
            "seed": self.seed,
            "sample_size": self.sample_size,
            "total_sets": len(all_sets),
            "selected_count": len(selected_sets),
            "timestamp": self.timestamp,
            "selected_sets": selected_sets,
            "created_at": datetime.now().isoformat()
        }
        
        sampling_info_file = self.reports_dir / "sampling_info.json"
        with open(sampling_info_file, 'w') as f:
            json.dump(sampling_info, f, indent=2)
        
        print(f"📝 Results saved:")
        print(f"   - {selected_file}")
        print(f"   - {sampling_info_file}")
    
    def remove_unselected_files(self, selected_sets: List[str], all_sets: List[str]):
        """Remove files that were not selected in sampling."""
        unselected_sets = set(all_sets) - set(selected_sets)
        removed_count = 0
        
        print(f"🗑️  Removing {len(unselected_sets)} unselected file sets...")
        
        for base_name in unselected_sets:
            file_extensions = ["_exec.py", "_exec_mapping.json", ".jsonl"]
            
            for ext in file_extensions:
                file_path = self.target_dir / f"{base_name}{ext}"
                if file_path.exists():
                    try:
                        file_path.unlink()
                        removed_count += 1
                    except Exception as e:
                        print(f"   ❌ Failed to remove {file_path.name}: {e}")
        
        print(f"✅ Removed {removed_count} files")
        
        # Verify final state
        remaining_exec_files = len(list(self.target_dir.glob("*_exec.py")))
        print(f"📊 Final state: {remaining_exec_files} file sets remaining")
    
    def sample(self):
        """Main sampling workflow."""
        try:
            # Step 1: Find all file sets
            all_sets = self.find_file_sets()
            if not all_sets:
                print("❌ No file sets found!")
                return False
            
            # Step 2: Verify file completeness
            print("🔎 Verifying file sets...")
            incomplete_sets = []
            for base_name in all_sets:
                is_complete, existing_files = self.verify_file_set(base_name)
                if not is_complete:
                    incomplete_sets.append((base_name, existing_files))
            
            if incomplete_sets:
                print(f"⚠️  Found {len(incomplete_sets)} incomplete file sets:")
                for base_name, files in incomplete_sets[:5]:  # Show first 5
                    print(f"   - {base_name}: {files}")
                if len(incomplete_sets) > 5:
                    print(f"   ... and {len(incomplete_sets) - 5} more")
                
                response = input("Continue anyway? (y/N): ")
                if response.lower() not in ['y', 'yes']:
                    print("🚫 Operation cancelled.")
                    return False
            
            # Step 3: Create backup
            backup_path = self.create_backup()
            
            # Step 4: Sample file sets
            selected_sets = self.sample_file_sets(all_sets)
            
            # Step 5: Save results
            self.save_sampling_results(selected_sets, all_sets)
            
            # Step 6: Remove unselected files
            self.remove_unselected_files(selected_sets, all_sets)
            
            print("✅ Sampling completed successfully!")
            print(f"🎯 Selected {len(selected_sets)}/{len(all_sets)} file sets")
            return True
            
        except Exception as e:
            print(f"❌ Error during sampling: {e}")
            return False
    
    def restore(self):
        """Restore from backup."""
        backup_info_path = self.reports_dir / "backup_info.json"
        
        if not backup_info_path.exists():
            print("❌ No backup information found!")
            return False
        
        try:
            with open(backup_info_path, 'r') as f:
                backup_info = json.load(f)
            
            backup_path = Path(backup_info["backup_path"])
            
            if not backup_path.exists():
                print(f"❌ Backup directory not found: {backup_path}")
                return False
            
            print(f"🔄 Restoring from backup: {backup_path}")
            print(f"📅 Backup created: {backup_info['created_at']}")
            
            # Confirm restoration
            response = input("⚠️  This will replace current data. Continue? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("🚫 Restoration cancelled.")
                return False
            
            # Remove current directory and restore from backup
            if self.target_dir.exists():
                shutil.rmtree(self.target_dir)
            
            shutil.copytree(backup_path, self.target_dir)
            
            print("✅ Restoration completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error during restoration: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Random data sampler with backup functionality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--action", 
        choices=["sample", "restore"],
        default="sample",
        help="Action to perform (default: sample)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible sampling (default: 42)"
    )
    
    parser.add_argument(
        "--sample-size",
        type=int,
        default=300,
        help="Number of samples to select (default: 300)"
    )
    
    parser.add_argument(
        "--target-dir",
        default="atomic_conversation_units/success_conversations/Combined",
        help="Target directory to sample"
    )
    
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory to save reports"
    )
    
    args = parser.parse_args()
    
    # Create sampler instance
    sampler = DataSampler(
        target_dir=args.target_dir,
        reports_dir=args.reports_dir,
        seed=args.seed,
        sample_size=args.sample_size
    )
    
    # Execute action
    if args.action == "sample":
        success = sampler.sample()
    elif args.action == "restore":
        success = sampler.restore()
    else:
        print(f"❌ Unknown action: {args.action}")
        success = False
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
