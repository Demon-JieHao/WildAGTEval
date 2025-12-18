# Copyright SimilarAPIs

import os

FOLDER_PATH = os.path.dirname(__file__)

with open(os.path.join(FOLDER_PATH, "wiki_short.md"), "r") as f:
    WIKI = f.read()
