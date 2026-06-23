# Week 4 Notes

## Goal

The goal of Week 4 was to add coverage measurement, crash logging, and automated experiment reporting to the fuzzing framework.

## Coverage Measurement

Coverage.py was integrated into the project to measure how much of the target program is exercised during fuzzing experiments.

Coverage reports can now be generated directly from experiment runs.

### Coverage Results

* Overall coverage: 76%
* Calculator target coverage: 72%

HTML coverage reports are also generated for detailed inspection.

## Logging Infrastructure

A structured logging system was implemented.

Each executed input is recorded along with:

* Input value
* Execution result
* Error type
* Error message
* Execution time

Results are stored in JSONL format for later analysis.

## Automated Summary Generation

A summary script was developed to process experiment logs and generate overall statistics.

### Latest Experimental Results

* Total inputs tested: 100
* Valid inputs: 8
* Error inputs: 92

### Error Types Observed

* SyntaxError: 68
* ValueError: 13
* KeyError: 4
* IndentationError: 4
* ZeroDivisionError: 3

Summary reports are automatically saved in JSON format.

## Deliverables Completed

* Coverage reporting
* HTML coverage generation
* Automated logging system
* Summary report generation
* Experimental data collection pipeline

## Next Steps

Week 5 will focus on prompt design and AI-generated test input creation for the AI-guided fuzzing component.
