# Shopping Planning Assistant
**Domain Combination**: TransactionEnv + CulinaryControlEnv + TimeNotificationEnv  
**Total Tools**: 32 tools (12 + 12 + 8)

## Description
This package focuses on end-to-end meal planning and procurement workflows. It combines e-commerce transactions with culinary planning and temporal coordination for comprehensive shopping and meal management scenarios.

## Included Data Files

### TransactionEnv (12 tools)
- `products_expanded.json` - Product catalog with pricing and categories
- `orders_expanded.json` - Order history and transaction records
- `shopping_carts_expanded.json` - Active shopping cart contents

### CulinaryControlEnv (12 tools)
- `recipes_expanded.json` - Recipe database with ingredients and instructions
- `restaurants_expanded.json` - Restaurant information and menus
- `favorite_recipes_expanded.json` - User favorite recipes
- `favorite_restaurants_expanded.json` - User favorite restaurants
- `meal_plans_expanded.json` - Meal planning and scheduling
- `delivery_orders_expanded.json` - Food delivery order history

### TimeNotificationEnv (8 tools)
- `notifications_expanded.json` - System notifications and alerts
- `reminders_expanded.json` - User reminders and scheduled tasks
- `alarms_expanded.json` - Alarm settings and schedules

### Core Data
- `users_expanded.json` - User profiles and preferences

## Example Use Cases
- Weekly meal planning with automated shopping and cooking reminders
- Budget-conscious recipe planning with price comparison
- Special event meal preparation with timeline management
- Grocery list generation from meal plans with delivery scheduling
- Cost optimization across recipes and ingredient sourcing
