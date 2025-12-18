# Complexity Environment Variables Reference

This document contains all uncertainty environment variables implemented across the API system. A total of **60 uncertainty environment variables** have been identified across **6** different uncertainty types.

## Overview

- **Total Complexities**: 60
- **Uncertainty Types**: 6  
  - Ad-hoc Rules
  - Unclear Functionality Boundari
  - Partially Irrelevant Information  
  - Informational Notice  
  - Feature Limitation Error  
  - System Failure Error  

## Environment Variables by Type

### 🚨 FEATURE_LIMITATION_ERROR (8 variables)

These uncertainties simulate service limitations that require LLM agents to find alternative approaches or parameter adjustments.

```bash
ENABLE__FEATURE_LIMITATION_ERROR__GET_CALL_HISTORY=true
ENABLE__FEATURE_LIMITATION_ERROR__GET_MESSAGES=true
ENABLE__FEATURE_LIMITATION_ERROR__GET_NOTIFICATIONS=true
ENABLE__FEATURE_LIMITATION_ERROR__GET_USER_INVENTORY=true
ENABLE__FEATURE_LIMITATION_ERROR__NEWS_PERSONALIZED=true
ENABLE__FEATURE_LIMITATION_ERROR__STOCK_WATCHLIST=true
ENABLE__FEATURE_LIMITATION_ERROR__TRACK_ORDER=true
ENABLE__FEATURE_LIMITATION_ERROR__WEATHER_FORECAST=true
```

**Key Characteristics:**
- Functions return `success: false` with hints for workarounds
- Tests LLM problem-solving and technical adaptation skills
- Requires systematic approaches and parameter adjustments

### 📊 PARTIALLY_IRRELEVANT_INFORMATION (8 variables)

These uncertainties add excessive or tangentially related information to function responses, testing LLM's ability to filter relevant data.

```bash
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__FIND_CALL_DEVICE=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_CALL_HISTORY=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_MESSAGES=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_RESTAURANT_MENU=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__KNOWLEDGE_LOOKUP=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__SEARCH_RECIPES=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__STOCK_WATCHLIST=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__WEATHER_FORECAST=true
```

**Key Characteristics:**
- Functions still succeed but return inflated responses
- Tests LLM information filtering and relevance detection
- Challenges response processing and summarization skills

### 💡 INFORMATIONAL_NOTICE (8 variables)

These uncertainties add informational messages or notifications to function responses without affecting core functionality.

```bash
ENABLE__INFORMATIONAL_NOTICE__COLOR_SET=true
ENABLE__INFORMATIONAL_NOTICE__CREATE_MEAL_PLAN=true
ENABLE__INFORMATIONAL_NOTICE__GET_MEDIA_DETAILS=true
ENABLE__INFORMATIONAL_NOTICE__GET_NOTIFICATIONS=true
ENABLE__INFORMATIONAL_NOTICE__MAKE_CALL=true
ENABLE__INFORMATIONAL_NOTICE__SEARCH_MEDIA=true
ENABLE__INFORMATIONAL_NOTICE__TEMPERATURE_SET=true
ENABLE__INFORMATIONAL_NOTICE__STOCK_WATCHLIST=true
```

**Key Characteristics:**
- Functions succeed with additional informational content
- Tests LLM's ability to handle extra context gracefully
- Evaluates response clarity and user communication skills

### ⚡ SYSTEM_FAILURE_ERROR (8 variables)

These uncertainties simulate complex infrastructure failures with highly technical error messages that require LLM agents to parse technical jargon and translate it into user-friendly explanations.

```bash
ENABLE__SYSTEM_FAILURE_ERROR__COLOR_SET=true
ENABLE__SYSTEM_FAILURE_ERROR__GET_USER_INVENTORY=true
ENABLE__SYSTEM_FAILURE_ERROR__MAKE_CALL=true
ENABLE__SYSTEM_FAILURE_ERROR__PLACE_DELIVERY_ORDER=true
ENABLE__SYSTEM_FAILURE_ERROR__PLAY=true
ENABLE__SYSTEM_FAILURE_ERROR__SEND_MESSAGE=true
ENABLE__SYSTEM_FAILURE_ERROR__STOCK_PRICE=true
ENABLE__SYSTEM_FAILURE_ERROR__TRACK_DELIVERY_ORDER=true
```

