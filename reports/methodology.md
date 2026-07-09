# Methodology

## Research Goal

The purpose of this project is to investigate whether AI-guided fuzzing can find software bugs more effectively than traditional random fuzzing.

To evaluate this, two fuzzing approaches are implemented and tested on the same target program:

* Traditional random fuzzing
* AI-guided fuzzing using a local Large Language Model

The goal is to compare both approaches using the same execution pipeline, logging system, and evaluation metrics.

## Target Program

For the initial experiment, a simple calculator program was selected as the target. The calculator accepts arithmetic expressions as input and evaluates them using Python's Abstract Syntax Tree (AST) functionality.

The calculator was chosen because it is small, easy to understand, and provides a controlled environment for testing different fuzzing techniques. It can also generate a variety of errors when given malformed, unexpected, or unsafe arithmetic inputs.

The calculator supports basic arithmetic operations such as:

* Addition
* Subtraction
* Multiplication
* Division
* Parentheses

Because the target program is simple and controlled, it is useful for comparing how different fuzzers generate valid inputs, invalid inputs, and edge cases.

## Random Fuzzer

A random fuzzer was developed as the baseline approach.

The random fuzzer generates random strings containing numbers, arithmetic operators, parentheses, and alphabetic characters. These inputs are then supplied to the calculator program.

The purpose of the random fuzzer is to represent a traditional unguided fuzzing strategy. It does not understand the structure of arithmetic expressions. Instead, it produces random input strings and relies on chance to generate meaningful test cases or trigger errors.

When an error occurs, the input, error type, error message, and execution time are recorded in a structured log file. This allows the behavior of the random fuzzer to be analyzed later.

## AI-Guided Fuzzer

An AI-guided fuzzing component was developed to generate calculator test inputs using a local Large Language Model.

Unlike the random fuzzer, the AI-guided fuzzer does not generate inputs through random character selection. Instead, it uses a structured prompt to ask the model for calculator expressions.

The AI-guided fuzzer uses the local Ollama model:

* qwen3:1.7b

This model was selected because it can run locally and supports reproducible experimentation.

The AI-guided fuzzer generates a mixture of:

* Valid arithmetic expressions
* Invalid arithmetic expressions
* Division-by-zero cases
* Parentheses-heavy expressions
* Large-number expressions
* Other calculator edge cases

The generated model output is cleaned and validated before execution. This validation step is necessary because language models may return explanations, markdown formatting, numbering, duplicate lines, or other unwanted text.

After validation, the AI-generated inputs are executed using the same executor and logger used by the random fuzzer.

## AI Input Generation Strategy

The AI-guided fuzzer uses prompt-based input generation.

The model is prompted to generate calculator fuzzing inputs using numbers, operators, and parentheses. The prompt asks for one input per line and instructs the model not to include explanations or markdown.

The generated output is passed through a validator before execution. The validator removes unwanted text and keeps only calculator-like expressions.

This pipeline has three main stages:

* Generate inputs using the language model
* Clean and validate generated inputs
* Execute validated inputs against the calculator target

This design allows the AI-guided fuzzer to produce more structured inputs than the random fuzzer while still testing both valid and invalid calculator behavior.

## Pilot Experiments and Methodology Refinement

Several pilot experiments were performed before the final fair comparison.

These pilot experiments are important because they show how the experimental design was refined.

### Initial AI-Guided Experiment

The first working AI-guided experiment generated 20 inputs.

The result was:

| Metric             | AI-Guided Fuzzer |
| ------------------ | ---------------: |
| Total Inputs       |               20 |
| Valid Inputs       |               18 |
| Crash/Error Inputs |                2 |

The observed error type was:

* ZeroDivisionError

This showed that the AI-guided fuzzer could generate meaningful calculator expressions. However, this experiment was not a fair comparison because the random fuzzer had been tested with 100 inputs, while the AI-guided fuzzer had only been tested with 20 inputs.

### Failed Attempt to Generate 100 Inputs Directly

To make the comparison fair, the next attempt was to ask the model to generate 100 inputs in a single request.

This approach failed because the local qwen3:1.7b model timed out after 120 seconds.

This showed that generating 100 inputs in one model call was not reliable in the current local setup.

### Multi-Round Generation Attempt

To avoid timeout issues, the AI-guided fuzzer was changed to generate smaller batches.

Instead of asking the model for 100 inputs at once, the fuzzer asked for 20 inputs per generation round.

This approach worked better, but it introduced a new fairness problem.

One AI-guided experiment produced:

| Metric             | AI-Guided Fuzzer |
| ------------------ | ---------------: |
| Total Inputs       |              121 |
| Valid Inputs       |               69 |
| Crash/Error Inputs |               52 |

The observed error types were:

