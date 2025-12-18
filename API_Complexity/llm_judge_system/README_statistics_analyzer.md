# LLM Judge Statistics Analyzer

A comprehensive tool for analyzing batch summary statistics from LLM Judge results across multiple experimental conditions.

## Overview

The Statistics Analyzer processes LLM Judge results organized in the following directory structure:
```
test_with_uncertainties/${ENV_DIR}/turn_level_tf_${model_config}_adhoc+unclear_${error_type}_${seed}/${func}/judge_results/
```

It automatically:
- Discovers paths containing `judge_results` directories
- Parses metadata from directory names (environment, model, error type, seed, function)
- Collects `batch_summary_run_*.json` files from multiple runs
- Calculates mean and standard deviation statistics
- Generates formatted tables and detailed JSON output

## Usage Examples

### Basic Usage

```bash
# Analyze all feature_limitation results for track_order function
python llm_judge_system/statistics_analyzer.py \
  --pattern "test_with_uncertainties/*/turn_level_tf_*_adhoc+unclear_feature_limitation_*/track_order/"

# Analyze all functions for a specific environment
python llm_judge_system/statistics_analyzer.py \
  --pattern "test_with_uncertainties/TransactionEnv_transformed/turn_level_tf_*_adhoc+unclear_*_*/*/"
```

### Multi-Pattern Analysis

```bash
# Compare feature_limitation vs system_failure for track_order
python llm_judge_system/statistics_analyzer.py \
  --patterns \
    "test_with_uncertainties/*/turn_level_tf_*_adhoc+unclear_feature_limitation_*/track_order/" \
    "test_with_uncertainties/*/turn_level_tf_*_adhoc+unclear_system_failure_*/track_order/"
```

### Save Detailed Results

```bash
# Generate both table output and detailed JSON
python llm_judge_system/statistics_analyzer.py \
  --pattern "test_with_uncertainties/*/*/" \
  --output detailed_results.json \
  --verbose
```

### Advanced Patterns

```bash
# Analyze specific model configurations
python llm_judge_system/statistics_analyzer.py \
  --pattern "test_with_uncertainties/*/turn_level_tf_claude37_*_adhoc+unclear_*_*/*/"

# Analyze all conditions (default)
python llm_judge_system/statistics_analyzer.py
```

## Output Format

### Console Table
```
====================================================================================================
LLM JUDGE STATISTICS SUMMARY
====================================================================================================
Environment     Model        Function           Error Type   Mean±Std     Count
----------------------------------------------------------------------------------------------------
TransactionEnv  claude3  track_order        feature      3.83±0.05    3
TransactionEnv  claude3  track_order        feature      3.81±0.03    3
TransactionEnv  ambersontes  track_order        feature      3.31±0.06    3
====================================================================================================

OVERALL STATISTICS:
Total Conditions: 3
Overall Mean: 3.650
Overall Std: 0.298
Min Mean: 3.307
Max Mean: 3.833
```

### JSON Output
```json
{
  "table_summary": "============================================================================================================================================\nLLM JUDGE STATISTICS SUMMARY\n============================================================================================================================================\nEnvironment     Model                          Function           Error Type           Mean±Std     Count   \n--------------------------------------------------------------------------------------------------------------------------------------------\nTransactionEnv  ambersontest                   track_order        feature_limitation   3.31±0.06    3       \nTransactionEnv  claude37_no_think          track_order        feature_limitation   3.81±0.03    3       \nTransactionEnv  claude37_think             track_order        feature_limitation   3.83±0.05    3       \n============================================================================================================================================\n\nOVERALL STATISTICS:\nTotal Conditions: 3\nOverall Mean: 3.650\nOverall Std: 0.298\nMin Mean: 3.307\nMax Mean: 3.833",
  "detailed_results": {
    "TransactionEnv_transformed_claude37_think_feature_limitation_track_order": {
      "metadata": {
        "env_dir": "TransactionEnv_transformed",
        "model_config": "claude37_think",
        "error_type": "feature_limitation",
        "seed": "s0",
        "func": "track_order"
      },
      "statistics": {
        "mean": 3.833333333333333,
        "std": 0.046188021535170105,
        "count": 3
      },
      "raw_scores": [3.78, 3.86, 3.86]
    }
  },
  "overall_statistics": {
    "total_conditions": 3,
    "overall_mean": 3.65,
    "overall_std": 0.29756418541962404,
    "min_mean": 3.3066666666666666,
    "max_mean": 3.833333333333333
  }
}
```

## Command Line Arguments

- `--pattern PATTERN`: Single glob pattern to analyze
- `--patterns PATTERN [PATTERN ...]`: Multiple patterns to analyze simultaneously  
- `--output FILE`: Save detailed JSON results to file
- `--verbose`: Show additional processing information
- `--help`: Display help message with examples

## Supported Path Patterns

The tool recognizes these path components:
- `${ENV_DIR}`: Environment directory (e.g., TransactionEnv_transformed)
- `${model_config}`: Model configuration (e.g., claude37_think, claude37_no_think, ambersontest)
- `${error_type}`: Error type (e.g., feature_limitation, system_failure)
- `${seed}`: Seed identifier (e.g., s0, s1, s2)
- `${func}`: Function name (e.g., track_order, get_messages)

## Wildcard Patterns

Use `*` wildcards to match multiple values:
- `*/` matches any directory
- `*_adhoc+unclear_*` matches any error configuration
- `turn_level_tf_*` matches any model configuration

## Data Collection Logic

1. **Path Discovery**: Uses glob patterns to find matching directories
2. **Judge Results Filtering**: Only processes paths containing `judge_results/` subdirectories
3. **Batch Summary Collection**: Collects `batch_summary_run_*.json` files from:
   - `judge_results/run_*/batch_summary_run_*.json`
   - `judge_results/batch_summary_run_*.json`
4. **Score Extraction**: Extracts `average_score` from each batch summary
5. **Statistics Calculation**: Computes mean, standard deviation, and count per condition

## Error Handling

- **Path Parsing**: Warns about unparseable paths but continues processing
- **Missing Files**: Warns about unreadable JSON files but continues
- **Empty Results**: Reports when no batch summaries are found
- **JSON Errors**: Gracefully handles malformed JSON files

## Integration

The tool integrates seamlessly with existing LLM Judge workflows:
- Works with any `batch_summary_run_*.json` files generated by LLM Judge
- Compatible with multi-run experimental setups
- Supports various directory structures and naming conventions
- Can be automated in evaluation pipelines

## Performance

- Efficient glob-based path discovery
- Lazy loading of JSON files
- Memory-efficient processing of large result sets
- Fast statistics computation using Python's statistics module
