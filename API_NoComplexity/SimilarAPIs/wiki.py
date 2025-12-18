# Copyright TransactionEnv

# Import the wiki content from the markdown file
import os

# Read the wiki content from the markdown file
with open(os.path.join(os.path.dirname(__file__), 'wiki.md'), 'r') as f:
    WIKI = f.read()
