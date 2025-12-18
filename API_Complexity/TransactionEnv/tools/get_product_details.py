# Copyright TransactionEnv

import json
from typing import Any, Dict, Optional
from TransactionEnv.tool import Tool
from TransactionEnv.helpers import find_product_by_id


class GetProductDetails(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], product_id: str) -> str:
        """
        Get detailed information about a specific product.
        
        Args:
            data: The data dictionary containing products
            product_id: ID of the product to retrieve
            
        Returns:
            A JSON string with the result of the operation
        """
        # Input validation
        if not product_id:
            return json.dumps({
                "success": False,
                "message": "Product ID is required"
            })
        
        # Find the product
        product = find_product_by_id(data, product_id)
        
        if not product:
            return json.dumps({
                "success": False,
                "message": f"Product with ID '{product_id}' not found"
            })
        
        # Return full product details
        return json.dumps({
            "success": True,
            "details": product,
            "message": f"Retrieved details for '{product.get('name')}'"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_product_details",
                "description": "Get detailed information about a specific product by its ID. Returns comprehensive product details including description, price, stock availability, and images.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_id": {
                            "type": "string",
                            "description": "The unique ID of the product to retrieve details for. This ID is usually obtained from search_product results."
                        }
                    },
                    "required": ["product_id"]
                },
                "error_cases": [
                    "Missing product ID: The product ID parameter is not provided",
                    "Product not found: No product exists with the specified ID"
                ]
            }
        }
