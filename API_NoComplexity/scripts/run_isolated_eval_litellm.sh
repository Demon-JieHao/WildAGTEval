#!/bin/bash

# Unified Teacher Forcing Batch Ablation Runner
# Tests complexity ON/OFF ablation experiments with turn_level_tf mode
# Based on run_error_based_complexity_batch.sh structure

set -e  # Exit on any error

# =============================================================================
# Path Configuration - Portable across different user environments
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_BASE="${RESULTS_BASE:-$(dirname "$PROJECT_ROOT")/results}"

echo "🚀 Starting Teacher Forcing Ablation batch testing..."
echo "📋 Testing complexity ON/OFF ablation experiments"
echo "📂 Results will be saved to: ${RESULTS_BASE}"

# Fixed parameter
mode="turn_level_tf"

# Variable arrays
model_configs=("gpt4omini")  # 
seeds=("s0") # "s1" "s2" "s3" "s4")
envs=("Combined") # Use "Combined_toy" to test # "Combined_deref") # "Combined50" "Combined_deref50"

# Ablation experiment configurations
# Format: "complexity_name:on_off:prompt:uncertainty:target_functions_config:output_suffix"
# ! with clean API version
declare -a ABLATION_CONFIGS=(
    "adhoc:OFF:none:none:target_functions_adhoc.yaml:_adhocTRG"
)

# Helper function to set model-specific configurations (LiteLLM version)
set_model_config() {
    local model_config=$1
    MODEL_ID=""
    THINKING_FLAG=""

    case "$model_config" in
        "gpt4omini")
            MODEL_ID="gpt-4o-mini"
            THINKING_FLAG=""
            ;;
    esac
}

# Ensure OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
  echo "❌ ERROR: OPENAI_API_KEY is not set."
  echo "Please run: export OPENAI_API_KEY='sk-xxxxxx'"
  exit 1
fi


# Helper function to set environment-specific output directory
set_env_dir() {
    local env=$1
    case "$env" in
        "Combined50")
            ENV_DIR="Combined50"
            ;;
        "Combined_deref50")
            ENV_DIR="Combined_deref50"
            ;;
        "Combined")
            ENV_DIR="Combined"
            ;;
        "Combined_deref")
            ENV_DIR="Combined_deref"
            ;;
    esac
}


# Helper function to parse ablation config
parse_ablation_config() {
    local config=$1
    IFS=':' read -ra PARTS <<< "$config"
    COMPLEXITY_NAME="${PARTS[0]}"
    ON_OFF="${PARTS[1]}"
    PROMPT="${PARTS[2]}"
    UNCERTAINTY="${PARTS[3]}"
    TARGET_FUNCTIONS_CONFIG="${PARTS[4]}"
    OUTPUT_SUFFIX="${PARTS[5]}"
}

# Main processing loop
total_combinations=0
completed_combinations=0

