# Copyright Common Transform Registry

"""
Central registry for transform functions.
Maps each tool to its transform function and the key parameter to transform.
"""

# Dictionary mapping each tool to its transform function and the key parameter to transform
transform_registry = {
    "make_call": {
        "module": "CommunicationController.tools.make_call",
        "class": "MakeCall",
        "key_param": "phone_number"
    },
    "get_call_history": {
        "module": "CommunicationController.tools.get_call_history",
        "class": "GetCallHistory",
        "key_param": "time_range"
    },
    "play": {
        "module": "MediaControlEnv.tools.play",
        "class": "Play",
        "key_param": "media_id"
    },
    "color_set": {
        "module": "SmartHomeEnv.tools.color_set",
        "class": "ColorSet",
        "key_param": "color"
    },
    "lock_unlock": {
        "module": "SmartHomeEnv.tools.lock_unlock",
        "class": "LockUnlock",
        "key_param": "endpoints"
    },
    "lock_lock": {
        "module": "SmartHomeEnv.tools.lock_lock",
        "class": "LockLock",
        "key_param": "endpoints"
    },
    "stock_price": {
        "module": "InformationControlEnv.tools.stock_price",
        "class": "StockPrice",
        "key_param": "symbol"
    },
    "track_order": {
        "module": "TransactionEnv.tools.track_order",
        "class": "TrackOrder",
        "key_param": "order_id"
    }
    # Additional tools can be registered here in the future
}


def register_transform(function_name, module_path, class_name, key_param):
    """Register a new transform function in the registry.
    
    Args:
        function_name: Tool name (e.g., "make_call")
        module_path: Module path (e.g., "CommunicationController.tools.make_call")
        class_name: Class name (e.g., "MakeCall")
        key_param: Name of the key parameter to transform (e.g., "phone_number")
    """
    transform_registry[function_name] = {
        "module": module_path,
        "class": class_name,
        "key_param": key_param
    }
