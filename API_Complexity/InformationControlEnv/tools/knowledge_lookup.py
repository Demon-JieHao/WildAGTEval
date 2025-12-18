# Copyright InformationControlEnv

import json
import os
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_mock_data_by_key, add_query_to_history
from datetime import datetime


def get_irrelevant_data(category: str, key: str) -> Dict:
    """Load irrelevant data from irrelevant_mock_data.json"""
    try:
        with open('common/data/irrelevant_mock_data.json', 'r') as f:
            irrelevant_data = json.load(f)
        return irrelevant_data.get(category, {}).get(key, {})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}


class KnowledgeLookup(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], keyword: str) -> str:
        """
        Look up general knowledge about a keyword.
        
        Args:
            data: The data dictionary containing all information
            keyword: The keyword to look up
            
        Returns:
            A JSON string with the knowledge result
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        uncertainty_partially_irrelevant_information_enabled = os.getenv('ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__KNOWLEDGE_LOOKUP', 'false').lower() == 'true'
        
        if not keyword:
            return json.dumps({
                "success": False,
                "message": "No keyword provided"
            })
        
        # Normalize keyword for lookup
        keyword_normalized = keyword.lower().replace(" ", "_")
        
        # Get knowledge data
        knowledge_result = get_mock_data_by_key(data, "knowledge", keyword_normalized)
        
        if not knowledge_result:
            # Get available keywords
            knowledge_data = data.get("mock_data", {}).get("knowledge", {})
            available_keywords = list(knowledge_data.keys())
            
            return json.dumps({
                "success": False,
                "message": f"No information found for keyword: {keyword}",
                "available_keywords": available_keywords
            })
        
        if uncertainty_partially_irrelevant_information_enabled:
            ### ADDED: Combine basic definition with extended information ###
            extended_info = get_irrelevant_data("knowledge", keyword_normalized)
            if extended_info:
                knowledge_result = knowledge_result + "\n" + extended_info
            ### END ADDED ###
        
        # Add query to history
        user = get_current_user(data)
        if user:
            query = {
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "tool": "knowledge_lookup",
                "parameters": {"keyword": keyword},
                "result": "success"
            }
            add_query_to_history(data, query)
        
        return json.dumps({
            "success": True,
            "keyword": keyword,
            "definition": knowledge_result,
            "source": "General Knowledge Base"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "knowledge_lookup",
                "description": "Look up general knowledge about a keyword. Provides definitions and explanations for various topics including technology, science, and general concepts.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "The keyword to look up (e.g., 'python', 'artificial_intelligence', 'quantum_computing')"
                        }
                    },
                    "required": ["keyword"]
                },
                "error_cases": [
                    "No keyword provided: The keyword parameter is empty or not provided.",
                    "Keyword not found: Returns error with list of available keywords.",
                    "Invalid keyword format: Spaces in keywords will be replaced with underscores."
                ]
            }
        }
