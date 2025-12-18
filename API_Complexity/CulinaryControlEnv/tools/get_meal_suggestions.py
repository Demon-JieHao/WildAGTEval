# Copyright CulinaryControlEnv

import json
import random
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import search_recipes


class GetMealSuggestions(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], meal_type: Optional[str] = None, 
               dietary: Optional[List[str]] = None, cuisine: Optional[str] = None,
               max_time: Optional[int] = None, count: int = 3) -> str:
        """
        Get personalized meal suggestions based on preferences and dietary restrictions.
        
        Args:
            data: The data dictionary containing recipes
            meal_type: Type of meal (breakfast, lunch, dinner, snack)
            dietary: List of dietary preferences (vegetarian, vegan, etc.)
            cuisine: Preferred cuisine type
            max_time: Maximum preparation time in minutes
            count: Number of suggestions to return
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if meal_type and meal_type not in ["breakfast", "lunch", "dinner", "snack"]:
            return json.dumps({
                "success": False,
                "message": "Meal type must be one of: breakfast, lunch, dinner, snack"
            })
            
        if count < 1 or count > 10:
            count = 3  # Default to 3 if invalid
        
        # Check if the current user is set
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user is currently selected"
            })
        
        # Get user culinary preferences
        user_prefs = {}
        for user in data.get("users", []):
            if user["user_id"] == current_user:
                user_prefs = user.get("culinary_info", {})
                break
        
        # Combine user dietary preferences with requested dietary preferences
        user_dietary = user_prefs.get("dietary_preferences", [])
        if dietary:
            # Add requested dietary preferences without duplicates
            combined_dietary = list(set(user_dietary + dietary))
        else:
            combined_dietary = user_dietary
            
        # Get user's favorite cuisines if none specified
        if not cuisine and "favorite_cuisines" in user_prefs:
            # Randomly pick one of the user's favorite cuisines
            favorite_cuisines = user_prefs.get("favorite_cuisines", [])
            if favorite_cuisines:
                cuisine = random.choice(favorite_cuisines)
        
        # Search for recipes based on combined preferences
        search_results = search_recipes(
            data,
            query=None,
            cuisine=cuisine,
            difficulty=None,
            max_time=max_time,
            dietary=combined_dietary if combined_dietary else None,
            sort_by="rating",
            limit=50  # Get a larger pool to filter from
        )
        
        # Filter by meal type if specified
        if meal_type:
            filtered_results = []
            for recipe in search_results:
                tags = recipe.get("tags", [])
                if meal_type in tags:
                    filtered_results.append(recipe)
            
            if filtered_results:
                search_results = filtered_results
        
        # Get user's favorite recipes
        favorite_recipe_ids = []
        for favorite in data.get("favorite_recipes", []):
            if favorite.get("user_id") == current_user:
                favorite_recipe_ids.append(favorite.get("recipe_id"))
        
        # Prioritize recipes that aren't already favorites
        non_favorite_results = [r for r in search_results if r.get("recipe_id") not in favorite_recipe_ids]
        
        # Select recipes
        suggestions = []
        if len(non_favorite_results) >= count:
            # Prefer recipes that aren't already favorites
            suggestions = random.sample(non_favorite_results, count)
        elif search_results:
            # Fall back to any matching recipes, including favorites
            if len(search_results) > count:
                suggestions = random.sample(search_results, count)
            else:
                suggestions = search_results
        
        # Format suggestions
        formatted_suggestions = []
        for recipe in suggestions:
            formatted_suggestions.append({
                "recipe_id": recipe.get("recipe_id"),
                "name": recipe.get("name"),
                "cuisine": recipe.get("cuisine"),
                "difficulty": recipe.get("difficulty"),
                "preparation_time": recipe.get("preparation_time"),
                "dietary_info": recipe.get("dietary_info", []),
                "rating": recipe.get("rating"),
                "is_favorite": recipe.get("recipe_id") in favorite_recipe_ids
            })
        
        # Create response message
        if meal_type:
            message = f"Suggested recipes for {meal_type}"
        else:
            message = "Suggested recipes based on your preferences"
            
        if cuisine:
            message += f" ({cuisine} cuisine)"
        
        if not formatted_suggestions:
            message = "No matching recipes found based on your criteria"
        
        return json.dumps({
            "success": True,
            "count": len(formatted_suggestions),
            "suggestions": formatted_suggestions,
            "dietary_info": combined_dietary,
            "user_preferences_applied": bool(user_prefs),
            "message": message
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_meal_suggestions",
                "description": "Get personalized meal suggestions based on the user's preferences, dietary restrictions, and other criteria. The suggestions are prioritized based on the user's past favorites and dietary needs.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "meal_type": {
                            "type": "string",
                            "enum": ["breakfast", "lunch", "dinner", "snack"],
                            "description": "(Optional) Type of meal to get suggestions for."
                        },
                        "dietary": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "(Optional) List of dietary preferences to filter by (e.g., 'vegetarian', 'vegan', 'gluten-free'). This will be combined with the user's stored preferences."
                        },
                        "cuisine": {
                            "type": "string",
                            "description": "(Optional) Preferred cuisine type (e.g., 'Italian', 'Mexican'). If not specified, the system may suggest recipes from the user's favorite cuisines."
                        },
                        "max_time": {
                            "type": "integer",
                            "description": "(Optional) Maximum preparation time in minutes. Only recipes that can be prepared within this time will be suggested."
                        },
                        "count": {
                            "type": "integer",
                            "description": "(Optional) Number of suggestions to return. Default is 3, maximum is 10."
                        }
                    }
                },
                "error_cases": [
                    "Invalid meal type: meal_type must be one of 'breakfast', 'lunch', 'dinner', or 'snack'",
                    "Invalid count: count must be between 1 and 10",
                    "No user selected: A user must be selected to get personalized suggestions",
                    "No matching recipes: No recipes match the specified criteria"
                ]
            }
        }
