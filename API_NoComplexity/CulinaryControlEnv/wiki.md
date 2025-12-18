# CulinaryControlEnv Documentation

CulinaryControlEnv provides tools for searching, managing, and interacting with recipes, restaurants, and delivery services. It allows users to find recipes based on various criteria, manage meal plans, search for restaurants, view menus, and place delivery orders.

## Concepts

### Recipes
Recipes are the core content type for cooking-related functionality. Each recipe includes:
- Name, description, and cuisine type
- Ingredients list with quantities
- Step-by-step cooking instructions
- Preparation time and difficulty level
- Dietary information (vegetarian, vegan, gluten-free, etc.)
- Rating and number of reviews

### Meal Plans
Meal plans help users organize their cooking schedule. A meal plan consists of:
- Name and description
- Date range (start/end dates)
- Meals per day (breakfast, lunch, dinner, snacks)
- Recipe IDs assigned to specific meals and days

### Restaurants
Restaurant entities include:
- Name, location, and contact information
- Cuisine types
- Price range indicator
- Rating and number of reviews
- Operation hours
- Menu items with prices and descriptions

### Delivery Orders
Delivery orders track food ordered from restaurants:
- Order ID and timestamp
- Restaurant information
- Ordered items with quantities and prices
- Delivery address and contact information
- Status (placed, preparing, in-transit, delivered)
- Total cost including taxes and delivery fees

## Tools

### Recipe Management

#### search_recipes
Find recipes matching specified criteria such as name, cuisine type, difficulty level, preparation time, and dietary restrictions.

#### get_recipe_details
Retrieve complete details for a specific recipe including ingredients, instructions, nutritional information, and reviews.

#### save_favorite_recipe
Save a recipe to the current user's favorites list for easy access later.

#### create_custom_recipe
Create a new recipe with custom name, ingredients, instructions, and other details.

### Meal Planning

#### create_meal_plan
Create a new meal plan for a specified date range with assigned recipes.

#### get_meal_suggestions
Get personalized meal suggestions based on dietary preferences, previously enjoyed recipes, or nutritional requirements.

#### schedule_meal
Add a specific recipe to a meal plan for a particular day and meal type.

### Restaurant Interaction

#### search_restaurants
Find restaurants based on location, cuisine type, price range, and rating.

#### get_restaurant_menu
View the complete menu for a specific restaurant including pricing and item descriptions.

### Order Management

#### place_delivery_order
Place a food delivery order from a restaurant with specified items and delivery address.


#### track_delivery_order
Check the current status and estimated delivery time of an food delivery order.

## Best Practices

1. **User Context**: Always operate in the context of the current user for personalized experiences.

2. **Dietary Awareness**: Respect dietary restrictions and preferences when recommending recipes or restaurants.

3. **Time Management**: Consider preparation time when suggesting recipes, especially for daily meal planning.

4. **Location Awareness**: Use the user's location when searching for restaurants to ensure delivery availability.

5. **Error Handling**: Properly handle cases where recipes, restaurants, or orders are not found.

## Usage Examples

### Finding and Saving a Recipe

```python
# Search for Italian pasta recipes
recipes = invoke_tool("search_recipes", query="pasta", cuisine="italian", limit=5)

# Get details for a specific recipe
recipe_details = invoke_tool("get_recipe_details", recipe_id="recipe123")

# Save recipe to favorites
invoke_tool("save_favorite_recipe", recipe_id="recipe123")
```

### Creating a Meal Plan

```python
# Create a weekly meal plan
meal_plan = invoke_tool("create_meal_plan", 
                        name="Healthy Week", 
                        start_date="2025-06-12", 
                        end_date="2025-06-18", 
                        meals_per_day=["breakfast", "lunch", "dinner"])

# Get some meal suggestions
suggestions = invoke_tool("get_meal_suggestions", 
                          dietary=["vegetarian"], 
                          meal_type="dinner")

# Schedule a meal in the plan
invoke_tool("schedule_meal", 
            plan_id=meal_plan["plan_id"], 
            recipe_id="recipe456", 
            day="2025-06-13", 
            meal_type="dinner")
```

### Ordering Food Delivery

```python
# Search for nearby restaurants
restaurants = invoke_tool("search_restaurants", 
                          cuisine_type="japanese", 
                          location="New York", 
                          price_range="$$")

# Get the menu for a restaurant
menu = invoke_tool("get_restaurant_menu", restaurant_id="rest789")

# Place a delivery order
order = invoke_tool("place_delivery_order",
                    restaurant_id="rest789",
                    items=[{"item_id": "item1", "quantity": 2}, 
                          {"item_id": "item2", "quantity": 1}],
                    delivery_address="123 Main St")

# Track the order status
status = invoke_tool("track_delivery_order", order_id=order["order_id"])
```

## Data Structure

The CulinaryControlEnv maintains several data collections:

1. `recipes`: Collection of recipe objects
2. `favorite_recipes`: User-specific recipe favorites
3. `meal_plans`: User-created meal planning schedules
4. `restaurants`: Restaurant information with menus
5. `delivery_orders`: Order records with status information

All user-specific data references the centralized user system through `user_id` fields, ensuring integration with other environments.