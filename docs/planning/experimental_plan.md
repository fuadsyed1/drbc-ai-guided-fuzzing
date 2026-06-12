# Week 2 Experimental Plan

## Target Program

The selected target program is a calculator parser located at:

`src/targets/calculator.py`

The calculator accepts arithmetic expressions such as addition, subtraction, multiplication, division, and parentheses.

## Bug Categories

This project will focus on the following bug categories:

1. Crash bugs
2. Exception bugs
3. Logic bugs

## Fuzzers

### Random Fuzzer

The random fuzzer generates random arithmetic-like strings and sends them to the calculator.

File:

`src/fuzzers/random_fuzzer.py`

### AI-Guided Fuzzer Skeleton

The AI-guided fuzzer currently uses selected intelligent test inputs. Later, this will be replaced with LLM-generated inputs.

File:

`src/fuzzers/ai_fuzzer.py`

## Evaluation Metrics

The experiment will compare:

- Total inputs tested
- Successful inputs
- Error inputs
- Unique error types
- Time to first error
- Code coverage, if added later

## Current Test Result

Random fuzzer:

- Total inputs: 100
- Error inputs: 96

AI-guided fuzzer skeleton:

- Total inputs: 9
- Successful inputs: 4
- Error inputs: 5

## Experimental Method

Both fuzzers will run against the same calculator target program. Their generated inputs and errors will be logged in the `results/logs/` folder. The results will later be compared to determine whether AI-guided input generation can find meaningful errors more efficiently than random fuzzing.