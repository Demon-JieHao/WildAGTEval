# Dataset Dependencies in mock_API_with_7Domains

This document outlines the dependency relationships between the various JSON data files in the mock_API_with_7Domains project. Understanding these dependencies is crucial when expanding or modifying the datasets to maintain data integrity.

## 1. Core Data Dependencies

### devices.json
- **Dependencies**: 
  - `home_id` from users.json (home the device belongs to)
  - `id` from groups.json (group IDs in the device's groups array)

### groups.json
- **Dependencies**:
  - `home_id` from users.json (home the group belongs to)

## 2. Communication-Related Data Dependencies

### contacts.json
- **Dependencies**: 
  - `user_id` from users.json (contact owner)

### message_history.json
- **Dependencies**:
  - `user_id` from users.json (message-related user)
  - `contact_id` from contacts.json (message recipient)

### call_history.json
- **Dependencies**: 
  - `user_id` from users.json (call-related user)
  - `contact_id` from contacts.json (call recipient)
  - `endpoint` from devices.json (device used for the call)

## 3. Media-Related Data Dependencies

### playlists.json
- **Dependencies**:
  - `user_id` from users.json (playlist owner)
  - `id` values from media_database.json (referenced in the items array as song1, song2, etc.)
    - Note: Items array values map to the id field in the music section of media_database.json

## 4. Time and Notification-Related Data Dependencies

### alarms.json
- **Dependencies**:
  - `user_id` from users.json (alarm owner)
  - `endpoint` from devices.json (via device_endpoint field, specifying which device triggers the alarm)

### notifications.json
- **Dependencies**:
  - `user_id` from users.json (notification target)

### reminders.json
- **Dependencies**:
  - `user_id` from users.json (reminder owner)

## 5. Culinary-Related Data Dependencies

### favorite_recipes.json
- **Dependencies**:
  - `user_id` from users.json (preference owner)
  - `recipe_id` from recipes.json (favorite recipe)

### favorite_restaurants.json
- **Dependencies**:
  - `user_id` from users.json (preference owner)
  - `restaurant_id` from restaurants.json (favorite restaurant)

### meal_plans.json
- **Dependencies**:
  - `user_id` from users.json (meal plan owner)
  - `recipe_id` from recipes.json (recipes included in each meal in the meals array)

## 6. Shopping and Order-Related Data Dependencies

### shopping_carts.json
- **Dependencies**:
  - `user_id` from users.json (used directly as the shopping cart key)
  - `product_id` from products.json (for each item in the items array)

### orders.json
- **Dependencies**:
  - `user_id` from users.json (order placer)
  - `product_id` from products.json (for each item in the items array)
  - `transaction_info.payment_methods.id` from users.json (via payment.method_id field)
  - `transaction_info.addresses.id` from users.json (via shipping.address_id field)

### delivery_orders.json
- **Dependencies**:
  - `user_id` from users.json (order placer)
  - `restaurant_id` from restaurants.json (restaurant)
  - `menu[].item_id` from restaurants.json (item_id values in the items array)

## 7. Information Search-Related Data Dependencies

### queries.json
- **Dependencies**:
  - `user_id` from users.json (query executor)
  - `tool` from one of API functions
  - `parameters` object contains various search parameters but does not directly reference FKs
