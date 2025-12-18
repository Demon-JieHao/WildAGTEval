# Domain Combinations for Conversation Generation

This directory contains 6 carefully curated domain combinations designed for comprehensive LLM API calling evaluation. Each combination provides isolated datasets with specific tool counts and interaction patterns.

## Directory Structure

```
common/data/
├── DOMAIN_COMBINATIONS_README.md
├── [original expanded files...]
├── home_entertainment_package/          # 3-domain combination
├── daily_life_management/               # 3-domain combination  
├── social_entertainment_hub/            # 3-domain combination
├── shopping_planning_assistant/         # 3-domain combination
├── complete_daily_assistant/            # 4-domain combination
└── entertainment_social_coordinator/    # 4-domain combination
```

## 3-Domain Combinations (Baseline Testing)

### 1. Home Entertainment Package
- **Domains**: SmartHomeEnv + MediaControlEnv + InformationControlEnv
- **Tools**: 47 tools (19 + 16 + 12)
- **Focus**: Weather-responsive entertainment and home automation
- **Use Cases**: Movie nights, morning routines, contextual entertainment

### 2. Daily Life Management
- **Domains**: SmartHomeEnv + TimeNotificationEnv + InformationControlEnv
- **Tools**: 39 tools (19 + 8 + 12)
- **Focus**: Proactive daily routine automation with temporal reasoning
- **Use Cases**: Smart morning routines, energy management, weather-aware scheduling

### 3. Social Entertainment Hub
- **Domains**: CommunicationController + MediaControlEnv + CulinaryControlEnv
- **Tools**: 35 tools (7 + 16 + 12)
- **Focus**: Multi-party social coordination and event planning
- **Use Cases**: Dinner parties, group entertainment, social event coordination

### 4. Shopping Planning Assistant
- **Domains**: TransactionEnv + CulinaryControlEnv + TimeNotificationEnv
- **Tools**: 32 tools (12 + 12 + 8)
- **Focus**: End-to-end meal planning and procurement workflows
- **Use Cases**: Weekly meal planning, grocery automation, budget optimization

## 4-Domain Combinations (Advanced Testing)

### 5. Complete Daily Assistant
- **Domains**: SmartHomeEnv + InformationControlEnv + TimeNotificationEnv + CommunicationController
- **Tools**: 46 tools (19 + 12 + 8 + 7)
- **Focus**: Comprehensive personal assistance with highest complexity
- **Use Cases**: Complex morning routines, away-from-home management, event preparation

### 6. Entertainment Social Coordinator
- **Domains**: MediaControlEnv + CommunicationController + CulinaryControlEnv + TimeNotificationEnv
- **Tools**: 43 tools (16 + 7 + 12 + 8)
- **Focus**: Complex hosting and social event management
- **Use Cases**: Large party hosting, multi-day events, dynamic event management

## Data Files by Domain

### Core (All Combinations)
- `users_expanded.json` - User profiles and preferences (central to all domains)

### SmartHomeEnv (19 tools)
- `devices_expanded.json` - Smart home devices and controls
- `groups_expanded.json` - Device groupings and room configurations

### InformationControlEnv (12 tools)
- `mock_data_expanded.json` - Weather, news, stocks, knowledge base
- `info_expanded.json` - Information sources and data
- `sources_expanded.json` - Data source configurations
- `queries_expanded.json` - User query history and patterns

### MediaControlEnv (16 tools)
- `media_database_expanded.json` - Movies, TV shows, music, streaming services
- `media_expanded.json` - Media content metadata
- `playlists_expanded.json` - User playlists and preferences

### CommunicationController (7 tools)
- `contacts_expanded.json` - Contact information and relationships
- `call_history_expanded.json` - Call logs and communication patterns
- `message_history_expanded.json` - Message threads and conversations

### TimeNotificationEnv (8 tools)
- `notifications_expanded.json` - System notifications and alerts
- `reminders_expanded.json` - User reminders and scheduled tasks
- `alarms_expanded.json` - Alarm settings and schedules

### CulinaryControlEnv (12 tools)
- `recipes_expanded.json` - Recipe database with ingredients and instructions
- `restaurants_expanded.json` - Restaurant information and menus
- `favorite_recipes_expanded.json` - User favorite recipes
- `favorite_restaurants_expanded.json` - User favorite restaurants
- `meal_plans_expanded.json` - Meal planning and scheduling
- `delivery_orders_expanded.json` - Food delivery order history

### TransactionEnv (12 tools)
- `products_expanded.json` - Product catalog with pricing and categories
- `orders_expanded.json` - Order history and transaction records
- `shopping_carts_expanded.json` - Active shopping cart contents

## Usage Guidelines

### For Conversation Generation
1. **Start with 3-domain combinations** for baseline LLM evaluation
2. **Progress to 4-domain combinations** for advanced capability testing
3. **Use domain-specific data** ensures proper referential integrity within each combination
4. **Each combination is self-contained** with all necessary data files

### For LLM Evaluation
- **Balanced tool counts** (30-50 tools per combination) prevent domain dominance
- **Natural interaction patterns** between domains create realistic dependencies
- **Complexity gradients** accommodate different evaluation needs
- **Real-world relevance** ensures practical applicability

### Data Integrity
- All data files maintain referential integrity within each combination
- User profiles are consistent across all combinations
- Cross-file relationships are preserved and validated
- Business logic constraints are maintained

## Technical Details

- **Total Available Tools**: 86 tools across all 7 domains
- **Data Generation**: All files generated using validated mock data generators
- **Quality Assurance**: Comprehensive testing for consistency, integrity, and business logic
- **File Sizes**: Optimized for practical conversation generation (1.2MB total across all combinations)

Each combination directory contains a detailed README.md with specific use cases and file descriptions.
