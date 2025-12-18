# Copyright CommunicationController

import json
import re
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Match
from CommunicationController.tool import Tool
from CommunicationController.helpers import get_user_call_history, find_contact_by_id


def is_valid_iso8601_duration(time_range: str) -> bool:
    """
    Validate if the provided string is a valid ISO 8601 duration format.
    Must start with 'P' and contain at least one valid designator with a non-zero value.
    
    Valid examples:
    - P7D (7 days)
    - P1W (1 week)
    - P1DT12H30M (1 day, 12 hours, 30 minutes)
    - PT24H (24 hours)
    """
    # Basic validation: must start with P
    if not time_range or not time_range.startswith('P'):
        return False
    
    # Simple regex pattern for ISO 8601 duration
    # P[nY][nM][nW][nD][T[nH][nM][nS]]
    pattern = r'^P((\d+Y)?(\d+M)?(\d+W)?(\d+D)?)?(T(\d+H)?(\d+M)?(\d+S)?)?$'
    
    # Check if the pattern matches
    match = re.match(pattern, time_range)
    if not match:
        return False
        
    # Extract all duration components
    duration_parts = re.findall(r'(\d+)[YMWDHMS]', time_range)
    
    # Ensure at least one valid duration value is present and non-zero
    return any(int(x) > 0 for x in duration_parts if x)


def parse_iso8601_duration(duration: str) -> timedelta:
    """
    Parse ISO 8601 duration format into a timedelta object.
    
    Args:
        duration: ISO 8601 duration string (e.g., "P7D", "P1DT12H30M")
    Returns:
        timedelta object representing the duration
    """
    if not is_valid_iso8601_duration(duration):
        raise ValueError(f"Invalid ISO 8601 duration format: {duration}")
    
    years = months = weeks = days = hours = minutes = seconds = 0
    
    # Extract the time part (if exists)
    parts = duration.split('T')
    date_part = parts[0][1:]  # Remove the 'P'
    time_part = parts[1] if len(parts) > 1 else ''
    
    # Extract values from date part
    current_value = ""
    for char in date_part:
        if char.isdigit():
            current_value += char
        else:
            if char == 'Y' and current_value:
                years = int(current_value)
            elif char == 'M' and current_value:
                months = int(current_value)
            elif char == 'W' and current_value:
                weeks = int(current_value)
            elif char == 'D' and current_value:
                days = int(current_value)
            current_value = ""
    
    # Extract values from time part
    current_value = ""
    for char in time_part:
        if char.isdigit():
            current_value += char
        else:
            if char == 'H' and current_value:
                hours = int(current_value)
            elif char == 'M' and current_value:
                minutes = int(current_value)
            elif char == 'S' and current_value:
                seconds = int(current_value)
            current_value = ""
    
    # Convert years and months to days (approximation)
    days += years * 365
    days += months * 30
    
    # Create timedelta
    return timedelta(
        days=days + weeks * 7, 
        hours=hours, 
        minutes=minutes, 
        seconds=seconds
    )


def safe_parse_duration(time_range: str) -> timedelta:
    """
    Try parsing ISO 8601 duration first, then fallback to simple formats like '7d', '2w', '24h', '60min', '7'.
    """
    try:
        # 1️⃣ ISO 8601 형식 시도
        return parse_iso8601_duration(time_range)
    except Exception:
        # 2️⃣ 비ISO 포맷 fallback
        time_range = time_range.strip().lower()
        if time_range.endswith("d"):
            return timedelta(days=int(time_range[:-1]))
        elif time_range.endswith("w"):
            return timedelta(weeks=int(time_range[:-1]))
        elif time_range.endswith("m"):
            return timedelta(days=30 * int(time_range[:-1]))
        elif time_range.endswith("y"):
            return timedelta(days=365 * int(time_range[:-1]))
        elif time_range.endswith("h"):
            return timedelta(hours=int(time_range[:-1]))
        elif time_range.endswith("min"):
            return timedelta(minutes=int(time_range[:-3]))
        elif time_range.isdigit():
            return timedelta(days=int(time_range))
        else:
            raise ValueError(f"Unsupported duration format: {time_range}")
        
