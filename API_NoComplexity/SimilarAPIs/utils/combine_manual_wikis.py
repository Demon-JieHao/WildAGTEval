#!/usr/bin/env python3

import os
import re
import glob
from typing import Dict, List, Optional

# Constants
SIMILARAPIS_DIR = "../"
WIKI_MANUAL_DIR = "../wiki"
OUTPUT_DIR = "../output"


def extract_get_info(file_path: str) -> Optional[str]:
    """Extract the get_info method from the Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find the get_info method
        get_info_match = re.search(r'def get_info\(\).*?return\s*({.*?)}(?=\s*@|\s*$)', content, re.DOTALL)
        if get_info_match:
            get_info = get_info_match.group(1) + "}"
            return get_info
    except Exception as e:
        print(f"Error extracting get_info from {file_path}: {e}")
    return None


def combine_get_info(directory: str) -> str:
    """Combine all get_info methods from Python files."""
    result = []
    for file_path in sorted(glob.glob(os.path.join(directory, "*.py"))):
        if "__init__" in file_path or "utils" in file_path:
            continue
        
        file_name = os.path.basename(file_path).replace('.py', '')
        get_info_content = extract_get_info(file_path)
        
        if get_info_content:
            result.append(f"# {file_name}\n{get_info_content}\n\n")
        else:
            print(f"Could not extract get_info from {file_path}")
    
    return "\n".join(result)


def combine_wikis(directory: str) -> str:
    """Combine all wiki files into a single document."""
    result = []
    for file_path in sorted(glob.glob(os.path.join(directory, "*.md"))):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            file_name = os.path.basename(file_path).replace('.md', '')
            result.append(f"# {file_name}\n{content}\n\n")
        except Exception as e:
            print(f"Error reading wiki from {file_path}: {e}")
    
    return "\n".join(result)


def main():
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Extract and combine all get_info methods
    print("Extracting get_info from Python files...")
    get_info_content = combine_get_info(SIMILARAPIS_DIR)
    with open(os.path.join(OUTPUT_DIR, "combined_get_info.txt"), 'w', encoding='utf-8') as f:
        f.write(get_info_content)
    print("Generated combined_get_info.txt")
    
    # Combine manual wikis
    print("Combining manual wiki files...")
    manual_wikis_content = combine_wikis(WIKI_MANUAL_DIR)
    with open(os.path.join(SIMILARAPIS_DIR, "wiki.md"), 'w', encoding='utf-8') as f:
        f.write(manual_wikis_content)
    print("Generated wiki.md")


if __name__ == "__main__":
    main()