**Key Characteristics:**
- Functions return `success: false` with complex technical error messages
- Tests LLM technical terminology translation skills
- Requires sophisticated error communication and user confidence management
- Challenges domain-specific infrastructure knowledge (telecommunications, payment systems, smart home, etc.)

### 🎲 ADHOC Rules (8 variables)

These uncertainties simulate ad-hoc, unstable real-world conditions (e.g., flaky external services, transient failures, repeated retries). They are often used together with *consecutive failure* logic in the evaluator.

```bash
ENABLE__ADHOC__TRACK_ORDER=true
ENABLE__ADHOC__LOCK_LOCK=true
ENABLE__ADHOC__LOCK_UNLOCK=true
ENABLE__ADHOC__COLOR_SET=true
ENABLE__ADHOC__GET_CALL_HISTORY=true
ENABLE__ADHOC__MAKE_CALL=true
ENABLE__ADHOC__PLAY=true
ENABLE__ADHOC__STOCK_PRICE=true
```

**Key Characteristics:**
- Functions may intermittently fail or behave unpredictably
- Often combined with logic that detects consecutive failures across steps
- Tests LLM robustness, retry strategies, and error-aware planning

### Unclear Functionality Boundary (20 functions)

This complexity category challenges agents to discern between functions that possess superficial similarities yet distinct operational semantics. This ambiguity is introduced into the LLM agent's environment via the prompt specification located at `API_Complexity/extracted_api/centralized_prompt_unclear.md`.

The specific functions exhibiting these overlapping characteristics include:
```bash
   [
        'broadcast_alert', 'color_scene_set', 'color_temperature_set',
        'create_calendar_event', 'create_timer', 'device_deactivate',
        'fetch_notification_status', 'find_communication_device',
        'get_calendar_events', 'get_content_details', 'get_device_inventory',
        'hvac_mode_set', 'initiate_call_session', 'place_pickup_order',
        'place_restaurant_order', 'schedule_action', 'search_contact_directory',
        'send_chat_message', 'sync_messages', 'temperature_schedule'
    ]
```

## Functions by Environment

### CommunicationController (5 functions)

```bash
# Feature Limitation + Partially Irrelevant + ADHOC
ENABLE__FEATURE_LIMITATION_ERROR__GET_CALL_HISTORY=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_CALL_HISTORY=true
ENABLE__ADHOC__GET_CALL_HISTORY=true

ENABLE__FEATURE_LIMITATION_ERROR__GET_MESSAGES=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_MESSAGES=true

# Single Uncertainties
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__FIND_CALL_DEVICE=true
ENABLE__INFORMATIONAL_NOTICE__MAKE_CALL=true

# System Failure + ADHOC
ENABLE__SYSTEM_FAILURE_ERROR__MAKE_CALL=true
ENABLE__SYSTEM_FAILURE_ERROR__SEND_MESSAGE=true
ENABLE__ADHOC__MAKE_CALL=true
```

### InformationControlEnv (5 functions)

```bash
# Feature Limitation + Partially Irrelevant + Informational Notice
ENABLE__FEATURE_LIMITATION_ERROR__STOCK_WATCHLIST=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__STOCK_WATCHLIST=true
ENABLE__INFORMATIONAL_NOTICE__STOCK_WATCHLIST=true

ENABLE__FEATURE_LIMITATION_ERROR__WEATHER_FORECAST=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__WEATHER_FORECAST=true

# Single Uncertainties
ENABLE__FEATURE_LIMITATION_ERROR__NEWS_PERSONALIZED=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__KNOWLEDGE_LOOKUP=true

# System Failure + ADHOC
ENABLE__SYSTEM_FAILURE_ERROR__STOCK_PRICE=true
ENABLE__ADHOC__STOCK_PRICE=true
```

### SmartHomeEnv (5 functions)

```bash
# Feature Limitation + System Failure
ENABLE__FEATURE_LIMITATION_ERROR__GET_USER_INVENTORY=true
ENABLE__SYSTEM_FAILURE_ERROR__GET_USER_INVENTORY=true

# Informational + System Failure + ADHOC
ENABLE__INFORMATIONAL_NOTICE__COLOR_SET=true
ENABLE__SYSTEM_FAILURE_ERROR__COLOR_SET=true
ENABLE__ADHOC__COLOR_SET=true

# Informational Only
ENABLE__INFORMATIONAL_NOTICE__TEMPERATURE_SET=true

# ADHOC Only
ENABLE__ADHOC__LOCK_LOCK=true
ENABLE__ADHOC__LOCK_UNLOCK=true
```

