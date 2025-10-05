#!/bin/bash
export PYTHONPATH=$(pwd)/../..
DATASET=("HumanEval")
FEEDBACK_TYPES=("minimal_feedback")
declare -A MODELS=(
    ["GPT"]="gpt-4o-2024-11-20"
)

for DATASET in "${DATASET[@]}"; do
  for MODEL in "${!MODELS[@]}"; do
      VERSION="${MODELS[$MODEL]}"

      for FEEDBACK in "${FEEDBACK_TYPES[@]}"; do

          echo "Single-round fixing for model $MODEL ($VERSION), feedback $FEEDBACK, dataset $DATASET"

          python ../code/evaluate.py \
              --dataset "$DATASET" \
              --model "$MODEL" \
              --version "$VERSION" \
              --feedback "$FEEDBACK" \
              --function "single_fix"
      done
  done
done
