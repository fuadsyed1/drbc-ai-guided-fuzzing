# Implementation Details

The AI-guided fuzzing framework was implemented in Python. The implementation is organized into separate modules for fuzzers, utility functions, experiments, result logging, and analysis scripts.

## Random Fuzzer Implementation

The random fuzzer is implemented in `src/fuzzers/random_fuzzer.py`.

It generates random strings using numbers, arithmetic operators, parentheses, and alphabetic characters. It also includes several edge cases such as empty input, division by zero, incomplete parentheses, invalid identifiers, and large-number expressions.

The random fuzzer provides a `generate_batch` function that produces a specified number of test inputs. This function was used in the Week 7 pilot experiment to generate 50 random inputs.

## AI-Guided Fuzzer Implementation

The AI-guided fuzzer is implemented in `src/fuzzers/ai_fuzzer.py`.

The AI fuzzer uses a structured prompt to request calculator fuzzing inputs from a local Large Language Model. The selected model is `qwen3:1.7b`, running locally through Ollama.

The AI prompt asks the model to generate a mix of valid arithmetic expressions, invalid expressions, division-by-zero cases, parentheses-heavy expressions, and large-number expressions.

## AI Generator

The AI generator is implemented in `src/utils/ai_generator.py`.

This component connects to Ollama and sends the prompt to the selected local model. It captures the model output and returns the raw generated text to the AI fuzzer.

During implementation, timeout and output formatting issues were observed. These issues showed that local model generation must be handled carefully, especially when requesting a large number of inputs.

## AI Validator

The AI validator is implemented in `src/utils/ai_validator.py`.

The validator cleans the model output before execution. It removes blank lines, explanations, markdown formatting, numbering, duplicate inputs, and lines that do not look like calculator expressions.

This step is necessary because language models may produce extra text even when instructed not to explain.

## Execution and Logging

Generated inputs are executed using the shared execution utility. Both random and AI-generated inputs use the same execution process.

The result logger saves each execution result in JSONL format. Each line represents one test case result. This format makes it easy to store, inspect, and summarize experiments.

## Week 6 Experiment Runner

The Week 6 AI experiment runner was implemented in `experiments/ai_guided_fuzzing/run_ai_fuzzer.py`.

This runner was updated to stop after exactly 100 executed AI inputs. This was necessary because an earlier multi-round AI run produced 121 inputs, which made comparison with the 100-input random fuzzer unfair.

The final Week 6 setup allowed a fair 100 vs 100 comparison.

## Week 7 Pilot Experiment Runner

The Week 7 pilot runner is implemented in `experiments/week7_pilot/run_pilot_experiment.py`.

This script runs a smaller pilot experiment using:

* 50 random inputs
* 50 AI-guided inputs

The Week 7 pilot results are saved separately from the Week 6 results. This prevents overwriting the final Week 6 comparison and keeps different experiment stages organized.

## Week 7 Summary Script

The Week 7 summary script is implemented in `experiments/week7_pilot/summarize_week7_pilot.py`.

This script reads the Week 7 random and AI JSONL result logs and calculates:

* Total inputs
* Valid inputs
* Crash/error inputs
* Unique inputs
* Duplicate inputs
* Average execution time
* Error type counts

During testing, the first version of the summary script incorrectly counted all inputs as crash/error inputs. The issue was caused by incorrect handling of the result log format.

The script was fixed so that it correctly detects valid executions and error cases.

## Implementation Summary

The implementation now supports both full comparison experiments and smaller pilot experiments.

The framework can generate inputs, execute them against the calculator target, log results, summarize outcomes, and compare random fuzzing with AI-guided fuzzing.

This modular structure makes it easier to extend the project in future weeks with additional targets, improved prompts, coverage analysis, and hybrid fuzzing strategies.
