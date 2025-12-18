# Copyright CulinaryControlEnv

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.base_env import BaseEnvironment
from common.shared_memory_service import SharedMemoryService
from CulinaryControlEnv.tools import ALL_TOOLS
from CulinaryControlEnv.rules import RULES
from CulinaryControlEnv.wiki import WIKI
from CulinaryControlEnv.helpers import (
    find_recipe_by_id, search_recipes, get_user_favorite_recipes,
    find_restaurant_by_id, search_restaurants, get_restaurant_menu,
    get_user_meal_plans, get_user_delivery_orders, find_delivery_order_by_id
)
from typing import Optional, Dict, Any, List


class CulinaryControlEnv(BaseEnvironment):
    """
    Culinary Control Environment for recipe management, meal planning,
    restaurant search, and delivery order management.
    """
    
    def __init__(self):
        """
        Initialize the Culinary Control Environment.
        """
        self.rules = RULES
        self.wiki = WIKI
        super().__init__()  # This will call _initialize_environment_data and _load_tools
        
    def _initialize_environment_data(self) -> None:
        """Initialize CulinaryControlEnv-specific data structures"""
        # Initialize recipe data if it doesn't exist
        if "recipes" not in self.data:
            self.data["recipes"] = []
        
        # Initialize restaurant data if it doesn't exist
        if "restaurants" not in self.data:
            self.data["restaurants"] = []
        
        # Initialize favorite recipes data if it doesn't exist
        if "favorite_recipes" not in self.data:
            self.data["favorite_recipes"] = []
        
        # Initialize favorite restaurants data if it doesn't exist
        if "favorite_restaurants" not in self.data:
            self.data["favorite_restaurants"] = []
        
        # Initialize meal plans data if it doesn't exist
        if "meal_plans" not in self.data:
            self.data["meal_plans"] = []
        
        # Initialize delivery orders data if it doesn't exist
        if "delivery_orders" not in self.data:
            self.data["delivery_orders"] = []
            
        # Ensure user culinary info structure exists
        for user in self.data.get("users", []):
            if "culinary_info" not in user:
                user["culinary_info"] = {
                    "dietary_preferences": [],
                    "allergies": [],
                    "cooking_skill_level": "beginner",
                    "favorite_cuisines": []
                }
    
    def _load_tools(self) -> Dict[str, Any]:
        """Load CulinaryControlEnv-specific tools"""
        # Convert from list to dict format expected by base class
        tools_dict = {}
        for tool in ALL_TOOLS:
            tool_info = tool.get_info()
            if 'function' in tool_info and 'name' in tool_info['function']:
                tool_name = tool_info['function']['name']
                tools_dict[tool_name] = tool
        return tools_dict
    
    def _save_data(self) -> None:
        """
        Legacy method required by base class.
        In the new design, data is only stored in memory and never saved to disk.
        """
        # Don't save to disk, just update memory service
        self.memory_service.update_data(self.data)
    
    def get_tool_info(self) -> List[Dict[str, Any]]:
        """
        Get information about all available tools.
        
        Returns:
            List of tool information dictionaries
        """
        return [tool.get_info() for tool in self.tools.values()]
    
    def get_rules(self) -> List[str]:
        """
        Get all rules for the environment.
        
        Returns:
            List of rule strings
        """
        return self.rules
    
    def get_wiki(self) -> str:
        """
        Get the wiki documentation for the environment.
        
        Returns:
            Wiki documentation string
        """
        return self.wiki
    
    def search_recipes(self, query: Optional[str] = None, 
                       cuisine: Optional[str] = None, 
                       difficulty: Optional[str] = None,
                       max_time: Optional[int] = None,
                       dietary: Optional[List[str]] = None,
                       sort_by: Optional[str] = None,
                       limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for recipes based on various criteria.
        
        Args:
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
        return search_recipes(
            self.data, 
            query=query, 
            cuisine=cuisine, 
            difficulty=difficulty, 
            max_time=max_time, 
            dietary=dietary, 
            sort_by=sort_by, 
            limit=limit
        )
    
    def get_recipe(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific recipe.
        
        Args:
            recipe_id: The ID of the recipe to retrieve
            
        Returns:
            The recipe dictionary if found, None otherwise
        """
        return find_recipe_by_id(self.data, recipe_id)
    
    def search_restaurants(self, query: Optional[str] = None,
                          location: Optional[str] = None,
                          cuisine_type: Optional[str] = None,
                          price_range: Optional[str] = None,
                          rating_min: Optional[float] = None,
                          sort_by: Optional[str] = None,
                          limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for restaurants based on various criteria.
        
        Args:
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
        return search_restaurants(
            self.data,
            query=query,
            location=location,
            cuisine_type=cuisine_type,
            price_range=price_range,
            rating_min=rating_min,
            sort_by=sort_by,
            limit=limit
        )
    
    def get_restaurant(self, restaurant_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific restaurant.
        
        Args:
            restaurant_id: The ID of the restaurant to retrieve
            
        Returns:
            The restaurant dictionary if found, None otherwise
        """
        return find_restaurant_by_id(self.data, restaurant_id)
    
    def get_restaurant_menu(self, restaurant_id: str) -> List[Dict[str, Any]]:
        """
        Get the menu for a specific restaurant.
        
        Args:
            restaurant_id: The ID of the restaurant
            
        Returns:
            List of menu items for the restaurant
        """
        return get_restaurant_menu(self.data, restaurant_id)
    
    def get_user_favorite_recipes(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get favorite recipes for a user.
        
        Args:
            user_id: The user ID (if None, uses current user)
            
        Returns:
            List of favorite recipe dictionaries for the user
        """
        return get_user_favorite_recipes(self.data, user_id)
    
    def get_user_meal_plans(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get meal plans for a user.
        
        Args:
            user_id: The user ID (if None, uses current user)
            
        Returns:
            List of meal plan dictionaries for the user
        """
        return get_user_meal_plans(self.data, user_id)
    
    def get_user_delivery_orders(self, user_id: Optional[str] = None, 
                                limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get delivery orders for a user.
        
        Args:
            user_id: The user ID (if None, uses current user)
            limit: Maximum number of orders to return
            
        Returns:
            List of delivery order dictionaries for the user
        """
        return get_user_delivery_orders(self.data, user_id, limit)
    
    def get_delivery_order(self, order_id: str, user_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific delivery order.
        
        Args:
            order_id: The ID of the order to retrieve
            user_id: If provided, ensures the order belongs to this user
            
        Returns:
            The order dictionary if found, None otherwise
        """
        return find_delivery_order_by_id(self.data, order_id, user_id)