class GetCallHistory(Tool):
    @staticmethod
    def _extract_call_id_number(call_id: str) -> int:
        """Extract number from call_id (e.g., call5 -> 5, call14 -> 14)"""
        match = re.match(r'call(\d+)', call_id)
        return int(match.group(1)) if match else 0
    
    @staticmethod
    def _enrich_call_with_telecom_metadata(call):
        """Add telecom analytics and marketing data to call record using deterministic generation"""
        enriched_call = call.copy()
        call_id = call.get('call_id', 'call0')
        
        # Extract call number for deterministic calculations
        call_num = GetCallHistory._extract_call_id_number(call_id)
        
        # Add network performance metrics
        enriched_call["network_quality_score"] = 70 + (call_num * 7) % 31  # 70-100
        enriched_call["signal_strength_avg"] = round(-80 + ((call_num * 11) % 30), 3)  # -80 to -50
        enriched_call["packet_loss_rate"] = round(((call_num * 13) % 50) / 1000, 3)  # 0.0-0.05
        enriched_call["jitter_ms"] = round(((call_num * 17) % 300) / 10, 3)  # 0-30
        enriched_call["codec_efficiency_rating"] = round(0.7 + ((call_num * 19) % 30) / 100, 3)  # 0.7-1.0
        
        # Add customer analytics
        enriched_call["customer_satisfaction_prediction"] = 60 + (call_num * 23) % 36  # 60-95
        enriched_call["churn_risk_score"] = round(0.1 + ((call_num * 29) % 70) / 100, 3)  # 0.1-0.8
        enriched_call["lifetime_value_tier"] = ["bronze", "silver", "gold", "platinum"][(call_num * 31) % 4]
        enriched_call["engagement_frequency_percentile"] = 20 + (call_num * 37) % 80  # 20-99
        
        # Add marketing/promotional data
        enriched_call["eligible_plan_upgrades"] = (call_num * 41) % 6  # 0-5
        enriched_call["promotional_offer_match_score"] = 40 + (call_num * 43) % 61  # 40-100
        enriched_call["international_calling_upsell_potential"] = round(0.2 + ((call_num * 47) % 70) / 100, 3)  # 0.2-0.9
        enriched_call["data_plan_optimization_savings"] = round(5.0 + ((call_num * 53) % 450) / 10, 3)  # 5.0-50.0
        
        # Add operational metadata
        enriched_call["tower_id"] = f"TWR-{1000 + (call_num * 59) % 9000}"  # TWR-1000 to TWR-9999
        enriched_call["routing_efficiency_score"] = round(0.6 + ((call_num * 61) % 40) / 100, 3)  # 0.6-1.0
        enriched_call["billing_cycle_position"] = 1 + (call_num * 67) % 30  # 1-30
        enriched_call["usage_pattern_cluster"] = ["business", "personal", "mixed", "international"][(call_num * 71) % 4]
        
        # Add predictive analytics
        enriched_call["next_call_probability_24h"] = round(0.1 + ((call_num * 73) % 80) / 100, 3)  # 0.1-0.9
        enriched_call["preferred_calling_time_window"] = ["morning", "afternoon", "evening", "night"][(call_num * 79) % 4]
        enriched_call["communication_preference_score"] = {
            "voice": round(0.3 + ((call_num * 83) % 70) / 100, 3),  # 0.3-1.0
            "video": round(0.1 + ((call_num * 89) % 70) / 100, 3),  # 0.1-0.8
            "messaging": round(0.2 + ((call_num * 97) % 70) / 100, 3)  # 0.2-0.9
        }
        
        # Add quality of service metrics
        enriched_call["qos_metrics"] = {
            "mos_score": round(3.5 + ((call_num * 101) % 100) / 100, 3),  # 3.5-4.5
            "r_factor": 70 + (call_num * 103) % 24,  # 70-93
            "connection_setup_time_ms": 500 + (call_num * 107) % 2500,  # 500-3000
            "handover_count": (call_num * 109) % 6  # 0-5
        }
        
        return enriched_call

    @staticmethod
    def invoke(data: Dict[str, Any], time_range: str, limit: int = 10) -> str:
        """
        Get call history for the current user.
        
        Args:
            data: The data dictionary containing call history
            time_range: Time range in ISO 8601 format (e.g., 'P7D' for 7 days, 'P1DT12H30M' for 1 day, 12 hours, 30 minutes).
            limit: Maximum number of calls to return
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behaviors should be activated ###
        import os
        uncertainty_partially_irrelevant_information_enabled = os.getenv('ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_CALL_HISTORY', 'false').lower() == 'true'
        uncertainty_feature_limitation_error_enabled = os.getenv('ENABLE__FEATURE_LIMITATION_ERROR__GET_CALL_HISTORY', 'false').lower() == 'true'
        uncertainty_adhoc_enabled = os.getenv('ENABLE__ADHOC__GET_CALL_HISTORY', 'false').lower() == 'true'

        # Get the current user's ID
        user_id = data.get("current_user")
        if not user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in"
            })
        
        # Validate time_range format
        if uncertainty_adhoc_enabled:
            if not is_valid_iso8601_duration(time_range):
                return json.dumps({
                    "success": False,
                    "message": "Invalid time range format."
                })
            
        # Parse the time range and calculate the start time
        try:
            duration = safe_parse_duration(time_range)
            start_time = datetime.utcnow() - duration
            print("current time inside get_call_history: ", datetime.utcnow())
            print("current time inside get_call_history: ", datetime.utcnow().isoformat())
            print("current time inside get_call_history: ", datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))

            
            ### ADDED: Feature limitation check - restrict access to historical data ###
            if uncertainty_feature_limitation_error_enabled:
                # Calculate days in the requested duration (for potential logging/analysis)
                days_requested = duration.total_seconds() / (24 * 3600)
                
                return json.dumps({
                    "success": False,
                    "message": "Extended historical data temporarily unavailable; recent call records remain accessible"
                })
            ### END ADDED ###
            
        except ValueError as e:
            return json.dumps({
                "success": False,
                "message": str(e)
            })
            
        # Get call history with time range filter
        calls = get_user_call_history(data, user_id, start_time=start_time, limit=limit)
        
        # Add contact names to calls for better display
        enhanced_calls = []
        for call in calls:
            call_copy = call.copy()
            contact_id = call_copy.get("contact_id")
            
            if contact_id:
                contact = find_contact_by_id(data, contact_id, user_id)
                if contact:
                    call_copy["contact_name"] = contact.get("name")
            
            # Format duration in minutes and seconds
            duration = call_copy.get("duration", 0)
            if duration > 0:
                minutes = duration // 60
                seconds = duration % 60
                if minutes > 0:
                    call_copy["duration_formatted"] = f"{minutes} min {seconds} sec"
                else:
                    call_copy["duration_formatted"] = f"{seconds} sec"
            else:
                call_copy["duration_formatted"] = "0 sec"
            
            ### ADDED: Enrich call with extensive telecom analytics and marketing data when uncertainty is enabled ###
            if uncertainty_partially_irrelevant_information_enabled:
                call_copy = GetCallHistory._enrich_call_with_telecom_metadata(call_copy)
            ### END ADDED ###
            
            enhanced_calls.append(call_copy)
        
        # Return result
        return json.dumps({
            "success": True,
            "message": f"Retrieved {len(calls)} call records",
            "calls": enhanced_calls
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_call_history",
                "description": "Get call history for the current user. This tool retrieves the user's call records, including incoming and outgoing calls, with details such as duration and status.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "time_range": {
                            "type": "string",
                            "description": "Time range in ISO 8601 format (e.g., 'P1DT12H30M')."
                            # "description": "Time range in ISO 8601 format (e.g., 'P1DT12H30M' for 1 day, 12 hours, 30 minutes)."
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of call records to return. Default is 10.",
                            "minimum": 1
                        }
                    },
                    "required": ["time_range"]
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to view call history.",
                    "Invalid time range format: The time_range must be in ISO 8601 duration format prefixed with 'P' (e.g., 'P7D', 'P1DT12H30M')."
                ]
            }
        }

    @staticmethod
    def transform(input_value: str, data: Dict[str, Any] = None) -> str:
        """
        Convert various time range formats to ISO 8601 duration format.
        
        Supported input formats:
        1. Plain numbers ("7", "14") - interpreted as days
        2. Number + unit format:
           - "7d", "14d" - days
           - "2w", "4w" - weeks
           - "3m", "6m" - months
           - "1y", "2y" - years
        3. Time units:
           - "24h", "48h" - hours
           - "60min", "90min" - minutes
        4. Quoted strings ('"7"', "'7'") - will strip quotes and process
        5. Complete invoke_tool statements:
           - 'invoke_tool("get_call_history", time_range="7", limit=5)'
           - Will extract the time_range value and transform it
        
        Args:
            input_value: Time range string to convert
            
        Returns:
            ISO 8601 duration format string, or original value if conversion not possible
        """
        # Import re module at the top level of the function to ensure it's available everywhere
        import re
        # Handle complete invoke_tool statements
        if isinstance(input_value, str) and "invoke_tool" in input_value and "time_range=" in input_value:
            # Extract the time_range value using regex
            # This will match both time_range="7" and time_range='7' patterns
            time_range_pattern = r'time_range=["\']([^"\']+)["\']'
            match = re.search(time_range_pattern, input_value)
            
            if match:
                time_range_value = match.group(1)
                transformed_value = GetCallHistory.transform(time_range_value)
                
                # Always replace the value, even if it seems to be the same (might differ in case)
                # For example, 'p7d' should be replaced with 'P7D'
                if 'time_range="' in input_value:
                    # Handle double quotes
                    return input_value.replace(f'time_range="{time_range_value}"', f'time_range="{transformed_value}"')
                else:
                    # Handle single quotes
                    return input_value.replace(f"time_range='{time_range_value}'", f"time_range='{transformed_value}'")
            
        # Already ISO 8601 format
        if isinstance(input_value, str) and (input_value.startswith('P') or input_value.startswith('p')):
            # Ensure consistent uppercase format for ISO 8601 durations
            if input_value.startswith('p'):
                return input_value.upper()
            return input_value
            
        # Handle quoted strings (e.g., "7" or '7')
        if isinstance(input_value, str):
            # Strip double quotes
            if (input_value.startswith('"') and input_value.endswith('"')) or \
               (input_value.startswith("'") and input_value.endswith("'")):
                if len(input_value) >= 2:
                    try:
                        # Extract the content between quotes
                        unquoted = input_value[1:-1]
                        # Try to transform the unquoted value
                        transformed = GetCallHistory.transform(unquoted)
                        if transformed != unquoted:  # If transformation was successful
                            return transformed
                    except (IndexError, ValueError):
                        pass  # Proceed with original value if any error occurs
        
        # Plain number - interpret as days
        try:
            days = int(input_value)
            if days > 0:
                return f"P{days}D"
        except (ValueError, TypeError):
            pass
        
        if isinstance(input_value, str):
            input_value = input_value.lower().strip()
            
            # Days (d)
            match = re.match(r'^(\d+)d$', input_value)
            if match:
                days = int(match.group(1))
                if days > 0:
                    return f"P{days}D"
            
            # Weeks (w)
            match = re.match(r'^(\d+)w$', input_value)
            if match:
                weeks = int(match.group(1))
                if weeks > 0:
                    return f"P{weeks}W"
            
            # Months (m)
            match = re.match(r'^(\d+)m$', input_value)
            if match:
                months = int(match.group(1))
                if months > 0:
                    return f"P{months}M"
            
            # Years (y)
            match = re.match(r'^(\d+)y$', input_value)
            if match:
                years = int(match.group(1))
                if years > 0:
                    return f"P{years}Y"
            
            # Hours (h)
            match = re.match(r'^(\d+)h$', input_value)
            if match:
                hours = int(match.group(1))
                if hours > 0:
                    return f"PT{hours}H"
            
            # Minutes (min)
            match = re.match(r'^(\d+)min$', input_value)
            if match:
                minutes = int(match.group(1))
                if minutes > 0:
                    return f"PT{minutes}M"
        
        # Return original value if no conversion possible
        return input_value
