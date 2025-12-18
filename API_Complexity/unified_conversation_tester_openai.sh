#!/bin/bash

# Unified Conversation Testing Script
# Tests JSONL files across all conversation environments with step-by-step LLM evaluation
# Replaces individual environment-specific test scripts

set -e  # Exit on any error

# Basic Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVALUATOR_SCRIPT="$SCRIPT_DIR/step_by_step_llm_evaluator_teacher_forcing_openai.py"
CONVERSATIONS_DIR="$SCRIPT_DIR/atomic_conversation_units/success_conversations"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Default configuration for all environments (jobs:max-steps:timeout)
DEFAULT_JOBS=20
DEFAULT_MAX_STEPS=15
DEFAULT_TIMEOUT=130.0

# Enhanced options
MODEL_ID=""
ENABLE_THINKING=false
PROMPT_PATH=""
UNCERTAINTY_CONFIG=""

# Teacher Forcing options
TEACHER_FORCING=false
TURN_LEVEL_TF=false
TARGET_FUNCTIONS_CONFIG=""

# OpenAI API options
MODEL_TYPE="claude"
BASE_URL=""
API_KEY=""
MODEL=""

# Function to print usage
usage() {
    cat << EOF
Usage: $0 --env ENVIRONMENT [OPTIONS]

Test JSONL files in conversation environments with step-by-step LLM evaluation

ENVIRONMENT OPTIONS:
    --env ENV_NAME         Test specific environment (e.g., TransactionEnv)
    --env "ENV1,ENV2"      Test multiple environments (comma-separated)
    --env all              Test all available environments
    --env list             List all available environments

OPTIONS:
    -j, --jobs NUM         Number of parallel jobs (default: $DEFAULT_JOBS)
    -o, --output DIR       Output directory for results (default: {env_name}_test_results)
    --max-steps NUM        Maximum steps per query (default: $DEFAULT_MAX_STEPS)
    --timeout NUM          Timeout per step in seconds (default: $DEFAULT_TIMEOUT)
    -v, --verbose          Show verbose output
    -h, --help             Show this help message

    # Enhanced evaluation options
    --model-id MODEL_ID    Model ID to use (e.g., claude-3-sonnet, claude-3-haiku)
    --enable-thinking      Enable thinking mode for enhanced reasoning
    --prompt-path PATH     Path to custom centralized prompt file
    --uncertainty-config PATH  Path to uncertainty configuration YAML file

    # Teacher Forcing evaluation options
    --teacher-forcing      Enable Teacher Forcing evaluation mode
    --turn-level-tf        Enable Turn-Level Teacher Forcing evaluation
    --target-functions-config PATH  Path to target functions YAML config (required for Turn-Level TF)

    # OpenAI API options
    --model-type TYPE      Model type to use (claude|mistral|openai, default: claude)
    --model MODEL          Model name (required for openai, e.g., "Qwen/Qwen3-32B")
    --base-url URL         Base URL for OpenAI-compatible APIs (required for openai)
    --api-key KEY          API key for OpenAI-compatible APIs (optional)

EXAMPLES:
    # Test TransactionEnv with default settings
    $0 --env TransactionEnv

    # Test ComplexScenarios with custom parameters
    $0 --env ComplexScenarios --jobs 20 --timeout 200

    # Test multiple environments
    $0 --env "TransactionEnv,ComplexScenarios"

    # Test all available environments
    $0 --env all

    # List available environments
    $0 --env list

    # Enhanced evaluation with thinking mode
    $0 --env TransactionEnv \\
       --model-id "claude37" \\
       --enable-thinking \\
       --jobs 50 --max-steps 15 --timeout 130

    # With uncertainty configuration
    $0 --env ComplexScenarios \\
       --uncertainty-config "uncertainty_configs/system_failure_only.yaml" \\
       --prompt-path "extracted_api/centralized_prompt_unclear.md"

    # Teacher Forcing evaluation examples
    # Basic Teacher Forcing mode
    $0 --env TransactionEnv --teacher-forcing \\
       -o teacher_forcing_results --verbose

    # Turn-Level Teacher Forcing with uncertainty
    $0 --env TransactionEnv \\
       --turn-level-tf \\
       --target-functions-config "uncertainty_configs/target_functions.yaml" \\
       --uncertainty-config "uncertainty_configs/system_failure_only.yaml" \\
       -o turn_level_tf_results --verbose

    # Complete advanced setup (as you were using)
    $0 --env TransactionEnv \\
       --output "test_with_uncertainties/TransactionEnv/claude37_think_adhoc_system_failure_seed1" \\
       --jobs 50 --max-steps 15 --timeout 130 \\
       --model-id "claude37" \\
       --enable-thinking \\
       --prompt-path "extracted_api/centralized_prompt_unclear.md" \\
       --uncertainty-config "uncertainty_configs/system_failure_only.yaml" \\
       --turn-level-tf \\
       --target-functions-config "uncertainty_configs/target_functions.yaml"

    # OpenAI API examples
    # Basic OpenAI API usage
    $0 --env TransactionEnv \\
       --model-type openai \\
       --base-url "http://127.0.0.1:8000/v1" \\
       --model "Qwen/Qwen3-32B" \\
       --jobs 20 --max-steps 15 --timeout 130

    # OpenAI API with thinking mode and uncertainty
    $0 --env ComplexScenarios \\
       --model-type openai \\
       --base-url "http://127.0.0.1:8000/v1" \\
       --model "Qwen/Qwen3-32B" \\
       --enable-thinking \\
       --uncertainty-config "uncertainty_configs/system_failure_only.yaml" \\
       --prompt-path "extracted_api/centralized_prompt_unclear.md" \\
       --jobs 20 --max-steps 15 --timeout 130

    # OpenAI API with Teacher Forcing
    $0 --env TransactionEnv \\
       --model-type openai \\
       --base-url "http://127.0.0.1:8000/v1" \\
       --model "Qwen/Qwen3-32B" \\
       --teacher-forcing \\
       --enable-thinking \\
       --jobs 20 --max-steps 15 --timeout 130

EOF
}

