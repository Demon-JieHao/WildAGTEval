instruction="""
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
Check the current status and estimated delivery time of an order.

## Best Practices

1. **User Context**: Always operate in the context of the current user for personalized experiences.

2. **Dietary Awareness**: Respect dietary restrictions and preferences when recommending recipes or restaurants.

3. **Time Management**: Consider preparation time when suggesting recipes, especially for daily meal planning.

4. **Location Awareness**: Use the user's location when searching for restaurants to ensure delivery availability.

5. **Error Handling**: Properly handle cases where recipes, restaurants, or orders are not found.

"""
