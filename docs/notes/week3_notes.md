# Week 3 Notes

## Goal

The goal of Week 3 was to improve the baseline random fuzzer, automate test execution, and verify the crash detection workflow.

## Random Fuzzer Improvements

The random fuzzer was updated to generate a wider variety of test inputs. In addition to random combinations of numbers, operators, parentheses, and alphabetic characters, several edge-case inputs were added.

Examples include:

* Division by zero
* Unbalanced parentheses
* Invalid expressions
* Large numerical values
* Empty inputs

These additions increased the variety of test cases supplied to the calculator program.

## Automated Test Execution

An automated execution pipeline was implemented.

Instead of manually testing individual inputs, batches of generated inputs can now be executed automatically against the calculator target.

The execution framework records:

* Input value
* Program output
* Error type
* Error message
* Execution time

## Crash Detection Verification

A crash detection workflow was created and tested.

Several known inputs were used to verify that the system correctly distinguishes between successful executions and failures.

### Verification Inputs

* 1+2
* 1/0
* (1+2
* abc+1
* 999*999

The framework successfully detected and categorized the resulting exceptions.

## Deliverables Completed

* Improved random input generation
* Edge-case input generation
* Automated test execution
* Crash detection workflow verification

## Next Steps

Week 4 will focus on coverage measurement, structured logging, and experimental data collection.