# Function to discover available environments
discover_environments() {
    if [[ ! -d "$CONVERSATIONS_DIR" ]]; then
        print_error "Conversations directory not found: $CONVERSATIONS_DIR"
        return 1
    fi
    
    find "$CONVERSATIONS_DIR" -maxdepth 1 -type d ! -name "success_conversations" -exec basename {} \; | sort
}


# Function to test a single file
test_single_file() {
    local jsonl_file="$1"
    local filename=$(basename "$jsonl_file")
    local filename_no_ext="${filename%.jsonl}"
    local output_file="$OUTPUT_DIR/${filename_no_ext}_test_result.json"
    local log_file="$OUTPUT_DIR/${filename_no_ext}_test.log"
    
    echo "  🔄 Testing: $filename"
    
    # Run step-by-step evaluation
    local eval_args=("$jsonl_file" "--output" "$output_file" "--max-steps" "$MAX_STEPS" "--timeout" "$TIMEOUT")
    
    # Add enhanced options if provided
    if [[ -n "$MODEL_ID" ]]; then
        eval_args+=("--model-id" "$MODEL_ID")
    fi
    
    if [[ "$ENABLE_THINKING" == true ]]; then
        eval_args+=("--enable-thinking")
    fi
    
    if [[ -n "$PROMPT_PATH" ]]; then
        eval_args+=("--prompt-path" "$PROMPT_PATH")
    fi
    
    if [[ -n "$UNCERTAINTY_CONFIG" ]]; then
        eval_args+=("--uncertainty-config" "$UNCERTAINTY_CONFIG")
    fi
    
    # Add Teacher Forcing options if provided
    if [[ "$TEACHER_FORCING" == true ]]; then
        eval_args+=("--teacher-forcing")
    fi
    
    if [[ "$TURN_LEVEL_TF" == true ]]; then
        eval_args+=("--turn-level-tf")
    fi
    
    if [[ -n "$TARGET_FUNCTIONS_CONFIG" ]]; then
        eval_args+=("--target-functions-config" "$TARGET_FUNCTIONS_CONFIG")
    fi
    
    # Add OpenAI API options if provided
    if [[ -n "$MODEL_TYPE" ]]; then
        eval_args+=("--model-type" "$MODEL_TYPE")
    fi
    
    if [[ -n "$BASE_URL" ]]; then
        eval_args+=("--base-url" "$BASE_URL")
    fi
    
    if [[ -n "$API_KEY" ]]; then
        eval_args+=("--api-key" "$API_KEY")
    fi
    
    if [[ -n "$MODEL" ]]; then
        eval_args+=("--model" "$MODEL")
    fi
    
    if [[ "$VERBOSE" == true ]]; then
        eval_args+=("--verbose")
    fi
    
    if python "$EVALUATOR_SCRIPT" "${eval_args[@]}" > "$log_file" 2>&1; then
        echo "  ✅ Completed: $filename"
        return 0
    else
        echo "  ❌ Failed: $filename"
        if [[ -f "$log_file" ]]; then
            echo "    Error: $(tail -1 "$log_file")"
        fi
        return 1
    fi
}

