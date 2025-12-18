#!/bin/bash

# Unified Teacher Forcing Batch Ablation Analysis Script
# Unified analysis for Teacher Forcing ablation experiment results
# Based on run_TransactionEnv_transformed_analysis_refactored.sh structure

set -e  # Exit on any error

# =============================================================================
# Path Configuration - Portable across different user environments
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_BASE="${RESULTS_BASE:-$(dirname "$PROJECT_ROOT")/results}"

echo "🚀 Starting Teacher Forcing Ablation unified analysis..."
echo "📋 Using unified_analyzer.py for ablation experiment analysis"
echo "📂 Analyzing results from: ${RESULTS_BASE}"

# Check if unified_analyzer.py exists
if [[ ! -f "unified_analyzer.py" ]]; then
    echo "❌ Error: unified_analyzer.py not found in current directory"
    exit 1
fi

# Fixed parameter (must match ablation batch script)
mode="turn_level_tf"

# Variable arrays (must match ablation batch script)
model_configs=("qwen235b_inst" "qwen235b_think" "claude37_think" "claude40_think" "claude40_no_think" "claude37_no_think" "claude35" "deepseekr1_qwen" "mistral_24b" "qwen3_32b" "oss_120b" "oss_120b_noThink")
seeds=("s0" "s1" "s2" "s3" "s4")
envs=("Combined_transformed" "Combined" "Combined_transformed_openai" "Combined_openai" "Combined50_transformed" "Combined50" "Combined50_transformed_openai" "Combined50_openai")
# ("Combined_deref50_transformed" "Combined_deref50" "Combined_deref50_transformed_openai" "Combined_deref50_openai")

# Ablation experiment configurations (must match ablation batch script)
# Format: "complexity_name:on_off:prompt:uncertainty:target_functions_config:output_suffix"
declare -a ABLATION_CONFIGS=(
    "unclear:OFF:adhoc:adhoc:target_functions_unclear.yaml:_unclearTRG"
    "unclear:ON:adhoc+unclear:adhoc:target_functions_unclear.yaml:_unclearTRG"
    "info_notice:OFF:adhoc+unclear:adhoc:target_functions_informational_notice.yaml:_infonoticeTRG"
    "info_notice:ON:adhoc+unclear:informational_notice:target_functions_informational_notice.yaml:_infonoticeTRG"
    "irrelevant_data:OFF:adhoc+unclear:adhoc:target_functions_partially_irrelevant.yaml:_irrelevantTRG"
    "irrelevant_data:ON:adhoc+unclear:partially_irrelevant:target_functions_partially_irrelevant.yaml:_irrelevantTRG"
    "adhoc:ON:adhoc:adhoc:target_functions_adhoc.yaml:_adhocTRG"
)


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
        "Combined_transformed_openai")
            ENV_DIR="Combined_transformed_openai"
            ;;
        "Combined50")
            ENV_DIR="Combined50"
            ;;
        "Combined_openai")
            ENV_DIR="Combined_openai"
            ;;
        "Combined")
            ENV_DIR="Combined"
            ;;
        "Combined_deref50_transformed")
            ENV_DIR="Combined_deref50_transformed"
            ;;
        "Combined_deref50")
            ENV_DIR="Combined_deref50"
            ;;
        "Combined50_transformed_openai")
            ENV_DIR="Combined50_transformed_openai"
            ;;
        "Combined50_openai")
            ENV_DIR="Combined50_openai"
            ;;
        "Combined_deref50_transformed_openai")
            ENV_DIR="Combined_deref50_transformed_openai"
            ;;
        "Combined_deref50_openai")
            ENV_DIR="Combined_deref50_openai"
            ;;
        "Complex_natural_new_transformed")
            ENV_DIR="ComplexScenarios_transformed"
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

# Calculate total combinations for progress tracking (×2 for normal + ad_hoc)
config_count=${#ABLATION_CONFIGS[@]}
model_count=${#model_configs[@]}
seed_count=${#seeds[@]}
env_count=${#envs[@]}
total_combinations=$((config_count * model_count * seed_count * env_count * 2)) # ×2 for normal + ad_hoc

echo "📊 Total analysis combinations to process: ${total_combinations}"
echo ""

# Execute all combinations
for config in "${ABLATION_CONFIGS[@]}"; do
    parse_ablation_config "$config"
    
    echo "🔄 Processing ablation: ${COMPLEXITY_NAME} ${ON_OFF}"
    
    for model_config in "${model_configs[@]}"; do
        for seed in "${seeds[@]}"; do
            for env in "${envs[@]}"; do
                # Set environment-specific output directory
                set_env_dir "$env"
                
                # Build result directory path matching ablation batch script output (portable)
                RESULT_DIR="${RESULTS_BASE}/${ENV_DIR}/${mode}_${model_config}_${PROMPT}_${UNCERTAINTY}_${seed}${OUTPUT_SUFFIX}"
                
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
                echo "    🎯 [${completed_combinations}/${total_combinations}] Ad-hoc Analysis: complexity=${COMPLEXITY_NAME}_${ON_OFF}, model=${model_config}, seed=${seed}, env=${env}"
                
                ANALYSIS_DIR="${RESULT_DIR}_AdhocEval_analysis"
                
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
    
    echo "✅ Completed ablation: ${COMPLEXITY_NAME} ${ON_OFF}"
    echo ""
done

echo ""
echo "🎉 Teacher Forcing Ablation unified analysis completed!"
echo "📊 Processed ${completed_combinations} analysis combinations"
echo "📂 Analysis results saved in:"
echo "   - ${RESULTS_BASE}/*_analysis/ (normal)"
echo "   - ${RESULTS_BASE}/*_AdhocEval_analysis/ (ad-hoc)"
echo ""
echo "🔍 Analysis types performed:"
echo "   - Normal analysis: --batch"
echo "   - Ad-hoc analysis: --batch --ad_hoc"
echo ""
echo "⚙️  Configuration:"
echo "   - Mode: ${mode} (fixed)"
echo "   - Models: ${model_configs[*]}"
echo "   - Seeds: ${seeds[*]}"
echo "   - Environments: ${envs[*]}"
echo "   - Total ablation configs: ${#ABLATION_CONFIGS[@]}"
echo ""
echo "🔍 Ablation experiments analyzed:"
echo "   - unclear OFF: prompt=adhoc, unc=none, target=unclear (suffix: _uncOFF)"
echo "   - unclear ON: prompt=adhoc+unclear, unc=none, target=unclear"
echo "   - info_notice OFF: prompt=adhoc+unclear, unc=none, target=informational_notice (suffix: _uncOFF)"
echo "   - info_notice ON: prompt=adhoc+unclear, unc=informational_notice, target=informational_notice"
echo "   - irrelevant_data OFF: prompt=adhoc+unclear, unc=none, target=partially_irrelevant (suffix: _uncOFF)"
echo "   - irrelevant_data ON: prompt=adhoc+unclear, unc=partially_irrelevant, target=partially_irrelevant"
echo "   - adhoc ON: prompt=adhoc, unc=none, target=adhoc"
