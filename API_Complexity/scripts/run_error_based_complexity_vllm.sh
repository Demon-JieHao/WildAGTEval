#!/bin/bash

# OpenAI API Error-based Complexity Batch Runner
# Tests error types (system_failure, feature_limitation) with specific functions using OpenAI API
# Based on run_error_based_complexity_batch_son4_combined50.sh
# Fixed: mode=turn_level_tf, prompt=adhoc+unclear

set -e  # Exit on any error

# =============================================================================
# Path Configuration - Portable across different user environments
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_BASE="${RESULTS_BASE:-$(dirname "$PROJECT_ROOT")/results}"

echo "🚀 Starting OpenAI API Error-based Complexity batch testing..."
echo "📋 Testing system_failure and feature_limitation with specific functions"
echo "📂 Results will be saved to: ${RESULTS_BASE}"

# OpenAI API Configuration
BASE_URL="http://127.0.0.1:8000/v1"
API_KEY=""  # Not used for vLLM

# Fixed parameters
mode="turn_level_tf"
prompt="adhoc+unclear"

# Variable arrays (OpenAI version)
model_configs=("oss_120b") # "oss_120b" "qwen235b_inst" "qwen235b_think" "oss_120b" ("deepseekr1_qwen" "mistral_24b" "qwen3_32b" "oss_120b") 
seeds=("s0") #("s0" "s1" "s2") # "s3"
envs=("Combined_transformed") # "Combined50_transformed") # ("Combined_transformed_full") # ("TransactionEnv_transformed" "Complex_natural_new_transformed")

# Function mappings per error type
declare -A ERROR_FUNCTIONS
ERROR_FUNCTIONS[feature_limitation]="get_messages get_notifications weather_forecast track_order stock_watchlist news_personalized get_user_inventory get_call_history"
ERROR_FUNCTIONS[system_failure]="make_call place_delivery_order send_message color_set get_user_inventory play track_delivery_order stock_price"


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
        "qwen235b_think")
            MODEL_NAME="/checkpoint/Qwen3-235B-A22B-Thinking-2507"
            THINKING_FLAG=""
            ;;  
        "qwen235b_inst")
            MODEL_NAME="/checkpoint/Qwen3-235B-A22B-Instruct-2507"
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

# Helper function to set environment-specific output directory (same as run_openai_batch.sh)
set_env_dir() {
    local env=$1
    case "$env" in
        "Combined_transformed")
            ENV_DIR="Combined_transformed"
            ;;
        "Combined50_transformed")
            ENV_DIR="Combined50_transformed"
            ;;
    esac
}
# Main processing loop
total_combinations=0
completed_combinations=0

# Calculate total combinations for progress tracking
for error_type in feature_limitation system_failure; do
    func_array=(${ERROR_FUNCTIONS[$error_type]})
    func_count=${#func_array[@]}
    model_count=${#model_configs[@]}
    seed_count=${#seeds[@]}
    env_count=${#envs[@]}
    error_total=$((func_count * model_count * seed_count * env_count))
    total_combinations=$((total_combinations + error_total))
done

echo "📊 Total combinations to process: ${total_combinations}"
echo "🌐 OpenAI API Base URL: ${BASE_URL}"
echo ""


echo ""

# ! Execute all combinations
# for error_type in system_failure; do
for error_type in feature_limitation system_failure; do
    echo "🔄 Processing error type: ${error_type}"
    
    for func in ${ERROR_FUNCTIONS[$error_type]}; do
        echo "  📋 Processing function: ${func}"
        
        for model_config in "${model_configs[@]}"; do
            for seed in "${seeds[@]}"; do
                for env in "${envs[@]}"; do
                    completed_combinations=$((completed_combinations + 1))
                    echo ""
                    echo "🎯 [${completed_combinations}/${total_combinations}] Testing: error=${error_type}, func=${func}, model=${model_config}, seed=${seed}, env=${env}"
                    
                    # Set model-specific configurations
                    set_model_config "$model_config"
                    
                    # Set environment-specific output directory
                    set_env_dir "$env"
                    
                    # Build uncertainty and target-functions config paths
                    UNCERTAINTY_CONFIG="uncertainty_configs/${error_type}_${func}.yaml"
                    TARGET_FUNCTIONS_CONFIG="uncertainty_configs/target_functions_${func}.yaml"
                    
                    # Build output path with function subdirectory (portable)
                    OUTPUT_PATH="${RESULTS_BASE}/${ENV_DIR}_openai/${mode}_${model_config}_${prompt}_${error_type}_${seed}/${func}"
                    
                    # Check if config files exist
                    if [[ ! -f "$UNCERTAINTY_CONFIG" ]]; then
                        echo "⚠️  Warning: Uncertainty config not found: $UNCERTAINTY_CONFIG"
                        echo "   Skipping this combination..."
                        continue
                    fi
                    
                    if [[ ! -f "$TARGET_FUNCTIONS_CONFIG" ]]; then
                        echo "⚠️  Warning: Target functions config not found: $TARGET_FUNCTIONS_CONFIG"
                        echo "   Skipping this combination..."
                        continue
                    fi
                    
                    # Set prompt path based on model
                    PROMPT_PATH="extracted_api/centralized_prompt_unclear"
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
                        --turn-level-tf --target-functions-config \"${TARGET_FUNCTIONS_CONFIG}\" \
                        --verbose"
                    
                    # Execute command
                    echo "    💻 Executing: $(basename $0) with error=${error_type}, func=${func}"
                    if eval $CMD; then
                        echo "    ✅ Completed successfully"
                    else
                        echo "    ❌ Failed with exit code $?"
                        echo "    ⏭️  Continuing with next combination..."
                    fi
                done
            done
        done
        
        echo "  ✅ Completed function: ${func}"
    done
    
    echo "✅ Completed error type: ${error_type}"
    echo ""
done

echo ""
echo "🎉 OpenAI API Error-based Complexity batch testing completed!"
echo "📊 Processed ${completed_combinations} combinations"
echo "📂 Results saved in:"
echo "   - ${RESULTS_BASE}/"
echo ""
echo "🔍 Error types tested:"
echo "   - feature_limitation (8 functions: get_messages, get_notifications, weather_forecast, track_order, stock_watchlist, news_personalized, get_user_inventory, get_call_history)"
echo "   - system_failure (8 functions: make_call, place_delivery_order, send_message, color_set, get_user_inventory, play, track_delivery_order, stock_price)"
echo ""
echo "⚙️  Configuration:"
echo "   - Model Type: OpenAI API"
echo "   - Base URL: ${BASE_URL}"
echo "   - Mode: ${mode} (fixed)"
echo "   - Prompt: ${prompt} (fixed)"
echo "   - Models: ${model_configs[*]}"
echo "   - Seeds: ${seeds[*]}"
echo "   - Environments: ${envs[*]}"
echo ""
echo "🔧 To modify configuration:"
echo "   - Edit ERROR_FUNCTIONS array for different function mappings"
echo "   - Edit model_configs array for different models"
echo "   - Edit BASE_URL for different vLLM server endpoints"
echo "   - Edit seeds array for multiple random seeds"
echo "   - Edit envs array for different environments"
