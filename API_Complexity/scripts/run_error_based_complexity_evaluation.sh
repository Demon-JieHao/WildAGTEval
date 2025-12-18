#!/bin/bash

# Error-based Complexity Evaluation Script
# Evaluates inference results using LLM Judge system
# Runs evaluation for error types (system_failure, feature_limitation) with specific functions

set -e  # Exit on any error

# =============================================================================
# Path Configuration - Portable across different user environments
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
RESULTS_BASE="${RESULTS_BASE:-$(dirname "$PROJECT_ROOT")/results}"

echo "🔍 Starting Error-based Complexity Evaluation..."
echo "📋 Evaluating system_failure and feature_limitation results with LLM Judge"
echo "📂 Evaluating results from: ${RESULTS_BASE}"

# Fixed parameters (must match inference script)
mode="turn_level_tf"
prompt="adhoc+unclear"

# Variable arrays (must match inference script)
# # ! run claudemodels
# model_configs=("claude40_think" "claude40_no_think" "claude37_no_think" "claude35" "oss_120b" "oss_120b_noThink") # ! "claude40_think": after run all
# # ! run vllm models
# model_configs=("deepseekr1_qwen" "mistral_24b" "qwen3_32b", "oss_120b" "qwen235b_think") # 
# # ! run openai
# model_configs=("gpt4omini") # add more if you want
seeds=("s0") #("s0" "s1" "s2")
envs=("Combined_transformed") # "Combined_transformed_openai" "Combined50_transformed" "Combined_transformed" 

# Judge seeds for evaluation runs
judge_seeds=(0) # (0 1 2)

# Function mappings per error type
declare -A ERROR_FUNCTIONS
ERROR_FUNCTIONS[feature_limitation]="get_messages get_notifications weather_forecast track_order stock_watchlist news_personalized get_user_inventory get_call_history"
ERROR_FUNCTIONS[system_failure]="make_call place_delivery_order send_message color_set get_user_inventory play track_delivery_order stock_price"

# ERROR_FUNCTIONS[feature_limitation]="get_user_inventory"
# ERROR_FUNCTIONS[system_failure]="get_user_inventory"


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
        "Combined50_transformed_openai")
            ENV_DIR="Combined50_transformed_openai"
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
for error_type in feature_limitation system_failure; do
    func_array=(${ERROR_FUNCTIONS[$error_type]})
    func_count=${#func_array[@]}
    model_count=${#model_configs[@]}
    seed_count=${#seeds[@]}
    env_count=${#envs[@]}
    judge_count=${#judge_seeds[@]}
    error_total=$((func_count * model_count * seed_count * env_count * judge_count))
    total_combinations=$((total_combinations + error_total))
done

echo "📊 Total evaluation combinations to process: ${total_combinations}"
echo ""

# ! Execute all combinations
# ! for error_type in feature_limitation system_failure; do
for error_type in feature_limitation system_failure; do # feature_limitation system_failure
    echo "🔄 Processing error type: ${error_type}"
    
    for func in ${ERROR_FUNCTIONS[$error_type]}; do
        echo "  📋 Processing function: ${func}"
        
        for model_config in "${model_configs[@]}"; do
            for seed in "${seeds[@]}"; do
                for env in "${envs[@]}"; do
                    # Set environment-specific output directory
                    set_env_dir "$env"
                    
                    # Build agent directory path (portable)
                    AGENT_DIR="${RESULTS_BASE}/${ENV_DIR}/${mode}_${model_config}_${prompt}_${error_type}_${seed}/${func}/"
                    
                    # Check if agent directory exists
                    if [[ ! -d "$AGENT_DIR" ]]; then
                        echo "    ⚠️  Warning: Agent directory not found: $AGENT_DIR"
                        echo "    ⏭️  Skipping this combination..."
                        # Still count as completed for progress tracking
                        judge_count=${#judge_seeds[@]}
                        completed_combinations=$((completed_combinations + judge_count))
                        continue
                    fi
                    
                    # Check if there are any JSON files to evaluate
                    json_files=$(find "$AGENT_DIR" -name "*_${func}.json" 2>/dev/null | wc -l)
                    if [[ $json_files -eq 0 ]]; then
                        echo "    ⚠️  Warning: No matching JSON files found in: $AGENT_DIR"
                        echo "    ⏭️  Skipping this combination..."
                        # Still count as completed for progress tracking
                        judge_count=${#judge_seeds[@]}
                        completed_combinations=$((completed_combinations + judge_count))
                        continue
                    fi
                    
                    echo "    📁 Found ${json_files} files to evaluate in: $AGENT_DIR"
                    
                    # Run evaluation for each judge seed
                    for judge_seed in "${judge_seeds[@]}"; do
                        completed_combinations=$((completed_combinations + 1))
                        echo ""
                        echo "    🎯 [${completed_combinations}/${total_combinations}] Evaluating: error=${error_type}, func=${func}, model=${model_config}, seed=${seed}, env=${env}, judge_seed=${judge_seed}"
                        
                        # Build output directory path
                        OUTPUT_DIR="${AGENT_DIR}judge_results/run_${judge_seed}"
                        
                        # Build evaluation command
                        CMD="python llm_judge_system/main.py --batch \
                            --agent_dir \"${AGENT_DIR}\" \
                            --output_dir \"${OUTPUT_DIR}\" \
                            --file_pattern \"*_${func}.json\" \
                            --max_workers 50 \
                            --run_id ${judge_seed}"
                        
                        # Execute evaluation
                        echo "        💻 Executing LLM Judge evaluation..."
                        if eval $CMD; then
                            echo "        ✅ Evaluation completed successfully"
                            
                            # Check results
                            if [[ -d "$OUTPUT_DIR" ]]; then
                                result_files=$(find "$OUTPUT_DIR" -name "*.json" 2>/dev/null | wc -l)
                                echo "        📊 Generated ${result_files} evaluation result files"
                            fi
                        else
                            echo "        ❌ Evaluation failed with exit code $?"
                            echo "        ⏭️  Continuing with next evaluation..."
                        fi
                    done
                done
            done
        done
        
        echo "  ✅ Completed function: ${func}"
    done
    
    echo "✅ Completed error type: ${error_type}"
    echo ""
done

echo ""
echo "🎉 Error-based Complexity Evaluation completed!"
echo "📊 Processed ${completed_combinations} evaluation combinations"
echo "📂 Results saved in:"
echo "   - ${RESULTS_BASE}/*/judge_results/"
echo ""
echo "🔍 Evaluation structure:"
echo "   - Error types: feature_limitation, system_failure"
echo "   - Judge seeds per combination: ${judge_seeds[*]}"
echo "   - Output format: {agent_dir}/judge_results/run_{judge_seed}/"
echo ""
echo "⚙️  Configuration:"
echo "   - Mode: ${mode} (fixed)"
echo "   - Prompt: ${prompt} (fixed)" 
echo "   - Models: ${model_configs[*]}"
echo "   - Seeds: ${seeds[*]}"
echo "   - Environments: ${envs[*]}"
echo "   - Judge Seeds: ${judge_seeds[*]}"
