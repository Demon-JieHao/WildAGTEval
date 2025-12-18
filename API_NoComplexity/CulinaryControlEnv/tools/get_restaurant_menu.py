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
    def _get_sponsored_restaurant(restaurant_num, data):
        """Get sponsored restaurant based on deterministic selection"""
        all_restaurants = data.get("restaurants", [])
        if not all_restaurants:
            return {}
        
        # Select sponsored restaurant
        sponsor_idx = (restaurant_num * 23) % len(all_restaurants)
        sponsored_restaurant = all_restaurants[sponsor_idx].copy()
        
        # Add sponsor-specific metadata
        sponsored_restaurant["sponsor_name"] = ["FoodPartner", "RestaurantAds", "DiningNetwork"][restaurant_num % 3]
        sponsored_restaurant["promotion_type"] = ["featured", "premium", "trending"][restaurant_num % 3]
        sponsored_restaurant["advertisement_budget"] = round(1000 + (restaurant_num * 150) % 5000, 2)
        sponsored_restaurant["click_through_rate"] = round(0.05 + (restaurant_num * 0.02) % 0.15, 3)
        
        return sponsored_restaurant
    
    @staticmethod
    def _get_ai_recommended_restaurants(restaurant_num, data):
        """Get AI recommended restaurants based on deterministic selection"""
        all_restaurants = data.get("restaurants", [])
        if not all_restaurants:
            return []
        
        # Select recommended restaurants
        rec_indices = [(restaurant_num * 31 + i * 37) % len(all_restaurants) for i in range(2)]
        recommendations = []
        
        for i, idx in enumerate(rec_indices):
            rec_restaurant = all_restaurants[idx].copy()
            rec_restaurant["recommendation_score"] = round(0.7 + (i * 0.1), 2)
            rec_restaurant["recommendation_reason"] = [
                "location_based", 
                "trending_in_area", 
                "complementary_cuisine", 
                "user_preference_match"
            ][i % 4]
            recommendations.append(rec_restaurant)
        
        return recommendations
    
    @staticmethod
    def _get_similar_restaurants(restaurant_num, data):
        """Get similar restaurants based on deterministic selection"""
        all_restaurants = data.get("restaurants", [])
        if not all_restaurants:
            return []
        
        # Use deterministic selection to get similar restaurants
        similar_indices = [(restaurant_num * 13 + i * 17) % len(all_restaurants) for i in range(2)]
        similar_restaurants = []
        
        for i, idx in enumerate(similar_indices):
            similar_restaurant = all_restaurants[idx].copy()
            similar_restaurant["similarity_score"] = round(0.65 + (i * 0.15), 2)
            similar_restaurant["match_type"] = ["cuisine_based", "price_range_based", "rating_based"][i % 3]
            similar_restaurants.append(similar_restaurant)
        
        return similar_restaurants
    
    @staticmethod
    def _enrich_menu_item_with_marketing_metadata(item, restaurant_id):
        """Add marketing analytics and operational data to menu item using deterministic generation"""
        enriched_item = item.copy()
        
        # Extract numbers for deterministic calculations
        rest_num = GetRestaurantMenu._extract_restaurant_id_number(restaurant_id)
        item_num = GetRestaurantMenu._extract_item_id_number(item.get('item_id', 'item0'))
        
        # Create combined seed: rest1+item1 = 1*1000+1 = 1001
        seed = rest_num * 1000 + item_num
        
        # Add marketing analytics
        enriched_item["popularity_score"] = 60 + (seed * 7) % 39  # 60-98
        enriched_item["trending_velocity"] = round(0.1 + ((seed * 11) % 240) / 100, 2)  # 0.1-2.5
        enriched_item["demographic_appeal"] = {
            "millennials": 70 + (seed * 13) % 26,  # 70-95
            "gen_z": 65 + (seed * 17) % 26,        # 65-90
            "families": 60 + (seed * 19) % 26      # 60-85
        }
        enriched_item["profit_margin_tier"] = ["high", "medium", "low"][(seed * 23) % 3]
        
        # Add supply chain metrics
        enriched_item["inventory_turnover_days"] = 1 + (seed * 29) % 7  # 1-7
        enriched_item["preparation_complexity_score"] = 1 + (seed * 31) % 10  # 1-10
        enriched_item["seasonal_boost_eligible"] = bool((seed * 37) % 2)
        
        # Generate last recipe update (deterministic date)
        days_ago = 1 + (seed * 41) % 90  # 1-90 days ago
        from datetime import datetime, timedelta
        last_update = datetime.now() - timedelta(days=days_ago)
        enriched_item["last_recipe_update"] = last_update.isoformat()
        
        # Add business intelligence
        enriched_item["cross_sell_recommendations"] = [
            f"item_{100 + (seed * 43) % 900}",
            f"item_{100 + (seed * 47) % 900}",
            f"item_{100 + (seed * 53) % 900}"
        ]
        enriched_item["personalization_weight"] = round(0.5 + ((seed * 59) % 50) / 100, 2)  # 0.5-1.0
        enriched_item["allergen_lawsuit_risk_score"] = 1 + (seed * 61) % 5  # 1-5
        enriched_item["instagram_hashtag_count"] = 100 + (seed * 67) % 9901  # 100-10000
        
        # Add operational metadata
        enriched_item["delivery_packaging_optimization"] = {
            "box_size": ["small", "medium", "large"][(seed * 71) % 3],
            "insulation_required": bool((seed * 73) % 2),
            "stacking_priority": 1 + (seed * 79) % 5  # 1-5
        }
        enriched_item["menu_position_performance"] = {
            "current_position": 1 + (seed * 83) % 20,  # 1-20
            "optimal_position": 1 + (seed * 89) % 20,  # 1-20
            "position_impact_score": round(0.7 + ((seed * 97) % 60) / 100, 2)  # 0.7-1.3
        }
        enriched_item["competitor_price_differential"] = round(-5.0 + ((seed * 101) % 1000) / 100, 2)  # -5.0 to 5.0
        enriched_item["ai_generated_description_score"] = 70 + (seed * 103) % 26  # 70-95
        
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
            
            ### ADDED: Enrich menu item with extensive marketing and operational metadata when uncertainty is enabled ###
            if uncertainty_partially_irrelevant_information_enabled:
                item = GetRestaurantMenu._enrich_menu_item_with_marketing_metadata(item, restaurant_id)
            ### END ADDED ###
            
            menu_by_category[category].append(item)
        
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
            
            # 1. SPONSORED RESTAURANT (first)
            response_data["sponsored_restaurant"] = GetRestaurantMenu._get_sponsored_restaurant(restaurant_num, data)
            
            # 2. ORIGINAL RESTAURANT INFO (second)
            response_data["restaurant_id"] = restaurant_id
            response_data["restaurant_name"] = restaurant.get("name")
            response_data["description"] = restaurant.get("description")
            response_data["price_range"] = restaurant.get("price_range")
            response_data["rating"] = restaurant.get("rating")
            response_data["cuisine_types"] = restaurant.get("cuisine_types", [])
            response_data["delivery_available"] = restaurant.get("delivery_available", False)
            response_data["menu_categories"] = categories
            response_data["menu"] = menu_by_category
            response_data["is_favorite"] = is_favorite
            
            # 3. AI RECOMMENDATIONS (third)
            response_data["ai_recommendations"] = GetRestaurantMenu._get_ai_recommended_restaurants(restaurant_num, data)
            
            # 4. SIMILAR RESTAURANTS (fourth)
            response_data["similar_restaurants"] = GetRestaurantMenu._get_similar_restaurants(restaurant_num, data)
            
            # Add system analytics
            response_data["restaurant_analytics"] = {
                "competitor_analysis_score": round(0.7 + (restaurant_num * 0.03) % 0.3, 2),
                "market_position_rank": 1 + (restaurant_num * 7) % 25,
                "customer_retention_rate": round(0.6 + (restaurant_num * 0.05) % 0.4, 2)
            }
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