# Function to test an environment
test_environment() {
    local env_name="$1"
    local env_dir="$CONVERSATIONS_DIR/$env_name"
    
    if [[ ! -d "$env_dir" ]]; then
        print_error "Environment directory not found: $env_dir"
        return 1
    fi
    
    print_info "🚀 Starting testing for environment: $env_name"
    
    # Use command line overrides or default values
    PARALLEL_JOBS=${PARALLEL_JOBS:-$DEFAULT_JOBS}
    MAX_STEPS=${MAX_STEPS:-$DEFAULT_MAX_STEPS}
    TIMEOUT=${TIMEOUT:-$DEFAULT_TIMEOUT}
    OUTPUT_DIR=${OUTPUT_DIR:-"${env_name}_test_results"}
    
    print_info "📁 Source: $env_dir"
    print_info "📊 Output: $OUTPUT_DIR"
    print_info "🧵 Parallel jobs: $PARALLEL_JOBS, Max steps: $MAX_STEPS, Timeout: ${TIMEOUT}s"
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    # Find all JSONL files
    print_info "🔍 Finding JSONL files in $env_name..."
    JSONL_FILES=($(find "$env_dir" -name "*.jsonl" -type f | sort))
    
    if [[ ${#JSONL_FILES[@]} -eq 0 ]]; then
        print_warning "No JSONL files found in $env_dir"
        return 0
    fi
    
    print_success "📋 Found ${#JSONL_FILES[@]} JSONL files"
    
    # Export function and variables for parallel execution
    export -f test_single_file
    export EVALUATOR_SCRIPT OUTPUT_DIR VERBOSE MAX_STEPS TIMEOUT MODEL_ID ENABLE_THINKING PROMPT_PATH UNCERTAINTY_CONFIG TEACHER_FORCING TURN_LEVEL_TF TARGET_FUNCTIONS_CONFIG MODEL_TYPE BASE_URL API_KEY MODEL
    
    # Record start time
    START_TIME=$(date +%s)
    
    print_info "🔄 Starting evaluation of ${#JSONL_FILES[@]} files..."
    
    # Run tests in parallel
    if command -v parallel >/dev/null 2>&1; then
        print_info "🧵 Using GNU parallel for processing"
        printf "%s\n" "${JSONL_FILES[@]}" | parallel -j "$PARALLEL_JOBS" --will-cite test_single_file {}
    else
        print_info "🧵 Using background processing (macOS compatible)"
        
        job_count=0
        for jsonl_file in "${JSONL_FILES[@]}"; do
            # Limit concurrent jobs
            while [[ $(jobs -r | wc -l) -ge $PARALLEL_JOBS ]]; do
                sleep 0.1
            done
            
            # Run test in background
            test_single_file "$jsonl_file" &
            ((job_count++))
            
            # Progress update
            if [[ $((job_count % 5)) -eq 0 ]]; then
                print_info "Started $job_count/${#JSONL_FILES[@]} jobs..."
            fi
        done
        
        # Wait for all background jobs to complete
        print_info "Waiting for all tests to complete..."
        wait
    fi
    
    # Count results
    SUCCESSFUL_FILES=$(find "$OUTPUT_DIR" -name "*_test_result.json" | wc -l)
    FAILED_FILES=$((${#JSONL_FILES[@]} - SUCCESSFUL_FILES))
    
    # Calculate duration
    END_TIME=$(date +%s)
    DURATION=$((END_TIME - START_TIME))
    
    print_success "🎉 $env_name testing completed!"
    print_info "📊 Results: ${#JSONL_FILES[@]} total, $SUCCESSFUL_FILES successful, $FAILED_FILES failed"
    print_info "⏱️ Duration: ${DURATION}s"
    print_success "✨ All done! Check $OUTPUT_DIR for detailed results"
    
    return 0
}

# Parse command line arguments
ENVIRONMENT=""
PARALLEL_JOBS=""
OUTPUT_DIR=""
MAX_STEPS=""
TIMEOUT=""
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -j|--jobs)
            PARALLEL_JOBS="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --max-steps)
            MAX_STEPS="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        --model-id)
            MODEL_ID="$2"
            shift 2
            ;;
        --enable-thinking)
            ENABLE_THINKING=true
            shift
            ;;
        --prompt-path)
            PROMPT_PATH="$2"
            shift 2
            ;;
        --uncertainty-config)
            UNCERTAINTY_CONFIG="$2"
            shift 2
            ;;
        --teacher-forcing)
            TEACHER_FORCING=true
            shift
            ;;
        --turn-level-tf)
            TURN_LEVEL_TF=true
            shift
            ;;
        --target-functions-config)
            TARGET_FUNCTIONS_CONFIG="$2"
            shift 2
            ;;
        --model-type)
            MODEL_TYPE="$2"
            shift 2
            ;;
        --base-url)
            BASE_URL="$2"
            shift 2
            ;;
        --api-key)
            API_KEY="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            print_error "Unexpected argument: $1"
            usage
            exit 1
            ;;
    esac
