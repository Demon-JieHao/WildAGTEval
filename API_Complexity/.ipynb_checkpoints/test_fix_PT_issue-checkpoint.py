#!/usr/bin/env python3

import re
from datetime import datetime, timedelta

def is_valid_iso8601_duration(time_range: str) -> bool:
    """
    Validate if the provided string is a valid ISO 8601 duration format.
    Must start with 'P' and contain at least one valid designator with a non-zero value.
    
    Valid examples:
    - P7D (7 days)
    - P1W (1 week)
    - P1DT12H30M (1 day, 12 hours, 30 minutes)
    - PT24H (24 hours)
    """
    # Basic validation: must start with P
    if not time_range or not time_range.startswith('P'):
        return False
    
    # Simple regex pattern for ISO 8601 duration
    pattern = r'^P((\d+Y)?(\d+M)?(\d+W)?(\d+D)?)?(T(\d+H)?(\d+M)?(\d+S)?)?$'
    
    # Check if the pattern matches
    match = re.match(pattern, time_range)
    if not match:
        return False
        
    # Extract all duration components
    duration_parts = re.findall(r'(\d+)[YMWDHMS]', time_range)
    
    # Ensure at least one valid duration value is present and non-zero
    return any(int(x) > 0 for x in duration_parts if x)

# Test the updated validation function with the problematic "PT" input
problem_cases = ["P", "T", "PT", "P0D", "PT0H", "PT0M", "PT0S"]
print("Testing edge cases that should be invalid:")
for case in problem_cases:
    print(f"{case}: {'Valid' if is_valid_iso8601_duration(case) else 'Invalid'}")

print("\nTesting valid cases:")
valid_cases = ["P1D", "P7D", "PT1H", "P1DT12H30M", "PT24H"]
for case in valid_cases:
    print(f"{case}: {'Valid' if is_valid_iso8601_duration(case) else 'Invalid'}")
