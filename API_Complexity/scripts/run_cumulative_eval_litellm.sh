#!/bin/bash

# LiteLLM Cumulative Evaluation Runner
# Minimal modification from run_cumulative_eval.sh
# Uses GPT (gpt-4o-mini) via LiteLLM instead of Claude Bedrock

# Refactored TransactionEnv_transformed Batch Runner
# Clean structure with arrays and helper functions for easy expansion

set -e  # Exit on any error

# =============================================================================
# Path Configuration - Portable across different user environments
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_BASE="${RESULTS_BASE:-$(dirname "$PROJECT_ROOT")/results}"

echo "🚀 Starting TransactionEnv_transformed batch testing (Refactored)..."
echo "📋 Using unified_conversation_tester.sh with improved structure"
echo "📂 Results will be saved to: ${RESULTS_BASE}"

# Variable arrays for easy expansion
model_configs=("gpt4omini")
seeds=("s0") #  "s1" "s2" "s3" "s4")
envs=("Combined_transformed") # "Combined50_transformed" "Combined_deref_transformed" "Combined_deref50_transformed") # ("TransactionEnv_transformed") # ("TransactionEnv_transformed" "Complex_natural_new_transformed")
uncertainties=("adhoc" "partially_irrelevant" "informational_notice") # 

# Uncertainty-Prompt mapping based on requirements
declare -A UNCERTAINTY_PROMPTS
UNCERTAINTY_PROMPTS[adhoc]="adhoc+unclear adhoc"
UNCERTAINTY_PROMPTS[informational_notice]="adhoc+unclear"
UNCERTAINTY_PROMPTS[partially_irrelevant]="adhoc+unclear"

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

# Helper function to get prompts for a given uncertainty
get_prompts_for_uncertainty() {
    local unc=$1
    echo "${UNCERTAINTY_PROMPTS[$unc]}"
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
                    OUTPUT_PATH="${RESULTS_BASE}/${ENV_DIR}/${model_config}_${prompt}_${unc}_${seed}"
                    
                    # Build command: "--use-litellm" is included
                    CMD="./unified_conversation_tester.sh \
                        --env ${env} \
                        --output \"${OUTPUT_PATH}\" \
                        --jobs 50 --max-steps 15 --timeout 130 \
                        --model-id \"${MODEL_ID}\" \
                        ${THINKING_FLAG} \
                        --use-litellm \
                        --prompt-path \"extracted_api/centralized_prompt\$([ \"\$prompt\" = \"adhoc+unclear\" ] && echo \"_unclear\").md\" \
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
echo "🎉 TransactionEnv_transformed batch testing completed!"
echo "📊 Processed ${completed_combinations} combinations"
echo "📂 Results saved in:"
echo "   - ${RESULTS_BASE}/"
echo ""
echo "🔍 Uncertainty types tested:"
echo "   - none (prompts: adhoc+unclear, adhoc)"
echo "   - informational_notice (prompts: adhoc+unclear)"
echo "   - partially_irrelevant (prompts: adhoc+unclear)"
echo ""
echo "⚙️  Configuration:"
echo "   - Models: ${model_configs[*]}"
echo "   - Seeds: ${seeds[*]}"
echo "   - Environments: ${envs[*]}"
echo "   - Uncertainties: ${uncertainties[*]}"
