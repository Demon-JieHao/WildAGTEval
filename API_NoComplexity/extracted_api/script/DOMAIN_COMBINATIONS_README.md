# Domain API Combination Script

This script creates combined API files based on the domain selection guide for conversation generation and LLM evaluation.

## Quick Start

Generate all 6 domain combinations at once:
```bash
python extracted_api/script/combine_domain_apis.py all
```

Generate a specific combination:
```bash
python extracted_api/script/combine_domain_apis.py home_entertainment
```

List all available combinations:
```bash
python extracted_api/script/combine_domain_apis.py list
```

## Available Domain Combinations

Based on `domain_selection_guide.md`, the following 6 combinations are available:

### 3-Domain Combinations

#### 1. Home & Entertainment Package (`home_entertainment`)
- **Domains**: SmartHomeEnv + MediaControlEnv + InformationControlEnv
- **Tools**: 47 total (19 + 16 + 12)
- **Output**: `HomeEntertainmentAPI.json`
- **Use Case**: Evening routines, movie night preparation, weather-responsive entertainment

#### 2. Daily Life Management (`daily_life_management`)
- **Domains**: SmartHomeEnv + TimeNotificationEnv + InformationControlEnv
- **Tools**: 39 total (19 + 8 + 12)
- **Output**: `DailyLifeManagementAPI.json`
- **Use Case**: Morning/evening automation, weather-aware scheduling, energy-efficient routines

#### 3. Social & Entertainment Hub (`social_entertainment`)
- **Domains**: CommunicationController + MediaControlEnv + CulinaryControlEnv
- **Tools**: 35 total (7 + 16 + 12)
- **Output**: `SocialEntertainmentAPI.json`
- **Use Case**: Party hosting, group movie nights, social event coordination

#### 4. Shopping & Planning Assistant (`shopping_planning`)
- **Domains**: TransactionEnv + CulinaryControlEnv + TimeNotificationEnv
- **Tools**: 32 total (12 + 12 + 8)
- **Output**: `ShoppingPlanningAPI.json`
- **Use Case**: Meal planning, budget management, cooking reminders

### 4-Domain Combinations

#### 5. Complete Daily Assistant (`complete_daily_assistant`)
- **Domains**: SmartHomeEnv + InformationControlEnv + TimeNotificationEnv + CommunicationController
- **Tools**: 46 total (19 + 12 + 8 + 7)
- **Output**: `CompleteDailyAssistantAPI.json`
- **Use Case**: Comprehensive daily life management, intelligent personal assistance

#### 6. Entertainment & Social Coordinator (`entertainment_social_coordinator`)
- **Domains**: MediaControlEnv + CommunicationController + CulinaryControlEnv + TimeNotificationEnv
- **Tools**: 43 total (16 + 7 + 12 + 8)
- **Output**: `EntertainmentSocialCoordinatorAPI.json`
- **Use Case**: Large event hosting, multi-day event planning, dynamic event management

## Output Location

All combined API files are saved to: `extracted_api/combined_api_file/`

## Usage Examples

```bash
# Create all combinations
python combine_domain_apis.py all

# Create just the home entertainment package
python combine_domain_apis.py home_entertainment

# Create the complete daily assistant combination
python combine_domain_apis.py complete_daily_assistant

# List all available combinations with descriptions
python combine_domain_apis.py list
```

## Script Features

- ✅ **Configurable combinations** based on domain selection guide
- ✅ **Automatic directory creation** for output files
- ✅ **Tool count validation** against expected values
- ✅ **Detailed progress reporting** with breakdown by domain
- ✅ **Error handling** with clear error messages
- ✅ **Flexible usage** - create individual or all combinations

## Integration with Conversation Generation

These domain combinations are designed for:

1. **3-domain combinations**: Baseline LLM evaluation and general capability assessment
2. **4-domain combinations**: Advanced reasoning evaluation and complex scenario testing
3. **Diverse complexity levels**: From 32 to 47 tools per combination
4. **Real-world scenarios**: Each combination reflects genuine user interaction patterns

## File Structure

```
extracted_api/
├── api_file/                    # Individual domain API files (input)
├── combined_api_file/           # Combined domain API files (output)
│   ├── HomeEntertainmentAPI.json
│   ├── DailyLifeManagementAPI.json
│   ├── SocialEntertainmentAPI.json
│   ├── ShoppingPlanningAPI.json
│   ├── CompleteDailyAssistantAPI.json
│   └── EntertainmentSocialCoordinatorAPI.json
└── script/
    ├── combine_domain_apis.py   # Main combination script
    └── extract_all_apis.py      # Individual API extraction script
```

## Dependencies

The script requires all individual domain API files to be present in `extracted_api/api_file/`. 
Run `python extract_all_apis.py` first if needed to generate the individual API files.
