#!/bin/bash

# OpenAI API Batch Runner
# Uses vLLM server for OpenAI-compatible API testing

set -e  # Exit on any error

# =============================================================================
# Path Configuration - Portable across different user environments
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_BASE="${RESULTS_BASE:-$(dirname "$PROJECT_ROOT")/results}"

echo "🚀 Starting OpenAI API batch testing..."
echo "📋 Using unified_conversation_tester.sh with OpenAI API support"
echo "📂 Results will be saved to: ${RESULTS_BASE}"

# OpenAI API Configuration
BASE_URL="http://127.0.0.1:8000/v1"
API_KEY=""  # Not used for vLLM

# Variable arrays for easy expansion
model_configs=("qwen235b_inst") # "qwen235b_think" "qwen235b_think" "oss_120b" ("deepseekr1_qwen" "mistral_24b" "qwen3_32b" "oss_120b") 
seeds=("s0" "s1" "s2") # ("s0" "s1" "s2" "s3")
envs=("Combined") # Use "Combined_toy" to test # "Combined50" "Combined_deref50"
uncertainties=("none") # "partially_irrelevant" "informational_notice" ("informational_notice")

# Uncertainty-Prompt mapping based on requirements
declare -A UNCERTAINTY_PROMPTS
# ! with clean API version
UNCERTAINTY_PROMPTS[none]="none"

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
# Helper function to get prompts for a given uncertainty
get_prompts_for_uncertainty() {
    local unc=$1
    echo "${UNCERTAINTY_PROMPTS[$unc]}"
}

# Helper function to set environment-specific output directory
set_env_dir() {
    local env=$1
    case "$env" in
        "TransactionEnv_transformed")
            ENV_DIR="TransactionEnv_transformed"
            ;;
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
        "Complex_natural_new_transformed")
            ENV_DIR="ComplexScenarios_transformed"
            ;;
    esac
}


# Main processing loop
total_combinations=0
completed_combinations=0

# Calculate total combinations for progress tracking
for model_config in "${model_configs[@]}"; do
    for unc in "${uncertainties[@]}"; do
        prompts_array=($(get_prompts_for_uncertainty "$unc"))
        prompt_count=${#prompts_array[@]}
        seed_count=${#seeds[@]}
        env_count=${#envs[@]}
        model_total=$((prompt_count * seed_count * env_count))
        total_combinations=$((total_combinations + model_total))
    done
done

echo "📊 Total combinations to process: ${total_combinations}"
echo "🌐 OpenAI API Base URL: ${BASE_URL}"
echo ""


# Execute all combinations
for model_config in "${model_configs[@]}"; do
    echo "🔄 Processing model: ${model_config}"
    
    for unc in "${uncertainties[@]}"; do
        echo "  📋 Processing uncertainty: ${unc}"
        
        # Get prompts for this uncertainty
        prompts_array=($(get_prompts_for_uncertainty "$unc"))
        
        for prompt in "${prompts_array[@]}"; do
            for seed in "${seeds[@]}"; do
                for env in "${envs[@]}"; do
                    completed_combinations=$((completed_combinations + 1))
                    echo ""
                    echo "🎯 [${completed_combinations}/${total_combinations}] Testing: model=${model_config}, unc=${unc}, prompt=${prompt}, seed=${seed}, env=${env}"
                    
                                       
                    # Set model-specific configurations
                    set_model_config "$model_config"
                    
                    # Set environment-specific output directory
                    set_env_dir "$env"
                    
                    # Build output path (portable across different user environments)
                    OUTPUT_PATH="${RESULTS_BASE}/${ENV_DIR}_openai/${model_config}_${prompt}_${unc}_${seed}"
                    
                    # Set prompt path based on prompt type and model
                    PROMPT_PATH="extracted_api/centralized_prompt"
                    if [[ "$prompt" == "adhoc+unclear" ]]; then
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
                        --uncertainty-config \"uncertainty_configs/\${unc}.yaml\" \
                        --verbose"
                    
                    # Execute command
                    echo "    💻 Executing: ${model_config} with unc=${unc}, prompt=${prompt}"
                    if eval $CMD; then
                        echo "    ✅ Completed successfully"
                    else
                        echo "    ❌ Failed with exit code $?"
                        echo "    ⏭️  Continuing with next combination..."
                    fi
                done
            done
        done
        
        echo "  ✅ Completed uncertainty: ${unc}"
    done
    
    echo "✅ Completed model: ${model_config}"
    echo ""
done

echo ""
echo "🎉 OpenAI API batch testing completed!"
echo "📊 Processed ${completed_combinations} combinations"
echo "📂 Results saved in:"
echo "   - ${RESULTS_BASE}/"
echo ""
echo "🔍 Uncertainty types tested:"
echo "   - none (prompts: adhoc)"
echo ""
echo "⚙️  Configuration:"
echo "   - Model Type: OpenAI API"
echo "   - Base URL: ${BASE_URL}"
echo "   - Models: ${model_configs[*]}"
echo "   - Seeds: ${seeds[*]}"
echo "   - Environments: ${envs[*]}"
echo "   - Uncertainties: ${uncertainties[*]}"
echo ""
echo "🔧 To modify configuration:"
echo "   - Edit model_configs array for different thinking modes"
echo "   - Edit models array for different model names"
echo "   - Edit BASE_URL for different vLLM server endpoints"
echo "   - Edit uncertainties array for different uncertainty types"
echo "   - Edit seeds array for multiple random seeds"
