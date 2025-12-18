# Copyright InformationControlEnv

import json
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_mock_data_by_key, add_query_to_history, format_stock_response
from datetime import datetime


class StockPrice(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], symbol: str) -> str:
        """
        Get current stock price for a symbol.
        
        Args:
            data: The data dictionary containing all information
            symbol: Stock symbol (e.g., AAPL, GOOGL, MSFT)
            
        Returns:
            A JSON string with the stock price information
        """
        if not symbol:
            return json.dumps({
                "success": False,
                "message": "No stock symbol provided"
            })
        
        # Normalize symbol to uppercase
        symbol_upper = symbol.upper()
        
        # Get stock data
        stock_data = get_mock_data_by_key(data, "stocks", symbol_upper)
        
        if not stock_data:
            # Get available symbols
            stocks_data = data.get("mock_data", {}).get("stocks", {})
            available_symbols = list(stocks_data.keys())
            
            return json.dumps({
                "success": False,
                "message": f"Stock symbol '{symbol}' not found",
                "available_symbols": available_symbols
            })
        
        # Add query to history
        user = get_current_user(data)
        if user:
            query = {
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "tool": "stock_price",
                "parameters": {"symbol": symbol},
                "result": "success"
            }
            add_query_to_history(data, query)
        
        return json.dumps({
            "success": True,
            "stock": stock_data,
            "formatted": format_stock_response(stock_data)
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "stock_price",
                "description": "Get current stock price for a symbol. Provides real-time price, change, and percentage change information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock symbol to look up (e.g., AAPL, GOOGL, MSFT, AMZN, TSLA, NVDA, META)"
                        }
                    },
                    "required": ["symbol"]
                },
                "error_cases": [
                    "No symbol provided: The symbol parameter is empty or not provided.",
                    "Symbol not found: Returns error with list of available symbols.",
                    "Invalid symbol format: Symbol will be converted to uppercase."
                ]
            }
        }
