# Copyright CulinaryControlEnv

from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import uuid


def find_recipe_by_id(data: Dict[str, Any], recipe_id: str) -> Optional[Dict[str, Any]]:
    """Find a recipe by its ID.
    
    Args:
        data: The data dictionary containing recipes
        recipe_id: The ID of the recipe to find
        
    Returns:
        The recipe dictionary if found, None otherwise
    """
    for recipe in data.get("recipes", []):
        if recipe.get("recipe_id") == recipe_id:
            return recipe
    return None


def search_recipes(data: Dict[str, Any], query: str = None, cuisine: str = None, 
                   difficulty: str = None, max_time: int = None, 
                   dietary: List[str] = None, sort_by: str = None, 
                   limit: int = 10) -> List[Dict[str, Any]]:
    """Search recipes based on various criteria.
    
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
        List of matching recipe dictionaries
    """
    recipes = data.get("recipes", [])
    results = []
    
    # Filter recipes
    for recipe in recipes:
        # Filter by query (name or description)
        if query and query.lower() not in recipe.get("name", "").lower() and \
           query.lower() not in recipe.get("description", "").lower():
            continue
            
        # Filter by cuisine
        if cuisine and recipe.get("cuisine") != cuisine:
            continue
            
        # Filter by difficulty level
        if difficulty and recipe.get("difficulty") != difficulty:
            continue
            
        # Filter by preparation time
        if max_time is not None and recipe.get("preparation_time", 0) > max_time:
            continue
            
        # Filter by dietary preferences
        if dietary:
            recipe_dietary = recipe.get("dietary_info", [])
            # Skip if any required dietary preference is not satisfied
            if not all(pref in recipe_dietary for pref in dietary):
                continue
            
        results.append(recipe)
    
    # Sort results if requested
    if sort_by:
        if sort_by == "time":
            results.sort(key=lambda r: r.get("preparation_time", 0))
        elif sort_by == "rating":
            results.sort(key=lambda r: r.get("rating", 0), reverse=True)
        elif sort_by == "name":
            results.sort(key=lambda r: r.get("name", ""))
    
    # Limit results
    if limit and limit > 0:
        results = results[:limit]
        
    return results


def find_restaurant_by_id(data: Dict[str, Any], restaurant_id: str) -> Optional[Dict[str, Any]]:
    """Find a restaurant by its ID.
    
    Args:
        data: The data dictionary containing restaurants
        restaurant_id: The ID of the restaurant to find
        
    Returns:
        The restaurant dictionary if found, None otherwise
    """
    for restaurant in data.get("restaurants", []):
        if restaurant.get("restaurant_id") == restaurant_id:
            return restaurant
    return None


def search_restaurants(data: Dict[str, Any], query: str = None, location: str = None,
                       cuisine_type: str = None, price_range: str = None,
                       rating_min: float = None, sort_by: str = None,
                       limit: int = 10) -> List[Dict[str, Any]]:
    """Search restaurants based on various criteria.
    
    Args:
        data: The data dictionary containing restaurants
        query: Search term for restaurant name
        location: Filter by location
        cuisine_type: Filter by cuisine type
        price_range: Filter by price range ($, $$, $$$, $$$$)
        rating_min: Minimum rating filter
        sort_by: Field to sort by ('rating', 'name', 'price')
        limit: Maximum number of results to return
        
    Returns:
        List of matching restaurant dictionaries
    """
    restaurants = data.get("restaurants", [])
    results = []
    
    # Filter restaurants
    for restaurant in restaurants:
        # Filter by query (name)
        if query and query.lower() not in restaurant.get("name", "").lower():
            continue
            
        # Filter by location
        if location and location.lower() not in restaurant.get("location", "").lower():
            continue
            
        # Filter by cuisine type
        if cuisine_type and cuisine_type not in restaurant.get("cuisine_types", []):
            continue
            
        # Filter by price range
        if price_range and restaurant.get("price_range") != price_range:
            continue
            
        # Filter by rating
        if rating_min is not None and restaurant.get("rating", 0) < rating_min:
            continue
            
        results.append(restaurant)
    
    # Sort results if requested
    if sort_by:
        if sort_by == "rating":
            results.sort(key=lambda r: r.get("rating", 0), reverse=True)
        elif sort_by == "name":
            results.sort(key=lambda r: r.get("name", ""))
        elif sort_by == "price":
            # Convert price range to number of $ signs for sorting
            def price_to_int(price_str):
                return len(price_str) if price_str else 0
            results.sort(key=lambda r: price_to_int(r.get("price_range", "")))
    
    # Limit results
    if limit and limit > 0:
        results = results[:limit]
        
    return results


