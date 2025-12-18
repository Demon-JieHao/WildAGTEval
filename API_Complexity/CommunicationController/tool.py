# Copyright CommunicationController

# Import the common base tool
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base_tool import BaseTool

# For backward compatibility, create an alias
Tool = BaseTool
