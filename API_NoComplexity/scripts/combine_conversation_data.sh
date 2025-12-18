#!/bin/bash

# Combine conversation data from specified source subdirectories
# Author: Auto-generated script
# Usage: ./scripts/combine_conversation_data.sh [source_base] [target_dir] [dir1] [dir2] [dir3] ...
# Example: ./scripts/combine_conversation_data.sh combined_conversations_deref Combined_deref MediaControlEnv TransactionEnv

set -e  # Exit on error

# Function to show usage
show_usage() {
    echo "Usage: $0 [source_base] [target_dir] [source_dir1] [source_dir2] [source_dir3] ..."
    echo ""
    echo "Combines conversation data from specified source base subdirectories into target directory."
    echo ""
    echo "Arguments:"
    echo "  source_base    Source base directory name (default: combined_conversations)"
    echo "  target_dir     Target directory name (default: Combined)"
    echo "  source_dirN    Specific subdirectory names to process"
    echo "                 If no subdirectories specified, all subdirectories will be processed automatically."
    echo ""
    echo "Examples:"
    echo "  $0                                    # Use defaults: combined_conversations -> Combined"
    echo "  $0 combined_conversations_deref       # Use: combined_conversations_deref -> Combined"
    echo "  $0 combined_conversations_deref Combined_deref    # Use: combined_conversations_deref -> Combined_deref"
    echo "  $0 combined_conversations_deref Combined_deref MediaControlEnv TransactionEnv"
    echo ""
    echo "Default source directory: atomic_conversation_units/success_conversations/combined_conversations/"
    echo "Default target directory: atomic_conversation_units/success_conversations/Combined/"
    exit 1
}

# Check if help requested
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_usage
fi

# Parse command line arguments
# Default values
SOURCE_BASE_NAME="combined_conversations"
TARGET_DIR_NAME="Combined"
SPECIFIC_DIRS=()

# Parse arguments
if [ $# -ge 1 ]; then
    SOURCE_BASE_NAME="$1"
    shift
fi

if [ $# -ge 1 ]; then
    TARGET_DIR_NAME="$1"
    shift
fi

# Remaining arguments are specific directories
SPECIFIC_DIRS=("$@")

# Define source and target paths
SOURCE_BASE="atomic_conversation_units/success_conversations/$SOURCE_BASE_NAME"
TARGET_DIR="atomic_conversation_units/success_conversations/$TARGET_DIR_NAME"

echo "=== Combining Conversation Data from $SOURCE_BASE_NAME ==="

# Check if source base directory exists
if [ ! -d "$SOURCE_BASE" ]; then
    echo "Error: Source directory '$SOURCE_BASE' not found!"
    exit 1
fi

# Get list of directories to process
if [ ${#SPECIFIC_DIRS[@]} -eq 0 ]; then
    echo "No specific directories provided - auto-detecting all subdirectories..."
    # Get all subdirectories in source base
    DIRS_TO_PROCESS=($(find "$SOURCE_BASE" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort))
    echo "Auto-detected directories:"
    for dir in "${DIRS_TO_PROCESS[@]}"; do
        echo "  - $dir"
    done
else
    echo "Processing specified directories:"
    DIRS_TO_PROCESS=("${SPECIFIC_DIRS[@]}")
    for dir in "${DIRS_TO_PROCESS[@]}"; do
        echo "  - $dir"
    done
fi

echo ""
echo "Source base directory: $SOURCE_BASE/"
echo "Target directory: $TARGET_DIR/"
echo ""

# 1. Clean and create target directory
echo "=== BEFORE Copying ==="
if [ -d "$TARGET_DIR" ]; then
    BEFORE_COUNT=$(find "$TARGET_DIR/" -type f 2>/dev/null | wc -l)
    echo "Existing $TARGET_DIR_NAME directory found with $BEFORE_COUNT files"
    echo "Removing existing $TARGET_DIR_NAME directory..."
    rm -rf "$TARGET_DIR"
else
    BEFORE_COUNT=0
    echo "No existing $TARGET_DIR_NAME directory found"
fi

echo "Creating fresh $TARGET_DIR_NAME directory..."
mkdir -p "$TARGET_DIR"

# Validate source directories and count files
echo ""
echo "Source directories validation:"
TOTAL_SOURCE_FILES=0
VALID_DIRS=()

for dir in "${DIRS_TO_PROCESS[@]}"; do
    full_path="$SOURCE_BASE/$dir"
    if [ ! -d "$full_path" ]; then
        echo "  ❌ $dir: Directory not found!"
        echo "     Expected path: $full_path"
        exit 1
    else
        file_count=$(find "$full_path/" -type f 2>/dev/null | wc -l)
        echo "  ✅ $dir: $file_count files"
        TOTAL_SOURCE_FILES=$((TOTAL_SOURCE_FILES + file_count))
        VALID_DIRS+=("$dir")
    fi
done

echo ""
echo "Total source files: $TOTAL_SOURCE_FILES"

# Copy files from all source directories
echo ""
echo "Copying files..."
for dir in "${VALID_DIRS[@]}"; do
    echo "  Copying from $dir..."
    rsync -a --info=progress2 "$SOURCE_BASE/$dir/" "$TARGET_DIR/"
done

# 4. Count after copying
echo ""
echo "=== AFTER Copying ==="
AFTER_COUNT=$(find "$TARGET_DIR/" -type f | wc -l)
echo "Total files in $TARGET_DIR_NAME directory: $AFTER_COUNT"

echo ""
echo "File type breakdown:"
find "$TARGET_DIR/" -type f | sed 's/.*\.//' | sort | uniq -c | sort -nr | while read count ext; do
    echo "  .$ext files: $count"
done

echo ""
echo "=== Summary ==="
echo "Files added: $((AFTER_COUNT - BEFORE_COUNT))"

echo ""
echo "✅ Data combination completed successfully!"
echo "$TARGET_DIR_NAME directory: $TARGET_DIR/"
