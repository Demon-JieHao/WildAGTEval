# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import generate_recipe_id, get_current_timestamp


class CreateCustomRecipe(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, ingredients: List[Dict[str, Any]], 
              instructions: List[str], description: Optional[str] = None,
              cuisine: Optional[str] = None, difficulty: Optional[str] = "medium",
              preparation_time: Optional[int] = None, cooking_time: Optional[int] = None,
              servings: Optional[int] = 4, dietary_info: Optional[List[str]] = None,
              tags: Optional[List[str]] = None) -> str:
        """
        Create a new custom recipe.
        
        Args:
            data: The data dictionary
            name: Name of the recipe
            ingredients: List of ingredients with quantities
            instructions: List of step-by-step instructions
            description: Brief description of the recipe
            cuisine: Type of cuisine (e.g., Italian, Mexican)
            difficulty: Difficulty level (easy, medium, hard)
            preparation_time: Time in minutes for preparation
            cooking_time: Time in minutes for cooking
            servings: Number of servings the recipe yields
            dietary_info: List of dietary specifications (e.g., vegetarian, vegan)
            tags: List of tags for the recipe
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if not name:
            return json.dumps({
                "success": False,
                "message": "Recipe name is required"
            })
            
        if not ingredients or len(ingredients) == 0:
            return json.dumps({
                "success": False,
                "message": "At least one ingredient is required"
            })
            
        if not instructions or len(instructions) == 0:
            return json.dumps({
                "success": False,
                "message": "At least one instruction step is required"
            })
            
        if difficulty is not None and difficulty not in ["easy", "medium", "hard"]:
            return json.dumps({
                "success": False,
                "message": "Difficulty must be one of: easy, medium, hard"
            })
            
        if preparation_time is not None and preparation_time < 0:
            return json.dumps({
                "success": False,
                "message": "Preparation time cannot be negative"
            })
            
        if cooking_time is not None and cooking_time < 0:
            return json.dumps({
                "success": False,
                "message": "Cooking time cannot be negative"
            })
            
        if servings is not None and servings <= 0:
            return json.dumps({
                "success": False,
                "message": "Number of servings must be positive"
            })
        
        # Check if the current user is set
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user is currently selected"
            })
        
        # Generate a sequential recipe ID
        recipe_id = generate_recipe_id(data)
        
        # Create the new recipe
        new_recipe = {
            "recipe_id": recipe_id,
            "name": name,
            "description": description or f"Custom recipe for {name}",
            "cuisine": cuisine,
            "difficulty": difficulty,
            "preparation_time": preparation_time,
            "cooking_time": cooking_time,
            "servings": servings,
            "ingredients": ingredients,
            "instructions": instructions,
            "dietary_info": dietary_info or [],
            "rating": 0,
            "reviews_count": 0,
            "tags": tags or [],
            "author": current_user,
            "created_at": get_current_timestamp(),
            "is_custom": True
        }
        
        # Add recipe to data
        if "recipes" not in data:
            data["recipes"] = []
            
        data["recipes"].append(new_recipe)
        
        # Success response
        return json.dumps({
            "success": True,
            "message": f"Custom recipe '{name}' created successfully",
            "recipe_id": recipe_id,
            "recipe": {
                "recipe_id": recipe_id,
                "name": name,
                "description": new_recipe["description"],
                "cuisine": cuisine,
                "difficulty": difficulty,
                "preparation_time": preparation_time,
                "cooking_time": cooking_time,
                "servings": servings,
                "ingredients_count": len(ingredients),
                "instructions_count": len(instructions),
                "author": current_user
            }
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_custom_recipe",
                "description": "Create a new recipe with custom ingredients, instructions, and other details. The recipe will be added to the system and can be searched, viewed, and saved like any other recipe.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the recipe."
                        },
                        "ingredients": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "Name of the ingredient"
                                    },
                                    "quantity": {
                                        "type": "string",
                                        "description": "Amount of the ingredient with unit (e.g., '2 cups', '1/2 teaspoon')"
                                    },
                                    "notes": {
                                        "type": "string",
                                        "description": "Optional notes about the ingredient (e.g., 'finely chopped', 'at room temperature')"
                                    }
                                },
                                "required": ["name", "quantity"]
                            },
                            "description": "List of ingredients with quantities."
                        },
                        "instructions": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "List of step-by-step instructions."
                        },
                        "description": {
                            "type": "string",
                            "description": "(Optional) Brief description of the recipe."
                        },
                        "cuisine": {
                            "type": "string",
                            "description": "(Optional) Type of cuisine (e.g., Italian, Mexican, Thai)."
                        },
                        "difficulty": {
                            "type": "string",
                            "enum": ["easy", "medium", "hard"],
                            "description": "(Optional) Difficulty level of the recipe. Default is 'medium'."
                        },
                        "preparation_time": {
                            "type": "integer",
                            "description": "(Optional) Time in minutes for preparation."
                        },
                        "cooking_time": {
                            "type": "integer",
                            "description": "(Optional) Time in minutes for cooking."
                        },
                        "servings": {
                            "type": "integer",
                            "description": "(Optional) Number of servings the recipe yields. Default is 4."
                        },
                        "dietary_info": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "(Optional) List of dietary specifications (e.g., 'vegetarian', 'vegan', 'gluten-free')."
                        },
                        "tags": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "(Optional) List of tags for the recipe (e.g., 'breakfast', 'quick', 'dessert')."
                        }
                    },
                    "required": ["name", "ingredients", "instructions"]
                },
                "error_cases": [
                    "Recipe name is missing: The name parameter is required.",
                    "Ingredients list is empty: At least one ingredient is required.",
                    "Instructions list is empty: At least one instruction step is required.",
                    "Invalid difficulty level: Difficulty must be one of 'easy', 'medium', or 'hard'.",
                    "Invalid time values: Preparation and cooking times cannot be negative.",
                    "Invalid servings: Number of servings must be positive.",
                    "No user selected: A user must be selected to create a recipe."
                ]
            }
        }
