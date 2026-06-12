# Week 2 Notes

## Goal

The goal of Week 2 was to select a target program, define the experimental design, and begin building the baseline components needed for the fuzzing experiments.

## Target Program Selection

A calculator parser was selected as the target program for the initial experiments. The calculator accepts arithmetic expressions and evaluates them using Python's AST functionality.

The calculator was chosen because it is simple, easy to understand, and provides a controlled environment for comparing different fuzzing approaches.

## Experimental Design

The project will compare two fuzzing approaches:

1. Random Fuzzing
2. AI-Guided Fuzzing

Both approaches will be tested against the same target program and evaluated using the same metrics.

### Evaluation Metrics

* Total inputs tested
* Successful executions
* Error-triggering inputs
* Unique error types
* Time to first error
* Code coverage (future work)

## Random Fuzzer

A baseline random fuzzer was implemented.

The fuzzer generates random strings containing:

* Numbers
* Arithmetic operators
* Parentheses
* Random alphabetic characters

Generated inputs are sent to the calculator program and any resulting errors are recorded in a log file.

### Initial Results

* Total inputs tested: 100
* Successful inputs: 6
* Error inputs: 94

Most generated inputs produced syntax or validation errors because they did not follow valid arithmetic expression formats.

## AI-Guided Fuzzer Prototype

A simple AI-guided fuzzing prototype was created.

The current version uses manually selected test cases designed to represent:

* Valid expressions
* Invalid expressions
* Division-by-zero conditions
* Large numerical values
* Unbalanced parentheses

### Initial Results

* Total inputs tested: 9
* Successful inputs: 4
* Error inputs: 5

This prototype serves as the foundation for future integration with a Large Language Model.

## Literature Review Progress

The five selected research papers were reviewed and summarized:

1. AFLFast
2. AFLGo
3. Dissecting AFL
4. Fuzz4All
5. mGPTFuzz

These papers provide background on traditional fuzzing, directed fuzzing, fuzzing evaluation, and AI-assisted fuzzing techniques.

## Deliverables Completed

* Target program selected
* Experimental plan completed
* Methodology draft completed
* Random fuzzer implemented
* AI-guided fuzzer prototype implemented
* Literature review completed

## Next Steps

Week 3 will focus on improving the random fuzzer, expanding test generation capabilities, and preparing for more detailed experimental evaluation.