### TimeNotificationEnv (1 function)

```bash
# Feature Limitation + Informational Notice
ENABLE__FEATURE_LIMITATION_ERROR__GET_NOTIFICATIONS=true
ENABLE__INFORMATIONAL_NOTICE__GET_NOTIFICATIONS=true
```

### CulinaryControlEnv (4 functions)

```bash
# Informational Notice
ENABLE__INFORMATIONAL_NOTICE__CREATE_MEAL_PLAN=true

# Partially Irrelevant Information
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_RESTAURANT_MENU=true
ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__SEARCH_RECIPES=true

# System Failure Error
ENABLE__SYSTEM_FAILURE_ERROR__PLACE_DELIVERY_ORDER=true
```

### MediaControlEnv (3 functions)

```bash
# Informational Notice
ENABLE__INFORMATIONAL_NOTICE__GET_MEDIA_DETAILS=true
ENABLE__INFORMATIONAL_NOTICE__SEARCH_MEDIA=true

# System Failure + ADHOC
ENABLE__SYSTEM_FAILURE_ERROR__PLAY=true
ENABLE__ADHOC__PLAY=true
```

### TransactionEnv (2 functions)

```bash
# Feature Limitation + ADHOC
ENABLE__FEATURE_LIMITATION_ERROR__TRACK_ORDER=true
ENABLE__ADHOC__TRACK_ORDER=true

# System Failure Error
ENABLE__SYSTEM_FAILURE_ERROR__TRACK_DELIVERY_ORDER=true
```

## Functions with Multiple Uncertainties

The following functions have multiple uncertainty types implemented:

1. **get_call_history** (CommunicationController)
   - `ENABLE__FEATURE_LIMITATION_ERROR__GET_CALL_HISTORY`
   - `ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_CALL_HISTORY`
   - `ENABLE__ADHOC__GET_CALL_HISTORY`

2. **get_messages** (CommunicationController)
   - `ENABLE__FEATURE_LIMITATION_ERROR__GET_MESSAGES`
   - `ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_MESSAGES`

3. **get_notifications** (TimeNotificationEnv)
   - `ENABLE__FEATURE_LIMITATION_ERROR__GET_NOTIFICATIONS`
   - `ENABLE__INFORMATIONAL_NOTICE__GET_NOTIFICATIONS`

4. **stock_watchlist** (InformationControlEnv)
   - `ENABLE__FEATURE_LIMITATION_ERROR__STOCK_WATCHLIST`
   - `ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__STOCK_WATCHLIST`
   - `ENABLE__INFORMATIONAL_NOTICE__STOCK_WATCHLIST`

5. **weather_forecast** (InformationControlEnv)
   - `ENABLE__FEATURE_LIMITATION_ERROR__WEATHER_FORECAST`
   - `ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__WEATHER_FORECAST`

6. **make_call** (CommunicationController)
   - `ENABLE__INFORMATIONAL_NOTICE__MAKE_CALL`
   - `ENABLE__SYSTEM_FAILURE_ERROR__MAKE_CALL`
   - `ENABLE__ADHOC__MAKE_CALL`

7. **color_set** (SmartHomeEnv)
   - `ENABLE__INFORMATIONAL_NOTICE__COLOR_SET`
   - `ENABLE__SYSTEM_FAILURE_ERROR__COLOR_SET`
   - `ENABLE__ADHOC__COLOR_SET`

8. **get_user_inventory** (SmartHomeEnv)
   - `ENABLE__FEATURE_LIMITATION_ERROR__GET_USER_INVENTORY`
   - `ENABLE__SYSTEM_FAILURE_ERROR__GET_USER_INVENTORY`

9. ...

## Usage Instructions

### Single Uncertainty Activation
```bash
export ENABLE__FEATURE_LIMITATION_ERROR__TRACK_ORDER=true
python your_test_script.py
```

### Multiple Uncertainty Activation
```bash
export ENABLE__FEATURE_LIMITATION_ERROR__GET_CALL_HISTORY=true
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_CALL_HISTORY=true
export ENABLE__ADHOC__GET_CALL_HISTORY=true
python your_test_script.py
```

