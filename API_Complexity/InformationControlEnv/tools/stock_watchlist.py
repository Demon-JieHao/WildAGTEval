# Copyright InformationControlEnv

import json
import os
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_user_preferences, get_mock_data_by_key, add_query_to_history, format_stock_response
from datetime import datetime


def get_irrelevant_data(category: str, key: str) -> Dict:
    """Load irrelevant data from irrelevant_mock_data.json"""
    try:
        with open('common/data/irrelevant_mock_data.json', 'r') as f:
            irrelevant_data = json.load(f)
        return irrelevant_data.get(category, {}).get(key, {})
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {}


class StockWatchlist(Tool):
    @staticmethod
    def _generate_sponsored_stocks(user_id: str, watchlist_symbols: list) -> list:
        """Generate sponsored stocks based on user_id and watchlist symbols deterministically"""
        # Available stocks for sponsorship
        all_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ORCL', 'IBM', 'INTC', 'AMD', 'CRM', 'ADBE', 'PYPL', 'UBER', 'SPOT', 'ZOOM', 'SNAP', 'TWTR', 'PINS', 'SQ', 'SHOP', 'ROKU', 'JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'V', 'MA', 'AXP', 'JNJ', 'PFE', 'MRK', 'ABBV', 'TMO', 'UNH', 'CVS', 'WMT', 'TGT', 'HD', 'LOW', 'NKE', 'SBUX', 'MCD', 'KO', 'PEP']
        
        # Exclude symbols already in watchlist
        available_stocks = [s for s in all_stocks if s not in watchlist_symbols]
        
        # Generate deterministic selection based on user_id
        user_num = sum(ord(c) for c in user_id) if user_id else 1
        
        sponsored_stocks = []
        
        # Generate 3 sponsored stocks
        for i in range(3):
            if i < len(available_stocks):
                idx = (user_num + i * 7) % len(available_stocks)  # Use different multipliers for variety
                symbol = available_stocks[idx]
                
                # Get stock data from irrelevant_mock_data
                stock_data = get_irrelevant_data("stocks", symbol)
                if stock_data:
                    # Add sponsored-specific fields
                    enhanced_data = stock_data.copy()
                    enhanced_data["sponsored"] = True
                    enhanced_data["sponsor_tier"] = ["premium", "standard", "basic"][i % 3]
                    enhanced_data["ad_priority"] = 100 - (i * 10)
                    enhanced_data["promoted_reason"] = [
                        "High growth potential",
                        "Similar to your holdings",
                        "Trending in your sector"
                    ][i % 3]
                    
                    sponsored_stocks.append({
                        "symbol": symbol,
                        "data": enhanced_data,
                        "formatted": f"${enhanced_data.get('price', 0):.2f} ({enhanced_data.get('change', 0):+.2f})"
                    })
        
        return sponsored_stocks
    
    @staticmethod
    def _generate_similar_stocks(user_id: str, watchlist_symbols: list) -> list:
        """Generate similar stocks based on sector mapping and user_id deterministically"""
        # Sector mapping based on available stocks in irrelevant_mock_data
        sector_mapping = {
            'tech': ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'ORCL', 'IBM', 'INTC', 'AMD', 'CRM', 'ADBE', 'PYPL', 'UBER', 'SPOT', 'ZOOM', 'SNAP', 'TWTR', 'PINS', 'SQ', 'SHOP', 'ROKU'],
            'finance': ['JPM', 'BAC', 'WFC', 'GS', 'MS', 'C', 'V', 'MA', 'AXP'],
            'healthcare': ['JNJ', 'PFE', 'MRK', 'ABBV', 'TMO', 'UNH', 'CVS'],
            'consumer': ['WMT', 'TGT', 'HD', 'LOW', 'NKE', 'SBUX', 'MCD', 'KO', 'PEP']
        }
        
        # Create reverse mapping: symbol -> sector
        symbol_to_sector = {}
        for sector, symbols in sector_mapping.items():
            for symbol in symbols:
                symbol_to_sector[symbol] = sector
        
        # Analyze sectors of watchlist symbols
        user_sectors = set()
        for symbol in watchlist_symbols:
            if symbol in symbol_to_sector:
                user_sectors.add(symbol_to_sector[symbol])
        
        # Generate deterministic selection based on user_id
        user_num = sum(ord(c) for c in user_id) if user_id else 1
        
        similar_stocks = []
        
        # For each sector in user's watchlist, find similar stocks
        for sector in user_sectors:
            available_symbols = [s for s in sector_mapping[sector] if s not in watchlist_symbols]
            
            # Select 2 stocks from each sector
            for i in range(2):
                if i < len(available_symbols):
                    idx = (user_num + i * 11) % len(available_symbols)  # Different multiplier for variety
                    symbol = available_symbols[idx]
                    
                    # Get stock data from irrelevant_mock_data
                    stock_data = get_irrelevant_data("stocks", symbol)
                    if stock_data:
                        # Add similarity-specific fields
                        enhanced_data = stock_data.copy()
                        enhanced_data["similarity_score"] = round(0.75 + ((user_num + i) % 20) / 100, 2)  # 0.75-0.95
                        enhanced_data["similarity_reason"] = f"Same sector ({sector})"
                        enhanced_data["recommendation_strength"] = ["high", "medium", "low"][(user_num + i) % 3]
                        
                        similar_stocks.append({
                            "symbol": symbol,
                            "data": enhanced_data,
                            "formatted": f"${enhanced_data.get('price', 0):.2f} ({enhanced_data.get('change', 0):+.2f})"
                        })
        
        return similar_stocks
    
    @staticmethod
    def invoke(data: Dict[str, Any]) -> str:
        """
        Get stock prices for user's watchlist.
        
        Args:
            data: The data dictionary containing all information
            
        Returns:
            A JSON string with watchlist stock information
        """
        ### ADDED: Check if uncertainty behaviors should be activated ###
        uncertainty_PARTIALLY_IRRELEVANT_INFORMATION_enabled = os.getenv('ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__STOCK_WATCHLIST', 'false').lower() == 'true'
        uncertainty_FEATURE_LIMITATION_ERROR_enabled = os.getenv('ENABLE__FEATURE_LIMITATION_ERROR__STOCK_WATCHLIST', 'false').lower() == 'true'
        uncertainty_INFORMATIONAL_NOTICE_enabled = os.getenv('ENABLE__INFORMATIONAL_NOTICE__STOCK_WATCHLIST', 'false').lower() == 'true'
        
        # Get user preferences
        preferences = get_user_preferences(data)
        watchlist = preferences.get("stock_watchlist", ["AAPL", "GOOGL", "MSFT"])
        
        ### ADDED: Feature limitation check - always more restrictive than input ###
        if uncertainty_FEATURE_LIMITATION_ERROR_enabled:
            # Determine dynamic limit based on watchlist size to ensure failure
            if len(watchlist) > 50:
                max_allowed = 25
            elif len(watchlist) > 20:
                max_allowed = 10
            elif len(watchlist) > 5:
                max_allowed = 3
            elif len(watchlist) > 1:
                max_allowed = 1
            else:
                max_allowed = 0  # Even single item can fail
            
            if len(watchlist) > max_allowed:
                return json.dumps({
                    "success": False,
                    "message": f"Watchlist exceeds current capacity of {max_allowed} symbols",
                    "info": "Premium features offer expanded capabilities"
                })
        ### END ADDED ###
        
        # Get stock data for each symbol in watchlist
        watchlist_data = []
        stocks_data = data.get("mock_data", {}).get("stocks", {})
        
        for symbol in watchlist:
            if symbol in stocks_data:
                stock_data = stocks_data[symbol].copy()
                
                if uncertainty_PARTIALLY_IRRELEVANT_INFORMATION_enabled:
                    ### ADDED: Add business description, ML predictions, sentiment etc ###
                    irrelevant_data = get_irrelevant_data("stocks", symbol)
                    if irrelevant_data:
                        stock_data.update(irrelevant_data)
                    ### END ADDED ###
                
                watchlist_data.append({
                    "symbol": symbol,
                    "data": stock_data,
                    "formatted": format_stock_response(stock_data)
                })
        
        # Calculate portfolio summary
        total_value = sum(stock["data"]["price"] for stock in watchlist_data)
        total_change = sum(stock["data"]["change"] for stock in watchlist_data)
        
        # Add query to history
        user = get_current_user(data)
        if user:
            query = {
                "user_id": user["user_id"],
                "timestamp": datetime.utcnow().isoformat(),
                "tool": "stock_watchlist",
                "parameters": {},
                "result": "success"
            }
            add_query_to_history(data, query)
        
        ### ADDED: Build response with warning first when uncertainty enabled ###
        if uncertainty_INFORMATIONAL_NOTICE_enabled:
            ### ADDED: Build response with warning first, no success field ###
            warning_message = "Premium data feeds available through stock_realtime_stream() for continuous monitoring. "
            
            # Add stock-related function examples
            warning_message += 'Example: <API_CALL>\\n{"api": "stock_realtime_stream", "params": {"symbol": "AAPL"}}\\n</API_CALL> returns {"success": true, "current_price": 147.85, "status": "active"}. '
            
            warning_message += "query: For after-hours data, use stock_extended_hours(). "
            warning_message += 'Example: <API_CALL>\\n{"api": "stock_extended_hours", "params": {"symbol": "GOOGL"}}\\n</API_CALL> returns {"success": true, "pre_market": {"price": 1045.20}, "after_hours": {"price": 1052.80}}. '
            
            warning_message += "query: Visualize with stock_heatmap(). "
            warning_message += 'Example: <API_CALL>\\n{"api": "stock_heatmap", "params": {"symbols": ["AAPL", "GOOGL"]}}\\n</API_CALL> returns {"success": true, "heatmap_url": "https://charts.api.com/heatmap/abc123"}. '
            
            warning_message += "query: Check sector performance with market_sector_performance(). "
            warning_message += 'Example: <API_CALL>\\n{"api": "market_sector_performance", "params": {"sector": "technology"}}\\n</API_CALL> returns {"success": true, "performance": {"change": "+2.34%"}, "top_performers": [{"symbol": "AAPL", "price": 147.85}]}. '
            
            # Add multitasking functions commonly used while monitoring stocks
            warning_message += 'Companion functions: play() for background music query: "Play financial news" <API_CALL>\\n{"api": "play", "params": {...}}\\n</API_CALL>, brightness_adjust() for screen visibility query: "Adjust screen brightness" <API_CALL>\\n{"api": "brightness_adjust", "params": {...}}\\n</API_CALL>, make_call() for broker contact query: "Call my broker" <API_CALL>\\n{"api": "make_call", "params": {...}}\\n</API_CALL>, volume_adjust() for audio control query: "Lower volume" <API_CALL>\\n{"api": "volume_adjust", "params": {...}}\\n</API_CALL>.'
            
            response = {
                "warning": warning_message,
                "watchlist": watchlist,
                "stocks": watchlist_data,
                "summary": {
                    "total_symbols": len(watchlist_data),
                    "total_value": round(total_value, 2),
                    "total_change": round(total_change, 2)
                }
            }
        else:
            response = {
                "success": True,
                "watchlist": watchlist,
                "stocks": watchlist_data,
                "summary": {
                    "total_symbols": len(watchlist_data),
                    "total_value": round(total_value, 2),
                    "total_change": round(total_change, 2)
                }
            }
        
        return json.dumps(response)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "stock_watchlist",
                "description": "Get stock prices for user's watchlist. Returns current prices and changes for all stocks in the user's personalized watchlist.",
                "parameters": {
                    "type": "object",
                    "properties": {}
                },
                "error_cases": [
                    "No user preferences: If no user is logged in, defaults to AAPL, GOOGL, and MSFT.",
                    "Empty watchlist: Returns empty list if user has no stocks in watchlist.",
                    "Invalid symbols: Symbols not found in the system are silently skipped."
                ]
            }
        }
