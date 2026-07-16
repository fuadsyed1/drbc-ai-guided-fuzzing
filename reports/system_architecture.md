# System Architecture

The AI-guided fuzzing framework is designed to compare traditional random fuzzing with AI-guided fuzzing in a controlled experimental environment. The framework uses the same target program, execution engine, logging system, and evaluation metrics for both fuzzing approaches.

The system is divided into several main components: input generation, AI output validation, execution, logging, summary generation, and comparison analysis.

## Input Generation Layer

The input generation layer contains two fuzzing strategies.

The first strategy is the random fuzzer. It generates random calculator inputs using numbers, operators, parentheses, and alphabetic characters. This fuzzer does not understand the structure of arithmetic expressions. Its purpose is to represent a traditional unguided fuzzing baseline.

The second strategy is the AI-guided fuzzer. It uses a local Large Language Model to generate calculator test inputs from a structured prompt. The prompt asks the model to produce valid arithmetic expressions, invalid expressions, division-by-zero cases, parentheses-heavy expressions, and large-number expressions.

## AI Output Validation Layer

The AI-guided fuzzer includes an output validation layer because language model output is not always directly usable. The model may return explanations, blank lines, markdown formatting, numbering, duplicate inputs, or other unwanted text.

The validator cleans the model output and keeps only calculator-like expressions. This step makes the generated inputs suitable for automated execution.

## Execution Layer

Both fuzzers send their generated inputs to the same execution engine. The execution engine runs each input against the calculator target program.

Using the same execution layer is important because it ensures that random fuzzing and AI-guided fuzzing are evaluated under the same conditions.

## Target Program

The target program is a calculator expression evaluator. It accepts arithmetic expressions and evaluates them using Python's Abstract Syntax Tree functionality.

The calculator target is small, controlled, and useful for early fuzzing experiments. It can produce valid outputs for correct arithmetic expressions and errors for malformed or unsafe inputs.

## Logging Layer

The logging layer records the result of every executed input. Each result is saved in structured JSONL format.

The log records include the input value, execution result, execution time, error type, and error message when applicable. This makes the experiment results easier to analyze later.

## Summary and Comparison Layer

After experiments are executed, summary scripts read the JSONL result logs and calculate metrics such as total inputs, valid inputs, crash/error inputs, unique inputs, duplicate inputs, average execution time, and error type distribution.

The comparison layer then compares the random fuzzer results with the AI-guided fuzzer results.

## Architecture Summary

The overall framework follows this workflow:

Prompt or random generation leads to test inputs. These inputs are validated when necessary, executed against the calculator target, logged in structured result files, summarized, and compared using shared evaluation metrics.

This architecture supports controlled comparison between random fuzzing and AI-guided fuzzing while preserving separate result files for different experiment stages.
