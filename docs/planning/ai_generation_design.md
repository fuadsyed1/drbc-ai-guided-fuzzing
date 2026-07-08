# AI Input Generation Design

## Goal

The goal of the AI-guided fuzzer is to generate calculator test inputs using a language model rather than purely random character generation.

## Language Model

The initial implementation will use Qwen3:1.7b running locally through Ollama.

Larger models may be evaluated in future experiments to determine whether model size influences fuzzing effectiveness.

## Generation Pipeline

The AI-guided fuzzing workflow will follow the pipeline below:

Prompt
→ Language Model
→ Generated Calculator Inputs
→ Input Validation
→ Test Execution
→ Result Logging
→ Coverage Measurement
→ Experiment Summary

## Input Types

The language model will be instructed to generate:

* Valid arithmetic expressions
* Invalid arithmetic expressions
* Division-by-zero cases
* Parentheses-heavy expressions
* Large-number expressions
* Edge-case inputs

## Evaluation Metrics

The AI-guided fuzzer will be evaluated using:

* Total inputs tested
* Successful executions
* Error-triggering inputs
* Unique error types
* Code coverage
* Execution time

These metrics will be compared against the baseline random fuzzer.

## Week 6 Implementation Plan

The AI-guided fuzzer will be implemented using the existing fuzzing pipeline.

Planned files:

* `src/utils/ai_generator.py`  
  Sends prompts to the language model and receives generated inputs.

* `src/utils/ai_validator.py`  
  Cleans model output by removing explanations, blank lines, numbering, and duplicate inputs.

* `src/fuzzers/ai_fuzzer.py`  
  Uses the generator and validator to produce AI-guided fuzzing inputs.

* `experiments/ai_fuzzing/run_ai_fuzzer.py`  
  Runs the AI-generated inputs through the existing executor and logger.

* `experiments/ai_fuzzing/summarize_ai_results.py`  
  Summarizes AI fuzzing results in the same format as the random fuzzing summary.