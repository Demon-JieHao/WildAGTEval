# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import find_recipe_by_id


class GetRecipeDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], recipe_id: str) -> str:
        """
        Get detailed information about a specific recipe.
        
        Args:
            data: The data dictionary containing recipes
            recipe_id: The ID of the recipe to retrieve details for
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if not recipe_id:
            return json.dumps({
                "success": False,
                "message": "Recipe ID is required"
            })
        
        # Find the recipe
        recipe = find_recipe_by_id(data, recipe_id)
        if not recipe:
            return json.dumps({
                "success": False,
                "message": f"Recipe with ID '{recipe_id}' not found"
            })
        
        # Check if recipe is in user's favorites
        is_favorite = False
        user_id = data.get("current_user")
        if user_id:
            favorite_recipes = data.get("favorite_recipes", [])
            for favorite in favorite_recipes:
                if favorite.get("user_id") == user_id and favorite.get("recipe_id") == recipe_id:
                    is_favorite = True
                    break
        
        return json.dumps({
            "success": True,
            "recipe_id": recipe.get("recipe_id"),
            "name": recipe.get("name"),
            "description": recipe.get("description"),
            "cuisine": recipe.get("cuisine"),
            "difficulty": recipe.get("difficulty"),
            "preparation_time": recipe.get("preparation_time"),
            "cooking_time": recipe.get("cooking_time"),
            "servings": recipe.get("servings"),
            "ingredients": recipe.get("ingredients", []),
            "instructions": recipe.get("instructions", []),
            "nutrition_info": recipe.get("nutrition_info", {}),
            "dietary_info": recipe.get("dietary_info", []),
            "rating": recipe.get("rating"),
            "reviews_count": recipe.get("reviews_count", 0),
            "image_url": recipe.get("image_url", ""),
            "tags": recipe.get("tags", []),
            "author": recipe.get("author", ""),
            "is_favorite": is_favorite,
            "formatted": f"{recipe.get('name')} - {recipe.get('description')[:100]}... ({recipe.get('preparation_time', 0)} min, {recipe.get('difficulty', 'unknown')} difficulty)"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_recipe_details",
                "description": "Get detailed information about a specific recipe including ingredients, instructions, nutritional information, and reviews.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipe_id": {
                            "type": "string",
                            "description": "The unique identifier of the recipe to retrieve details for."
                        }
                    },
                    "required": ["recipe_id"]
                },
                "error_cases": [
                    "Recipe ID is missing: The recipe_id parameter is required.",
                    "Recipe not found: No recipe exists with the provided ID."
                ]
            }
        }
