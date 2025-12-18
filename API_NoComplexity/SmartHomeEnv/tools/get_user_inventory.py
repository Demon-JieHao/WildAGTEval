# Copyright SmartHomeEnv

import json
from typing import Any, Dict, List, Optional
from SmartHomeEnv.tool import Tool
from SmartHomeEnv.helpers import get_current_user, get_user_home_id


class GetUserInventory(Tool):
    @staticmethod
    def invoke(data: Dict[str, Any], user_id: Optional[str] = None) -> str:
        """
        Get the inventory of devices and groups for a user.
        
        Args:
            data: The data dictionary
            user_id: (Optional) The user ID to get inventory for (if None, uses current user)
            
        Returns:
            A JSON string with the user's inventory
        """
        ### ADDED: Check if uncertainty behavior should be activated ###
        import os
        uncertainty_feature_limitation_error_enabled = os.getenv('ENABLE__FEATURE_LIMITATION_ERROR__GET_USER_INVENTORY', 'false').lower() == 'true'
        uncertainty_system_failure_error_enabled = os.getenv('ENABLE__SYSTEM_FAILURE_ERROR__GET_USER_INVENTORY', 'false').lower() == 'true'
        
        ### ADDED: Handle system failure error first (complete failure scenario) ###
        if uncertainty_system_failure_error_enabled:
            # Deterministic database cluster failure scenarios
            failure_scenarios = [
                {
                    "error": "INFRA_DB_POOL_EXHAUSTED_0x7F3A",
                    "message": "PostgreSQL connection pool exhausted after 30s timeout on primary cluster node pg-inventory-prod-01.internal:5432, failover to secondary pg-inventory-prod-02.internal unsuccessful due to replication lag >8000ms, circuit breaker activated at threshold 50 failed connections",
                    "technical_details": {
                        "connection_string": "postgresql://svc-inventory@pg-inventory-prod-01.internal:5432/device_registry?sslmode=require&pool_size=100&pool_timeout=30",
                        "pool_stats": "active=100, idle=0, waiting=47, max_overflow=20",
                        "cluster_state": "PRIMARY_DEGRADED",
                        "last_successful_query": "2024-03-15T14:32:11.234Z",
                        "replication_lag_ms": 8247,
                        "circuit_breaker_status": "OPEN"
                    },
                    "error_code": "DB_CLUSTER_FAILURE_001",
                    "severity": "CRITICAL",
                    "incident_id": "DB-INV-2024-0704-004"
                },
                {
                    "error": "DATABASE_SHARD_COORDINATOR_FAILURE",
                    "message": "Database shard coordinator service failure: inventory_shard_manager crashed with OutOfMemoryError, connection routing table corrupted, 4 out of 8 shards unreachable, automatic failover disabled due to split-brain detection in consensus protocol",
                    "technical_details": {
                        "shard_manager_status": "CRASHED",
                        "available_shards": "4/8",
                        "routing_table_status": "CORRUPTED",
                        "consensus_protocol": "RAFT",
                        "split_brain_detected": True,
                        "last_checkpoint": "2024-07-04T15:45:33.891Z"
                    },
                    "error_code": "SHARD_COORD_FAILURE_002",
                    "severity": "HIGH",
                    "incident_id": "SHARD-INV-2024-0704-005"
                }
            ]
            
            # Use deterministic failure selection
            failure = failure_scenarios[0]  # Always use PostgreSQL connection pool exhausted for consistency
            
            return json.dumps({
                "success": False,
                "error": failure["error"],
                "message": failure["message"],
                "technical_details": failure["technical_details"],
                "error_code": failure["error_code"],
                "severity": failure["severity"],
                "incident_id": failure["incident_id"],
                "timestamp": "2024-07-04T17:52:47.123Z",
                "service": "SmartHomeEnv.get_user_inventory",
                "correlation_id": "fixed-correlation-inv-12345",
                "trace_id": "trace-inv-67890"
            })
        
        ### ADDED: Feature limitation check - always triggers when enabled ###
        if uncertainty_feature_limitation_error_enabled and user_id is None:
            return json.dumps({
                "success": False,
                "message": "Inventory retrieval temporarily limited due to system maintenance. Targeted queries for specified user ids remain available."
            })
        ### END ADDED ###
        
        # Get the user and home ID
        if user_id is None:
            user = get_current_user(data)
            if not user:
                return json.dumps({
                    "success": False,
                    "message": "No current user set"
                })
            user_id = user["user_id"]
            home_id = user["home_id"]
        else:
            for u in data["users"]:
                if u["user_id"] == user_id:
                    user = u
                    home_id = u["home_id"]
                    break
            else:
                return json.dumps({
                    "success": False,
                    "message": f"User with ID '{user_id}' not found"
                })
        
        # Get the user's devices
        devices = []
        for device in data["devices"]:
            if device["home_id"] == home_id:
                if "PHONE" not in device["endpoint_categories"]:
                    devices.append({
                        "endpoint": device["endpoint"],
                        "name": device["name"],
                        "alternate_names": device["alternate_names"],
                        # "endpoint_categories": device["endpoint_categories"],
                        # "supported_apis": device["supported_apis"],
                        # "groups": device["groups"],
                        # "state": device.get("state", {})
                    })
        
        # Get the user's groups
        groups = []
        for group in data["groups"]:
            if group["home_id"] == home_id:
                groups.append({
                    "id": group["id"],
                    "name": group["name"],
                    "type": group["type"],
                    "has_echo_device": group["has_echo_device"]
                })
        
        # Get the user's current space
        current_space = user.get("current_space")
        
        return json.dumps({
            "success": True,
            "user_id": user_id,
            "name": user["name"],
            "home_id": home_id,
            "current_space": current_space,
            "devices": devices,
            "groups": groups
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "get_user_inventory",
                "description": "Get the inventory of devices and groups for a user. This tool retrieves comprehensive information about all devices and groups associated with a user's home, including device states, supported APIs, and group memberships. It's particularly useful for discovering available devices and their capabilities before sending commands.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "(Optional) The user ID to get inventory for. If not provided, uses the current user."
                        }
                    }
                },
                "error_cases": [
                    "No current user set: This error occurs when no user_id is provided and no current user is set in the system.",
                    "User not found: The specified user_id does not exist in the system.",
                    "Home not found: The user exists but does not have an associated home."
                ]
            }
        }
