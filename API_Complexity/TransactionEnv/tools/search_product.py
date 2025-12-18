# Copyright TransactionEnv

import json
from typing import Any, Dict, List, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import search_products


class SearchProduct(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], query: Optional[str] = None, 
               category: Optional[str] = None, min_price: Optional[float] = None, 
               max_price: Optional[float] = None, sort_by: Optional[str] = None, 
               limit: int = 10) -> str:
        """
        Search for products based on various criteria.
        
        Args:
            data: The data dictionary containing products
            query: Search term for product name or description
            category: Filter by product category
            min_price: Minimum price filter
            max_price: Maximum price filter
            sort_by: Field to sort by ('price', 'price_desc', 'rating', 'name')
            limit: Maximum number of results to return
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if min_price is not None and min_price < 0:
            return json.dumps({
                "success": False,
                "message": "Minimum price cannot be negative"
            })
            
        if max_price is not None and max_price < 0:
            return json.dumps({
                "success": False,
                "message": "Maximum price cannot be negative"
            })
            
        if min_price is not None and max_price is not None and min_price > max_price:
            return json.dumps({
                "success": False,
                "message": "Minimum price cannot be greater than maximum price"
            })
            
        if limit is not None and limit < 1:
            limit = 10  # Default to 10 if invalid
        
        # Valid sort options
        valid_sort_options = ["price", "price_desc", "rating", "name"]
        if sort_by is not None and sort_by not in valid_sort_options:
            return json.dumps({
                "success": False,
                "message": f"Invalid sort option. Valid options are: {', '.join(valid_sort_options)}"
            })
        
        # Search products
        results = search_products(data, query, category, min_price, max_price, sort_by, limit)
        
        # Format results for display (compact version)
        formatted_results = []
        for product in results:
            formatted_results.append({
                "product_id": product.get("product_id"),
                "name": product.get("name"),
                "price": product.get("price"),
                "category": product.get("category"),
                # "rating": product.get("rating"),
                "stock": product.get("stock")
            })
        
        # Create categories list from results for user convenience
        categories = sorted(list(set(p.get("category") for p in results if p.get("category"))))
        
        return json.dumps({
            "success": True,
            "count": len(results),
            "categories": categories,
            "results": formatted_results,
            "message": f"Found {len(results)} product(s)" if results else "No products found matching your criteria"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "search_product",
                "description": "Search for products based on various criteria like name, category, and price range. Returns a list of products matching the search criteria.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "(Optional) Search term to match against product names and descriptions."
                        },
                        "category": {
                            "type": "string",
                            "description": "(Optional) Filter products by specific category (e.g., 'electronics', 'smart_home', 'wearables')."
                        },
                        "min_price": {
                            "type": "number",
                            "description": "(Optional) Minimum price filter. Products with prices below this value will be excluded."
                        },
                        "max_price": {
                            "type": "number",
                            "description": "(Optional) Maximum price filter. Products with prices above this value will be excluded."
                        },
                        "sort_by": {
                            "type": "string",
                            "enum": ["price", "price_desc", "rating", "name"],
                            "description": "(Optional) Sort results by: 'price' (lowest to highest), 'price_desc' (highest to lowest), 'rating' (highest rated first), or 'name' (alphabetical)."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "(Optional) Maximum number of results to return. Defaults to 10."
                        }
                    }
                },
                "error_cases": [
                    "Invalid price range: min_price > max_price",
                    "Invalid limit: limit < 1",
                    "Invalid sort option: sort_by must be one of the allowed values",
                    "No products found: No products match the search criteria"
                ]
            }
        }
