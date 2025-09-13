#!/bin/bash
export PYTHONPATH=$(pwd)/...
DATASET="HumanEval"  # or HumanEval

 FEEDBACK_TYPES=("mixed_feedback")
# FEEDBACK_TYPES=("mixed_feedback")
declare -A MODELS=(
    # ["GPT"]="gpt-4o-2024-11-20"
    #  ["Claude"]="claude-3-5-sonnet-20241022"
#    ["Gemini"]="gemini-1.5-pro"
    # ["GLM"]="glm-4-plus"
    # ["Qwen"]="qwen2.5-72b-instruct"
     ["Deepseek"]="deepseek-r1-250528"
)

for MODEL in "${!MODELS[@]}"; do
    VERSION="${MODELS[$MODEL]}"

    for FEEDBACK in "${FEEDBACK_TYPES[@]}"; do

        echo "Multi-round fixing for model $MODEL ($VERSION), feedback $FEEDBACK, dataset $DATASET"

        python src/code/evaluate.py \
            --dataset "$DATASET" \
            --model "$MODEL" \
            --version "$VERSION" \
            --feedback "$FEEDBACK" \
            --function "multi_fix"
    done
done
