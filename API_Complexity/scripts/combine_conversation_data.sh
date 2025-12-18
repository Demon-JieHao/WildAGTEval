#!/bin/bash

# Combine conversation data from combined_conversations subdirectories
# Author: Auto-generated script
# Usage: ./scripts/combine_conversation_data.sh [dir1] [dir2] [dir3] ...
# Example: ./scripts/combine_conversation_data.sh MediaControlEnv TransactionEnv

set -e  # Exit on error

# Function to show usage
show_usage() {
    echo "Usage: $0 [source_dir1] [source_dir2] [source_dir3] ..."
    echo ""
    echo "Combines conversation data from combined_conversations subdirectories into Combined directory."
    echo ""
    echo "Arguments:"
    echo "  source_dirN    Directory names under atomic_conversation_units/success_conversations/combined_conversations/"
    echo "                 If no arguments provided, all subdirectories will be processed automatically."
    echo ""
    echo "Examples:"
    echo "  $0                          # Process all subdirectories automatically"
    echo "  $0 MediaControlEnv TransactionEnv"
    echo "  $0 CompanyResearch_BrandReferences CulinaryControlEnv_RestaurantDelivery"
    echo ""
    echo "Source directory: atomic_conversation_units/success_conversations/combined_conversations/"
    echo "Target directory: atomic_conversation_units/success_conversations/Combined/"
    exit 1
}

# Check if help requested
if [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    show_usage
fi

echo "=== Combining Conversation Data from combined_conversations ==="

# Define source and target paths
SOURCE_BASE="atomic_conversation_units/success_conversations/combined_conversations"
TARGET_DIR="atomic_conversation_units/success_conversations/Combined"

# Check if source base directory exists
if [ ! -d "$SOURCE_BASE" ]; then
    echo "Error: Source directory '$SOURCE_BASE' not found!"
    exit 1
fi

# Get list of directories to process
if [ $# -eq 0 ]; then
    echo "No arguments provided - auto-detecting all subdirectories..."
    # Get all subdirectories in combined_conversations
    DIRS_TO_PROCESS=($(find "$SOURCE_BASE" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort))
    echo "Auto-detected directories:"
    for dir in "${DIRS_TO_PROCESS[@]}"; do
        echo "  - $dir"
    done
else
    echo "Processing specified directories:"
    DIRS_TO_PROCESS=("$@")
    for dir in "${DIRS_TO_PROCESS[@]}"; do
        echo "  - $dir"
    done
fi

echo ""
echo "Source base directory: $SOURCE_BASE/"
echo "Target directory: $TARGET_DIR/"
echo ""

# 1. Clean and create Combined directory
echo "=== BEFORE Copying ==="
if [ -d "$TARGET_DIR" ]; then
    BEFORE_COUNT=$(find "$TARGET_DIR/" -type f 2>/dev/null | wc -l)
    echo "Existing Combined directory found with $BEFORE_COUNT files"
    echo "Removing existing Combined directory..."
    rm -rf "$TARGET_DIR"
else
    BEFORE_COUNT=0
    echo "No existing Combined directory found"
fi

echo "Creating fresh Combined directory..."
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
echo "Total files in Combined directory: $AFTER_COUNT"

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
echo "Combined directory: $TARGET_DIR/"