### Bulk Activation Script
```bash
#!/bin/bash
# Activate all Feature Limitation Errors
export ENABLE__FEATURE_LIMITATION_ERROR__GET_CALL_HISTORY=true
export ENABLE__FEATURE_LIMITATION_ERROR__GET_MESSAGES=true
export ENABLE__FEATURE_LIMITATION_ERROR__GET_NOTIFICATIONS=true
export ENABLE__FEATURE_LIMITATION_ERROR__GET_USER_INVENTORY=true
export ENABLE__FEATURE_LIMITATION_ERROR__NEWS_PERSONALIZED=true
export ENABLE__FEATURE_LIMITATION_ERROR__STOCK_WATCHLIST=true
export ENABLE__FEATURE_LIMITATION_ERROR__TRACK_ORDER=true
export ENABLE__FEATURE_LIMITATION_ERROR__WEATHER_FORECAST=true

# Activate all Partially Irrelevant Information
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__FIND_CALL_DEVICE=true
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_CALL_HISTORY=true
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_MESSAGES=true
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__GET_RESTAURANT_MENU=true
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__KNOWLEDGE_LOOKUP=true
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__SEARCH_RECIPES=true
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__STOCK_WATCHLIST=true
export ENABLE__PARTIALLY_IRRELEVANT_INFORMATION__WEATHER_FORECAST=true

# Activate all Informational Notices
export ENABLE__INFORMATIONAL_NOTICE__COLOR_SET=true
export ENABLE__INFORMATIONAL_NOTICE__CREATE_MEAL_PLAN=true
export ENABLE__INFORMATIONAL_NOTICE__GET_MEDIA_DETAILS=true
export ENABLE__INFORMATIONAL_NOTICE__GET_NOTIFICATIONS=true
export ENABLE__INFORMATIONAL_NOTICE__MAKE_CALL=true
export ENABLE__INFORMATIONAL_NOTICE__SEARCH_MEDIA=true
export ENABLE__INFORMATIONAL_NOTICE__TEMPERATURE_SET=true
export ENABLE__INFORMATIONAL_NOTICE__STOCK_WATCHLIST=true

# Activate all System Failure Errors
export ENABLE__SYSTEM_FAILURE_ERROR__COLOR_SET=true
export ENABLE__SYSTEM_FAILURE_ERROR__GET_USER_INVENTORY=true
export ENABLE__SYSTEM_FAILURE_ERROR__MAKE_CALL=true
export ENABLE__SYSTEM_FAILURE_ERROR__PLACE_DELIVERY_ORDER=true
export ENABLE__SYSTEM_FAILURE_ERROR__PLAY=true
export ENABLE__SYSTEM_FAILURE_ERROR__SEND_MESSAGE=true
export ENABLE__SYSTEM_FAILURE_ERROR__STOCK_PRICE=true
export ENABLE__SYSTEM_FAILURE_ERROR__TRACK_DELIVERY_ORDER=true

# Activate all ADHOC Uncertainties
export ENABLE__ADHOC__TRACK_ORDER=true
export ENABLE__ADHOC__LOCK_LOCK=true
export ENABLE__ADHOC__LOCK_UNLOCK=true
export ENABLE__ADHOC__COLOR_SET=true
export ENABLE__ADHOC__GET_CALL_HISTORY=true
export ENABLE__ADHOC__MAKE_CALL=true
export ENABLE__ADHOC__PLAY=true
export ENABLE__ADHOC__STOCK_PRICE=true
```

## Related Files

- **Demo Scripts**: `uncertainty_demos/` directory contains test scripts for each uncertainty
- **Evaluation References**: `function_uncertainty_references/` contains LLM evaluation criteria
- **Documentation**: Individual uncertainty types are documented in their respective reference files

## Statistics Summary

| Uncertainty Type | Count | Percentage |
|------------------|-------|------------|
| Feature Limitation Error | 8 | 20.0% |
| Partially Irrelevant Information | 8 | 20.0% |
| Informational Notice | 8 | 20.0% |
| System Failure Error | 8 | 20.0% |
| Adhoc Rules | 8 | 20.0% |
| Unclear Functionality Boundary | 20 | 33.3% |
| **Total** | **60** | **100% |

---

*Last updated: December 11, 2025*
*Total uncertainties tracked: 60*
