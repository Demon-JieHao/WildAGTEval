# LLM Judge System

An automated evaluation system for agent responses using Claude API to assess behavioral alignment against function-specific criteria.

## Overview

The LLM Judge system evaluates agent error-handling responses by comparing them against reference markdown files containing detailed evaluation criteria. It uses Claude API to perform behavioral alignment assessment rather than exact matching, making it suitable for complex error-handling scenarios where multiple valid responses exist.

## Features

- **Single File Evaluation**: Evaluate individual agent responses
- **Batch Processing**: Process multiple files in parallel using multiprocessing
- **Auto-matching**: Automatically find matching reference files for agent responses
- **Structured Output**: Generate detailed JSON evaluation reports with scores and evidence
- **Function-Specific Criteria**: Support different evaluation criteria for different functions
- **Claude API Integration**: Uses Claude Opus for consistent, high-quality evaluations

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Claude API credentials (choose one):

**Option A: AWS Bedrock (Recommended)**
```bash
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
# Or use ~/.aws/credentials file
```

**Option B: Direct Anthropic API**
```bash
export ANTHROPIC_API_KEY="your_api_key"
```

**Option C: .env file**
Create a `.env` file in the eval_mock_API_Real directory:
```
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
# OR
ANTHROPIC_API_KEY=your_api_key
```

## Directory Structure

```
eval_mock_API_Real/
├── llm_judge_system/           # Main system code
├── turn_level_tf_results/      # Agent response files
├── function_uncertainty_references/  # Reference markdown files
└── judge_results/              # Output directory (created automatically)
```

## Usage

### Quick Start

Run from the `eval_mock_API_Real` directory:

```bash
# Test configuration
python llm_judge_system/main.py --config

# Setup directories
python llm_judge_system/main.py --setup

# Single evaluation with auto-matching
python llm_judge_system/main.py --agent_json ./turn_level_tf_results/featlimit/Conv_user1_TransactionEnv_shopping_batch_scenario4_orders_TurnLevelTF_Turn2_Step0_track_order.json

# Batch evaluation
python llm_judge_system/main.py --batch --agent_dir ./turn_level_tf_results/featlimit/ --max_files 5
```

### Command Line Options

#### Single Evaluation Mode
```bash
python llm_judge_system/main.py \
  --agent_json path/to/agent.json \
  [--reference_md path/to/reference.md] \
  [--output path/to/output.json] \
  [--run_id 0]
```

#### Batch Evaluation Mode
```bash
python llm_judge_system/main.py --batch \
  --agent_dir path/to/agent/directory/ \
  [--reference_dir path/to/reference/directory/] \
  [--output_dir path/to/output/directory/] \
  [--file_pattern "*_track_order.json"] \
  [--max_files 10] \
  [--max_workers 50] \
  [--sequential] \
  [--run_id 0]
```

### Examples

**Single Evaluation with Manual Reference:**
```bash
python llm_judge_system/main.py \
  --agent_json ./turn_level_tf_results/featlimit/Conv_user1_TransactionEnv_shopping_batch_scenario4_orders_TurnLevelTF_Turn2_Step0_track_order.json \
  --reference_md ./function_uncertainty_references/track_order_feature_limitation_error.md \
  --output ./judge_results/single_eval.json
```

**Batch Evaluation with Limits:**
```bash
python llm_judge_system/main.py --batch \
  --agent_dir ./turn_level_tf_results/featlimit/ \
  --output_dir ./judge_results/batch_run_1 \
  --max_files 20 \
  --max_workers 10 \
  --run_id 1
```

**Sequential Processing (for debugging):**
```bash
python llm_judge_system/main.py --batch \
  --agent_dir ./turn_level_tf_results/featlimit/ \
  --sequential \
  --max_files 5
```

## Output Format

The system generates structured JSON evaluation results:

```json
{
  "evaluation_summary": {
    "agent_response_path": "/absolute/path/to/agent.json",
    "reference_markdown_path": "/absolute/path/to/reference.md",
    "function_name": "track_order",
    "total_score": "2/5",
    "overall_performance": "Below Average"
  },
  "detailed_scores": {
    "situation_understanding": {
      "score": "2/5",
      "level": "Below Average",
      "evidence": "Agent tried multiple carriers but used incorrect order ID format",
      "reasoning": "Shows partial understanding but failed format analysis",
      "reference_criteria": "✅ Excellent Response requires correct format analysis..."
    }
  },
  "improvement_suggestions": [
    "Analyze order ID format structure before making alternative attempts"
  ],
  "alignment_assessment": "Agent showed systematic approach but failed core requirement"
}
```

## Supported Functions

Currently supports evaluation of these functions:
- `track_order` - Order tracking with feature limitation errors
- `get_messages` - Message retrieval with various error types

## Reference File Matching

The system automatically matches agent files to reference files:
- `*_track_order.json` → `track_order_feature_limitation_error.md`
- `*_get_messages.json` → `get_messages_feature_limitation_error.md`

## Configuration

Key configuration options in `config.py`:
- **Claude Model**: `us.anthropic.claude-opus-4-20250514-v1:0`
- **Temperature**: `0.1` (low for consistent evaluation)
- **Max Workers**: `50` (for parallel processing)
- **Max Tokens**: `2000` (sufficient for detailed evaluations)

## Troubleshooting

### Common Issues

1. **Claude API Errors**
   - Check your credentials are set correctly
   - Verify AWS/Anthropic API access
   - Check rate limits

2. **File Not Found Errors**
   - Ensure agent JSON files exist in specified directory
   - Check reference markdown files are present
   - Verify file patterns match your files

3. **JSON Parsing Errors**
   - Claude occasionally returns non-JSON responses
   - Error results are saved with raw responses for debugging
   - Try reducing max_tokens if responses are cut off

4. **Multiprocessing Issues**
   - Use `--sequential` flag to disable parallel processing
   - Reduce `--max_workers` if experiencing resource issues

### Debugging

Enable verbose output by examining intermediate files:
- Check `judge_results/` directory for saved evaluations
- Review error files prefixed with `error_`
- Examine batch summary files for statistics

## Development

### Adding New Functions

1. Add function name to `FILE_PATTERNS['supported_functions']` in `config.py`
2. Update file matching logic in `find_matching_reference_file()`
3. Create corresponding reference markdown files

### Testing

Test individual components:
```bash
# Test Claude client
python llm_judge_system/claude_client.py

# Test single evaluation
python llm_judge_system/judge_evaluator.py

# Test batch processing
python llm_judge_system/batch_judge.py

# Test configuration
python llm_judge_system/config.py
```

## Performance

- **Single evaluation**: ~10-30 seconds per file
- **Batch processing**: Scales linearly with number of workers
- **Memory usage**: Minimal per worker process
- **Rate limits**: Respects Claude API rate limits automatically

## Support

For issues related to:
- **Claude API**: Check Anthropic documentation
- **File formats**: Ensure JSON and Markdown files are properly formatted
- **Performance**: Adjust max_workers and max_files parameters
- **Evaluation criteria**: Review reference markdown files for expected format
