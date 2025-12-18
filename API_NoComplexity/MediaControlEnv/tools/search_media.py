# Copyright MediaControlEnv

import json
from typing import Any, Dict, List, Optional
from MediaControlEnv.tool import Tool
from MediaControlEnv.helpers import find_media_by_title


class SearchMedia(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], query: str, media_type: Optional[str] = None, limit: Optional[int] = 10) -> str:
        """
        Search for media by title.
        
        Args:
            data: The data dictionary containing media database
            query: Search query (partial title match)
            media_type: Optional filter by type (movie, tv_show, song, album, playlist)
            limit: Maximum number of results to return (default: 10)
            
        Returns:
            A JSON string with the search results
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_informational_notice_enabled = os.getenv('ENABLE__INFORMATIONAL_NOTICE__SEARCH_MEDIA', 'false').lower() == 'true'
        
        if not query:
            return json.dumps({
                "success": False,
                "message": "No search query provided"
            })
        
        # Validate limit
        if limit is None:
            limit = 10
        elif limit < 1:
            return json.dumps({
                "success": False,
                "message": "Limit must be at least 1"
            })
        
        # Search for media
        results = find_media_by_title(data, query, media_type)
        
        # Limit results
        results = results[:limit]
        
        if results:
            # Format results
            formatted_results = []
            for item in results:
                formatted_item = {
                    "id": item.get("id"),
                    "title": item.get("title"),
                    "type": item.get("type"),
                    "year": item.get("year", ""),
                    "genre": item.get("genre", []),
                    "services": item.get("services", [])
                }
                
                # Add type-specific fields
                if item.get("type") == "song":
                    formatted_item["artist"] = item.get("artist", "")
                    formatted_item["album"] = item.get("album", "")
                elif item.get("type") == "album":
                    formatted_item["artist"] = item.get("artist", "")
                    formatted_item["tracks"] = item.get("tracks", 0)
                elif item.get("type") == "tv_show":
                    formatted_item["seasons"] = item.get("seasons", 0)
                    formatted_item["episodes"] = item.get("episodes", 0)
                
                formatted_results.append(formatted_item)
            
            ### ADDED: Build base response ###
            response = {
                "success": True,
                "count": len(formatted_results),
                "results": formatted_results,
                "message": f"Found {len(formatted_results)} media items matching '{query}'"
            }
            
            ### ADDED: Include informational notices when uncertainty is enabled ###
            if uncertainty_informational_notice_enabled:
                # Add multiple helpful but potentially confusing notices
                response["info"] = f"FYI: advanced_search() is available for more complex queries with filters like year ranges, ratings, and multiple genres. It also supports fuzzy matching for misspellings."
                
                response["performance_note"] = f"This search completed in standard time. For reference, browse_by_genre() provides pre-indexed results that load faster for genre-based discovery, especially useful when exploring content without specific titles in mind."
                
                response["alternative_approaches"] = {
                    "trending": "get_trending() is available if you're interested in currently popular content across all services",
                    "recommendations": "get_recommendations() can suggest similar content based on viewing history",
                    "voice_search": "voice_search() also handles natural language queries if that fits your use case better"
                }
                
                # Add context-specific notices based on search characteristics
                if len(query) < 3:
                    response["search_tip"] = "Short queries like this work fine, though longer search terms (4+ characters) typically yield more precise results. The fuzzy_search() function is particularly good with partial matches."
                
                if media_type:
                    response["filter_info"] = f"You're filtering by {media_type}, which is great! Just so you know, browse_by_category() offers pre-filtered collections by media type with additional subcategories."
                
                if len(formatted_results) == limit:
                    response["pagination_note"] = f"Results were limited to {limit} items as requested. The paginated_search() function is available for handling larger result sets with built-in pagination support, useful for comprehensive searches."
            
            return json.dumps(response)
        else:
            ### ADDED: Build base response for no results ###
            response = {
                "success": True,
                "count": 0,
                "results": [],
                "message": f"No media found matching '{query}'"
            }
            
            ### ADDED: Include informational notices even for empty results ###
            if uncertainty_informational_notice_enabled:
                response["search_suggestions"] = {
                    "tip": "No results found with exact/partial title match. Here are some alternatives:",
                    "fuzzy_search": "fuzzy_search() handles misspellings and similar-sounding titles",
                    "browse": "browse_all() lets you explore the full catalog with filters",
                    "discover": "discover_content() uses AI to find content based on descriptions rather than titles"
                }
                
                response["info"] = "This search uses partial title matching. For reference, semantic_search() understands context and plot descriptions if you're looking for content by theme rather than title."
            
            return json.dumps(response)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_media",
                "description": "Search for media content by title. Supports partial matching and optional filtering by media type.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query for media title (partial match supported)"
                        },
                        "media_type": {
                            "type": "string",
                            "enum": ["movie", "tv_show", "song", "album", "playlist"],
                            "description": "Optional filter by media type"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of results to return (default: 10)",
                            "default": 10
                        }
                    },
                    "required": ["query"]
                },
                "error_cases": [
                    "No search query: The query parameter is empty or not provided.",
                    "Invalid limit: The limit parameter is less than 1."
                ]
            }
        }
