# Week 5 Notes

## Goal

The goal of Week 5 was to design the AI-guided input generation approach and prepare the framework for integration with a language model.

## AI Input Generation Design

An AI input generation strategy was designed for the calculator fuzzing target.

The AI-guided approach will use a language model to generate calculator test inputs instead of relying on random character generation.

The planned workflow is:

Prompt → Language Model → Generated Inputs → Validation → Execution → Logging → Coverage Measurement → Summary Generation

## Language Model Selection

Qwen3:1.7b was selected as the initial language model for implementation.

The model will run locally through Ollama and will be used to generate calculator expressions for fuzzing experiments.

Larger models may be evaluated in future experiments to determine whether model size affects fuzzing performance.

## Prompt Library

A prompt library was created to support different categories of test generation.

Prompt categories include:

* Valid arithmetic expressions
* Invalid arithmetic expressions
* Division-by-zero cases
* Parentheses-heavy expressions
* Large-number expressions
* Mixed fuzzing inputs

These prompts will be used to generate diverse test cases for the AI-guided fuzzer.

## Output Validation Design

A validation and cleaning strategy was designed for AI-generated outputs.

The validation process will:

* Remove blank lines
* Remove explanations
* Remove numbering
* Remove duplicate inputs
* Filter invalid output formats

This ensures that generated inputs can be executed directly by the fuzzing framework.

## Methodology Updates

The project methodology was updated to include the AI input generation strategy and planned AI-guided fuzzing workflow.

## Deliverables Completed

* AI input generation design
* Prompt library
* Output validation design
* Methodology updates
* Week 6 implementation plan

## Next Steps

Week 6 will focus on implementing the AI-guided fuzzer, integrating the language model with the fuzzing pipeline, and automating execution of AI-generated test cases.