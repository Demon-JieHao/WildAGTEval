# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import find_recipe_by_id


class ScheduleMeal(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], plan_id: str, recipe_id: str, 
              day: str, meal_type: str, notes: Optional[str] = None) -> str:
        """
        Add a specific recipe to a meal plan for a particular day and meal type.
        
        Args:
            data: The data dictionary
            plan_id: ID of the meal plan
            recipe_id: ID of the recipe to add
            day: Date in format YYYY-MM-DD
            meal_type: Type of meal (breakfast, lunch, dinner, snack)
            notes: Optional notes about the meal
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if not plan_id:
            return json.dumps({
                "success": False,
                "message": "Meal plan ID is required"
            })
            
        if not recipe_id:
            return json.dumps({
                "success": False,
                "message": "Recipe ID is required"
            })
            
        if not day:
            return json.dumps({
                "success": False,
                "message": "Day is required"
            })
            
        if not meal_type:
            return json.dumps({
                "success": False,
                "message": "Meal type is required"
            })
            
        # Validate meal type
        valid_meal_types = ["breakfast", "lunch", "dinner", "snack"]
        if meal_type not in valid_meal_types:
            return json.dumps({
                "success": False,
                "message": f"Invalid meal type: {meal_type}. Valid types are: {', '.join(valid_meal_types)}"
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
            
        # Find the meal plan for the current user
        meal_plan = None
        for plan in data.get("meal_plans", []):
            if plan.get("plan_id") == plan_id and plan.get("user_id") == current_user:
                meal_plan = plan
                break
                
        if not meal_plan:
            return json.dumps({
                "success": False,
                "message": f"Meal plan with ID '{plan_id}' not found or does not belong to the current user"
            })
            
        # Check if the day exists in the meal plan
        day_entry = None
        for entry in meal_plan.get("meals", []):
            if entry.get("day") == day:
                day_entry = entry
                break
                
        if not day_entry:
            return json.dumps({
                "success": False,
                "message": f"Day '{day}' not found in the meal plan"
            })
            
        # Check if the meal type exists for this day
        if meal_type not in day_entry.get("meals", {}):
            return json.dumps({
                "success": False,
                "message": f"Meal type '{meal_type}' not found in the meal plan for day '{day}'"
            })
            
        # Update the meal plan
        day_entry["meals"][meal_type] = {
            "recipe_id": recipe_id,
            "notes": notes or ""
        }
        
        # Success response
        return json.dumps({
            "success": True,
            "plan_id": plan_id,
            "day": day,
            "meal_type": meal_type,
            "recipe_id": recipe_id,
            "recipe_name": recipe.get("name"),
            "message": f"Added {recipe.get('name')} to {meal_type} on {day}"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "schedule_meal",
                "description": "Add a specific recipe to a meal plan for a particular day and meal type. This allows users to build a complete meal plan by assigning recipes to specific days and meal slots.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "plan_id": {
                            "type": "string",
                            "description": "The unique identifier of the meal plan to update."
                        },
                        "recipe_id": {
                            "type": "string",
                            "description": "The unique identifier of the recipe to add to the plan."
                        },
                        "day": {
                            "type": "string",
                            "description": "The day to schedule the meal for, in YYYY-MM-DD format."
                        },
                        "meal_type": {
                            "type": "string",
                            "enum": ["breakfast", "lunch", "dinner", "snack"],
                            "description": "The type of meal to schedule."
                        },
                        "notes": {
                            "type": "string",
                            "description": "(Optional) Additional notes about the meal, such as preparation instructions or variations."
                        }
                    },
                    "required": ["plan_id", "recipe_id", "day", "meal_type"]
                },
                "error_cases": [
                    "Meal plan ID is missing: The plan_id parameter is required.",
                    "Recipe ID is missing: The recipe_id parameter is required.",
                    "Day is missing: The day parameter is required.",
                    "Meal type is missing: The meal_type parameter is required.",
                    "Invalid meal type: Meal type must be one of 'breakfast', 'lunch', 'dinner', or 'snack'.",
                    "Recipe not found: No recipe exists with the provided ID.",
                    "Meal plan not found: No meal plan exists with the provided ID for the current user.",
                    "Day not found: The specified day is not included in the meal plan.",
                    "Meal type not found: The specified meal type is not included in the meal plan for the specified day.",
                    "No user selected: A user must be selected to schedule a meal."
                ]
            }
        }
