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
        similar_indices = [(recipe_num * 13 + i * 17) % len(all_recipes) for i in range(1)]
        similar_recipes = []
        
        for i, idx in enumerate(similar_indices):
            similar_recipe = all_recipes[idx].copy()
            similar_recipe["similarity_score"] = round(0.65 + (i * 0.15), 2)
            similar_recipe["match_type"] = ["ingredient_based", "cuisine_based", "difficulty_based"][i % 3]
            similar_recipes.append(similar_recipe)
        
        return similar_recipes
    
    @staticmethod
    def _get_sponsored_content(recipe_num, data):
        """Get sponsored recipe content based on deterministic selection"""
        all_recipes = data.get("recipes", [])
        if not all_recipes:
            return {}
        
        # Select sponsored recipe
        sponsor_idx = (recipe_num * 23) % len(all_recipes)
        sponsored_recipe = all_recipes[sponsor_idx].copy()
        
        # Add sponsor-specific metadata
        sponsored_recipe["sponsor_name"] = ["CookingBrand", "FoodCorp", "RecipePartner"][recipe_num % 3]
        sponsored_recipe["promotion_type"] = ["featured", "premium", "trending"][recipe_num % 3]
        sponsored_recipe["click_through_rate"] = round(0.12 + (recipe_num * 0.03) % 0.2, 3)
        
        return sponsored_recipe
    
    @staticmethod
    def _get_ai_recommendations(recipe_num, data):
        """Get AI recommended recipes based on deterministic selection"""
        all_recipes = data.get("recipes", [])
        if not all_recipes:
            return []
        
        # Select recommended recipes
        rec_indices = [(recipe_num * 31 + i * 37) % len(all_recipes) for i in range(2)]
        recommendations = []
        
        for i, idx in enumerate(rec_indices):
            rec_recipe = all_recipes[idx].copy()
            rec_recipe["recommendation_score"] = round(0.75 + (i * 0.05), 2)
            rec_recipe["recommendation_reason"] = [
                "based_on_past_preferences", 
                "trending_in_your_area", 
                "seasonal_suggestion", 
                "complements_your_diet"
            ][i % 4]
            recommendations.append(rec_recipe)
        
        return recommendations
    
    @staticmethod
    def _enrich_recipe_with_marketing_metadata(recipe, data):
        """Add marketing analytics and personalization data to recipe using deterministic generation"""
        enriched_recipe = {}
        
        # Extract recipe number for deterministic calculations
        recipe_num = SearchRecipes._extract_recipe_id_number(recipe.get('recipe_id', 'recipe0'))
        

        # 5. Original recipe information (placed after distracting content)
        enriched_recipe["recipe_id"] = recipe.get("recipe_id")
        enriched_recipe["name"] = recipe.get("name")
        enriched_recipe["description"] = recipe.get("description")
        enriched_recipe["cuisine"] = recipe.get("cuisine")
        enriched_recipe["difficulty"] = recipe.get("difficulty")
        enriched_recipe["preparation_time"] = recipe.get("preparation_time")
        enriched_recipe["cooking_time"] = recipe.get("cooking_time")
        enriched_recipe["servings"] = recipe.get("servings")
        enriched_recipe["ingredients"] = recipe.get("ingredients")
        enriched_recipe["instructions"] = recipe.get("instructions")
        enriched_recipe["nutrition_info"] = recipe.get("nutrition_info")
        enriched_recipe["dietary_info"] = recipe.get("dietary_info", [])
        enriched_recipe["rating"] = recipe.get("rating")
        enriched_recipe["reviews_count"] = recipe.get("reviews_count")
        enriched_recipe["image_url"] = recipe.get("image_url")
        enriched_recipe["tags"] = recipe.get("tags", [])

        # 1. Similar recipes first (before original recipe info)
        enriched_recipe["similar_recipes"] = SearchRecipes._get_similar_recipes(recipe_num, data)
        
        # 2. Sponsored content
        enriched_recipe["sponsored_content"] = SearchRecipes._get_sponsored_content(recipe_num, data)
        
        # 3. Marketing and engagement analytics
        enriched_recipe["user_engagement_score"] = round(85 + (recipe_num * 7) % 15, 1)  # 85.0-100.0
        enriched_recipe["trending_coefficient"] = round(0.65 + (recipe_num * 11) % 35 / 100, 2)  # 0.65-1.00
        enriched_recipe["seasonal_boost_active"] = bool((recipe_num * 13) % 3 == 0)
        enriched_recipe["promotional_tier"] = ["standard", "featured", "premium"][(recipe_num * 17) % 3]
        
        # 4. AI recommendations (more distracting content)
        enriched_recipe["ai_recommendations"] = SearchRecipes._get_ai_recommendations(recipe_num, data)
                
        # 6. More marketing metadata after original recipe
        enriched_recipe["personalization_metadata"] = {
            "demographic_appeal_index": {
                "millennials": round(70 + (recipe_num * 19) % 30, 1),  # 70.0-100.0
                "gen_x": round(65 + (recipe_num * 23) % 35, 1),        # 65.0-100.0
                "boomers": round(60 + (recipe_num * 29) % 40, 1)       # 60.0-100.0
            },
            "ml_recommendation_weight": round(0.7 + (recipe_num * 31) % 30 / 100, 3),  # 0.7-1.0
            "user_preference_match_score": round(75 + (recipe_num * 37) % 25, 1)  # 75.0-100.0
        }
        
        # 7. Content performance metrics
        enriched_recipe["view_to_cook_conversion"] = round(0.15 + (recipe_num * 41) % 20 / 100, 3)  # 0.15-0.35
        
        # Calculate session duration deterministically
        minutes = 3 + (recipe_num * 43) % 5  # 3-7 minutes
        seconds = (recipe_num * 47) % 60     # 0-59 seconds
        enriched_recipe["average_session_duration"] = f"{minutes}m {seconds}s"
        
        enriched_recipe["cross_platform_performance"] = {
            "mobile": round(80 + (recipe_num * 53) % 20, 1),   # 80.0-100.0
            "desktop": round(75 + (recipe_num * 59) % 25, 1),  # 75.0-100.0
            "tablet": round(70 + (recipe_num * 61) % 30, 1)    # 70.0-100.0
        }
        
        # 8. Supply chain and inventory data
        enriched_recipe["ingredient_availability_score"] = round(0.85 + (recipe_num * 67) % 15 / 100, 2)  # 0.85-1.00
        enriched_recipe["supplier_diversity_index"] = round(0.6 + (recipe_num * 71) % 40 / 100, 2)  # 0.6-1.0
        enriched_recipe["cost_efficiency_rating"] = ["A", "B", "C"][(recipe_num * 73) % 3]
        
        # 9. Content metadata
        month = 1 + (recipe_num * 79) % 12  # 1-12
        day = 1 + (recipe_num * 83) % 28    # 1-28
        enriched_recipe["last_content_refresh"] = f"2024-{month:02d}-{day:02d}"
        
        enriched_recipe["content_quality_score"] = round(85 + (recipe_num * 89) % 15, 1)  # 85.0-100.0
        enriched_recipe["seo_optimization_level"] = ["basic", "enhanced", "premium"][(recipe_num * 97) % 3]
        
        # 10. Related content suggestions
        enriched_recipe["related_content_suggestions"] = [
            f"recipe_{(recipe_num * 101 + i * 103) % 1000}" for i in range(3)
        ]
        
        return enriched_recipe

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
        formatted_results = []
        for recipe in results:
            if uncertainty_partially_irrelevant_information_enabled:
                ### ADDED: Mix extensive irrelevant metadata with core recipe data ###
                enriched_recipe = SearchRecipes._enrich_recipe_with_marketing_metadata(recipe, data)
                formatted_results.append(enriched_recipe)
                ### END ADDED ###
            else:
                # Original compact version
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
