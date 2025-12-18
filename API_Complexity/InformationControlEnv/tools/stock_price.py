# Copyright InformationControlEnv

import json
import os
import re
from typing import Any, Dict
from InformationControlEnv.tool import Tool
from InformationControlEnv.helpers import get_current_user, get_mock_data_by_key, add_query_to_history, format_stock_response
from datetime import datetime, timezone


class StockPrice(Tool):
    @staticmethod
    def transform(input_value: str, data: Dict[str, Any] = None) -> str:
        """
        Convert stock symbol into required format (exchange:symbol)
        
        Rules applied:
        1. If already in correct format (exchange:symbol), return as is
        2. If only a simple symbol is provided, add default exchange prefix
        3. Support conversion of symbol parameter value inside invoke_tool statements
        
        Args:
            input_value: Value to convert (stock symbol or invoke_tool statement)
            
        Returns:
            Converted stock symbol or invoke_tool statement
        """
        # Define exchange mapping
        # NYSE (New York Stock Exchange) hosts major companies across diverse sectors including finance (JPM, GS), healthcare (JNJ, PFE), and retail (WMT, HD)
        # NASDAQ (National Association of Securities Dealers Automated Quotations) is home to many leading technology companies including tech giants (AAPL, MSFT), internet services (GOOGL, META), and semiconductors (NVDA, INTC)
        # \n New York Stock Exchange hosts major tech companies including UBER, ORCL.
        # \n National Association of Securities Dealers Automated Quotations hosts major companies including SBUX, PEP.
        ticker_exchange_map = {
            'AAPL': 'NASDAQ', 'GOOGL': 'NASDAQ', 'MSFT': 'NASDAQ', 'AMZN': 'NASDAQ', 
            'TSLA': 'NASDAQ', 'META': 'NASDAQ', 'NVDA': 'NASDAQ', 'NFLX': 'NASDAQ',
            'ORCL': 'NYSE', 'IBM': 'NYSE', 'INTC': 'NASDAQ', 'AMD': 'NASDAQ',
            'CRM': 'NYSE', 'ADBE': 'NASDAQ', 'PYPL': 'NASDAQ', 'UBER': 'NYSE',
            'SPOT': 'NYSE', 'ZOOM': 'NASDAQ', 'SNAP': 'NYSE', 'TWTR': 'NYSE',
            'PINS': 'NYSE', 'SQ': 'NYSE', 'SHOP': 'NYSE', 'ROKU': 'NASDAQ',
            'JPM': 'NYSE', 'BAC': 'NYSE', 'WFC': 'NYSE', 'GS': 'NYSE',
            'MS': 'NYSE', 'C': 'NYSE', 'V': 'NYSE', 'MA': 'NYSE',
            'AXP': 'NYSE', 'JNJ': 'NYSE', 'PFE': 'NYSE', 'MRK': 'NYSE',
            'ABBV': 'NYSE', 'TMO': 'NYSE', 'UNH': 'NYSE', 'CVS': 'NYSE',
            'WMT': 'NYSE', 'TGT': 'NYSE', 'HD': 'NYSE', 'LOW': 'NYSE',
            'NKE': 'NYSE', 'SBUX': 'NASDAQ', 'MCD': 'NYSE', 'KO': 'NYSE', 'PEP': 'NASDAQ'
        }
        
        # Handle invoke_tool statements
        if isinstance(input_value, str) and "invoke_tool" in input_value and "symbol=" in input_value:
            # Extract symbol parameter value
            symbol_pattern = r'symbol=["\']([^"\']+)["\']'
            match = re.search(symbol_pattern, input_value)
            
            if match:
                symbol = match.group(1)
                # Get the symbol to be transformed
                transformed_symbol = StockPrice.transform(symbol)
                if transformed_symbol != symbol:
                    # Replace the original symbol with the transformed one in the string
                    if 'symbol="' in input_value:
                        return input_value.replace(f'symbol="{symbol}"', f'symbol="{transformed_symbol}"')
                    else:
                        return input_value.replace(f"symbol='{symbol}'", f"symbol='{transformed_symbol}'")
        
        # Handle single symbol input
        if isinstance(input_value, str):
            # If colon is included, verify if the exchange prefix is correct
            if ":" in input_value:
                exchange, ticker = input_value.split(":", 1)
                ticker = ticker.upper()
                if ticker in ticker_exchange_map and ticker_exchange_map[ticker] != exchange:
                    # If the exchange prefix is incorrect, convert to the correct one
                    correct_exchange = ticker_exchange_map[ticker]
                    return f"{correct_exchange}:{ticker}"
            # If only ticker is provided, add the exchange prefix
            elif input_value.upper() in ticker_exchange_map:
                upper_symbol = input_value.upper()
                exchange = ticker_exchange_map[upper_symbol]
                return f"{exchange}:{upper_symbol}"
        
        # Return the original input if conversion is not possible
        return input_value
    
    @staticmethod
    def invoke(data: Dict[str, Any], symbol: str) -> str:
        """
        Get current stock price for a symbol.
        
        Args:
            data: The data dictionary containing all information
            symbol: Stock symbol with exchange prefix (e.g., NYSE:AAPL, NASDAQ:GOOGL)
            
        Returns:
            A JSON string with the stock price information
        """
        if not symbol:
            return json.dumps({
                "success": False,
                "message": "No stock symbol provided"
            })
        uncertainty_adhoc_enabled = os.getenv("ENABLE__ADHOC__STOCK_PRICE", "false").lower() == "true"

        # Validate symbol format (compare with result from transform function)
        if uncertainty_adhoc_enabled:
            transformed_symbol = StockPrice.transform(symbol)
            if transformed_symbol != symbol:
                return json.dumps({
                    "success": False,
                    "message": f"Invalid symbol."
                })
            
        # Check for system failure error uncertainty
        uncertainty_system_failure_error_enabled = os.getenv("ENABLE__SYSTEM_FAILURE_ERROR__STOCK_PRICE", "false").lower() == "true"
        
        if uncertainty_system_failure_error_enabled:
            ### ADDED: Simulate financial data provider infrastructure failure ###
            failure_scenario = {
                "error": "MKTDATA_FIX_ENGINE_FAILURE_0x7F3A",
                "message": "FIX 4.4 engine disconnected from primary market data gateway MDG-NYSE-01 after exceeding max pending message queue depth (65536). Multicast feed on 239.192.1.20:14002 reporting sequence gap >1000000, recovery via TCP replay failed with EAGAIN. Circuit breaker triggered on tag 35=W subscription overflow.",
                "fix_session_id": "FIX.4.4:MDPROV01->APICLIENT",
                "last_sequence": 982746521,
                "gap_detected": 982747522,
                "multicast_group": "239.192.1.20:14002",
                "error_code": "FIX_SEQ_GAP_CRITICAL"
            }
            
            return json.dumps({
                "success": False,
                "error": failure_scenario["error"],
                "message": failure_scenario["message"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "trace_id": "mktdata-fixed-correlation-98765",
                "datacenter": "us-east-1a",
                "pod": "mdp-fixed-12",
                "fix_session_id": failure_scenario["fix_session_id"],
                "last_sequence": failure_scenario["last_sequence"],
                "gap_detected": failure_scenario["gap_detected"],
                "multicast_group": failure_scenario["multicast_group"],
                "error_code": failure_scenario["error_code"]
            })
        
        # If format is valid, remove exchange prefix for DB lookup
        if ":" in symbol:
            exchange, ticker = symbol.split(":", 1)
            lookup_symbol = ticker.upper()  # DB 조회용 심볼
        else:
            lookup_symbol = symbol.upper()
        
        # Get stock data (retrieve using simple ticker)
        stock_data = get_mock_data_by_key(data, "stocks", lookup_symbol)
        
        if not stock_data:
            # Get available symbols
            stocks_data = data.get("mock_data", {}).get("stocks", {})
            available_symbols = list(stocks_data.keys())
            
            return json.dumps({
                "success": False,
                "message": f"Stock symbol '{symbol}' not found",
                "available_symbols": available_symbols
            })
        
        # Record the query in user history
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
                "description": "Get current stock price for a symbol. Provides real-time price information.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock symbol prefixed with exchange identifier separated by colon with no spaces. The exchange prefix matches the stock's actual listing exchange."
                        }
                    },
                    "required": ["symbol"]
                },
                "error_cases": [
                    "No symbol provided: The symbol parameter is empty or not provided.",
                    "Invalid symbol format: Symbol must include correct exchange prefix.",
                    "Symbol not found: Returns error with list of available symbols."
                ]
            }
        }
