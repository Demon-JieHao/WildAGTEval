# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import search_restaurants


class SearchRestaurants(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], query: Optional[str] = None, 
               location: Optional[str] = None, cuisine_type: Optional[str] = None,
               price_range: Optional[str] = None, rating_min: Optional[float] = None,
               sort_by: Optional[str] = None, limit: int = 10) -> str:
        """
        Search restaurants based on various criteria.
        
        Args:
            data: The data dictionary containing restaurants
            query: Search term for restaurant name
            location: Filter by location
            cuisine_type: Filter by cuisine type
            price_range: Filter by price range ($, $$, $$$, $$$$)
            rating_min: Minimum rating filter
            sort_by: Field to sort by ('rating', 'name', 'price')
            limit: Maximum number of results to return
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if price_range is not None and price_range not in ["$", "$$", "$$$", "$$$$"]:
            return json.dumps({
                "success": False,
                "message": "Price range must be one of: $, $$, $$$, $$$$"
            })
            
        if rating_min is not None and (rating_min < 0 or rating_min > 5):
            return json.dumps({
                "success": False,
                "message": "Rating minimum must be between 0 and 5"
            })
            
        if sort_by is not None and sort_by not in ["rating", "name", "price"]:
            return json.dumps({
                "success": False,
                "message": "Sort option must be one of: rating, name, price"
            })
            
        if limit is not None and limit < 1:
            limit = 10  # Default to 10 if invalid
        
        # Search restaurants
        results = search_restaurants(data, query, location, cuisine_type, price_range, rating_min, sort_by, limit)
        
        # Format results for display (compact version)
        formatted_results = []
        for restaurant in results:
            formatted_results.append({
                "restaurant_id": restaurant.get("restaurant_id"),
                "name": restaurant.get("name"),
                "location": restaurant.get("location"),
                "cuisine_types": restaurant.get("cuisine_types", []),
                "price_range": restaurant.get("price_range"),
                "rating": restaurant.get("rating"),
                "delivery_available": restaurant.get("delivery_available", False),
                "menu_item_count": len(restaurant.get("menu", []))
            })
        
        # Create cuisine list from results for user convenience
        cuisines = []
        for restaurant in results:
            cuisines.extend(restaurant.get("cuisine_types", []))
        cuisines = sorted(list(set(cuisines)))
        
        return json.dumps({
            "success": True,
            "count": len(results),
            "cuisines": cuisines,
            "results": formatted_results,
            "message": f"Found {len(results)} restaurant(s)" if results else "No restaurants found matching your criteria"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_restaurants",
                "description": "Search for restaurants based on various criteria like name, location, cuisine type, price range, and rating. Returns a list of restaurants matching the search criteria.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "(Optional) Search term to match against restaurant names."
                        },
                        "location": {
                            "type": "string",
                            "description": "(Optional) Filter restaurants by location."
                        },
                        "cuisine_type": {
                            "type": "string",
                            "description": "(Optional) Filter restaurants by cuisine type (e.g., 'Italian', 'Japanese', 'Indian')."
                        },
                        "price_range": {
                            "type": "string",
                            "enum": ["$", "$$", "$$$", "$$$$"],
                            "description": "(Optional) Filter restaurants by price range from $ (least expensive) to $$$$ (most expensive)."
                        },
                        "rating_min": {
                            "type": "number",
                            "description": "(Optional) Minimum rating filter (0-5). Only restaurants with ratings greater than or equal to this value will be returned."
                        },
                        "sort_by": {
                            "type": "string",
                            "enum": ["rating", "name", "price"],
                            "description": "(Optional) Sort results by: 'rating' (highest rated first), 'name' (alphabetical), or 'price' (lowest to highest)."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "(Optional) Maximum number of results to return. Defaults to 10."
                        }
                    }
                },
                "error_cases": [
                    "Invalid price range: price_range must be one of '$', '$$', '$$$', or '$$$$'",
                    "Invalid rating minimum: rating_min must be between 0 and 5",
                    "Invalid sort option: sort_by must be one of 'rating', 'name', or 'price'",
                    "No restaurants found: No restaurants match the search criteria"
                ]
            }
        }
