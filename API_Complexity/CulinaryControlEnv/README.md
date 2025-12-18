# CulinaryControlEnv

CulinaryControlEnv is a comprehensive environment for managing culinary-related activities. It provides tools for searching recipes, planning meals, finding restaurants, and ordering food delivery.

## Features

### Recipe Management
- Search for recipes based on various criteria (name, cuisine, dietary restrictions, etc.)
- View detailed recipe information including ingredients and instructions
- Save favorite recipes for quick access
- Create custom recipes with personalized ingredients and instructions

### Meal Planning
- Create structured meal plans spanning multiple days
- Schedule specific recipes for breakfast, lunch, dinner, and snacks
- Get personalized meal suggestions based on preferences and dietary needs

### Restaurant Interaction
- Search for restaurants based on location, cuisine type, and other criteria
- View detailed restaurant information and menus
- Save favorite restaurants for quick access

### Food Delivery
- Place food delivery orders from supported restaurants
- View order details and status
- Track delivery progress in real-time

## Tools Available

### Recipe Tools
- `search_recipes`: Find recipes matching specific criteria
- `get_recipe_details`: Get comprehensive information about a recipe
- `save_favorite_recipe`: Add a recipe to your favorites
- `create_custom_recipe`: Create your own custom recipe

### Meal Planning Tools
- `create_meal_plan`: Create a structured meal plan for a date range
- `schedule_meal`: Add a specific recipe to a meal plan
- `get_meal_suggestions`: Get personalized recipe suggestions

### Restaurant Tools
- `search_restaurants`: Find restaurants matching specific criteria
- `get_restaurant_menu`: View a restaurant's menu items

### Delivery Tools
- `place_delivery_order`: Order food delivery from a restaurant
- `view_delivery_order`: View details of a placed order
- `track_delivery_order`: Check the status of a delivery

## Integration with Other Environments

CulinaryControlEnv is designed to work seamlessly with other environments through the shared memory service. It maintains its own specific data collections while integrating with the centralized user system.

## Usage Example

```python
# Import the environment
from CulinaryControlEnv import CulinaryControlEnv

# Create and initialize environment
culinary_env = CulinaryControlEnv()

# Set current user
culinary_env.set_current_user("user1")

# Search for recipes
result = culinary_env.invoke_tool("search_recipes", query="pasta", cuisine="Italian")

# Get detailed information about a recipe
recipe_details = culinary_env.invoke_tool("get_recipe_details", recipe_id="recipe1")

# Create a meal plan
meal_plan = culinary_env.invoke_tool("create_meal_plan", 
                                    name="Weekly Dinner Plan",
                                    start_date="2025-06-15",
                                    end_date="2025-06-21")

# Schedule a meal in the plan
culinary_env.invoke_tool("schedule_meal",
                         plan_id=meal_plan["plan_id"],
                         recipe_id="recipe1",
                         day="2025-06-15",
                         meal_type="dinner")
```

## Data Storage

The environment uses several JSON data files:
- `recipes.json`: Collection of recipes with detailed information
- `restaurants.json`: Restaurant information with menus
- `favorite_recipes.json`: User-specific recipe favorites
- `favorite_restaurants.json`: User-specific restaurant favorites
- `meal_plans.json`: User-created meal plans
- `delivery_orders.json`: Order details and status information

All user-specific data references the centralized user system through `user_id` fields.
