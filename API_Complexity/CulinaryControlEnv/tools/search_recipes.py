# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import search_recipes


class SearchRecipes(Tool):
    @staticmethod
    def _extract_recipe_id_number(recipe_id: str) -> int:
        """Extract number from recipe_id (e.g., recipe1 -> 1, recipe40 -> 40)"""
        import re
        match = re.match(r'recipe(\d+)', recipe_id)
        return int(match.group(1)) if match else 0
    
    @staticmethod
    def _get_similar_recipes(recipe_num, data):
        """Get similar recipes based on deterministic selection"""
        all_recipes = data.get("recipes", [])
        if not all_recipes:
            return []
        
        # Use deterministic selection to get similar recipes
        similar_indices = [(recipe_num * 13 + i * 17) % len(all_recipes) for i in range(4)]
        similar_recipes = []
        
        for i, idx in enumerate(similar_indices):
            similar_recipe = {
                "recipe_id": all_recipes[idx].get("recipe_id"),
                "name": all_recipes[idx].get("name"),
                "cuisine": all_recipes[idx].get("cuisine"),
                "difficulty": all_recipes[idx].get("difficulty"),
                "preparation_time": all_recipes[idx].get("preparation_time"),
                "rating": all_recipes[idx].get("rating"),
                "dietary_info": all_recipes[idx].get("dietary_info", [])
            }
            similar_recipes.append(similar_recipe)
        
        return similar_recipes
    
    @staticmethod
    def _get_sponsored_content(recipe_num, data):
        """Get sponsored recipe content based on deterministic selection"""
        all_recipes = data.get("recipes", [])
        if not all_recipes:
            return []
        
        # Select 4 sponsored recipes
        sponsor_indices = [(recipe_num * 23 + i * 29) % len(all_recipes) for i in range(4)]
        sponsored_recipes = []
        
        for i, idx in enumerate(sponsor_indices):
            sponsored_recipe = {
                "recipe_id": all_recipes[idx].get("recipe_id"),
                "name": all_recipes[idx].get("name"),
                "cuisine": all_recipes[idx].get("cuisine"),
                "difficulty": all_recipes[idx].get("difficulty"),
                "preparation_time": all_recipes[idx].get("preparation_time"),
                "rating": all_recipes[idx].get("rating"),
                "dietary_info": all_recipes[idx].get("dietary_info", [])
            }
            sponsored_recipes.append(sponsored_recipe)
        
        return sponsored_recipes
    
    @staticmethod
    def _get_ai_recommendations(recipe_num, data):
        """Get AI recommended recipes based on deterministic selection"""
        all_recipes = data.get("recipes", [])
        if not all_recipes:
            return []
        
        # Select recommended recipes
        rec_indices = [(recipe_num * 31 + i * 37) % len(all_recipes) for i in range(5)]
        recommendations = []
        
        for i, idx in enumerate(rec_indices):
            rec_recipe = {
                "recipe_id": all_recipes[idx].get("recipe_id"),
                "name": all_recipes[idx].get("name"),
                "cuisine": all_recipes[idx].get("cuisine"),
                "difficulty": all_recipes[idx].get("difficulty"),
                "preparation_time": all_recipes[idx].get("preparation_time"),
                "rating": all_recipes[idx].get("rating"),
                "dietary_info": all_recipes[idx].get("dietary_info", [])
            }
            recommendations.append(rec_recipe)
        
        return recommendations
    
    @staticmethod
    def _mix_all_recipes_with_source_types(original_recipes, data):
        """Mix original recipes with sponsored, similar, and AI recommended recipes"""
        mixed_results = []
        
        # Calculate how many additional recipes to add to reach ~40 total
        target_total = 40
        num_original = len(original_recipes)
        additional_needed = max(0, target_total - num_original)
        
        # Distribute additional recipes across categories
        if additional_needed > 0:
            similar_count = additional_needed // 3
            sponsored_count = additional_needed // 3
            ai_count = additional_needed - similar_count - sponsored_count
        else:
            similar_count = sponsored_count = ai_count = 0
        
        # Add fixed number of additional recipes regardless of original count
        all_recipes = data.get("recipes", [])
        if all_recipes:
            # 1. Add sponsored content recipes first
            for i in range(sponsored_count):
                idx = (i * 23 + 29) % len(all_recipes)
                sponsored_recipe = {
                    "recipe_id": all_recipes[idx].get("recipe_id"),
                    "name": all_recipes[idx].get("name"),
                    "cuisine": all_recipes[idx].get("cuisine"),
                    "difficulty": all_recipes[idx].get("difficulty"),
                    "preparation_time": all_recipes[idx].get("preparation_time"),
                    "rating": all_recipes[idx].get("rating"),
                    "dietary_info": all_recipes[idx].get("dietary_info", []),
                    "source_type": "sponsored_content"
                }
                mixed_results.append(sponsored_recipe)
        
        # 2. Add original search results
        for recipe in original_recipes:
            original_recipe = {
                "recipe_id": recipe.get("recipe_id"),
                "name": recipe.get("name"),
                "cuisine": recipe.get("cuisine"),
                "difficulty": recipe.get("difficulty"),
                "preparation_time": recipe.get("preparation_time"),
                "rating": recipe.get("rating"),
                "dietary_info": recipe.get("dietary_info", []),
                "source_type": "search_result"
            }
            mixed_results.append(original_recipe)
        
        if all_recipes:
            # 3. Add similar recipes
            for i in range(similar_count):
                idx = (i * 13 + 17) % len(all_recipes)
                similar_recipe = {
                    "recipe_id": all_recipes[idx].get("recipe_id"),
                    "name": all_recipes[idx].get("name"),
                    "cuisine": all_recipes[idx].get("cuisine"),
                    "difficulty": all_recipes[idx].get("difficulty"),
                    "preparation_time": all_recipes[idx].get("preparation_time"),
                    "rating": all_recipes[idx].get("rating"),
                    "dietary_info": all_recipes[idx].get("dietary_info", []),
                    "source_type": "similar_recipes"
                }
                mixed_results.append(similar_recipe)
            
            # 4. Add AI recommended recipes
            for i in range(ai_count):
                idx = (i * 31 + 37) % len(all_recipes)
                ai_recipe = {
                    "recipe_id": all_recipes[idx].get("recipe_id"),
                    "name": all_recipes[idx].get("name"),
                    "cuisine": all_recipes[idx].get("cuisine"),
                    "difficulty": all_recipes[idx].get("difficulty"),
                    "preparation_time": all_recipes[idx].get("preparation_time"),
                    "rating": all_recipes[idx].get("rating"),
                    "dietary_info": all_recipes[idx].get("dietary_info", []),
                    "source_type": "ai_recommendations"
                }
                mixed_results.append(ai_recipe)
        
        return mixed_results

    @staticmethod
    def invoke(data: Dict[str, Any], query: Optional[str] = None,
               cuisine: Optional[str] = None, difficulty: Optional[str] = None, 
               max_time: Optional[int] = None, dietary: Optional[List[str]] = None, 
               sort_by: Optional[str] = None, limit: int = 10) -> str:
        """
        Search recipes based on various criteria.
        
        Args:
            data: The data dictionary containing recipes
            query: Search term for recipe name or description
            cuisine: Filter by cuisine type
            difficulty: Filter by difficulty level (easy, medium, hard)
            max_time: Maximum preparation time in minutes
            dietary: List of dietary preferences (vegetarian, vegan, etc.)
            sort_by: Field to sort by ('time', 'rating', 'name')
            limit: Maximum number of results to return
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_partially_irrelevant_information_enabled = os.getenv('ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__SEARCH_RECIPES', 'false').lower() == 'true'
        
        # Input validation
        if max_time is not None and max_time < 0:
            return json.dumps({
                "success": False,
                "message": "Maximum time cannot be negative"
            })
            
        if difficulty is not None and difficulty not in ["easy", "medium", "hard"]:
            return json.dumps({
                "success": False,
                "message": "Difficulty must be one of: easy, medium, hard"
            })
            
        if sort_by is not None and sort_by not in ["time", "rating", "name"]:
            return json.dumps({
                "success": False,
                "message": "Sort option must be one of: time, rating, name"
            })
            
        if limit is not None and limit < 1:
            limit = 10  # Default to 10 if invalid
        
        # Search recipes
        results = search_recipes(data, query, cuisine, difficulty, max_time, dietary, sort_by, limit)
        
        # Format results for display
        if uncertainty_partially_irrelevant_information_enabled:
            ### ADDED: Mix all recipes with source types ###
            formatted_results = SearchRecipes._mix_all_recipes_with_source_types(results, data)
            ### END ADDED ###
        else:
            # Normal mode - show only 7 fields
            formatted_results = []
            for recipe in results:
                formatted_results.append({
                    "recipe_id": recipe.get("recipe_id"),
                    "name": recipe.get("name"),
                    "cuisine": recipe.get("cuisine"),
                    "difficulty": recipe.get("difficulty"),
                    "preparation_time": recipe.get("preparation_time"),
                    "rating": recipe.get("rating"),
                    "dietary_info": recipe.get("dietary_info", [])
                })
        
        # Create cuisines list from results for user convenience
        cuisines = sorted(list(set(r.get("cuisine") for r in results if r.get("cuisine"))))
        
        # Build base response
        response_data = {
            "success": True,
            "count": len(results),
            "cuisines": cuisines,
            "results": formatted_results,
            "message": f"Found {len(results)} recipe(s)" if results else "No recipes found matching your criteria"
        }
        
        if uncertainty_partially_irrelevant_information_enabled:
            ### ADDED: Include system analytics in main response ###
            # Generate deterministic query performance metrics
            query_str = str(query or "")
            cuisine_str = str(cuisine or "")
            limit_str = str(limit)
            
            response_data["query_performance_metrics"] = {
                "response_time_ms": 45 + hash(query_str) % 100,
                "cache_hit_rate": round(0.75 + (hash(cuisine_str) % 25) / 100, 2),
                "query_complexity_score": round(2.5 + (hash(limit_str) % 3), 1)
            }
            response_data["content_freshness_indicators"] = {
                "data_staleness_hours": hash(limit_str) % 24,
                "next_refresh_scheduled": "2024-12-15T03:00:00Z",
                "content_accuracy_confidence": 0.94
            }

            response_data.pop("message")
            ### END ADDED ###
        
        return json.dumps(response_data)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_recipes",
                "description": "Search for recipes based on various criteria like name, cuisine type, difficulty level, preparation time, and dietary preferences. Returns a list of recipes matching the search criteria.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "(Optional) Search term to match against recipe names and descriptions."
                        },
                        "cuisine": {
                            "type": "string",
                            "description": "(Optional) Filter recipes by cuisine type (e.g., 'Italian', 'Japanese', 'Mexican')."
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["easy", "medium", "hard"],
                            "description": "(Optional) Filter recipes by difficulty level."
                        },
                        "max_time": {
                            "type": "integer",
                            "description": "(Optional) Maximum preparation time in minutes. Recipes that take longer than this will be excluded."
                        },
                        "dietary": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "(Optional) List of dietary preferences to filter by (e.g., 'vegetarian', 'vegan', 'gluten-free')."
                        },
                        "sort_by": {
                            "type": "string",
                            "enum": ["time", "rating", "name"],
                            "description": "(Optional) Sort results by: 'time' (fastest to prepare), 'rating' (highest rated first), or 'name' (alphabetical)."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "(Optional) Maximum number of results to return. Defaults to 10."
                        }
                    }
                },
                "error_cases": [
                    "Invalid difficulty level: difficulty must be one of 'easy', 'medium', or 'hard'",
                    "Invalid sort option: sort_by must be one of 'time', 'rating', or 'name'",
                    "Invalid limit: limit < 1",
                    "No recipes found: No recipes match the search criteria"
                ]
            }
        }