# Calculate total combinations for progress tracking
config_count=${#ABLATION_CONFIGS[@]}
model_count=${#model_configs[@]}
seed_count=${#seeds[@]}
env_count=${#envs[@]}
total_combinations=$((config_count * model_count * seed_count * env_count))

echo "📊 Total combinations to process: ${total_combinations}"
echo ""

# Execute all combinations
for config in "${ABLATION_CONFIGS[@]}"; do
    parse_ablation_config "$config"
    
    echo "🔄 Processing ablation: ${COMPLEXITY_NAME} ${ON_OFF}"
    
    for model_config in "${model_configs[@]}"; do
        for seed in "${seeds[@]}"; do
            for env in "${envs[@]}"; do
                completed_combinations=$((completed_combinations + 1))
                echo ""
                echo "🎯 [${completed_combinations}/${total_combinations}] Testing: complexity=${COMPLEXITY_NAME}_${ON_OFF}, model=${model_config}, seed=${seed}, env=${env}"
                
                # Set model-specific configurations
                set_model_config "$model_config"
                
                # Set environment-specific output directory
                set_env_dir "$env"
                
                # Build config file paths
                UNCERTAINTY_CONFIG="uncertainty_configs/${UNCERTAINTY}.yaml"
                TARGET_FUNCTIONS_PATH="uncertainty_configs/${TARGET_FUNCTIONS_CONFIG}"
                
                # Build output path with complexity and suffix (portable)
                OUTPUT_PATH="${RESULTS_BASE}/${ENV_DIR}/${mode}_${model_config}_${PROMPT}_${UNCERTAINTY}_${seed}${OUTPUT_SUFFIX}"
                
                # Check if config files exist
                if [[ ! -f "$UNCERTAINTY_CONFIG" ]]; then
                    echo "⚠️  Warning: Uncertainty config not found: $UNCERTAINTY_CONFIG"
                    echo "   Skipping this combination..."
                    continue
                fi
                
                if [[ ! -f "$TARGET_FUNCTIONS_PATH" ]]; then
                    echo "⚠️  Warning: Target functions config not found: $TARGET_FUNCTIONS_PATH"
                    echo "   Skipping this combination..."
                    continue
                fi
                
                # Set prompt path based on prompt type
                PROMPT_PATH="extracted_api/centralized_prompt"
                if [[ "$PROMPT" == "adhoc+unclear" ]]; then
                    PROMPT_PATH="${PROMPT_PATH}_unclear"
                fi
                PROMPT_PATH="${PROMPT_PATH}.md"
                
                # Build command
                CMD="./unified_conversation_tester.sh \
                    --env ${env} \
                    --output \"${OUTPUT_PATH}\" \
                    --jobs 60 --max-steps 15 --timeout 130 \
                    --model-id \"${MODEL_ID}\" \
                    ${THINKING_FLAG} \
                    --use-litellm \
                    --prompt-path \"${PROMPT_PATH}\" \
                    --uncertainty-config \"${UNCERTAINTY_CONFIG}\" \
                    --turn-level-tf --target-functions-config \"${TARGET_FUNCTIONS_PATH}\" \
                    --verbose"
                
                # Execute command
                echo "    💻 Executing: ${COMPLEXITY_NAME}_${ON_OFF} with prompt=${PROMPT}, unc=${UNCERTAINTY}"
                if eval $CMD; then
                    echo "    ✅ Completed successfully"
                else
                    echo "    ❌ Failed with exit code $?"
                    echo "    ⏭️  Continuing with next combination..."
                fi
            done
        done
    done
    
    echo "✅ Completed ablation: ${COMPLEXITY_NAME} ${ON_OFF}"
    echo ""
done

echo ""
echo "🎉 Teacher Forcing Ablation batch testing completed!"
echo "📊 Processed ${completed_combinations} combinations"
echo "📂 Results saved in:"
echo "   - ${RESULTS_BASE}/"
echo ""
echo "🔍 Ablation experiments conducted:"
echo "   - unclear OFF: prompt=adhoc, unc=none, target=unclear (suffix: _uncOFF)"
echo "   - unclear ON: prompt=adhoc+unclear, unc=none, target=unclear"
echo "   - info_notice OFF: prompt=adhoc+unclear, unc=none, target=informational_notice (suffix: _uncOFF)"
echo "   - info_notice ON: prompt=adhoc+unclear, unc=informational_notice, target=informational_notice"
echo "   - irrelevant_data OFF: prompt=adhoc+unclear, unc=none, target=partially_irrelevant (suffix: _uncOFF)"
echo "   - irrelevant_data ON: prompt=adhoc+unclear, unc=partially_irrelevant, target=partially_irrelevant"
echo "   - adhoc ON: prompt=adhoc, unc=none, target=adhoc"
echo ""
echo "⚙️  Configuration:"
echo "   - Mode: ${mode} (fixed)"
echo "   - Models: ${model_configs[*]}"
echo "   - Seeds: ${seeds[*]}"
echo "   - Environments: ${envs[*]}"
echo "   - Total ablation configs: ${#ABLATION_CONFIGS[@]}"
