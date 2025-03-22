#!/bin/bash
set -euo pipefail

export PYTHONPATH=$(pwd)/...
MODEL_NAME="Claude"
MODEL_VERSION="claude-3-5-sonnet-20241022"
FEEDBACK="test_feedback"
DATASET="CoderEval"

BASE_CMD="python src/code/evaluate.py --dataset ${DATASET} --model ${MODEL_NAME} --version ${MODEL_VERSION} --feedback ${FEEDBACK} --function single_fix"

experiments=(
    "Single-round fix without persona         | --no_persona"
    "Single-round fix with cot        | --is_cot"
    "Single-round fix without docstring       | --no_docstring"
    "Single-round fix without context         | --no_context"
    "Single-round fix with few-shot        | --is_few_shot"
    "Single-round fix without instructions | --no_instructions"
)

for exp in "${experiments[@]}"; do
    IFS='|' read -r name flags <<< "${exp}"
    echo "======================================================================"
    echo "Running experiment: ${name}"
    echo "Flags: ${flags}"
    eval "${BASE_CMD} ${flags}"
    echo -e "Experiment completed: ${name}\n"
done

echo "All experiments completed successfully."