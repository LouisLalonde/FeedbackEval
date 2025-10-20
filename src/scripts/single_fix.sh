#!/bin/bash
export PYTHONPATH=$(pwd)/../..
DATASET=("CoderEval")
FEEDBACK_TYPES=("compiler_feedback" "llm_skilled_feedback" "test_feedback" "minimal_feedback")
declare -A MODELS=(
    ["Claude"]="claude-3-5-sonnet-20241022"
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
