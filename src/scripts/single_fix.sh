#!/bin/bash
export PYTHONPATH=$(pwd)/...
DATASET="CoderEval"

FEEDBACK_TYPES=("test_feedback" "compiler_feedback" "human_feedback" "simple_feedback")
declare -A MODELS=(
    ["GPT"]="gpt-4o-2024-11-20"
    ["Claude"]="claude-3-5-sonnet-20241022"
    ["Gemini"]="gemini-1.5-pro"
    ["GLM"]="glm-4-plus"
    ["Qwen"]="qwen2.5-72b-instruct"
)

for MODEL in "${!MODELS[@]}"; do
    VERSION="${MODELS[$MODEL]}"

    for FEEDBACK in "${FEEDBACK_TYPES[@]}"; do

        echo "Single-round fixing for model $MODEL ($VERSION), feedback $FEEDBACK, dataset $DATASET"

        python src/code/evaluate.py \
            --dataset "$DATASET" \
            --model "$MODEL" \
            --version "$VERSION" \
            --feedback "$FEEDBACK" \
            --function "single_fix"
    done
done
