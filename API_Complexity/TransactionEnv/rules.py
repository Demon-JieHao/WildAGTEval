# Copyright TransactionEnv

# Rules for the TransactionEnv

RULES = [
    "Users can only access and modify their own shopping cart.",
    "Users can only access and view their own order history.",
    "Users can only cancel their own orders.",
    "Orders can only be cancelled if they are in 'pending' or 'processing' status.",
    "Products with zero stock cannot be added to the cart.",
    "The quantity of a product in the cart cannot exceed its available stock.",
    "A valid payment method and shipping address must be provided for checkout.",
    "Order IDs must be unique across the system.",
    "Product prices in the cart should reflect the current price in the product database.",
    "Order history should be sorted by creation date, with newest first.",
    "Order tracking information is only available for shipped orders.",
    "Order status can only progress forward, not backward (except for cancellations)."
]
