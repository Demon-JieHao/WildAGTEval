# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import find_recipe_by_id, save_favorite_recipe, get_user_favorite_recipes


class SaveFavoriteRecipe(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], recipe_id: str) -> str:
        """
        Save a recipe to the current user's favorites.
        
        Args:
            data: The data dictionary
            recipe_id: The ID of the recipe to save
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if not recipe_id:
            return json.dumps({
                "success": False,
                "message": "Recipe ID is required"
            })
        
        # Check if the current user is set
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user is currently selected"
            })
        
        # Check if the recipe exists
        recipe = find_recipe_by_id(data, recipe_id)
        if not recipe:
            return json.dumps({
                "success": False,
                "message": f"Recipe with ID '{recipe_id}' not found"
            })
        
        # Check if the recipe is already in favorites
        favorites = get_user_favorite_recipes(data, current_user)
        already_favorite = any(fav.get("recipe_id") == recipe_id for fav in favorites)
        
        if already_favorite:
            return json.dumps({
                "success": True,
                "message": f"Recipe '{recipe.get('name')}' is already in favorites",
                "already_favorite": True
            })
        
        # Save to favorites
        success = save_favorite_recipe(data, recipe_id, current_user)
        
        if success:
            return json.dumps({
                "success": True,
                "message": f"Recipe '{recipe.get('name')}' has been added to favorites",
                "already_favorite": False,
                "recipe_id": recipe_id,
                "recipe_name": recipe.get("name")
            })
        else:
            return json.dumps({
                "success": False,
                "message": f"Failed to add recipe to favorites"
            })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "save_favorite_recipe",
                "description": "Save a recipe to the current user's favorites list. The recipe will be accessible through the user's favorite recipes collection for easy access in the future.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipe_id": {
                            "type": "string",
                            "description": "The unique identifier of the recipe to save to favorites."
                        }
                    },
                    "required": ["recipe_id"]
                },
                "error_cases": [
                    "Recipe ID is missing: The recipe_id parameter is required.",
                    "Recipe not found: No recipe exists with the provided ID.",
                    "No user selected: A user must be selected before saving favorites.",
                    "Already in favorites: The recipe is already in the user's favorites list."
                ]
            }
        }
