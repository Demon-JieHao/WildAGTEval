# Copyright CulinaryControlEnv

"""
This module imports and defines all available tools for the Culinary Control Environment.
"""

from .search_recipes import SearchRecipes
from .get_recipe_details import GetRecipeDetails
from .save_favorite_recipe import SaveFavoriteRecipe
from .create_custom_recipe import CreateCustomRecipe
from .create_meal_plan import CreateMealPlan
from .get_meal_suggestions import GetMealSuggestions
from .schedule_meal import ScheduleMeal
from .search_restaurants import SearchRestaurants
from .get_restaurant_menu import GetRestaurantMenu
from .place_delivery_order import PlaceDeliveryOrder
from .track_delivery_order import TrackDeliveryOrder

# List of all tools available in the environment
ALL_TOOLS = [
    SearchRecipes,
    GetRecipeDetails,
    SaveFavoriteRecipe,
    CreateCustomRecipe,
    CreateMealPlan,
    GetMealSuggestions,
    ScheduleMeal,
    SearchRestaurants,
    GetRestaurantMenu,
    PlaceDeliveryOrder,
    TrackDeliveryOrder,
]

# Dictionary mapping tool names to classes
TOOLS_DICT = {
    tool.get_info()['function']['name']: tool
    for tool in ALL_TOOLS
}
