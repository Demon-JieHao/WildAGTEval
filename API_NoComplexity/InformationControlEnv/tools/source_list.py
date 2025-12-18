# Copyright InformationControlEnv

import json
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_sources_by_type


class SourceList(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], source_type: str = None) -> str:
        """
        List available information sources.
        
        Args:
            data: The data dictionary containing all information
            source_type: (Optional) Filter by source type (weather, news, knowledge, financial)
            
        Returns:
            A JSON string with available sources
        """
        sources = data.get("sources", [])
        
        if source_type:
            # Filter by type
            filtered_sources = get_sources_by_type(data, source_type)
            if not filtered_sources:
                # Get available types
                available_types = list(set(source["type"] for source in sources))
                return json.dumps({
                    "success": False,
                    "message": f"No sources found for type: {source_type}",
                    "available_types": available_types
                })
            sources = filtered_sources
        
        # Format sources for display
        formatted_sources = []
        for source in sources:
            formatted_sources.append({
                "id": source["source_id"],
                "name": source["name"],
                "type": source["type"],
                "description": source["description"],
                "supported_queries": source["supported_queries"],
                "reliability": source["reliability"]
            })
        
        return json.dumps({
            "success": True,
            "count": len(formatted_sources),
            "sources": formatted_sources,
            "filter": source_type if source_type else "all"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "source_list",
                "description": "List available information sources. Shows all data sources that can be queried for information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "source_type": {
                            "type": "string",
                            "description": "(Optional) Filter by source type (weather, news, knowledge, financial)"
                        }
                    }
                },
                "error_cases": [
                    "Invalid source type: Returns error with list of available types.",
                    "No sources: Returns empty list if no sources are configured."
                ]
            }
        }
