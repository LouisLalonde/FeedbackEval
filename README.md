# FeedbackEval: Evaluating Large Language Models in Feedback-Driven Code Repair

This is the official repository for the paper "FeedbackEval: Evaluating Large Language Models in Feedback-Driven Code
Repair".

## Benchmark Dataset

We construct a new benchmark, FeedbackEval, to systematically evaluate LLMs’ ability to interpret and
utilize various feedback types in code repair.

FeedbackEval consists of 394 coding tasks covering a diverse range of programming scenarios. In total, it includes 3,736
erroneous code instances, each paired with four distinct types of
feedback.

## Benchmark Format

The key components of the benchmark are defined as follows:

* **Erroneous Code**: A faulty function or code snippet requiring
  correction serves as the initial state for the repair task.
* **Docstring**: A high-level description of the code’s intended functionality.
* **Context**: Supplementary information about the project or surrounding code environment, such as related APIs, class
  definitions, or global variables.
* **Test Feedback**: This feedback explicitly identifies failing tests and expected outcomes,
  providing clear, actionable guidance for code correction.
* **Compiler Feedback**: This feedback highlights syntax errors, code style violations,
  and potential bugs, offering technical insights into structural
  flaws in the code.
* **Human Feedback**: This feedback mimics developer-generated suggestions in natural language, pointing out potential logic
  flaws and recommending
  best practices to improve code reliability and robustness.
* **Simple Feedback**: A minimalistic, generic form of feedback
  (e.g., “The code is wrong. Please fix it.”).

## Usage

Ensure you're using the right setup and following the proper directory structure to evaluate feedback-driven code repair
with our tool.

### Setup

1. Environment Setup

Ensure you're running Python 3.8 or newer. We recommend setting up a virtual environment:

```
conda create -n FeedbackEval python=3.8
conda activate FeedbackEval
```

2. Repository Setup

Install necessary dependencies:
```
pip install -r requirements.txt
```

### Evaluate

Run the script with arguments:
```
cd src/scripts

##If you want to run single-round repair:
$ ./single_fix.sh

##If you want to calculate single-round repair score:
$ ./single_score.sh

##If you want to run multi-round repair:
$ ./multi_fix.sh

##If you want to calculate multi-round repair score:
$ ./multi_score.sh

##If you want to run experiments in RQ4:
$ ./rq4.sh
```