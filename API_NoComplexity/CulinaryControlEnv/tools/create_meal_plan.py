# Copyright CulinaryControlEnv

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import generate_meal_plan_id, get_current_timestamp


class CreateMealPlan(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], name: str, start_date: str, end_date: str,
              description: Optional[str] = None, 
              meals_per_day: Optional[List[str]] = None) -> str:
        """
        Create a new meal plan for a specified date range.
        
        Args:
            data: The data dictionary
            name: Name of the meal plan
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            description: Optional description of the meal plan
            meals_per_day: List of meal types to include (breakfast, lunch, dinner, snack)
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_informational_notice_enabled = os.getenv('ENABLE__INFORMATIONAL_NOTICE__CREATE_MEAL_PLAN', 'false').lower() == 'true'
        
        # Input validation
        if not name:
            return json.dumps({
                "success": False,
                "message": "Meal plan name is required"
            })
            
        if not start_date or not end_date:
            return json.dumps({
                "success": False,
                "message": "Start and end dates are required"
            })
        
        # Validate date format and range
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            
            if end < start:
                return json.dumps({
                    "success": False,
                    "message": "End date must be on or after start date"
                })
                
            # Limit to reasonable range (e.g., 4 weeks)
            if (end - start).days > 28:
                return json.dumps({
                    "success": False,
                    "message": "Meal plan duration cannot exceed 28 days"
                })
        except ValueError:
            return json.dumps({
                "success": False,
                "message": "Invalid date format. Use YYYY-MM-DD"
            })
            
        # Validate meal types
        valid_meal_types = ["breakfast", "lunch", "dinner", "snack"]
        if meals_per_day:
            for meal in meals_per_day:
                if meal not in valid_meal_types:
                    return json.dumps({
                        "success": False,
                        "message": f"Invalid meal type: {meal}. Valid types are: {', '.join(valid_meal_types)}"
                    })
        else:
            # Default to all three main meals
            meals_per_day = ["breakfast", "lunch", "dinner"]
        
        # Check if the current user is set
        current_user = data.get("current_user")
        if not current_user:
            return json.dumps({
                "success": False,
                "message": "No user is currently selected"
            })
        
        # Generate a sequential meal plan ID
        plan_id = generate_meal_plan_id(data)
        
        # Generate meal plan structure
        meal_days = []
        current_date = start
        while current_date <= end:
            date_str = current_date.strftime("%Y-%m-%d")
            
            # Create empty meal slots structure
            meals_structure = {}
            for meal_type in meals_per_day:
                meals_structure[meal_type] = None
                
            meal_days.append({
                "day": date_str,
                "meals": meals_structure
            })
            
            current_date += timedelta(days=1)
        
        # Create the new meal plan
        new_meal_plan = {
            "plan_id": plan_id,
            "user_id": current_user,
            "name": name,
            "description": description or f"Meal plan for {start_date} to {end_date}",
            "start_date": start_date,
            "end_date": end_date,
            "created_at": get_current_timestamp(),
            "meals": meal_days,
            "notes": ""
        }
        
        # Add plan to data
        if "meal_plans" not in data:
            data["meal_plans"] = []
            
        data["meal_plans"].append(new_meal_plan)
        
        ### MODIFIED: Build success response with optional informational notices ###
        response = {
            "success": True,
            "plan_id": plan_id,
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "meals_per_day": meals_per_day,
            "days_count": len(meal_days),
            "message": f"Meal plan '{name}' created successfully"
        }
        
        if uncertainty_informational_notice_enabled:
            ### ADDED: Include helpful but potentially confusing informational notices ###
            response["info"] = "FYI: create_meal_plan_with_templates() is also available if you'd like to use pre-designed meal templates for common dietary preferences like vegetarian, keto, or Mediterranean diets"
            response["nutritional_note"] = "The create_nutritionally_balanced_meal_plan() function also exists and automatically calculates macronutrients and ensures daily nutritional requirements are met across all meals"
            response["recipe_tip"] = "Just so you know, create_meal_plan_with_recipes() can directly link recipes from our database to each meal slot, which some users find convenient for grocery planning"
            response["background_info"] = "This basic meal plan structure works well for general planning. For reference, we also have specialized functions for meal prep planning, budget-conscious meal planning, and family-style meal planning that handle portion sizing automatically"
            response["feature_notice"] = "Your meal plan has been created with empty meal slots. The auto_populate_meal_plan() function is available if you'd like to automatically fill these slots based on dietary preferences and past meal history"
        
        # Return response
        return json.dumps(response)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "create_meal_plan",
                "description": "Create a new meal plan for a specified date range. The meal plan will be a structured schedule for planning meals over multiple days.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the meal plan (e.g., 'Weekly Family Dinner Plan', 'Vegetarian Week')."
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Start date of the meal plan in YYYY-MM-DD format."
                        },
                        "end_date": {
                            "type": "string",
                            "description": "End date of the meal plan in YYYY-MM-DD format."
                        },
                        "description": {
                            "type": "string",
                            "description": "(Optional) Description of the meal plan."
                        },
                        "meals_per_day": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["breakfast", "lunch", "dinner", "snack"]
                            },
                            "description": "(Optional) List of meal types to include each day. Defaults to ['breakfast', 'lunch', 'dinner']."
                        }
                    },
                    "required": ["name", "start_date", "end_date"]
                },
                "error_cases": [
                    "Name is missing: The meal plan name is required.",
                    "Invalid dates: Start and end dates must be valid and in YYYY-MM-DD format.",
                    "Invalid date range: End date must be on or after start date.",
                    "Plan duration too long: Meal plan duration cannot exceed 28 days.",
                    "Invalid meal type: Meal types must be one of 'breakfast', 'lunch', 'dinner', or 'snack'.",
                    "No user selected: A user must be selected to create a meal plan."
                ]
            }
        }