done

# Teacher Forcing validation
if [[ "$TURN_LEVEL_TF" == true ]] && [[ -z "$TARGET_FUNCTIONS_CONFIG" ]]; then
    print_error "Turn-Level TF requires --target-functions-config"
    print_info "Example: --target-functions-config uncertainty_configs/target_functions.yaml"
    exit 1
fi

# Validate target functions config file exists
if [[ -n "$TARGET_FUNCTIONS_CONFIG" ]] && [[ ! -f "$TARGET_FUNCTIONS_CONFIG" ]]; then
    print_error "Target functions config file not found: $TARGET_FUNCTIONS_CONFIG"
    exit 1
fi

# OpenAI API validation
if [[ "$MODEL_TYPE" == "openai" ]] && [[ -z "$BASE_URL" ]]; then
    print_error "OpenAI model type requires --base-url"
    print_info "Example: --base-url \"http://127.0.0.1:8000/v1\""
    exit 1
fi

# Validate model type
if [[ "$MODEL_TYPE" != "claude" ]] && [[ "$MODEL_TYPE" != "mistral" ]] && [[ "$MODEL_TYPE" != "openai" ]]; then
    print_error "Invalid model type: $MODEL_TYPE"
    print_info "Supported types: claude, mistral, openai"
    exit 1
fi

# Validate setup
if [[ ! -f "$EVALUATOR_SCRIPT" ]]; then
    print_error "Evaluator script not found: $EVALUATOR_SCRIPT"
    exit 1
fi

if [[ -z "$ENVIRONMENT" ]]; then
    print_error "Environment must be specified with --env"
    usage
    exit 1
fi

# Handle special environment commands
if [[ "$ENVIRONMENT" == "list" ]]; then
    print_info "Available environments:"
    discover_environments | while read env; do
        echo "  📁 $env (default: jobs=$DEFAULT_JOBS, max-steps=$DEFAULT_MAX_STEPS, timeout=${DEFAULT_TIMEOUT}s)"
    done
    exit 0
fi

if [[ "$ENVIRONMENT" == "all" ]]; then
    print_info "Testing all available environments..."
    discover_environments | while read env; do
        echo ""
        test_environment "$env"
    done
    exit 0
fi

# Handle comma-separated environments
if [[ "$ENVIRONMENT" == *","* ]]; then
    IFS=',' read -ra ENVIRONMENTS <<< "$ENVIRONMENT"
    for env in "${ENVIRONMENTS[@]}"; do
        env=$(echo "$env" | xargs)  # Trim whitespace
        echo ""
        test_environment "$env"
    done
    exit 0
fi

# Test single environment
test_environment "$ENVIRONMENT"
