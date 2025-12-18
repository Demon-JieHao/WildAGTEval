# Copyright CommunicationController

import json
from typing import Any, Dict, List, Optional
from CommunicationController.tool import Tool
from CommunicationController.helpers import find_communication_devices, find_device_by_endpoint


class FindCallDevice(Tool):
    @staticmethod
    def _extract_endpoint_number(endpoint: str) -> int:
        """Extract number from endpoint for deterministic calculations"""
        if endpoint.isdigit():
            return int(endpoint)
        # Handle non-numeric endpoints like "5A", "18A", etc.
        return sum(ord(c) for c in endpoint)
    
    @staticmethod
    def _generate_sponsored_devices(endpoint_num: int) -> List[Dict[str, Any]]:
        """Generate sponsored devices based on deterministic selection"""
        sponsored_devices = []
        
        # Sponsored Device 1: Premium Smart Phone
        sponsored_devices.append({
            "endpoint": f"AD_{endpoint_num}_1",
            "name": ["TechPro Smart Phone X1", "EliteComm Mobile Pro", "NexusCall Device Plus"][endpoint_num % 3],
            "alternate_names": ["Mobile Phone", "Smart Device", "Communication Hub"],
            "endpoint_categories": ["PHONE", "COMMUNICATION_DEVICE"],
            "supported_apis": ["power_on", "power_off", "make_call", "send_message"],
            "groups": ["mobile_devices", "personal_devices", "premium_tier"],
            "home_id": f"retail_{(endpoint_num * 3) % 5 + 1}",
            "state": {
                "power": ["on", "off"][endpoint_num % 2],
                "battery": 50 + (endpoint_num * 17) % 50  # 50-99
            },
            "capabilities": ["microphone", "speaker", "video", "5G"],
            "price": f"${299 + (endpoint_num * 23) % 200}.99",  # $299-$499
            "model_year": 2024,
            "warranty_months": 12 + (endpoint_num * 7) % 24  # 12-36 months
        })
        
        # Sponsored Device 2: Wireless Headset
        sponsored_devices.append({
            "endpoint": f"AD_{endpoint_num}_2",
            "name": ["Premium Wireless Headset", "ProCall Bluetooth Headset", "Executive Audio Device"][endpoint_num % 3],
            "alternate_names": ["Headset", "Wireless Audio", "Bluetooth Device"],
            "endpoint_categories": ["COMMUNICATION_DEVICE", "AUDIO_DEVICE"],
            "supported_apis": ["power_on", "power_off", "make_call", "volume_adjust"],
            "groups": ["personal_devices", "audio_devices", "business_tier"],
            "home_id": f"vendor_{(endpoint_num * 5) % 4 + 1}",
            "state": {
                "power": ["on", "off"][(endpoint_num + 1) % 2],
                "volume": 30 + (endpoint_num * 13) % 70,  # 30-99
                "battery": 40 + (endpoint_num * 19) % 60  # 40-99
            },
            "capabilities": ["microphone", "speaker", "noise_cancellation"],
            "price": f"${149 + (endpoint_num * 31) % 100}.99",  # $149-$249
            "model_year": 2024,
            "warranty_months": 6 + (endpoint_num * 11) % 18  # 6-24 months
        })
        
        return sponsored_devices
    
    @staticmethod
    def _generate_similar_devices(endpoint_num: int) -> List[Dict[str, Any]]:
        """Generate similar devices based on deterministic selection"""
        similar_devices = []
        
        # Similar Device 1: Desktop Communication Hub
        similar_devices.append({
            "endpoint": f"SIM_{endpoint_num}_1",
            "name": ["Desktop Communication Hub", "Office Call Station", "Business Phone System"][endpoint_num % 3],
            "alternate_names": ["Desktop Phone", "Office Device", "Call Station"],
            "endpoint_categories": ["COMMUNICATION_DEVICE", "OFFICE_EQUIPMENT"],
            "supported_apis": ["power_on", "power_off", "make_call", "send_message", "volume_adjust"],
            "groups": ["office_devices", "business_equipment", "communication"],
            "home_id": f"market_{(endpoint_num * 11) % 5 + 1}",
            "state": {
                "power": ["on", "off"][(endpoint_num + 2) % 2],
                "volume": 45 + (endpoint_num * 23) % 55,  # 45-99
                "display_brightness": 60 + (endpoint_num * 27) % 40  # 60-99
            },
            "capabilities": ["microphone", "speaker", "display", "ethernet"],
            "similarity_score": round(0.75 + ((endpoint_num * 13) % 25) / 100, 2),  # 0.75-1.0
            "match_type": "functionality_based",
            "price": f"${179 + (endpoint_num * 33) % 120}.99"  # $179-$299
        })
        
        # Similar Device 2: Smart Watch with Call Support
        similar_devices.append({
            "endpoint": f"SIM_{endpoint_num}_2",
            "name": ["SmartWatch Call Edition", "Wearable Communication Device", "ConnectWear Pro"][endpoint_num % 3],
            "alternate_names": ["Smart Watch", "Wearable", "Watch Phone"],
            "endpoint_categories": ["WEARABLE", "COMMUNICATION_DEVICE", "HEALTH_DEVICE"],
            "supported_apis": ["power_on", "power_off", "make_call", "send_message"],
            "groups": ["wearable_devices", "health_devices", "personal_devices"],
            "home_id": f"outlet_{(endpoint_num * 19) % 3 + 1}",
            "state": {
                "power": "on",
                "battery": 30 + (endpoint_num * 47) % 70,  # 30-99
                "heart_rate": 60 + (endpoint_num * 53) % 40  # 60-99 bpm
            },
            "capabilities": ["microphone", "speaker", "gps", "health_monitoring"],
            "similarity_score": round(0.55 + ((endpoint_num * 21) % 35) / 100, 2),  # 0.55-0.90
            "match_type": "mobility_based",
            "price": f"${249 + (endpoint_num * 59) % 150}.99"  # $249-$399
        })
        
        return similar_devices
    
    @staticmethod
    def _enrich_device_with_metadata(device):
        """Add marketing scores, analytics, and promotional data to device information using deterministic generation"""
        import datetime
        
        enriched_device = device.copy()
        endpoint = device.get('endpoint', '0')
        
        # Convert endpoint to number for deterministic calculations
        endpoint_num = int(endpoint) if endpoint.isdigit() else sum(ord(c) for c in endpoint)
        
        # Add marketing and promotional scores
        enriched_device["marketing_priority_score"] = 60 + (endpoint_num * 7) % 36  # 60-95
        enriched_device["promotional_tier"] = ["premium", "standard", "basic"][(endpoint_num * 3) % 3]
        enriched_device["cross_sell_potential"] = round(0.4 + ((endpoint_num * 13) % 500) / 1000, 3)  # 0.4-0.9
        enriched_device["upsell_recommendation_strength"] = 1 + (endpoint_num * 11) % 10  # 1-10
        
        # Add usage analytics
        enriched_device["usage_frequency_percentile"] = 20 + (endpoint_num * 17) % 80  # 20-99
        enriched_device["user_satisfaction_index"] = round(3.5 + ((endpoint_num * 19) % 130) / 100, 3)  # 3.5-4.8
        enriched_device["feature_adoption_rate"] = round(0.3 + ((endpoint_num * 23) % 650) / 1000, 3)  # 0.3-0.95
        enriched_device["engagement_trending_direction"] = ["increasing", "stable", "decreasing"][(endpoint_num * 5) % 3]
        
        # Add technical telemetry
        enriched_device["performance_benchmark_score"] = 70 + (endpoint_num * 29) % 29  # 70-98
        enriched_device["reliability_metric"] = round(0.92 + ((endpoint_num * 31) % 79) / 1000, 3)  # 0.92-0.999
        enriched_device["latency_percentile_ms"] = 20 + (endpoint_num * 37) % 131  # 20-150
        enriched_device["resource_efficiency_rating"] = ["A+", "A", "B+", "B"][(endpoint_num * 41) % 4]
        
        # Add demographic and targeting data
        enriched_device["demographic_appeal_segments"] = ["tech_enthusiast", "business_professional", "casual_user"]
        enriched_device["age_group_affinity"] = {
            "18-24": round(0.6 + ((endpoint_num * 43) % 40) / 100, 3),  # 0.6-0.99
            "25-34": round(0.7 + ((endpoint_num * 47) % 30) / 100, 3),  # 0.7-0.99
            "35-44": round(0.5 + ((endpoint_num * 53) % 40) / 100, 3),  # 0.5-0.89
            "45+": round(0.4 + ((endpoint_num * 59) % 40) / 100, 3)     # 0.4-0.79
        }
        enriched_device["lifestyle_match_score"] = 65 + (endpoint_num * 61) % 28  # 65-92
        
        # Add inventory and supply chain data
        enriched_device["inventory_availability_score"] = round(0.7 + ((endpoint_num * 67) % 30) / 100, 3)  # 0.7-1.0
        enriched_device["supply_chain_reliability"] = ["high", "medium", "variable"][(endpoint_num * 71) % 3]
        enriched_device["seasonal_demand_coefficient"] = round(0.8 + ((endpoint_num * 73) % 50) / 100, 3)  # 0.8-1.3
        
        # Add competitive intelligence
        enriched_device["market_position_rank"] = 1 + (endpoint_num * 79) % 20  # 1-20
        enriched_device["competitor_feature_parity"] = round(0.75 + ((endpoint_num * 83) % 23) / 100, 3)  # 0.75-0.98
        enriched_device["price_competitiveness_index"] = round(0.85 + ((endpoint_num * 89) % 30) / 100, 3)  # 0.85-1.15
        
        # Add ML predictions
        enriched_device["churn_risk_prediction"] = round(0.05 + ((endpoint_num * 97) % 30) / 100, 3)  # 0.05-0.35
        enriched_device["next_upgrade_probability"] = round(0.2 + ((endpoint_num * 101) % 60) / 100, 3)  # 0.2-0.8
        enriched_device["feature_usage_forecast"] = {
            "next_7_days": 5 + (endpoint_num * 103) % 21,   # 5-25
            "next_30_days": 20 + (endpoint_num * 107) % 81  # 20-100
        }
        
        # Add system metadata
        enriched_device["metadata_version"] = "2.3.1"
        enriched_device["analytics_collection_enabled"] = True
        enriched_device["telemetry_opt_in_status"] = "full"
        
        return enriched_device

    @staticmethod
    def invoke(data: Dict[str, Any], device_name: Optional[str] = None, endpoint: Optional[str] = None) -> str:
        """
        Find devices that support communication features.
        
        Args:
            data: The data dictionary containing devices
            device_name: Optional name (or partial name) to search for
            endpoint: Optional specific endpoint ID to find
            
        Returns:
            A JSON string with the result of the operation
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_partially_irrelevant_information_enabled = os.getenv('ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__FIND_CALL_DEVICE', 'false').lower() == 'true'
        
        # Get the current user's ID
        user_id = data.get("current_user")
        if not user_id:
            return json.dumps({
                "success": False,
                "message": "No user is currently logged in"
            })
        
        # If endpoint is provided, look for that specific device
        if endpoint:
            # Get the user's home ID
            user = next((u for u in data.get("users", []) if u.get("user_id") == user_id), None)
            if not user:
                return json.dumps({
                    "success": False,
                    "message": "User information not found"
                })
            
            home_id = user.get("home_id")
            device = find_device_by_endpoint(data, endpoint, home_id)
            
            if not device:
                return json.dumps({
                    "success": False,
                    "message": f"Device with endpoint {endpoint} not found or not accessible"
                })
            
            # Check if the device supports communication (only make_call API)
            if "make_call" not in device.get("supported_apis", []):
                return json.dumps({
                    "success": False,
                    "message": f"Device {device.get('name')} does not support call features"
                })
            
            # Build base response
            response_data = {
                "success": True,
                "message": f"Found call device: {device.get('name')}"
            }
            
            if uncertainty_partially_irrelevant_information_enabled:
                # Get all user's devices
                user_devices = []
                for d in data.get("devices", []):
                    if d.get("home_id") == home_id:
                        user_devices.append(d)
                
                # Filter device attributes to only include specific fields
                def filter_device(device):
                    return {
                        "endpoint": device.get("endpoint"),
                        "name": device.get("name"),
                        "alternate_names": device.get("alternate_names", []),
                        "endpoint_categories": device.get("endpoint_categories", []),
                        "supported_apis": device.get("supported_apis", []),
                        "groups": device.get("groups", []),
                        "home_id": device.get("home_id")
                    }
                
                # Mix original device with all user devices
                all_devices = [device] + user_devices
                filtered_devices = [filter_device(d) for d in all_devices]
                
                # Deterministic shuffle based on user_id
                import random
                random.seed(hash(user_id) % 2147483647)
                random.shuffle(filtered_devices)
                
                response_data["devices"] = filtered_devices
            else:
                # Normal mode - just the device
                response_data["device"] = device
            
            return json.dumps(response_data)
        
        # Get all communication devices
        comm_devices = find_communication_devices(data, user_id)
        
        # Filter by name if provided
        if device_name:
            device_name_lower = device_name.lower()
            comm_devices = [
                device for device in comm_devices
                if device_name_lower in device.get("name", "").lower()
            ]
        
        # Return the devices
        if not comm_devices:
            message = "No call devices found"
            if device_name:
                message += f" matching '{device_name}'"
            
            return json.dumps({
                "success": True,
                "message": message,
                "devices": []
            })
        
        # Build base response
        response_data = {
            "success": True,
            "message": f"Found {len(comm_devices)} call device(s)"
        }
        
        if uncertainty_partially_irrelevant_information_enabled:
            # Get all user's devices
            user = next((u for u in data.get("users", []) if u.get("user_id") == user_id), None)
            if user:
                home_id = user.get("home_id")
                user_devices = []
                for d in data.get("devices", []):
                    if d.get("home_id") == home_id:
                        user_devices.append(d)
                
                # Filter device attributes to only include specific fields
                def filter_device(device):
                    return {
                        "endpoint": device.get("endpoint"),
                        "name": device.get("name"),
                        "alternate_names": device.get("alternate_names", []),
                        "endpoint_categories": device.get("endpoint_categories", []),
                        "supported_apis": device.get("supported_apis", []),
                        "groups": device.get("groups", []),
                        "home_id": device.get("home_id")
                    }
                
                # Mix communication devices with all user devices
                all_devices = comm_devices + user_devices
                filtered_devices = [filter_device(d) for d in all_devices]
                
                # Deterministic shuffle based on user_id
                import random
                random.seed(hash(user_id) % 2147483647)
                random.shuffle(filtered_devices)
                
                response_data["devices"] = filtered_devices
            else:
                # Fallback if no user found
                response_data["devices"] = comm_devices
        else:
            # Normal mode - just the devices
            response_data["devices"] = comm_devices
        
        return json.dumps(response_data)

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "find_call_device",
                "description": "Find devices that support call features. This tool searches for devices that can be used for making calls.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "device_name": {
                            "type": "string",
                            "description": "Optional name or partial name to search for. If not provided, returns all call devices."
                        },
                        "endpoint": {
                            "type": "string",
                            "description": "Optional specific endpoint ID to find a particular device."
                        }
                    }
                },
                "error_cases": [
                    "No user logged in: No user is currently logged in to search for devices.",
                    "Device not found: The specified device endpoint does not exist or is not accessible.",
                    "No call features: The device does not support any call features."
                ]
            }
        }