def get_user_favorite_recipes(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get favorite recipes for a user.
    
    Args:
        data: The data dictionary containing favorite recipes
        user_id: The user ID (if None, uses current user)
        
    Returns:
        List of favorite recipe dictionaries for the user
    """
    if not user_id:
        user_id = data.get("current_user")
    if not user_id:
        return []
        
    return [item for item in data.get("favorite_recipes", []) if item.get("user_id") == user_id]


def save_favorite_recipe(data: Dict[str, Any], recipe_id: str, user_id: Optional[str] = None) -> bool:
    """Save a recipe to a user's favorites.
    
    Args:
        data: The data dictionary
        recipe_id: The ID of the recipe to save
        user_id: The user ID (if None, uses current user)
        
    Returns:
        True if successful, False otherwise
    """
    if not user_id:
        user_id = data.get("current_user")
    if not user_id:
        return False
        
    # Check if the recipe exists
    recipe = find_recipe_by_id(data, recipe_id)
    if not recipe:
        return False
        
    # Check if the recipe is already in favorites
    favorites = get_user_favorite_recipes(data, user_id)
    for favorite in favorites:
        if favorite.get("recipe_id") == recipe_id:
            return True  # Already a favorite
    
    # Add to favorites
    if "favorite_recipes" not in data:
        data["favorite_recipes"] = []
        
    data["favorite_recipes"].append({
        "user_id": user_id,
        "recipe_id": recipe_id,
        "date_added": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    })
    
    return True


def get_user_meal_plans(data: Dict[str, Any], user_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get meal plans for a user.
    
    Args:
        data: The data dictionary containing meal plans
        user_id: The user ID (if None, uses current user)
        
    Returns:
        List of meal plan dictionaries for the user
    """
    if not user_id:
        user_id = data.get("current_user")
    if not user_id:
        return []
        
    return [plan for plan in data.get("meal_plans", []) if plan.get("user_id") == user_id]


def get_restaurant_menu(data: Dict[str, Any], restaurant_id: str) -> List[Dict[str, Any]]:
    """Get the menu for a restaurant.
    
    Args:
        data: The data dictionary containing restaurants
        restaurant_id: The ID of the restaurant
        
    Returns:
        The menu items list if found, empty list otherwise
    """
    restaurant = find_restaurant_by_id(data, restaurant_id)
    if not restaurant:
        return []
        
    return restaurant.get("menu", [])


def get_user_delivery_orders(data: Dict[str, Any], user_id: Optional[str] = None, limit: int = None) -> List[Dict[str, Any]]:
    """Get delivery orders for a user.
    
    Args:
        data: The data dictionary containing delivery orders
        user_id: The user ID (if None, uses current user)
        limit: Maximum number of orders to return
        
    Returns:
        List of delivery order dictionaries for the user
    """
    if not user_id:
        user_id = data.get("current_user")
    if not user_id:
        return []
        
    orders = [order for order in data.get("delivery_orders", []) if order.get("user_id") == user_id]
    
    # Sort by order date (newest first)
    orders.sort(key=lambda o: o.get("order_time", ""), reverse=True)
    
    if limit and limit > 0:
        return orders[:limit]
    return orders


def find_delivery_order_by_id(data: Dict[str, Any], order_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Find a delivery order by its ID.
    
    Args:
        data: The data dictionary containing delivery orders
        order_id: The ID of the order to find
        user_id: If provided, ensures the order belongs to this user
        
    Returns:
        The order dictionary if found, None otherwise
    """
    if not user_id:
        user_id = data.get("current_user")
        
    for order in data.get("delivery_orders", []):
        if order.get("order_id") == order_id:
            # If user_id is provided, check that the order belongs to this user
            if user_id and order.get("user_id") != user_id:
                continue
            return order
    return None


def generate_meal_plan_id(data: Dict[str, Any]) -> str:
    """Generate a sequential meal plan ID."""
    # Initialize meal_plans if it does not exist
    if "meal_plans" not in data:
        data["meal_plans"] = []
    
    # Extract only numeric parts from existing plan_id values
    existing_ids = []
    for plan in data["meal_plans"]:
        if "plan_id" in plan and plan["plan_id"].startswith("plan"):
            try:
                # Extract just the numeric part from IDs like 'plan1', 'plan2'
                num = int(plan["plan_id"].replace("plan", ""))
                existing_ids.append(num)
            except ValueError:
                # Ignore entries that fail to parse
                continue
    
    # Start from 1 if there are no existing numbers; otherwise use max + 1
    next_num = 1
    if existing_ids:
        next_num = max(existing_ids) + 1
    
    # Return the new ID
    return f"plan{next_num}"


def generate_order_id(data: Dict[str, Any]) -> str:
    """Generate a sequential delivery order ID."""
    # Initialize delivery_orders if it does not exist
    if "delivery_orders" not in data:
        data["delivery_orders"] = []
    
    # Extract only numeric parts from existing order_id values
    existing_ids = []
    for order in data["delivery_orders"]:
        if "order_id" in order and order["order_id"].startswith("dorder"):
            try:
                # Extract just the numeric part from IDs like 'dorder1', 'dorder2'
                num = int(order["order_id"].replace("dorder", ""))
                existing_ids.append(num)
            except ValueError:
                # Ignore entries that fail to parse
                continue
    
    # Start from 1 if there are no existing numbers; otherwise use max + 1
    next_num = 1
    if existing_ids:
        next_num = max(existing_ids) + 1
    
    # Return the new ID
    return f"dorder{next_num}"


def generate_recipe_id(data: Dict[str, Any]) -> str:
    """Generate a sequential recipe ID."""
    # Initialize recipes if it does not exist
    if "recipes" not in data:
        data["recipes"] = []
    
    # Extract only numeric parts from existing recipe_id values
    existing_ids = []
    for recipe in data["recipes"]:
        if "recipe_id" in recipe and recipe["recipe_id"].startswith("recipe"):
            try:
                # Extract just the numeric part from IDs like 'recipe1', 'recipe2'
                num = int(recipe["recipe_id"].replace("recipe", ""))
                existing_ids.append(num)
            except ValueError:
                # Ignore entries that fail to parse
                continue
    
    # Start from 1 if there are no existing numbers; otherwise use max + 1
    next_num = 1
    if existing_ids:
        next_num = max(existing_ids) + 1
    
    # Return the new ID
    return f"recipe{next_num}"


def get_current_timestamp() -> str:
    """Get the current timestamp in ISO format."""
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
