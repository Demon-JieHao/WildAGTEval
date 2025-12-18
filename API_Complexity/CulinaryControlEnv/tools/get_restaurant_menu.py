# Copyright CulinaryControlEnv

import json
from typing import Any, Dict, List, Optional
from CulinaryControlEnv.tool import Tool
from CulinaryControlEnv.helpers import find_restaurant_by_id, get_restaurant_menu


class GetRestaurantMenu(Tool):
    @staticmethod
    def _extract_restaurant_id_number(restaurant_id: str) -> int:
        """Extract number from restaurant_id (e.g., rest1 -> 1, rest25 -> 25)"""
        import re
        match = re.match(r'rest(\d+)', restaurant_id)
        return int(match.group(1)) if match else 0
    
    @staticmethod
    def _extract_item_id_number(item_id: str) -> int:
        """Extract number from item_id (e.g., item1 -> 1, item9 -> 9)"""
        import re
        match = re.match(r'item(\d+)', item_id)
        return int(match.group(1)) if match else 0
    
    @staticmethod
    def _get_sponsored_restaurants(restaurant_num, data):
        """Get multiple sponsored restaurants based on deterministic selection"""
        all_restaurants = data.get("restaurants", [])
        if not all_restaurants:
            return []
        
        # Generate 2 sponsored restaurants (reduced from 3)
        sponsor_indices = [(restaurant_num * 23 + i * 41) % len(all_restaurants) for i in range(2)]
        sponsored_restaurants = []
        
        for i, idx in enumerate(sponsor_indices):
            sponsored_restaurant = all_restaurants[idx].copy()
            sponsor_restaurant_id = sponsored_restaurant.get("restaurant_id")
            
            # Get real menu items from this restaurant
            from CulinaryControlEnv.helpers import get_restaurant_menu
            sponsor_menu_items = get_restaurant_menu(data, sponsor_restaurant_id)
            
            # Organize menu items by category (same format as main menu)
            menu_by_category = {}
            for item in sponsor_menu_items[:6]:  # Take up to 6 items
                category = item.get("category", "Uncategorized")
                if category not in menu_by_category:
                    menu_by_category[category] = []
                
                # Remove specific fields to reduce length
                simplified_item = item.copy()
                simplified_item.pop("category", None)
                simplified_item.pop("popular", None)
                simplified_item.pop("description", None)
                
                menu_by_category[category].append(simplified_item)
            
            # Extract the list of categories
            categories = sorted(menu_by_category.keys())
            
            sponsored_restaurant = {
                "restaurant_id": sponsor_restaurant_id,
                "name": sponsored_restaurant.get("name"),
                "rating": sponsored_restaurant.get("rating"),
                "cuisine_types": sponsored_restaurant.get("cuisine_types", [])[:2],
                "menu_categories": categories,
                "menu": menu_by_category
            }
            sponsored_restaurants.append(sponsored_restaurant)
        
        return sponsored_restaurants
    
    @staticmethod
    def _get_ai_recommended_restaurants(restaurant_num, data):
        """Get AI recommended restaurants based on deterministic selection"""
        all_restaurants = data.get("restaurants", [])
        if not all_restaurants:
            return []
        
        # Generate 3 AI recommended restaurants (reduced from 4)
        rec_indices = [(restaurant_num * 31 + i * 37) % len(all_restaurants) for i in range(1)]
        recommendations = []
        
        for i, idx in enumerate(rec_indices):
            rec_restaurant = all_restaurants[idx].copy()
            rec_restaurant_id = rec_restaurant.get("restaurant_id")
            
            # Get real menu items from this restaurant
            from CulinaryControlEnv.helpers import get_restaurant_menu
            rec_menu_items = get_restaurant_menu(data, rec_restaurant_id)
            
            # Organize menu items by category (same format as main menu)
            menu_by_category = {}
            for item in rec_menu_items[:6]:  # Take up to 6 items
                category = item.get("category", "Uncategorized")
                if category not in menu_by_category:
                    menu_by_category[category] = []
                
                # Remove specific fields to reduce length
                simplified_item = item.copy()
                simplified_item.pop("category", None)
                simplified_item.pop("popular", None)
                simplified_item.pop("description", None)
                
                menu_by_category[category].append(simplified_item)
            
            # Extract the list of categories
            categories = sorted(menu_by_category.keys())
            
            rec_restaurant = {
                "restaurant_id": rec_restaurant_id,
                "name": rec_restaurant.get("name"),
                "rating": rec_restaurant.get("rating"),
                "cuisine_types": rec_restaurant.get("cuisine_types", [])[:1],
                "menu_categories": categories,
                "menu": menu_by_category
            }
            recommendations.append(rec_restaurant)
        
        return recommendations
    
    @staticmethod
    def _get_similar_restaurants(restaurant_num, data):
        """Get similar restaurants based on deterministic selection"""
        all_restaurants = data.get("restaurants", [])
        if not all_restaurants:
            return []
        
        # Generate 2 similar restaurants (reduced from 3)
        similar_indices = [(restaurant_num * 13 + i * 17) % len(all_restaurants) for i in range(1)]
        similar_restaurants = []
        
        for i, idx in enumerate(similar_indices):
            similar_restaurant = all_restaurants[idx].copy()
            similar_restaurant_id = similar_restaurant.get("restaurant_id")
            
            # Get real menu items from this restaurant
            from CulinaryControlEnv.helpers import get_restaurant_menu
            similar_menu_items = get_restaurant_menu(data, similar_restaurant_id)
            
            # Organize menu items by category (same format as main menu)
            menu_by_category = {}
            for item in similar_menu_items[:6]:  # Take up to 6 items
                category = item.get("category", "Uncategorized")
                if category not in menu_by_category:
                    menu_by_category[category] = []
                
                # Remove specific fields to reduce length
                simplified_item = item.copy()
                simplified_item.pop("category", None)
                simplified_item.pop("popular", None)
                simplified_item.pop("description", None)
                
                menu_by_category[category].append(simplified_item)
            
            # Extract the list of categories
            categories = sorted(menu_by_category.keys())
            
            similar_restaurant = {
                "restaurant_id": similar_restaurant_id,
                "name": similar_restaurant.get("name"),
                "rating": similar_restaurant.get("rating"),
                "menu_categories": categories,
                "menu": menu_by_category
            }
            similar_restaurants.append(similar_restaurant)
        
        return similar_restaurants
    
    @staticmethod
    def _enrich_menu_item_with_marketing_metadata(item, restaurant_id):
        """Add simplified marketing analytics to menu item using deterministic generation"""
        enriched_item = item.copy()
        
        # Extract numbers for deterministic calculations
        rest_num = GetRestaurantMenu._extract_restaurant_id_number(restaurant_id)
        item_num = GetRestaurantMenu._extract_item_id_number(item.get('item_id', 'item0'))
        
        # Create combined seed: rest1+item1 = 1*1000+1 = 1001
        seed = rest_num * 1000 + item_num
        
        # Add only 5 essential marketing fields (reduced from 15+)
        enriched_item["popularity_score"] = 60 + (seed * 7) % 39  # 60-98
        enriched_item["trending_velocity"] = round(0.1 + ((seed * 11) % 240) / 100, 2)  # 0.1-2.5
        enriched_item["demographic_appeal"] = 70 + (seed * 13) % 26  # Single value instead of object
        enriched_item["profit_margin_tier"] = ["high", "medium", "low"][(seed * 23) % 3]
        enriched_item["cross_sell_recommendation"] = f"item_{100 + (seed * 43) % 900}"  # Single item instead of array
        
        return enriched_item

    @staticmethod
    def invoke(data: Dict[str, Any], restaurant_id: str) -> str:
        """
        Get the menu for a specific restaurant.
        
        Args:
            data: The data dictionary containing restaurants
            restaurant_id: ID of the restaurant to get the menu for
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_partially_irrelevant_information_enabled = os.getenv('ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_RESTAURANT_MENU', 'false').lower() == 'true'
        
        # Input validation
        if not restaurant_id:
            return json.dumps({
                "success": False,
                "message": "Restaurant ID is required"
            })
        
        # Find the restaurant
        restaurant = find_restaurant_by_id(data, restaurant_id)
        if not restaurant:
            return json.dumps({
                "success": False,
                "message": f"Restaurant with ID '{restaurant_id}' not found"
            })
        
        # Get the menu
        menu_items = get_restaurant_menu(data, restaurant_id)
        
        # Organize menu items by category
        menu_by_category = {}
        for item in menu_items:
            category = item.get("category", "Uncategorized")
            if category not in menu_by_category:
                menu_by_category[category] = []
            
            # Keep original items completely intact - no changes at all
            original_item = item.copy()  # Complete copy of original item
            menu_by_category[category].append(original_item)
        
        # Add confusion items from other restaurants to same categories
        if uncertainty_partially_irrelevant_information_enabled:
            restaurant_num = GetRestaurantMenu._extract_restaurant_id_number(restaurant_id)
            
            # Get items from sponsored restaurants
            sponsor_indices = [(restaurant_num * 23 + i * 41) % len(data.get("restaurants", [])) for i in range(2)]
            for i, idx in enumerate(sponsor_indices):
                if idx < len(data.get("restaurants", [])):
                    sponsor_restaurant = data.get("restaurants", [])[idx]
                    sponsor_items = get_restaurant_menu(data, sponsor_restaurant.get("restaurant_id"))
                    for item in sponsor_items[:4]:  # Add 4 items per sponsor (increased from 2)
                        category = item.get("category", "Uncategorized")
                        if category in menu_by_category:
                            simplified_item = item.copy()
                            simplified_item.pop("category", None)
                            simplified_item.pop("popular", None)
                            simplified_item.pop("description", None)
                            # Add source restaurant info
                            simplified_item["source_restaurant_id"] = sponsor_restaurant.get("restaurant_id")
                            simplified_item["source_restaurant_name"] = sponsor_restaurant.get("name")
                            simplified_item["source_type"] = "sponsored"
                            menu_by_category[category].append(simplified_item)
            
            # Get items from AI recommended restaurants
            rec_indices = [(restaurant_num * 31 + i * 37) % len(data.get("restaurants", [])) for i in range(2)]
            for i, idx in enumerate(rec_indices):
                if idx < len(data.get("restaurants", [])):
                    rec_restaurant = data.get("restaurants", [])[idx]
                    rec_items = get_restaurant_menu(data, rec_restaurant.get("restaurant_id"))
                    for item in rec_items[:4]:  # Add 4 items per recommendation (increased from 2)
                        category = item.get("category", "Uncategorized")
                        if category in menu_by_category:
                            simplified_item = item.copy()
                            simplified_item.pop("category", None)
                            simplified_item.pop("popular", None)
                            simplified_item.pop("description", None)
                            # Add source restaurant info
                            simplified_item["source_restaurant_id"] = rec_restaurant.get("restaurant_id")
                            simplified_item["source_restaurant_name"] = rec_restaurant.get("name")
                            simplified_item["source_type"] = "ai_recommended"
                            menu_by_category[category].append(simplified_item)
        
        # Extract the list of categories
        categories = sorted(menu_by_category.keys())
        
        # Check if the current user has this restaurant as a favorite
        is_favorite = False
        user_id = data.get("current_user")
        if user_id:
            favorite_restaurants = data.get("favorite_restaurants", [])
            for favorite in favorite_restaurants:
                if favorite.get("user_id") == user_id and favorite.get("restaurant_id") == restaurant_id:
                    is_favorite = True
                    break
        
        # Build base response
        response_data = {
            "success": True,
            "message": f"Retrieved menu for {restaurant.get('name')}"
        }
        
        if uncertainty_partially_irrelevant_information_enabled:
            # Extract restaurant number for deterministic calculations
            restaurant_num = GetRestaurantMenu._extract_restaurant_id_number(restaurant_id)
            
            # 1. SPONSORED RESTAURANTS (first) - now 2 restaurants
            response_data["sponsored_restaurants"] = GetRestaurantMenu._get_sponsored_restaurants(restaurant_num, data)
            
            # 2. ORIGINAL RESTAURANT INFO (second) - with mixed menu items
            response_data["restaurant_id"] = restaurant_id
            response_data["restaurant_name"] = restaurant.get("name")
            response_data["description"] = restaurant.get("description")
            response_data["price_range"] = restaurant.get("price_range")
            response_data["rating"] = restaurant.get("rating")
            response_data["cuisine_types"] = restaurant.get("cuisine_types", [])
            response_data["delivery_available"] = restaurant.get("delivery_available", False)
            response_data["menu_categories"] = categories
            response_data["menu"] = menu_by_category  # This now contains mixed items
            response_data["is_favorite"] = is_favorite
            
            # 3. AI RECOMMENDATIONS (third) - now 3 restaurants
            response_data["ai_recommendations"] = GetRestaurantMenu._get_ai_recommended_restaurants(restaurant_num, data)
            
            # 4. SIMILAR RESTAURANTS (fourth) - now 2 restaurants
            response_data["similar_restaurants"] = GetRestaurantMenu._get_similar_restaurants(restaurant_num, data)
        else:
            # Normal mode - compact response
            response_data.update({
                "restaurant_id": restaurant_id,
                "restaurant_name": restaurant.get("name"),
                "description": restaurant.get("description"),
                "price_range": restaurant.get("price_range"),
                "rating": restaurant.get("rating"),
                "cuisine_types": restaurant.get("cuisine_types", []),
                "delivery_available": restaurant.get("delivery_available", False),
                "menu_categories": categories,
                "menu": menu_by_category,
                "is_favorite": is_favorite
            })
        
        return json.dumps(response_data)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_restaurant_menu",
                "description": "Get the complete menu for a specific restaurant, including item details, prices, and categories.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "restaurant_id": {
                            "type": "string",
                            "description": "The unique identifier of the restaurant to retrieve menu for."
                        }
                    },
                    "required": ["restaurant_id"]
                },
                "error_cases": [
                    "Restaurant ID is missing: The restaurant_id parameter is required.",
                    "Restaurant not found: No restaurant exists with the provided ID."
                ]
            }
        }
