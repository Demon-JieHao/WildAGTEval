#!/bin/bash

# OpenAI API Teacher Forcing Batch Ablation Runner
# Uses vLLM server for OpenAI-compatible API testing with Teacher Forcing
# Based on run_unified_teacher_forcing_batch_ablation.sh structure

set -e  # Exit on any error

# =============================================================================
# Path Configuration - Portable across different user environments
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_BASE="${RESULTS_BASE:-$(dirname "$PROJECT_ROOT")/results}"

echo "🚀 Starting OpenAI API Teacher Forcing Ablation batch testing..."
echo "📋 Testing complexity ON/OFF ablation experiments with Turn-Level TF mode"
echo "📂 Results will be saved to: ${RESULTS_BASE}"

# OpenAI API Configuration
BASE_URL="http://127.0.0.1:8000/v1"
API_KEY=""  # Not used for vLLM

# Fixed parameter
mode="turn_level_tf"

# Variable arrays (based on modified run_openai_batch.sh)
model_configs=("oss_120b") # "oss_120b" "oss_120b_noThink" "oss_120b_noThink" "oss_120b" ("deepseekr1_qwen" "mistral_24b" "qwen3_32b" "oss_120b") 
seeds=("s0" "s1" "s2") # "s0" "s1" "s2" "s3" "s9" ("s0" "s1" "s2")
envs=("Combined") # "Combined_deref" "Combined50" "Combined_deref50"

# Ablation experiment configurations
# Format: "complexity_name:on_off:prompt:uncertainty:target_functions_config:output_suffix"
# ! with clean API version
declare -a ABLATION_CONFIGS=(
    "adhoc:OFF:none:none:target_functions_adhoc.yaml:_adhocTRG"
)

# Helper function to set model-specific configurations (OpenAI version)
set_model_config() {
    local model_config=$1
    MODEL_NAME=""
    THINKING_FLAG=""
    
    case "$model_config" in
        "qwen3_32b_think")
            MODEL_NAME="Qwen/Qwen3-32B"
            THINKING_FLAG="--enable-thinking"
            ;;
        "qwen3_32b")
            MODEL_NAME="Qwen/Qwen3-32B"
            THINKING_FLAG=""
            ;;
        "oss_120b")
            MODEL_NAME="/checkpoint/gpt-oss-120b"
            THINKING_FLAG=""
            ;;
        "oss_120b_noThink")
            MODEL_NAME="/checkpoint/gpt-oss-120b"
            THINKING_FLAG=""
            ;;
        "deepseekr1_qwen")
            MODEL_NAME="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
            THINKING_FLAG=""
            ;;
        "mistral_24b")
            MODEL_NAME="mistralai/Mistral-Small-3.2-24B-Instruct-2506"
            THINKING_FLAG=""
            ;;
    esac
}

# Helper function to set environment-specific output directory
set_env_dir() {
    local env=$1
    case "$env" in
        "Combined_transformed")
            ENV_DIR="Combined_transformed"
            ;;
        "Combined50_transformed")
            ENV_DIR="Combined50_transformed"
            ;;
        "Combined_deref50_transformed")
            ENV_DIR="Combined_deref50_transformed"
            ;;
        "Combined_deref_transformed")
            ENV_DIR="Combined_deref_transformed"
            ;;
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
echo "🌐 OpenAI API Base URL: ${BASE_URL}"
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
                OUTPUT_PATH="${RESULTS_BASE}/${ENV_DIR}_openai/${mode}_${model_config}_${PROMPT}_${UNCERTAINTY}_${seed}${OUTPUT_SUFFIX}"
                
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
                
                # Set prompt path based on prompt type and model
                PROMPT_PATH="extracted_api/centralized_prompt"
                if [[ "$PROMPT" == "adhoc+unclear" ]]; then
                    PROMPT_PATH="${PROMPT_PATH}_unclear"
                fi
                # Add model-specific suffixes
                PROMPT_PATH="${PROMPT_PATH}.md"
                
                # Build command with OpenAI API options
                CMD="./unified_conversation_tester_openai.sh \
                    --env ${env} \
                    --model-type openai \
                    --base-url \"${BASE_URL}\" \
                    --model \"${MODEL_NAME}\" \
                    --output \"${OUTPUT_PATH}\" \
                    --jobs 50 --max-steps 15 --timeout 130 \
                    ${THINKING_FLAG} \
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
echo "🎉 OpenAI API Teacher Forcing Ablation batch testing completed!"
echo "📊 Processed ${completed_combinations} combinations"
echo "📂 Results saved in:"
echo "   - ${RESULTS_BASE}/"
echo ""
echo "🔍 Ablation experiments conducted:"
echo "   - adhoc OFF: prompt=adhoc, unc=none, target=adhoc (suffix: _adhocTRG)"
echo ""
echo "⚙️  Configuration:"
echo "   - Model Type: OpenAI API"
echo "   - Base URL: ${BASE_URL}"
echo "   - Mode: ${mode} (fixed)"
echo "   - Models: ${model_configs[*]}"
echo "   - Seeds: ${seeds[*]}"
echo "   - Environments: ${envs[*]}"
echo "   - Total ablation configs: ${#ABLATION_CONFIGS[@]}"
echo ""
echo "🔧 To modify configuration:"
echo "   - Edit ABLATION_CONFIGS array for different ablation experiments"
echo "   - Edit model_configs array for different models"
echo "   - Edit BASE_URL for different vLLM server endpoints"
echo "   - Edit seeds array for multiple random seeds"
echo "   - Edit envs array for different environments"
