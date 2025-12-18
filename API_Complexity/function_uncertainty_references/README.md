# Function Uncertainty References

This directory contains evaluation criteria and reference materials for LLM testing with various function uncertainties. Each file documents specific uncertainty behaviors and provides detailed evaluation criteria for LLM Judge systems.

## Purpose

These reference files are designed to:
- Provide comprehensive evaluation criteria for LLM responses to function uncertainties
- Define ideal response patterns that LLMs should demonstrate
- Establish scoring rubrics for systematic evaluation
- Document common failure patterns to watch for

## File Structure

Each uncertainty reference file follows this structure:

1. **Error Scenario Overview** - Context and background
2. **Root Cause Analysis** - Technical explanation of the uncertainty
3. **Error Message Analysis** - Detailed breakdown of error messages and hints
4. **Expected Solution Approach** - Ideal LLM thought process
5. **Ideal Response Pattern** - Step-by-step examples of good responses
6. **Evaluation Criteria** - Scoring rubrics and assessment guidelines
7. **Common Mistakes** - Anti-patterns and failure modes to identify

## Available Uncertainty References

### get_messages_feature_limitation_error.md
- **Uncertainty Type**: Feature Limitation Error
- **Function**: `get_messages`
- **Scenario**: Temporary system limitation with misleading hint
- **Key Challenge**: Interpreting "recent history" hint for parameter adjustment
- **Environment Variable**: `ENABLE__FEATURE_LIMITATION_ERROR__GET_MESSAGES`

### get_notifications_feature_limitation_error.md
- **Uncertainty Type**: Feature Limitation Error
- **Function**: `get_notifications`
- **Scenario**: Historical notification access limitation with clearer hint
- **Key Challenge**: Interpreting "Recent activity remains available" hint for limit reduction
- **Environment Variable**: `ENABLE__FEATURE_LIMITATION_ERROR__GET_NOTIFICATIONS`

### weather_forecast_feature_limitation_error.md
- **Uncertainty Type**: Feature Limitation Error
- **Function**: `weather_forecast`
- **Scenario**: Regional weather data service limitations with geographic alternatives
- **Key Challenge**: Applying geographic knowledge and spatial reasoning for location alternatives
- **Environment Variable**: `ENABLE__FEATURE_LIMITATION_ERROR__WEATHER_FORECAST`

### track_order_feature_limitation_error.md
- **Uncertainty Type**: Feature Limitation Error
- **Function**: `track_order`
- **Scenario**: Shipping carrier service limitations with carrier reconstruction alternatives
- **Key Challenge**: String manipulation and format analysis for order ID reconstruction with alternative carriers
- **Environment Variable**: `ENABLE__FEATURE_LIMITATION_ERROR__TRACK_ORDER`

### stock_watchlist_feature_limitation_error.md
- **Uncertainty Type**: Feature Limitation Error
- **Function**: `stock_watchlist`
- **Scenario**: Watchlist capacity limitations with multi-function technical workaround
- **Key Challenge**: Function discovery, exchange knowledge, and data integration using stock_price alternative
- **Environment Variable**: `ENABLE__FEATURE_LIMITATION_ERROR__STOCK_WATCHLIST`

### news_personalized_feature_limitation_error.md
- **Uncertainty Type**: Feature Limitation Error
- **Function**: `news_personalized`
- **Scenario**: Personalization capacity limitations with multi-category technical workaround
- **Key Challenge**: User preferences discovery, news category knowledge, and data aggregation using news_by_category alternative
- **Environment Variable**: `ENABLE__FEATURE_LIMITATION_ERROR__NEWS_PERSONALIZED`

### get_user_inventory_feature_limitation_error.md
- **Uncertainty Type**: Feature Limitation Error
- **Function**: `get_user_inventory`
- **Scenario**: Automatic user detection limitations with explicit parameter workaround
- **Key Challenge**: Function signature analysis, parameter discovery, and systematic user ID testing
- **Environment Variable**: `ENABLE__FEATURE_LIMITATION_ERROR__GET_USER_INVENTORY`

### get_call_history_feature_limitation_error.md
- **Uncertainty Type**: Feature Limitation Error
- **Function**: `get_call_history`
- **Scenario**: Historical data access limitations with time range reduction workaround
- **Key Challenge**: Hint interpretation, ISO 8601 time range knowledge, and systematic time period reduction
- **Environment Variable**: `ENABLE__FEATURE_LIMITATION_ERROR__GET_CALL_HISTORY`

### make_call_system_failure_error.md
- **Uncertainty Type**: System Failure Error
- **Function**: `make_call`
- **Scenario**: Complex telecommunications infrastructure failures with technical error messages
- **Key Challenge**: Technical terminology translation, user communication, and error complexity handling
- **Environment Variable**: `ENABLE__SYSTEM_FAILURE_ERROR__MAKE_CALL`

