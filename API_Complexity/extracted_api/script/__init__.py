# Make the script directory a proper Python package
import sys
import os

# Add parent directory to path so we can import properly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