* ZeroDivisionError: 23
* SyntaxError: 29

This result was useful, but it was still not a fair final comparison because the AI-guided fuzzer used 121 inputs while the random fuzzer used only 100 inputs.

Because the AI-guided fuzzer had more test inputs, it had more opportunities to generate valid cases and errors. Therefore, the experiment needed to be corrected.

## Final Fair Comparison Setup

To make the comparison fair, both fuzzers were evaluated using the same number of total inputs.

The AI-guided fuzzer was updated to stop after exactly 100 executed inputs.

The final comparison used the following setup:

* Random fuzzer inputs: 100
* AI-guided fuzzer inputs: 100
* Target program: calculator expression evaluator
* AI model: qwen3:1.7b through Ollama
* Logging format: structured JSONL result logs
* Summary format: JSON summary files

Using the same number of total inputs avoids giving either fuzzer an advantage based only on input count.

## Data Collection

During each experiment, the following information is recorded:

* Input provided to the target program
* Execution result
* Error message generated by the program
* Number of successful executions
* Number of failed executions
* Execution time for each test case
* Exception type associated with each failure

The collected data is stored in structured log files for later analysis and comparison.

## Evaluation Metrics

The performance of the two fuzzing approaches is compared using the following measurements:

* Total number of inputs tested
* Number of valid inputs
* Number of crash/error inputs
* Average execution time
* Unique error types
* Code coverage

These metrics help evaluate whether AI-guided fuzzing improves input validity, error discovery, and target program exploration compared to random fuzzing.

## Coverage and Logging Infrastructure

To support experimentation, an automated execution and logging pipeline was developed.

Generated inputs are executed automatically, and the outcome of each execution is recorded.

For each test case, the framework records:

* Input value
* Execution result
* Execution time
* Error type
* Error message

Coverage measurements are collected using the coverage.py tool. Coverage reports can be generated in both terminal and HTML formats. This allows detailed inspection of which portions of the target program were exercised during fuzzing.

Experiment summaries are automatically generated and stored in structured JSON format to support later analysis and comparison.

## Experimental Procedure

The random fuzzer and AI-guided fuzzer are executed separately against the same calculator target program.

Each fuzzer generates and executes 100 total inputs.

For each input, the framework records whether execution was successful or produced an error. It also records the execution time and error type.

After each experiment, a summary script analyzes the result log and reports:

* Total inputs
* Valid inputs
* Crash/error inputs
* Average execution time
* Unique error types

A comparison script then compares the random fuzzer summary against the AI-guided fuzzer summary.

This procedure ensures that both fuzzers are evaluated using the same target program, input count, execution pipeline, logging format, and comparison metrics.

## Final Fair Comparison Result

The final fair comparison used 100 inputs for each fuzzer.

| Metric                 |  Random Fuzzer | AI-Guided Fuzzer |
| ---------------------- | -------------: | ---------------: |
| Total Inputs           |            100 |              100 |
| Valid Inputs           |              8 |               61 |
| Crash/Error Inputs     |             92 |               39 |
| Average Execution Time | 0.00002734 sec |   0.00003274 sec |

The random fuzzer produced the following error types:

* SyntaxError: 68
* ValueError: 13
* KeyError: 4
* IndentationError: 4
* ZeroDivisionError: 3

The AI-guided fuzzer produced the following error types:

* ZeroDivisionError: 29
* SyntaxError: 10

## Analysis

The AI-guided fuzzer generated significantly more valid calculator expressions than the random fuzzer.

Out of 100 total inputs, the AI-guided fuzzer generated 61 valid inputs, while the random fuzzer generated only 8 valid inputs.

This shows that AI-guided fuzzing was better at generating structured and meaningful arithmetic expressions.

The random fuzzer produced more crash/error inputs and discovered a wider variety of error types. This shows that random fuzzing is useful for generating malformed inputs and exposing parser-level failures.

The AI-guided fuzzer produced fewer unique error types, but it generated more targeted edge cases, especially division-by-zero cases.

These results suggest that the two approaches have different strengths.

Random fuzzing is useful for broad malformed-input exploration. AI-guided fuzzing is useful for generating valid, structured, and targeted edge-case inputs.

## Expected Results

The expectation was that AI-guided fuzzing would produce more meaningful test inputs and reach interesting program behaviors more quickly than purely random input generation.

The final fair comparison supports this expectation because the AI-guided fuzzer generated many more valid calculator inputs than the random fuzzer.

However, the random fuzzer produced a wider variety of error types. This suggests that AI-guided fuzzing should not fully replace random fuzzing.

A future hybrid fuzzing strategy may combine both methods:

* Random fuzzing for broad malformed-input exploration
* AI-guided fuzzing for structured and targeted edge-case generation