### place_delivery_order_system_failure_error.md
- **Uncertainty Type**: System Failure Error
- **Function**: `place_delivery_order`
- **Scenario**: Complex payment gateway infrastructure failures with SSL/TLS and PCI compliance error messages
- **Key Challenge**: Payment security terminology translation, user trust management, and payment safety communication
- **Environment Variable**: `ENABLE__SYSTEM_FAILURE_ERROR__PLACE_DELIVERY_ORDER`

### send_message_system_failure_error.md
- **Uncertainty Type**: System Failure Error
- **Function**: `send_message`
- **Scenario**: Complex message queue infrastructure failures with RabbitMQ/AMQP terminology and cluster management concepts
- **Key Challenge**: Message queue terminology translation, messaging status communication, and infrastructure complexity handling
- **Environment Variable**: `ENABLE__SYSTEM_FAILURE_ERROR__SEND_MESSAGE`

### color_set_system_failure_error.md
- **Uncertainty Type**: System Failure Error
- **Function**: `color_set`
- **Scenario**: Complex smart home hub infrastructure failures with ZigBee/Z-Wave terminology and embedded system concepts
- **Key Challenge**: Smart home infrastructure terminology translation, manual control alternatives communication, and hub failure complexity handling
- **Environment Variable**: `ENABLE__SYSTEM_FAILURE_ERROR__COLOR_SET`

### track_delivery_order_system_failure_error.md
- **Uncertainty Type**: System Failure Error
- **Function**: `track_delivery_order`
- **Scenario**: Complex GPS/mapping infrastructure failures with API terminology, circuit breaker patterns, and SSL certificate issues
- **Key Challenge**: Delivery vs tracking distinction, GPS/mapping terminology translation, and user anxiety management during delivery tracking failures
- **Environment Variable**: `ENABLE__SYSTEM_FAILURE_ERROR__TRACK_DELIVERY_ORDER`

### get_user_inventory_system_failure_error.md
- **Uncertainty Type**: System Failure Error
- **Function**: `get_user_inventory`
- **Scenario**: Complex database cluster infrastructure failures with PostgreSQL terminology, connection pool concepts, and replication lag issues
- **Key Challenge**: Database infrastructure terminology translation, system-wide vs user account issue distinction, and smart home inventory communication during database failures
- **Environment Variable**: `ENABLE__SYSTEM_FAILURE_ERROR__GET_USER_INVENTORY`

### play_system_failure_error.md
- **Uncertainty Type**: System Failure Error
- **Function**: `play`
- **Scenario**: Complex CDN infrastructure failures with BGP routing details, cache system failures, and network topology information
- **Key Challenge**: CDN infrastructure terminology translation, regional impact communication, and media streaming error handling during content delivery network failures
- **Environment Variable**: `ENABLE__SYSTEM_FAILURE_ERROR__PLAY`

### stock_price_system_failure_error.md
- **Uncertainty Type**: System Failure Error
- **Function**: `stock_price`
- **Scenario**: Complex financial data provider infrastructure failures with FIX protocol terminology, market data gateway specifications, and network infrastructure details
- **Key Challenge**: Financial infrastructure terminology translation, market vs infrastructure distinction, and financial data communication during market data system failures
- **Environment Variable**: `ENABLE__SYSTEM_FAILURE_ERROR__STOCK_PRICE`

## Usage

These files are intended for:

1. **LLM Judge Systems** - Automated evaluation of LLM responses
2. **Human Evaluators** - Manual assessment guidelines
3. **Development Teams** - Understanding uncertainty behaviors
4. **Research** - Studying LLM problem-solving capabilities

## Evaluation Approach

Each reference file provides:

### Scoring Scales
- **5/5 Exceptional**: Demonstrates advanced problem-solving
- **4/5 Good**: Shows solid understanding with minor gaps
- **3/5 Average**: Basic recognition but limited approach
- **2/5 Below Average**: Poor analysis and solution attempts
- **1/5 Poor**: Fails to recognize or address the uncertainty

### Key Evaluation Dimensions
- **Error Recognition**: Identifies and analyzes error conditions
- **Hint Interpretation**: Extracts actionable insights from error messages
- **Systematic Approach**: Develops logical problem-solving strategies
- **User Communication**: Explains situations and solutions clearly
- **Persistence**: Maintains problem-solving effort appropriately

## Integration with Demo Files

Each uncertainty reference corresponds to demo files in the `uncertainty_demos/` directory:
- Reference files provide evaluation criteria
- Demo files provide testing infrastructure
- Both work together to enable comprehensive LLM assessment

## Future Extensions

This directory can be extended with additional uncertainty types:
- `partially_irrelevant_information` uncertainties
- `data_inconsistency` uncertainties
- `performance_degradation` uncertainties
- `authentication_failures` uncertainties
- Custom uncertainty patterns

## Contributing

When adding new uncertainty references:

1. Follow the established file structure
2. Provide comprehensive evaluation criteria
3. Include concrete examples of good/bad responses
4. Define clear scoring rubrics
5. Document common failure patterns
6. Ensure alignment with corresponding demo files

This systematic approach enables consistent and thorough evaluation of LLM capabilities across various uncertainty scenarios.
