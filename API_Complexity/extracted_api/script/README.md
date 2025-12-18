# API Extraction Scripts

This directory contains scripts to extract API information from all environments in the CamelSyntheticAPI project.

## Quick Start

To extract APIs from all environments at once:

```bash
cd extracted_api/script
python extract_all_apis.py
```

Or make it executable and run directly:

```bash
./extract_all_apis.py
```

## What It Does

The master script `extract_all_apis.py` automatically runs all individual extraction scripts:

- `extract_smart_home_api.py` → `SmartHomeAPI.json`
- `extract_info_control_api.py` → `InformationControlAPI.json`
- `extract_media_control_api.py` → `MediaControlAPI.json`
- `extract_communication_controller_api.py` → `CommunicationControllerAPI.json`
- `extract_culinary_control_api.py` → `CulinaryControlEnvAPI.json`
- `extract_time_notification_api.py` → `TimeNotificationEnvAPI.json`
- `extract_transaction_api.py` → `TransactionEnvAPI.json`

## Output

All generated JSON files are saved to `../api_file/` directory.

## Features

- ✅ Runs all extraction scripts in sequence
- ✅ Error handling and timeout protection
- ✅ Progress reporting with clear status messages
- ✅ Comprehensive summary with tool counts
- ✅ Detects missing scripts and reports warnings
- ✅ Fast execution (typically completes in under 1 second)

## Individual Scripts

You can also run individual extraction scripts if needed:

```bash
python extract_smart_home_api.py
python extract_communication_controller_api.py
# etc.
```

## Troubleshooting

If a script fails:
1. Check the error message in the output
2. Ensure all environment dependencies are properly installed
3. Verify that the environment's `tools` directory and `ALL_TOOLS` are properly configured
4. Run the individual script directly to get more detailed error information
