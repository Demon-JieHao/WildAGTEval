# Transaction Environment

The TransactionEnv module provides e-commerce functionality to the One Environment system, allowing users to:

- Browse and search products
- Manage a shopping cart
- Complete checkout process
- Track order status
- View order history

## Architecture

TransactionEnv follows the same architecture as other environments in the system:

- `env.py`: Main environment class that inherits from BaseEnvironment
- `helpers.py`: Helper functions for data manipulation and business logic
- `tool.py`: Tool class that inherits from BaseTool
- `tools/`: Directory containing individual tool implementations
- `data/`: Directory for data loading/saving functionality
- `wiki.md`: Documentation for the environment

## Data Model

Transaction data is divided into three main categories:

1. **Products**: Items available for purchase
2. **Shopping Carts**: User-specific collections of products
3. **Orders**: Completed transactions with payment and shipping information

## Tools

### Product Management
- `search_product`: Search products by name, category, and price range
- `get_product_details`: Get detailed information about a specific product

### Cart Management
- `view_cart`: View the current user's shopping cart
- `add_to_cart`: Add a product to the cart
- `remove_from_cart`: Remove a product from the cart
- `update_cart_quantity`: Update the quantity of a product in the cart
- `clear_cart`: Remove all items from the cart

### Order Management
- `checkout`: Process a cart into an order
- `get_order_history`: View a user's order history
- `get_order_details`: Get detailed information about a specific order
- `track_order`: Get shipping status of an order
- `cancel_order`: Cancel an order if it's in a cancellable state

## Usage

To use the TransactionEnv in your application:

```python
from TransactionEnv import TransactionEnv
from common import register_environment, invoke_tool

# Create and register the environment
transaction_env = TransactionEnv()
register_environment("TransactionEnv", transaction_env)

# Set a user
transaction_env.set_current_user("user1")

# Use tools
result = invoke_tool("search_product", query="smart")
print(result)

# Add to cart
result = invoke_tool("add_to_cart", product_id="prod1", quantity=2)
print(result)

# Checkout
result = invoke_tool("checkout", payment_method_id="pm1", address_id="addr1")
print(result)
```

## Integration with User Data

TransactionEnv extends the user model with a `transaction_info` object containing:

- `payment_methods`: Array of payment methods (credit cards, etc.)
- `addresses`: Array of shipping addresses

## Business Rules

Key business rules implemented in TransactionEnv include:

1. Users can only access their own cart and orders
2. Product stock is checked and updated during cart operations and checkout
3. Orders can only be cancelled in certain states (pending, processing)
4. Payment methods and shipping addresses must be validated
5. Order data is persisted and tracked across sessions
