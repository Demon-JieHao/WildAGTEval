#!/bin/bash

# Refactored TransactionEnv_transformed Analysis Script
# Unified analysis for TransactionEnv_transformed refactored batch results
# Clean structure matching run_TransactionEnv_transformed_batch_refactored.sh

set -e  # Exit on any error

# =============================================================================
# Path Configuration - Portable across different user environments
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_BASE="${RESULTS_BASE:-$(dirname "$PROJECT_ROOT")/results}"

echo "🚀 Starting TransactionEnv_transformed unified analysis (Refactored)..."
echo "📋 Using unified_analyzer.py with improved structure"
echo "📂 Analyzing results from: ${RESULTS_BASE}"

# Check if unified_analyzer.py exists
if [[ ! -f "unified_analyzer.py" ]]; then
    echo "❌ Error: unified_analyzer.py not found in current directory"
    exit 1
fi

# Variable arrays (must match refactored batch script)
model_configs=("qwen235b_inst" "qwen235b_think" "claude37_think" "claude40_think" "claude40_no_think" "claude37_no_think" "claude35" "deepseekr1_qwen" "mistral_24b" "qwen3_32b" "oss_120b" "oss_120b_noThink")
seeds=("s0" "s1" "s2" "s3" "s4")   
envs=("Combined_transformed" "Combined" "Combined_transformed_openai" "Combined_openai" "Combined50_transformed" "Combined50" "Combined50_transformed_openai" "Combined50_openai") #  "Combined_transformed" 
uncertainties=("adhoc" "informational_notice" "partially_irrelevant")

# Uncertainty-Prompt mapping (must match refactored batch script)
declare -A UNCERTAINTY_PROMPTS
UNCERTAINTY_PROMPTS[adhoc]="adhoc+unclear adhoc"
UNCERTAINTY_PROMPTS[informational_notice]="adhoc+unclear"
UNCERTAINTY_PROMPTS[partially_irrelevant]="adhoc+unclear"

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
        "Combined50")
            ENV_DIR="Combined50"
            ;;
        "Combined")
            ENV_DIR="Combined"
            ;;
        "Combined50_transformed_openai")
            ENV_DIR="Combined50_transformed_openai"
            ;;
        "Combined50_openai")
            ENV_DIR="Combined50_openai"
            ;;
        "Combined_transformed_openai")
            ENV_DIR="Combined_transformed_openai"
            ;;
        "Combined_openai")
            ENV_DIR="Combined_openai"
            ;;
        "Complex_natural_new_transformed")
            ENV_DIR="ComplexScenarios_transformed"
            ;;
    esac
}

# Main processing loop
total_combinations=0
completed_combinations=0

# Calculate total combinations for progress tracking (×2 for normal + ad_hoc)
for model_config in "${model_configs[@]}"; do
    for unc in "${uncertainties[@]}"; do
        prompts_array=($(get_prompts_for_uncertainty "$unc"))
        prompt_count=${#prompts_array[@]}
        seed_count=${#seeds[@]}
        env_count=${#envs[@]}
        model_total=$((prompt_count * seed_count * env_count * 2)) # ×2 for normal + ad_hoc
        total_combinations=$((total_combinations + model_total))
    done
done

echo "📊 Total analysis combinations to process: ${total_combinations}"
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
                    # Set environment-specific output directory
                    set_env_dir "$env"
                    
                    # Build result directory path (portable across different user environments)
                    RESULT_DIR="${RESULTS_BASE}/${ENV_DIR}/${model_config}_${prompt}_${unc}_${seed}"
                    
                    # Check if result directory exists
                    if [[ ! -d "$RESULT_DIR" ]]; then
                        echo "    ⚠️  Warning: Result directory not found: $RESULT_DIR"
                        echo "    ⏭️  Skipping this combination..."
                        # Still count as completed for progress tracking (×2)
                        completed_combinations=$((completed_combinations + 2))
                        continue
                    fi
                    
                    # Ad-hoc Analysis
                    completed_combinations=$((completed_combinations + 1))
                    echo ""
                    echo "    🎯 [${completed_combinations}/${total_combinations}] Ad-hoc Analysis: model=${model_config}, unc=${unc}, prompt=${prompt}, seed=${seed}, env=${env}"
                    
                    ANALYSIS_DIR="${RESULTS_BASE}/${ENV_DIR}/${model_config}_AdhocEval_${prompt}_${unc}_${seed}_analysis"
                    
                    echo "        💻 Executing unified_analyzer.py (ad-hoc)..."
                    if python unified_analyzer.py "$RESULT_DIR" \
                        --batch \
                        --ad_hoc \
                        -o "$ANALYSIS_DIR" \
                        --config configs; then
                        echo "        ✅ Ad-hoc analysis completed successfully"
                    else
                        echo "        ❌ Ad-hoc analysis failed with exit code $?"
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
echo "🎉 TransactionEnv_transformed unified analysis completed!"
echo "📊 Processed ${completed_combinations} analysis combinations"
echo "📂 Analysis results saved in:"
echo "   - ${RESULTS_BASE}/*_analysis/ (normal)"
echo "   - ${RESULTS_BASE}/*_AdhocEval_*_analysis/ (ad-hoc)"
echo ""
echo "🔍 Analysis types performed:"
echo "   - Normal analysis: --batch"
echo "   - Ad-hoc analysis: --batch --ad_hoc"
echo ""
echo "⚙️  Configuration:"
echo "   - Models: ${model_configs[*]}"
echo "   - Seeds: ${seeds[*]}"
echo "   - Environments: ${envs[*]}"
echo "   - Uncertainties: ${uncertainties[*]}"
echo ""
echo "📋 Uncertainty-Prompt mapping:"
echo "   - none: adhoc+unclear, adhoc"
echo "   - informational_notice: adhoc+unclear"
echo "   - partially_irrelevant: adhoc+unclear"
