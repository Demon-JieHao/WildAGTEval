# Copyright SmartHomeEnv

RULES = [
    "For direct smart home commands, prioritize efficient action over conversation.",
    "Use user request context to determine appropriate action.",
    "When user intent is clear, choose the most direct & efficient action without unnecessary preliminary checks or API calls.",
    "For more complex or incomplete queries, or unclear user intent, use the Think tool to reason through the appropriate action.",
    "Always verify that a device supports an API before attempting to call it.",
    "When controlling a group of devices, apply the action to all devices in the group that support the API.",
    "If a device is not specified, use the user's current location to determine which devices to control.",
    "Provide clear and concise responses about the actions taken and their results.",
    "If an action fails, provide a helpful error message explaining why and suggesting alternatives.",
    "Always respect device limitations and capabilities when processing commands."
]
